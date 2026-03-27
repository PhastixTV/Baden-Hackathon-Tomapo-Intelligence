## Datenmodell
MongoDB Collection "traces" – wichtigste Felder für Anomalie-Erkennung:

coldChainSummary:
  - hadColdChainBreak: Boolean
  - isIntact: Boolean
  - highestTemperatureCelsius: Number
  - coldChainBreakCount: Number

qualityChecks[]:
  - status: String
  - detail.isWithinRange: Boolean
  - detail.limitExceeded: Boolean
  - detail.detected: Boolean (Pathogene)

certifications[]:
  - validUntil: Date
  - type: String (Bio, Fairtrade etc.)

LaboratoryDetail:
  - overallVerdict: String (PASS/FAIL)
  - legalLimitsExceeded: Boolean
  - microbiologicalResults[].detected: Boolean
  - chemicalResults[].mrlExceeded: Boolean

alerts[]:
  - severity: String (low/medium/high/critical)
  - status: String

## Datenmodell Dokumentation
Die vollständigen Datenmodell-Dateien liegen unter:
- docs/schema-final.html    → komplettes MongoDB Schema aller Felder
- docs/datamodel-uml-3.html → UML Übersicht aller Strukturen

## Was das Modell erkennen soll

KÜHLKETTE:
- coldChainSummary.hadColdChainBreak (Boolean → 0/1)
- coldChainSummary.isIntact (Boolean → 0/1)
- coldChainSummary.highestTemperatureCelsius (Number)
- coldChainSummary.lowestTemperatureCelsius (Number)
- coldChainSummary.coldChainBreakCount (Number)
- coldChainSummary.totalBreakDurationMinutes (Number)
- coldChainSummary.totalRefrigeratedTransportHours (Number)
- coldStorageDetail.coldChainBroken (Boolean → 0/1)
- coldStorageDetail.maxActualTemperatureCelsius (Number)
- coldStorageDetail.minActualTemperatureCelsius (Number)
- coldStorageDetail.avgActualTemperatureCelsius (Number)
- coldStorageDetail.targetTemperatureCelsius (Number)
- coldChainBreaks[].maxTemperatureReached → max Wert (Number)
- coldChainBreaks[].durationMinutes → Summe (Number)

TEMPERATUR:
- TemperatureCheckDetail.measuredCelsius (Number)
- TemperatureCheckDetail.minAllowedCelsius (Number)
- TemperatureCheckDetail.maxAllowedCelsius (Number)
- TemperatureCheckDetail.isWithinRange (Boolean → 0/1)
- refrigerationTemperatureCelsius (Number)
- wasRefrigerated (Boolean → 0/1)
- harvestTemperatureCelsius (Number)
- processingTemperatureCelsius (Number)
- displayTemperatureCelsius (Number)
- sampleArrivalTemperatureCelsius (Number)

MIKROBIOLOGIE:
- pathogensTested[].detected → Anzahl detected (Number)
- pathogensTested[].cfuPerGram → max Wert (Number)
- pathogensTested[].limitExceeded → Anzahl (Number)
- microbiologicalResults[].detected → Anzahl (Number)
- microbiologicalResults[].cfuPerGram → max Wert (Number)
- microbiologicalResults[].limitExceeded → Anzahl (Number)

CHEMIKALIEN:
- substancesTested[].measuredMgPerKg → max Wert (Number)
- substancesTested[].limitMgPerKg (Number)
- substancesTested[].limitExceeded → Anzahl (Number)
- chemicalResults[].measuredValue → max Wert (Number)
- chemicalResults[].mrlValue (Number)
- chemicalResults[].mrlExceeded → Anzahl (Number)
- chemicalResults[].belowLod (Boolean → 0/1)

LABOR:
- LaboratoryDetail.overallVerdict (PASS=0 / FAIL=1)
- LaboratoryDetail.legalLimitsExceeded (Boolean → 0/1)
- LaboratoryDetail.exceedanceCount (Number)
- LaboratoryDetail.isIso17025Accredited (Boolean → 0/1)
- nutritionalAnalysis.deviationFromDeclarationPercent (Number)
- nutritionalAnalysis.isWithinEuTolerance (Boolean → 0/1)
- physicalResults[].isWithinSpec → Anzahl false (Number)

