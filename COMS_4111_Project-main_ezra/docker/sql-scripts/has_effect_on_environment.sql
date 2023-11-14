INSERT INTO HasEffectOnEnvironment (MaterialID, ImpactID)
SELECT MaterialID, ImpactID
FROM EnvironmentalImpact
WHERE MaterialID BETWEEN 0 AND 82;
