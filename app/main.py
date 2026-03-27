from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
from ollama import chat, ChatResponse

app = FastAPI()


class ChatMessage(BaseModel):
    role: str
    content: str


class IntelligenceRequest(BaseModel):
    batchId: str
    productId: str
    chatHistory: Optional[list[ChatMessage]] = None

    # Kühlkette
    hadColdChainBreak: Optional[int] = None
    isIntact: Optional[int] = None
    highestTemperatureCelsius: Optional[float] = None
    lowestTemperatureCelsius: Optional[float] = None
    coldChainBreakCount: Optional[int] = None
    totalBreakDurationMinutes: Optional[float] = None
    totalRefrigeratedTransportHours: Optional[float] = None
    coldChainBroken: Optional[int] = None
    coldStorage_maxActualTemperatureCelsius: Optional[float] = None
    coldStorage_minActualTemperatureCelsius: Optional[float] = None
    coldStorage_avgActualTemperatureCelsius: Optional[float] = None
    coldStorage_targetTemperatureCelsius: Optional[float] = None
    coldChainBreaks_maxTemperatureReached: Optional[float] = None
    coldChainBreaks_totalDurationMinutes: Optional[float] = None

    # Temperatur
    measuredCelsius: Optional[float] = None
    minAllowedCelsius: Optional[float] = None
    maxAllowedCelsius: Optional[float] = None
    tempIsWithinRange: Optional[int] = None
    refrigerationTemperatureCelsius: Optional[float] = None
    wasRefrigerated: Optional[int] = None
    harvestTemperatureCelsius: Optional[float] = None
    processingTemperatureCelsius: Optional[float] = None
    displayTemperatureCelsius: Optional[float] = None
    sampleArrivalTemperatureCelsius: Optional[float] = None

    # Mikrobiologie
    pathogensDetectedCount: Optional[int] = None
    pathogensCfuPerGramMax: Optional[float] = None
    pathogensLimitExceededCount: Optional[int] = None
    microbiologicalDetectedCount: Optional[int] = None
    microbiologicalCfuPerGramMax: Optional[float] = None
    microbiologicalLimitExceededCount: Optional[int] = None

    # Chemikalien
    substancesMeasuredMgPerKgMax: Optional[float] = None
    substancesLimitMgPerKg: Optional[float] = None
    substancesLimitExceededCount: Optional[int] = None
    chemicalMeasuredValueMax: Optional[float] = None
    chemicalMrlValue: Optional[float] = None
    chemicalMrlExceededCount: Optional[int] = None
    chemicalBelowLod: Optional[int] = None

    # Labor
    overallVerdictFail: Optional[int] = None
    legalLimitsExceeded: Optional[int] = None
    exceedanceCount: Optional[int] = None
    isIso17025Accredited: Optional[int] = None
    nutritionalDeviationPercent: Optional[float] = None
    nutritionalIsWithinEuTolerance: Optional[int] = None
    physicalOutOfSpecCount: Optional[int] = None

    # Allergene
    allergenDetectedCount: Optional[int] = None
    allergenMeasuredMgPerKgMax: Optional[float] = None
    allergenLabelIncorrectCount: Optional[int] = None

    # Authentizität
    authenticityFailCount: Optional[int] = None
    authenticityConfidencePercentMin: Optional[float] = None

    # Zertifikate
    certificationDaysUntilExpiry: Optional[float] = None
    certificationAuditScore: Optional[float] = None
    nonConformitiesSeverityMax: Optional[int] = None
    nonConformitiesUncorrectedCount: Optional[int] = None
    nonConformitiesOverdueDays: Optional[float] = None

    # Visuelle Inspektion
    moldDetected: Optional[int] = None
    foreignBodyDetected: Optional[int] = None
    colorOk: Optional[int] = None
    shapeOk: Optional[int] = None
    surfaceOk: Optional[int] = None
    rejectionRate: Optional[float] = None
    visualDefectsFound: Optional[int] = None

    # Packaging
    isLeaking: Optional[int] = None
    isSealed: Optional[int] = None
    vacuumIntact: Optional[int] = None
    mapGasCompositionCorrect: Optional[int] = None
    labelingCorrect: Optional[int] = None
    barcodeReadable: Optional[int] = None
    fillWeightCorrect: Optional[int] = None
    packagingDefectsFound: Optional[int] = None

    # Gewicht
    measuredWeightG: Optional[float] = None
    targetWeightG: Optional[float] = None
    weightTolerancePercent: Optional[float] = None
    weightIsWithinTolerance: Optional[int] = None
    weightSampleSize: Optional[int] = None

    # Transport & Lagerung
    distanceKm: Optional[float] = None
    transportIsRefrigerated: Optional[int] = None
    co2EmissionsKg: Optional[float] = None
    transportDelayMinutes: Optional[float] = None
    maxDurationExceeded: Optional[int] = None
    storageAverageTemperatureCelsius: Optional[float] = None
    humidityPercent: Optional[float] = None
    storageDurationHours: Optional[float] = None
    importInspectionPassed: Optional[int] = None
    customsCleared: Optional[int] = None
    handlingCount: Optional[int] = None

    # Alerts
    alertsTotalCount: Optional[int] = None
    alertsSeverityMax: Optional[int] = None
    alertsActiveCount: Optional[int] = None

    # Traceability
    traceabilityCompleteness: Optional[float] = None
    traceabilityHasGaps: Optional[int] = None
    isThirdPartyVerified: Optional[int] = None
    verifiedStations: Optional[int] = None
    unknownStations: Optional[int] = None

    # Farming
    yieldPercent: Optional[float] = None
    areaHectares: Optional[float] = None
    isHaccpCertified: Optional[int] = None
    batchSizeKg: Optional[float] = None
    isMscCertified: Optional[int] = None
    isAscCertified: Optional[int] = None

    def has_ml_data(self) -> bool:
        all_fields = self.model_dump()
        base_fields = {"batchId", "productId", "chatHistory"}

        for field_name, field_value in all_fields.items():
            if field_name not in base_fields and field_value is not None:
                return True

        return False


@app.post("/analyze")
async def analyze(request: IntelligenceRequest):
    if request.has_ml_data():
        # → ML Pipeline + LLM Summary
        return {"route": "ml", "batchId": request.batchId}
    else:
        if request.chatHistory is None:
            return {"status:" "chatHistory is None"}
        def generate():
            stream = chat(
                model='llama3.2',
                messages=[{"role": m.role, "content": m.content} for m in (request.chatHistory or [])],
                stream=True,
            )
            for chunk in stream:
                chunk: ChatResponse
                yield chunk.message.content or ""

        return StreamingResponse(generate(), media_type="text/plain")


@app.get("/health")
async def health():
    return {"status": "ok"}