ALLERGENE:
- allergenResults[].detected → Anzahl (Number)
- allergenResults[].measuredMgPerKg → max Wert (Number)
- allergenResults[].declarationOnLabelCorrect → Anzahl false (Number)

AUTHENTIZITÄT:
- authenticityResults[].isAuthentic → Anzahl false (Number)
- authenticityResults[].confidencePercent → min Wert (Number)

ZERTIFIKATE:
- certifications[].validUntil → Tage bis Ablauf, kann negativ sein (Number)
- CertificationAuditDetail.score (Number)
- nonConformities[].severity → critical=3/major=2/minor=1 → max Wert (Number)
- nonConformities[].corrected → Anzahl false (Number)
- nonConformities[].correctionDeadline → Tage überfällig (Number)

VISUELLE INSPEKTION:
- VisualInspectionDetail.moldDetected (Boolean → 0/1)
- VisualInspectionDetail.foreignBodyDetected (Boolean → 0/1)
- VisualInspectionDetail.colorOk (Boolean → 0/1)
- VisualInspectionDetail.shapeOk (Boolean → 0/1)
- VisualInspectionDetail.surfaceOk (Boolean → 0/1)
- VisualInspectionDetail.rejectionRate (Number)
- VisualInspectionDetail.defectsFound → Anzahl (Number)

PACKAGING:
- PackagingIntegrityDetail.isLeaking (Boolean → 0/1)
- PackagingIntegrityDetail.isSealed (Boolean → 0/1)
- PackagingIntegrityDetail.vacuumIntact (Boolean → 0/1)
- PackagingIntegrityDetail.mapGasCompositionCorrect (Boolean → 0/1)
- PackagingIntegrityDetail.labelingCorrect (Boolean → 0/1)
- PackagingIntegrityDetail.barcodeReadable (Boolean → 0/1)
- PackagingIntegrityDetail.fillWeightCorrect (Boolean → 0/1)
- PackagingIntegrityDetail.defectsFound → Anzahl (Number)

GEWICHT:
- WeightCheckDetail.measuredWeightG (Number)
- WeightCheckDetail.targetWeightG (Number)
- WeightCheckDetail.tolerancePercent (Number)
- WeightCheckDetail.isWithinTolerance (Boolean → 0/1)
- WeightCheckDetail.sampleSize (Number)

TRANSPORT & LAGERUNG:
- TransportDetail.distanceKm (Number)
- TransportDetail.isRefrigerated (Boolean → 0/1)
- TransportDetail.co2EmissionsKg (Number)
- TransportDetail.scheduledArrival vs actualArrival → Verspätung in Minuten (Number)
- StorageDetail.maxDurationExceeded (Boolean → 0/1)
- StorageDetail.averageTemperatureCelsius (Number)
- StorageDetail.humidityPercent (Number)
- StorageDetail.storageDurationHours (Number)
- DistributionDetail.importInspectionPassed (Boolean → 0/1)
- DistributionDetail.customsCleared (Boolean → 0/1)
- DistributionDetail.handlingCount (Number)

ALERTS:
- alertIds[] → Anzahl total (Number)
- alerts[].severity → critical=4/high=3/medium=2/low=1 → max Wert (Number)
- alerts[].status → Anzahl active (Number)

TRACEABILITY:
- traceabilityScore.completeness (Number 0–1)
- traceabilityScore.hasGaps (Boolean → 0/1)
- traceabilityScore.isThirdPartyVerified (Boolean → 0/1)
- traceabilityScore.verifiedStations (Number)
- traceabilityScore.unknownStations (Number)

FARMING:
- HarvestDetail.yieldPercent (Number)
- FarmingDetail.areaHectares (Number)
- ProcessingDetail.isHaccpCertified (Boolean → 0/1)
- ProcessingDetail.batchSizeKg (Number)
- FishingDetail.isMscCertified (Boolean → 0/1)
- FishingDetail.isAscCertified (Boolean → 0/1)