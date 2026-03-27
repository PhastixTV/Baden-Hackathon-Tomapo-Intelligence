import json
import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
from ollama import chat, ChatResponse

app = FastAPI()

model = joblib.load("ml/model.pkl")
feature_order: list[str] = json.load(open("ml/feature_order.json"))

# (field, severity, category, expected, check)
# coldChainBroken & isIntact are intentionally excluded — they duplicate hadColdChainBreak
# overallVerdictFail excluded — legalLimitsExceeded already covers the critical case
ANOMALY_RULES = [
    # Cold chain — single break = high, multiple = critical
    ("hadColdChainBreak",                "high",     "coldChain",    0,        lambda v: v == 1),
    ("coldChainBreakCount",              "critical", "coldChain",    "<= 2",   lambda v: v > 2),
    ("coldChainBreakCount",              "high",     "coldChain",    0,        lambda v: 0 < v <= 2),
    ("tempIsWithinRange",                "medium",   "temperature",  1,        lambda v: v == 0),
    # Microbiology — any pathogen = critical
    ("pathogensDetectedCount",           "critical", "microbiology", 0,        lambda v: v > 0),
    ("pathogensLimitExceededCount",      "critical", "microbiology", 0,        lambda v: v > 0),
    ("microbiologicalLimitExceededCount","high",     "microbiology", 0,        lambda v: v > 0),
    # Chemical — legal violation = critical
    ("chemicalMrlExceededCount",         "critical", "chemical",     0,        lambda v: v > 0),
    ("substancesLimitExceededCount",     "high",     "chemical",     0,        lambda v: v > 0),
    # Laboratory
    ("legalLimitsExceeded",              "critical", "laboratory",   0,        lambda v: v == 1),
    ("overallVerdictFail",               "high",     "laboratory",   0,        lambda v: v == 1),
    # Allergens
    ("allergenLabelIncorrectCount",      "high",     "allergen",     0,        lambda v: v > 0),
    # Visual
    ("moldDetected",                     "high",     "visual",       0,        lambda v: v == 1),
    ("foreignBodyDetected",              "critical", "visual",       0,        lambda v: v == 1),
    # Packaging
    ("isLeaking",                        "high",     "packaging",    0,        lambda v: v == 1),
    ("isSealed",                         "medium",   "packaging",    1,        lambda v: v == 0),
    # Alerts
    ("alertsSeverityMax",                "critical", "alerts",       "< 3",    lambda v: v == 4),
    ("alertsSeverityMax",                "high",     "alerts",       "< 3",    lambda v: v == 3),
    ("alertsActiveCount",                "medium",   "alerts",       0,        lambda v: v > 2),
    # Traceability
    ("traceabilityHasGaps",              "medium",   "traceability", 0,        lambda v: v == 1),
    ("traceabilityCompleteness",         "medium",   "traceability", "> 0.8",  lambda v: v < 0.5),
]

SEVERITY_SCORE = {"critical": 25, "high": 15, "medium": 8, "low": 3}


def build_anomalies(fields: dict) -> list:
    anomalies = []
    seen = set()
    for field, severity, category, expected, check in ANOMALY_RULES:
        value = fields.get(field)
        key = (field, severity)
        if value is not None and check(value) and key not in seen:
            seen.add(key)
            anomalies.append({
                "severity": severity,
                "category": category,
                "field": field,
                "value": value,
                "expected": expected,
            })
    return anomalies


def calculate_risk_score(anomalies: list, ml_score: float) -> int:
    rule_score = sum(SEVERITY_SCORE.get(a["severity"], 0) for a in anomalies)
    ml_contribution = max(0, int((-ml_score - 0.1) / 0.5 * 20)) if ml_score < -0.1 else 0
    return min(100, rule_score + ml_contribution)


def get_risk_level(score: int) -> str:
    if score >= 76: return "critical"
    if score >= 51: return "high"
    if score >= 26: return "medium"
    return "low"


def get_recommendation(level: str) -> str:
    return {"critical": "do_not_sell", "high": "quarantine", "medium": "inspect", "low": "approve"}[level]


