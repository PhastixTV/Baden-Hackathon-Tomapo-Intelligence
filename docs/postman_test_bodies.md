# Postman Test Bodies

## Endpoints
- `POST http://localhost:8000/analyze` — all 90 fields required
- `POST http://localhost:8000/chat`    — chatHistory required, batchContext + productInfo optional
- `GET  http://localhost:8000/health`

---

## POST /analyze — Normal (meat, everything green)

```json
{
  "batchId": "batch-normal-001",
  "productId": "prod-meat-001",
  "hadColdChainBreak": 0,
  "isIntact": 1,
  "highestTemperatureCelsius": 6.8,
  "lowestTemperatureCelsius": 3.2,
  "coldChainBreakCount": 0,
  "totalBreakDurationMinutes": 0,
  "totalRefrigeratedTransportHours": 12,
  "coldChainBroken": 0,
  "coldStorage_maxActualTemperatureCelsius": 6.5,
  "coldStorage_minActualTemperatureCelsius": 3.1,
  "coldStorage_avgActualTemperatureCelsius": 5.0,
  "coldStorage_targetTemperatureCelsius": 5.0,
  "coldChainBreaks_maxTemperatureReached": 0,
  "coldChainBreaks_totalDurationMinutes": 0,
  "measuredCelsius": 5.2,
  "minAllowedCelsius": 0,
  "maxAllowedCelsius": 7,
  "tempIsWithinRange": 1,
  "refrigerationTemperatureCelsius": 5.0,
  "wasRefrigerated": 1,
  "harvestTemperatureCelsius": 18,
  "processingTemperatureCelsius": 5.5,
  "displayTemperatureCelsius": 5.0,
  "sampleArrivalTemperatureCelsius": 5.3,
  "pathogensDetectedCount": 0,
  "pathogensCfuPerGramMax": 0,
  "pathogensLimitExceededCount": 0,
  "microbiologicalDetectedCount": 0,
  "microbiologicalCfuPerGramMax": 850,
  "microbiologicalLimitExceededCount": 0,
  "substancesMeasuredMgPerKgMax": 0.01,
  "substancesLimitMgPerKg": 0.1,
  "substancesLimitExceededCount": 0,
  "chemicalMeasuredValueMax": 0.02,
  "chemicalMrlValue": 0.1,
  "chemicalMrlExceededCount": 0,
  "chemicalBelowLod": 1,
  "overallVerdictFail": 0,
  "legalLimitsExceeded": 0,
  "exceedanceCount": 0,
  "isIso17025Accredited": 1,
  "nutritionalDeviationPercent": 1.5,
  "nutritionalIsWithinEuTolerance": 1,
  "physicalOutOfSpecCount": 0,
  "allergenDetectedCount": 0,
  "allergenMeasuredMgPerKgMax": 0,
  "allergenLabelIncorrectCount": 0,
  "authenticityFailCount": 0,
  "authenticityConfidencePercentMin": 97,
  "certificationDaysUntilExpiry": 180,
  "certificationAuditScore": 92,
  "nonConformitiesSeverityMax": 0,
  "nonConformitiesUncorrectedCount": 0,
  "nonConformitiesOverdueDays": 0,
  "moldDetected": 0,
  "foreignBodyDetected": 0,
  "colorOk": 1,
  "shapeOk": 1,
  "surfaceOk": 1,
  "rejectionRate": 0.5,
  "visualDefectsFound": 0,
  "isLeaking": 0,
  "isSealed": 1,
  "vacuumIntact": 1,
  "mapGasCompositionCorrect": 1,
  "labelingCorrect": 1,
  "barcodeReadable": 1,
  "fillWeightCorrect": 1,
  "packagingDefectsFound": 0,
  "measuredWeightG": 498,
  "targetWeightG": 500,
  "weightTolerancePercent": 2,
  "weightIsWithinTolerance": 1,
  "weightSampleSize": 10,
  "distanceKm": 320,
  "transportIsRefrigerated": 1,
  "co2EmissionsKg": 12.5,
  "transportDelayMinutes": 15,
  "maxDurationExceeded": 0,
  "storageAverageTemperatureCelsius": 5.1,
  "humidityPercent": 65,
  "storageDurationHours": 18,
  "importInspectionPassed": 1,
  "customsCleared": 1,
  "handlingCount": 3,
  "alertsTotalCount": 0,
  "alertsSeverityMax": 0,
  "alertsActiveCount": 0,
  "traceabilityCompleteness": 0.97,
  "traceabilityHasGaps": 0,
  "isThirdPartyVerified": 1,
  "verifiedStations": 5,
  "unknownStations": 0,
  "yieldPercent": 88,
  "areaHectares": 12,
  "isHaccpCertified": 1,
  "batchSizeKg": 500,
  "isMscCertified": 0,
  "isAscCertified": 0
}
```

