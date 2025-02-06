from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app
app = FastAPI()

# Add CORS middleware to handle cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods like GET, POST, etc.
    allow_headers=["*"],  # Allow all headers
)

# Pydantic model for incoming data (train number)
class TrainNoRequest(BaseModel):
    trainNo: str

# Define POST route to receive train number
@app.post("/api/train")
async def train(train: TrainNoRequest):
    # Print the train number to the backend (server console)
    print(f"Received train number: {train.trainNo}")
    
    # You can also return the same message in the response
    return {"message": f"Train number {train.trainNo} is valid."}