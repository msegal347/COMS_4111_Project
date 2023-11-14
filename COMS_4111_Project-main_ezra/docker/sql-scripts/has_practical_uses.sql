INSERT INTO HasPracticalUses (MaterialID, ApplicationID)
SELECT m.MaterialID, a.ApplicationID
FROM Material m
JOIN IndustrialApplications a ON m.MaterialID = a.MaterialID
WHERE m.MaterialID BETWEEN 0 AND 82;

