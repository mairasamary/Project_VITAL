-- Project VITAL Assignment 4
-- Execute ONLY in a new, isolated A4 OpenEMR database.
-- Do not execute against an existing course or clinical database.

DROP PROCEDURE IF EXISTS check_a4_empty_database;

DELIMITER //
CREATE PROCEDURE check_a4_empty_database()
BEGIN
  IF (SELECT COUNT(*) FROM patient_data) > 0 OR (SELECT COUNT(*) FROM form_encounter) > 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'A4 initialization refused: database contains patient or encounter records';
  END IF;
END //
DELIMITER ;
CALL check_a4_empty_database();
DROP PROCEDURE IF EXISTS check_a4_empty_database;

CREATE TABLE IF NOT EXISTS vital_environment_identity (
    environment_name VARCHAR(64) PRIMARY KEY
);

INSERT INTO vital_environment_identity (environment_name)
VALUES ('vital-a4')
ON DUPLICATE KEY UPDATE environment_name = environment_name;