def extract_product_context(product: dict) -> str:
    def get(key, fallback="–"):
        val = product.get(key)
        return val if val not in (None, "", [], {}) else fallback

    def tags(key, limit=3):
        vals = product.get(key) or []
        return ", ".join(vals[:limit]) if vals else "–"

    active_alerts = product.get("activeAlerts") or []
    alert_summary = f"{len(active_alerts)} active"
    if active_alerts:
        top = active_alerts[0]
        alert_summary += f" | highest severity: {top.get('severity', '?')}"
        titles = [a.get("title", "") for a in active_alerts[:2] if a.get("title")]
        if titles:
            alert_summary += f" | {' / '.join(titles)}"

    traceability = product.get("traceabilityScore") or {}
    nutrient_levels = product.get("nutrientLevels") or {}
    cold_chain = "yes" if product.get("requiresColdChain") else "no"
    name = get("productName") if get("productName") != "-" else get("genericName")

    lines = [
        f"Name: {name}",
        f"Brand: {get('brands')}",
        f"Quantity: {get('productQuantity')} {get('productQuantityUnit')}",
        f"Category: {tags('categoriesTags', 2)}",
        f"Origin: {tags('countriesTags', 3)}",
        f"Nutri-Score: {get('nutriscoreGrade', '?').upper()}",
        f"Eco-Score: {get('ecoscoreGrade', '?').upper()}",
        f"NOVA group: {get('novaGroup', '?')}",
        f"Nutrient levels: fat={nutrient_levels.get('fat', '?')}, saturated-fat={nutrient_levels.get('saturatedFat', '?')}, sugars={nutrient_levels.get('sugars', '?')}, salt={nutrient_levels.get('salt', '?')}",
        f"Allergens: {tags('allergensTags', 10)}",
        f"Labels: {tags('labelsTags', 5)}",
        f"Cold chain required: {cold_chain}",
        f"Alerts: {alert_summary}",
        f"Traceability: {round(traceability.get('completeness', 0) * 100)}% complete",
    ]
    return "\n".join(lines)


def calculate_sustainability(fields: dict) -> dict:
    co2 = fields.get("co2EmissionsKg") or 0
    batch_kg = fields.get("batchSizeKg") or 100
    co2_per_kg = round(co2 / batch_kg, 3) if batch_kg > 0 else 0
    if co2_per_kg < 1: grade = "a"
    elif co2_per_kg < 2: grade = "b"
    elif co2_per_kg < 4: grade = "c"
    elif co2_per_kg < 7: grade = "d"
    else: grade = "e"
    return {
        "co2TotalKgPerKg": co2_per_kg,
        "ecoscoreGrade": grade,
        "transportEmissionsGramsCo2": int(co2 * 1000 * 0.28),
        "co2ByPhase": {
            "agriculture":   round(co2_per_kg * 0.37, 3),
            "processing":    round(co2_per_kg * 0.25, 3),
            "transportation":round(co2_per_kg * 0.28, 3),
            "packaging":     round(co2_per_kg * 0.10, 3),
        },
    }


class ChatMessage(BaseModel):
    role: str
    content: str


class IntelligenceRequest(BaseModel):
    batchId: str
    productId: str

    # Kühlkette
    hadColdChainBreak: int
    isIntact: int
    highestTemperatureCelsius: float
    lowestTemperatureCelsius: float
    coldChainBreakCount: int
    totalBreakDurationMinutes: float
    totalRefrigeratedTransportHours: float
    coldChainBroken: int
    coldStorage_maxActualTemperatureCelsius: float
    coldStorage_minActualTemperatureCelsius: float
    coldStorage_avgActualTemperatureCelsius: float
    coldStorage_targetTemperatureCelsius: float
    coldChainBreaks_maxTemperatureReached: float
    coldChainBreaks_totalDurationMinutes: float

    # Temperatur
    measuredCelsius: float
    minAllowedCelsius: float
    maxAllowedCelsius: float
    tempIsWithinRange: int
    refrigerationTemperatureCelsius: float
    wasRefrigerated: int
    harvestTemperatureCelsius: float
    processingTemperatureCelsius: float
    displayTemperatureCelsius: float
    sampleArrivalTemperatureCelsius: float

    # Mikrobiologie
    pathogensDetectedCount: int
    pathogensCfuPerGramMax: float
    pathogensLimitExceededCount: int
    microbiologicalDetectedCount: int
    microbiologicalCfuPerGramMax: float
    microbiologicalLimitExceededCount: int

    # Chemikalien
    substancesMeasuredMgPerKgMax: float
    substancesLimitMgPerKg: float
    substancesLimitExceededCount: int
    chemicalMeasuredValueMax: float
    chemicalMrlValue: float
    chemicalMrlExceededCount: int
    chemicalBelowLod: int

    # Labor
    overallVerdictFail: int
    legalLimitsExceeded: int
    exceedanceCount: int
    isIso17025Accredited: int
    nutritionalDeviationPercent: float
    nutritionalIsWithinEuTolerance: int
    physicalOutOfSpecCount: int

    # Allergene
    allergenDetectedCount: int
    allergenMeasuredMgPerKgMax: float
    allergenLabelIncorrectCount: int

    # Authentizität
    authenticityFailCount: int
    authenticityConfidencePercentMin: float

    # Zertifikate
    certificationDaysUntilExpiry: float
    certificationAuditScore: float
    nonConformitiesSeverityMax: int
    nonConformitiesUncorrectedCount: int
    nonConformitiesOverdueDays: float

    # Visuelle Inspektion
    moldDetected: int
    foreignBodyDetected: int
    colorOk: int
    shapeOk: int
    surfaceOk: int
    rejectionRate: float
    visualDefectsFound: int

    # Packaging
    isLeaking: int
    isSealed: int
    vacuumIntact: int
    mapGasCompositionCorrect: int
    labelingCorrect: int
    barcodeReadable: int
    fillWeightCorrect: int
    packagingDefectsFound: int

    # Gewicht
    measuredWeightG: float
    targetWeightG: float
    weightTolerancePercent: float
    weightIsWithinTolerance: int
    weightSampleSize: int

    # Transport & Lagerung
    distanceKm: float
    transportIsRefrigerated: int
    co2EmissionsKg: float
    transportDelayMinutes: float
    maxDurationExceeded: int
    storageAverageTemperatureCelsius: float
    humidityPercent: float
    storageDurationHours: float
    importInspectionPassed: int
    customsCleared: int
    handlingCount: int

    # Alerts
    alertsTotalCount: int
    alertsSeverityMax: int
    alertsActiveCount: int

    # Traceability
    traceabilityCompleteness: float
    traceabilityHasGaps: int
    isThirdPartyVerified: int
    verifiedStations: int
    unknownStations: int

    # Farming
    yieldPercent: float
    areaHectares: float
    isHaccpCertified: int
    batchSizeKg: float
    isMscCertified: int
    isAscCertified: int