---

## POST /analyze — High Risk (fish, cold chain break)

```json
{
  "batchId": "batch-warn-002",
  "productId": "prod-fish-002",
  "hadColdChainBreak": 1,
  "isIntact": 0,
  "highestTemperatureCelsius": 9.5,
  "lowestTemperatureCelsius": 0.8,
  "coldChainBreakCount": 1,
  "totalBreakDurationMinutes": 75,
  "totalRefrigeratedTransportHours": 8,
  "coldChainBroken": 1,
  "coldStorage_maxActualTemperatureCelsius": 9.5,
  "coldStorage_minActualTemperatureCelsius": 0.8,
  "coldStorage_avgActualTemperatureCelsius": 3.2,
  "coldStorage_targetTemperatureCelsius": 2.0,
  "coldChainBreaks_maxTemperatureReached": 9.5,
  "coldChainBreaks_totalDurationMinutes": 75,
  "measuredCelsius": 9.5,
  "minAllowedCelsius": 0,
  "maxAllowedCelsius": 4,
  "tempIsWithinRange": 0,
  "refrigerationTemperatureCelsius": 3.2,
  "wasRefrigerated": 1,
  "harvestTemperatureCelsius": 16,
  "processingTemperatureCelsius": 2.0,
  "displayTemperatureCelsius": 3.5,
  "sampleArrivalTemperatureCelsius": 9.5,
  "pathogensDetectedCount": 0,
  "pathogensCfuPerGramMax": 0,
  "pathogensLimitExceededCount": 0,
  "microbiologicalDetectedCount": 0,
  "microbiologicalCfuPerGramMax": 12000,
  "microbiologicalLimitExceededCount": 0,
  "substancesMeasuredMgPerKgMax": 0.02,
  "substancesLimitMgPerKg": 0.1,
  "substancesLimitExceededCount": 0,
  "chemicalMeasuredValueMax": 0.03,
  "chemicalMrlValue": 0.1,
  "chemicalMrlExceededCount": 0,
  "chemicalBelowLod": 1,
  "overallVerdictFail": 0,
  "legalLimitsExceeded": 0,
  "exceedanceCount": 0,
  "isIso17025Accredited": 1,
  "nutritionalDeviationPercent": 2.1,
  "nutritionalIsWithinEuTolerance": 1,
  "physicalOutOfSpecCount": 0,
  "allergenDetectedCount": 0,
  "allergenMeasuredMgPerKgMax": 0,
  "allergenLabelIncorrectCount": 0,
  "authenticityFailCount": 0,
  "authenticityConfidencePercentMin": 94,
  "certificationDaysUntilExpiry": 90,
  "certificationAuditScore": 85,
  "nonConformitiesSeverityMax": 0,
  "nonConformitiesUncorrectedCount": 0,
  "nonConformitiesOverdueDays": 0,
  "moldDetected": 0,
  "foreignBodyDetected": 0,
  "colorOk": 1,
  "shapeOk": 1,
  "surfaceOk": 1,
  "rejectionRate": 1.2,
  "visualDefectsFound": 1,
  "isLeaking": 0,
  "isSealed": 1,
  "vacuumIntact": 1,
  "mapGasCompositionCorrect": 1,
  "labelingCorrect": 1,
  "barcodeReadable": 1,
  "fillWeightCorrect": 1,
  "packagingDefectsFound": 0,
  "measuredWeightG": 495,
  "targetWeightG": 500,
  "weightTolerancePercent": 2,
  "weightIsWithinTolerance": 1,
  "weightSampleSize": 8,
  "distanceKm": 580,
  "transportIsRefrigerated": 1,
  "co2EmissionsKg": 18.4,
  "transportDelayMinutes": 40,
  "maxDurationExceeded": 0,
  "storageAverageTemperatureCelsius": 3.2,
  "humidityPercent": 70,
  "storageDurationHours": 24,
  "importInspectionPassed": 1,
  "customsCleared": 1,
  "handlingCount": 4,
  "alertsTotalCount": 1,
  "alertsSeverityMax": 2,
  "alertsActiveCount": 1,
  "traceabilityCompleteness": 0.91,
  "traceabilityHasGaps": 0,
  "isThirdPartyVerified": 1,
  "verifiedStations": 4,
  "unknownStations": 0,
  "yieldPercent": 82,
  "areaHectares": 0,
  "isHaccpCertified": 1,
  "batchSizeKg": 300,
  "isMscCertified": 1,
  "isAscCertified": 1
}
```

