-- Crée la base
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'FraudDetection')
BEGIN
    CREATE DATABASE FraudDetection;
END
GO

-- Utilise la base
USE FraudDetection;
GO

-- Crée la table
IF OBJECT_ID('TransactionsScored', 'U') IS NULL
BEGIN
    CREATE TABLE TransactionsScored (
        id INT IDENTITY(1,1) PRIMARY KEY,
        step INT,
        type VARCHAR(50),
        amount FLOAT,
        oldbalanceOrg FLOAT,
        newbalanceOrig FLOAT,
        oldbalanceDest FLOAT,
        newbalanceDest FLOAT,
        isFraudPred BIT,
        probFraud FLOAT,
        timestamp DATETIME
    );
END
GO
