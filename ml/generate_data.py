import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

CATEGORIES = ["fish", "meat", "vegetables", "beverages"]

# Normal temperature ranges per category (min, max) in Celsius
NORMAL_TEMP = {
    "fish":       (0.0,  2.0),
    "meat":       (3.0,  7.0),
    "vegetables": (0.0,  8.0),
    "beverages":  (4.0, 25.0),
}

# Max allowed temperature before cold chain break
MAX_TEMP = {
    "fish":       4.0,
    "meat":       7.0,
    "vegetables": 12.0,
    "beverages":  30.0,
}

# Normal CFU/g range (log scale: log10 of CFU/g)
NORMAL_CFU_LOG = {
    "fish":       (1.0, 4.0),
    "meat":       (1.0, 4.0),
    "vegetables": (1.0, 4.0),
    "beverages":  (0.0, 2.0),
}

# Normal MRL range in mg/kg
NORMAL_MRL = {
    "fish":       (0.0, 0.05),
    "meat":       (0.0, 0.05),
    "vegetables": (0.0, 0.10),
    "beverages":  (0.0, 0.05),
}


def normal_sample(category: str) -> dict:
    t_min, t_max = NORMAL_TEMP[category]
    temp = rng.uniform(t_min, t_max)
    cfu_log_min, cfu_log_max = NORMAL_CFU_LOG[category]
    cfu = 10 ** rng.uniform(cfu_log_min, cfu_log_max)
    mrl_min, mrl_max = NORMAL_MRL[category]
    mrl = rng.uniform(mrl_min, mrl_max)

    return {
        # Kühlkette
        "hadColdChainBreak": 0,
        "isIntact": 1,
        "highestTemperatureCelsius": round(temp + rng.uniform(0, 0.5), 2),
        "lowestTemperatureCelsius": round(temp - rng.uniform(0, 0.5), 2),
        "coldChainBreakCount": 0,
        "totalBreakDurationMinutes": 0.0,
        "totalRefrigeratedTransportHours": round(rng.uniform(2, 24), 1),
        "coldChainBroken": 0,
        "coldStorage_maxActualTemperatureCelsius": round(temp + rng.uniform(0, 0.3), 2),
        "coldStorage_minActualTemperatureCelsius": round(temp - rng.uniform(0, 0.3), 2),
        "coldStorage_avgActualTemperatureCelsius": round(temp, 2),
        "coldStorage_targetTemperatureCelsius": round((NORMAL_TEMP[category][0] + NORMAL_TEMP[category][1]) / 2, 1),
        "coldChainBreaks_maxTemperatureReached": 0.0,
        "coldChainBreaks_totalDurationMinutes": 0.0,
        # Temperatur
        "measuredCelsius": round(temp, 2),
        "minAllowedCelsius": round(NORMAL_TEMP[category][0], 1),
        "maxAllowedCelsius": round(MAX_TEMP[category], 1),
        "tempIsWithinRange": 1,
        "refrigerationTemperatureCelsius": round(temp, 2),
        "wasRefrigerated": 1,
        "harvestTemperatureCelsius": round(rng.uniform(15, 25), 1),
        "processingTemperatureCelsius": round(temp + rng.uniform(0, 1), 2),
        "displayTemperatureCelsius": round(temp + rng.uniform(0, 0.5), 2),
        "sampleArrivalTemperatureCelsius": round(temp + rng.uniform(0, 0.5), 2),
        # Mikrobiologie
        "pathogensDetectedCount": 0,
        "pathogensCfuPerGramMax": 0.0,
        "pathogensLimitExceededCount": 0,
        "microbiologicalDetectedCount": 0,
        "microbiologicalCfuPerGramMax": round(cfu, 2),
        "microbiologicalLimitExceededCount": 0,
        # Chemikalien
        "substancesMeasuredMgPerKgMax": round(mrl, 4),
        "substancesLimitMgPerKg": round(NORMAL_MRL[category][1] * 2, 3),
        "substancesLimitExceededCount": 0,
        "chemicalMeasuredValueMax": round(mrl, 4),
        "chemicalMrlValue": round(NORMAL_MRL[category][1] * 2, 3),
        "chemicalMrlExceededCount": 0,
        "chemicalBelowLod": int(mrl < 0.01),
        # Labor
        "overallVerdictFail": 0,
        "legalLimitsExceeded": 0,
        "exceedanceCount": 0,
        "isIso17025Accredited": 1,
        "nutritionalDeviationPercent": round(rng.uniform(0, 3), 2),
        "nutritionalIsWithinEuTolerance": 1,
        "physicalOutOfSpecCount": 0,
        # Allergene
        "allergenDetectedCount": 0,
        "allergenMeasuredMgPerKgMax": 0.0,
        "allergenLabelIncorrectCount": 0,
        # Authentizität
        "authenticityFailCount": 0,
        "authenticityConfidencePercentMin": round(rng.uniform(90, 100), 1),
        # Zertifikate
        "certificationDaysUntilExpiry": round(rng.uniform(30, 365), 0),
        "certificationAuditScore": round(rng.uniform(80, 100), 1),
        "nonConformitiesSeverityMax": 0,
        "nonConformitiesUncorrectedCount": 0,
        "nonConformitiesOverdueDays": 0.0,
        # Visuelle Inspektion
        "moldDetected": 0,
        "foreignBodyDetected": 0,
        "colorOk": 1,
        "shapeOk": 1,
        "surfaceOk": 1,
        "rejectionRate": round(rng.uniform(0, 2), 2),
        "visualDefectsFound": int(rng.integers(0, 2)),
        # Packaging
        "isLeaking": 0,
        "isSealed": 1,
        "vacuumIntact": 1,
        "mapGasCompositionCorrect": 1,
        "labelingCorrect": 1,
        "barcodeReadable": 1,
        "fillWeightCorrect": 1,
        "packagingDefectsFound": 0,
        # Gewicht
        "measuredWeightG": round(rng.uniform(450, 510), 1),
        "targetWeightG": 500.0,
        "weightTolerancePercent": 2.0,
        "weightIsWithinTolerance": 1,
        "weightSampleSize": int(rng.integers(5, 20)),
        # Transport & Lagerung
        "distanceKm": round(rng.uniform(50, 800), 1),
        "transportIsRefrigerated": 1,
        "co2EmissionsKg": round(rng.uniform(5, 50), 2),
        "transportDelayMinutes": round(rng.uniform(0, 30), 0),
        "maxDurationExceeded": 0,
        "storageAverageTemperatureCelsius": round(temp, 2),
        "humidityPercent": round(rng.uniform(50, 80), 1),
        "storageDurationHours": round(rng.uniform(2, 48), 1),
        "importInspectionPassed": 1,
        "customsCleared": 1,
        "handlingCount": int(rng.integers(1, 6)),
        # Alerts
        "alertsTotalCount": int(rng.integers(0, 2)),
        "alertsSeverityMax": int(rng.choice([0, 1], p=[0.7, 0.3])),
        "alertsActiveCount": 0,
        # Traceability
        "traceabilityCompleteness": round(rng.uniform(0.85, 1.0), 3),
        "traceabilityHasGaps": 0,
        "isThirdPartyVerified": 1,
        "verifiedStations": int(rng.integers(3, 8)),
        "unknownStations": 0,
        # Farming
        "yieldPercent": round(rng.uniform(75, 98), 1),
        "areaHectares": round(rng.uniform(1, 50), 2),
        "isHaccpCertified": 1,
        "batchSizeKg": round(rng.uniform(100, 5000), 1),
        "isMscCertified": int(category == "fish"),
        "isAscCertified": int(category == "fish"),
    }