---

## POST /analyze — Critical (vegetables, everything wrong)

```json
{
  "batchId": "batch-critical-003",
  "productId": "prod-veg-003",
  "hadColdChainBreak": 1,
  "isIntact": 0,
  "highestTemperatureCelsius": 24.0,
  "lowestTemperatureCelsius": 2.0,
  "coldChainBreakCount": 4,
  "totalBreakDurationMinutes": 420,
  "totalRefrigeratedTransportHours": 2,
  "coldChainBroken": 1,
  "coldStorage_maxActualTemperatureCelsius": 24.0,
  "coldStorage_minActualTemperatureCelsius": 2.0,
  "coldStorage_avgActualTemperatureCelsius": 14.0,
  "coldStorage_targetTemperatureCelsius": 4.0,
  "coldChainBreaks_maxTemperatureReached": 24.0,
  "coldChainBreaks_totalDurationMinutes": 420,
  "measuredCelsius": 22.0,
  "minAllowedCelsius": 0,
  "maxAllowedCelsius": 8,
  "tempIsWithinRange": 0,
  "refrigerationTemperatureCelsius": 14.0,
  "wasRefrigerated": 0,
  "harvestTemperatureCelsius": 22,
  "processingTemperatureCelsius": 18.0,
  "displayTemperatureCelsius": 20.0,
  "sampleArrivalTemperatureCelsius": 22.0,
  "pathogensDetectedCount": 3,
  "pathogensCfuPerGramMax": 1500000,
  "pathogensLimitExceededCount": 3,
  "microbiologicalDetectedCount": 3,
  "microbiologicalCfuPerGramMax": 8500000,
  "microbiologicalLimitExceededCount": 3,
  "substancesMeasuredMgPerKgMax": 1.85,
  "substancesLimitMgPerKg": 0.2,
  "substancesLimitExceededCount": 3,
  "chemicalMeasuredValueMax": 1.85,
  "chemicalMrlValue": 0.2,
  "chemicalMrlExceededCount": 3,
  "chemicalBelowLod": 0,
  "overallVerdictFail": 1,
  "legalLimitsExceeded": 1,
  "exceedanceCount": 5,
  "isIso17025Accredited": 1,
  "nutritionalDeviationPercent": 28.0,
  "nutritionalIsWithinEuTolerance": 0,
  "physicalOutOfSpecCount": 4,
  "allergenDetectedCount": 0,
  "allergenMeasuredMgPerKgMax": 0,
  "allergenLabelIncorrectCount": 0,
  "authenticityFailCount": 2,
  "authenticityConfidencePercentMin": 41,
  "certificationDaysUntilExpiry": -5,
  "certificationAuditScore": 48,
  "nonConformitiesSeverityMax": 3,
  "nonConformitiesUncorrectedCount": 4,
  "nonConformitiesOverdueDays": 12,
  "moldDetected": 1,
  "foreignBodyDetected": 1,
  "colorOk": 0,
  "shapeOk": 0,
  "surfaceOk": 0,
  "rejectionRate": 35.0,
  "visualDefectsFound": 12,
  "isLeaking": 1,
  "isSealed": 0,
  "vacuumIntact": 0,
  "mapGasCompositionCorrect": 0,
  "labelingCorrect": 0,
  "barcodeReadable": 1,
  "fillWeightCorrect": 0,
  "packagingDefectsFound": 5,
  "measuredWeightG": 430,
  "targetWeightG": 500,
  "weightTolerancePercent": 2,
  "weightIsWithinTolerance": 0,
  "weightSampleSize": 10,
  "distanceKm": 1200,
  "transportIsRefrigerated": 0,
  "co2EmissionsKg": 85.0,
  "transportDelayMinutes": 320,
  "maxDurationExceeded": 1,
  "storageAverageTemperatureCelsius": 18.0,
  "humidityPercent": 92,
  "storageDurationHours": 96,
  "importInspectionPassed": 0,
  "customsCleared": 1,
  "handlingCount": 9,
  "alertsTotalCount": 8,
  "alertsSeverityMax": 4,
  "alertsActiveCount": 5,
  "traceabilityCompleteness": 0.41,
  "traceabilityHasGaps": 1,
  "isThirdPartyVerified": 0,
  "verifiedStations": 2,
  "unknownStations": 3,
  "yieldPercent": 45,
  "areaHectares": 8,
  "isHaccpCertified": 0,
  "batchSizeKg": 800,
  "isMscCertified": 0,
  "isAscCertified": 0
}
```

