from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector  # Using MySQL instead of sqlite3

app = FastAPI()

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection details
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="SakarSPM"
    )

# Fetch the number of stops for a given train number from TrainDetails
def get_train_details(train_number: str):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT NumberOfStops FROM TrainDetails WHERE ID = %s", (train_number,))
        result = cursor.fetchone()
        if result:
            return result[0]  # Number of stops
        else:
            return None
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        connection.close()

# Get the stops for the given train number
def get_train_stops(train_number: str, number_of_stops: int):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        if number_of_stops == 5:
            # Fetch stops from TrainPath for 5 stops
            cursor.execute("SELECT FirstStop, SecondStop, ThirdStop, FourthStop, FifthStop FROM TrainPath WHERE ID = %s", (train_number,))
        elif number_of_stops == 12:
            # Fetch stops from TrainPath2 for 12 stops
            cursor.execute("SELECT FirstStop, SecondStop, ThirdStop, FourthStop, FifthStop, SixthStop, SeventhStop, EighthStop, NinthStop, TenthStop, EleventhStop, TwelevthStop FROM TrainPath2 WHERE ID = %s", (train_number,))
        else:
            return []  # Return empty list if no matching table

        stops = cursor.fetchone()
        if stops:
            return list(stops)
        else:
            return []
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        connection.close()

@app.get("/train-details/{train_number}")
async def train_details(train_number: str):
    # Step 1: Get number of stops for the given train number
    number_of_stops = get_train_details(train_number)
    
    if not number_of_stops:
        raise HTTPException(status_code=404, detail="Train number not found.")
    
    # Step 2: Fetch stops dynamically based on the number of stops
    stops = get_train_stops(train_number, number_of_stops)

    if not stops:
        raise HTTPException(status_code=404, detail="No stops found for this train number.")
    
    return {"stops": stops}