def anomalous_sample(category: str) -> dict:
    sample = normal_sample(category)

    anomaly_types = rng.choice(
        ["cold_chain", "microbiology", "chemical", "lab_fail", "alerts"],
        size=int(rng.integers(1, 4)),
        replace=False,
    )

    for anomaly in anomaly_types:
        if anomaly == "cold_chain":
            breach_temp = MAX_TEMP[category] + rng.uniform(2, 15)
            sample["hadColdChainBreak"] = 1
            sample["coldChainBroken"] = 1
            sample["isIntact"] = 0
            sample["coldChainBreakCount"] = int(rng.integers(1, 6))
            sample["totalBreakDurationMinutes"] = round(rng.uniform(30, 480), 0)
            sample["highestTemperatureCelsius"] = round(breach_temp, 2)
            sample["coldChainBreaks_maxTemperatureReached"] = round(breach_temp, 2)
            sample["coldChainBreaks_totalDurationMinutes"] = sample["totalBreakDurationMinutes"]
            sample["coldStorage_maxActualTemperatureCelsius"] = round(breach_temp, 2)
            sample["tempIsWithinRange"] = 0
            sample["measuredCelsius"] = round(breach_temp, 2)

        elif anomaly == "microbiology":
            cfu_anomaly = 10 ** rng.uniform(5, 7)
            sample["pathogensDetectedCount"] = int(rng.integers(1, 4))
            sample["pathogensCfuPerGramMax"] = round(cfu_anomaly, 0)
            sample["pathogensLimitExceededCount"] = int(rng.integers(1, 4))
            sample["microbiologicalDetectedCount"] = int(rng.integers(1, 4))
            sample["microbiologicalCfuPerGramMax"] = round(cfu_anomaly, 0)
            sample["microbiologicalLimitExceededCount"] = int(rng.integers(1, 4))

        elif anomaly == "chemical":
            mrl_limit = NORMAL_MRL[category][1] * 2
            mrl_exceeded = mrl_limit * rng.uniform(2, 10)
            sample["substancesMeasuredMgPerKgMax"] = round(mrl_exceeded, 4)
            sample["substancesLimitExceededCount"] = int(rng.integers(1, 4))
            sample["chemicalMeasuredValueMax"] = round(mrl_exceeded, 4)
            sample["chemicalMrlExceededCount"] = int(rng.integers(1, 4))
            sample["chemicalBelowLod"] = 0

        elif anomaly == "lab_fail":
            sample["overallVerdictFail"] = 1
            sample["legalLimitsExceeded"] = 1
            sample["exceedanceCount"] = int(rng.integers(1, 6))
            sample["nutritionalDeviationPercent"] = round(rng.uniform(10, 40), 2)
            sample["nutritionalIsWithinEuTolerance"] = 0
            sample["physicalOutOfSpecCount"] = int(rng.integers(1, 5))

        elif anomaly == "alerts":
            sample["alertsTotalCount"] = int(rng.integers(3, 10))
            sample["alertsSeverityMax"] = int(rng.choice([3, 4]))
            sample["alertsActiveCount"] = int(rng.integers(2, 6))
            sample["traceabilityHasGaps"] = 1
            sample["traceabilityCompleteness"] = round(rng.uniform(0.3, 0.65), 3)
            sample["unknownStations"] = int(rng.integers(1, 4))

    return sample


def sparse_normal_sample(category: str) -> dict:
    """Normal sample where only 30-50% of fields are filled (rest = 0).
    Teaches the model that sparse input is also normal."""
    sample = normal_sample(category)
    keys = list(sample.keys())
    n_keep = max(10, int(len(keys) * rng.uniform(0.3, 0.5)))
    keys_to_keep = set(rng.choice(keys, size=n_keep, replace=False))
    return {k: (v if k in keys_to_keep else 0) for k, v in sample.items()}


def generate(n_normal: int = 1000, n_sparse: int = 400, n_anomalous: int = 110) -> pd.DataFrame:
    rows = []

    for _ in range(n_normal):
        category = str(rng.choice(CATEGORIES))
        rows.append(normal_sample(category))

    for _ in range(n_sparse):
        category = str(rng.choice(CATEGORIES))
        rows.append(sparse_normal_sample(category))

    for _ in range(n_anomalous):
        category = str(rng.choice(CATEGORIES))
        rows.append(anomalous_sample(category))

    df = pd.DataFrame(rows)
    return df


if __name__ == "__main__":
    df = generate()
    output_path = "ml/training_data.csv"
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} rows -> {output_path}")
    print(f"Columns: {len(df.columns)}")