class ChatRequest(BaseModel):
    batchId: str
    productId: str
    chatHistory: list[ChatMessage]
    batchContext: Optional[dict] = None
    productInfo: Optional[dict] = None


@app.post("/analyze")
async def analyze(request: IntelligenceRequest):
    all_fields = request.model_dump()

    vector = {f: float(all_fields.get(f) or 0) for f in feature_order}
    df_vec = pd.DataFrame([vector])
    ml_score = float(model.score_samples(df_vec)[0])

    anomalies = build_anomalies(all_fields)
    risk_score = calculate_risk_score(anomalies, ml_score)
    level = get_risk_level(risk_score)
    sustainability = calculate_sustainability(all_fields)

    summary_prompt = (
        f"You are a food safety expert. Summarize this batch in 2-3 sentences:\n"
        f"Batch: {request.batchId} | Risk: {level} (score {risk_score}/100)\n"
        f"Detected anomalies: {json.dumps(anomalies, ensure_ascii=False)}\n"
        f"Be direct and concise."
    )
    llm_response = chat(
        model="llama3.2",
        messages=[{"role": "user", "content": summary_prompt}],
    )

    return {
        "batchId": request.batchId,
        "riskScore": risk_score,
        "riskLevel": level,
        "anomalies": anomalies,
        "sustainability": sustainability,
        "recommendation": get_recommendation(level),
        "summary": llm_response.message.content,
    }


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    messages = [{"role": m.role, "content": m.content} for m in request.chatHistory]

    if request.batchContext or request.productInfo:
        sections = [
            "You are a food safety assistant for the app 'Tomapo Intelligence'.",
            "Answer questions about this product and batch precisely and clearly.\n",
        ]

        if request.productInfo:
            sections.append("=== PRODUCT ===")
            sections.append(extract_product_context(request.productInfo))

        if request.batchContext:
            ctx = request.batchContext
            sustainability = ctx.get("sustainability", {})
            sections.append("\n=== BATCH ANALYSIS ===")
            sections.append(f"Batch: {request.batchId} | Risk: {ctx.get('riskLevel', '?')} (score {ctx.get('riskScore', 0)}/100)")
            sections.append(f"Recommendation: {ctx.get('recommendation', '?')}")
            sections.append(f"Anomalies: {json.dumps(ctx.get('anomalies', []), ensure_ascii=False)}")
            sections.append(f"Ecoscore: {sustainability.get('ecoscoreGrade', '?')} | CO2: {sustainability.get('co2TotalKgPerKg', 0)} kg/kg")

        messages = [{"role": "system", "content": "\n".join(sections)}] + messages

    def generate():
        stream = chat(
            model="llama3.2",
            messages=messages,
            stream=True,
        )
        for chunk in stream:
            chunk: ChatResponse
            yield chunk.message.content or ""

    return StreamingResponse(generate(), media_type="text/plain")


@app.get("/health")
async def health():
    return {"status": "ok"}