---

## POST /chat — No context

```json
{
  "batchId": "batch-warn-002",
  "productId": "prod-fish-002",
  "chatHistory": [
    { "role": "user", "content": "What is a cold chain break?" }
  ]
}
```

---

## POST /chat — With batchContext only

```json
{
  "batchId": "batch-warn-002",
  "productId": "prod-fish-002",
  "chatHistory": [
    { "role": "user", "content": "Why was this batch rated as high risk?" }
  ],
  "batchContext": {
    "batchId": "batch-warn-002",
    "riskScore": 57,
    "riskLevel": "high",
    "anomalies": [
      { "severity": "high", "category": "coldChain", "field": "hadColdChainBreak", "value": 1, "expected": 0 },
      { "severity": "high", "category": "coldChain", "field": "coldChainBreakCount", "value": 1, "expected": 0 },
      { "severity": "medium", "category": "temperature", "field": "tempIsWithinRange", "value": 0, "expected": 1 }
    ],
    "sustainability": { "co2TotalKgPerKg": 0.061, "ecoscoreGrade": "a", "transportEmissionsGramsCo2": 5152 },
    "recommendation": "quarantine",
    "summary": "Batch shows a cold chain breach reaching 9.5°C for 75 minutes. No pathogens detected but elevated bacterial count. Quarantine recommended pending full inspection."
  }
}
```

---

## POST /chat — With batchContext + productInfo

```json
{
  "batchId": "batch-warn-002",
  "productId": "prod-fish-002",
  "chatHistory": [
    { "role": "user", "content": "Is this product safe to eat given the cold chain issue?" }
  ],
  "batchContext": {
    "batchId": "batch-warn-002",
    "riskScore": 57,
    "riskLevel": "high",
    "anomalies": [
      { "severity": "high", "category": "coldChain", "field": "hadColdChainBreak", "value": 1, "expected": 0 },
      { "severity": "high", "category": "coldChain", "field": "coldChainBreakCount", "value": 1, "expected": 0 },
      { "severity": "medium", "category": "temperature", "field": "tempIsWithinRange", "value": 0, "expected": 1 }
    ],
    "sustainability": { "co2TotalKgPerKg": 0.061, "ecoscoreGrade": "a", "transportEmissionsGramsCo2": 5152 },
    "recommendation": "quarantine",
    "summary": "Batch shows a cold chain breach reaching 9.5°C for 75 minutes."
  },
  "productInfo": {
    "productName": "Atlantic Salmon Fillet",
    "brands": "Nordic Fresh",
    "productQuantity": 300,
    "productQuantityUnit": "g",
    "categoriesTags": ["fish", "seafood", "fresh-fish"],
    "countriesTags": ["Norway"],
    "nutriscoreGrade": "a",
    "ecoscoreGrade": "b",
    "novaGroup": 1,
    "nutrientLevels": { "fat": "moderate", "saturatedFat": "low", "sugars": "low", "salt": "low" },
    "allergensTags": ["fish"],
    "labelsTags": ["msc-certified", "no-additives"],
    "requiresColdChain": true,
    "activeAlerts": [
      { "severity": "high", "title": "Cold chain breach reported", "description": "Temperature exceeded safe limit during transport." }
    ],
    "traceabilityScore": { "completeness": 0.91, "verifiedStations": 4, "hasGaps": false, "isThirdPartyVerified": true }
  }
}
```
