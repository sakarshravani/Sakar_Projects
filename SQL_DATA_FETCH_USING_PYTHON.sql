-- Show all databases
SHOW DATABASES;

-- Select the SakarSPM database to work with
USE SakarSPM;

-- Show all tables in the SakarSPM database
SHOW TABLES;

-- Create a new TrainDetails table
CREATE TABLE TrainDetails (
    ID INT PRIMARY KEY,
    FromStation VARCHAR(100),
    ToStation VARCHAR(100),
    TrainType VARCHAR(50),
    NumberOfStops INT
);


-- Insert a new record into the TrainDetails table
INSERT INTO TrainDetails (ID, FromStation, ToStation, TrainType, NumberOfStops)
VALUES (12939, 'PUNE', 'JP', 'SF Exp', 5);

SELECT * FROM TrainDetails;

select * from TrainPath;

select * from TrainSRKM;

SELECT 
    td.ID,
    td.FromStation,
    td.ToStation,
    td.TrainType,
    td.NumberOfStops,
    tp.FirstStop,
    tp.SecondStop,
    tp.ThirdStop,
    tp.FourthStop,
    tp.FifthStop,
    ts.sec1_sr,
    ts.sec1_km,
    ts.sec2_sr,
    ts.sec2_km,
    ts.sec3_sr,
    ts.sec3_km,
    ts.sec4_sr,
    ts.sec4_km,
    ts.sec5_sr,
    ts.sec5_km
FROM 
    TrainDetails td
JOIN 
    TrainPath tp ON td.ID = tp.ID
JOIN 
    TrainSRKM ts ON td.ID = ts.ID;



   