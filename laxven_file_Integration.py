from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import pandas as pd
import io
import numpy as np
import os

app = FastAPI()

# Enable CORS (adjust allowed origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend URL if needed.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def safe_float(x):
    try:
        fx = float(x)
        if np.isnan(fx) or np.isinf(fx):
            return 0.0
        return fx
    except Exception:
        return 0.0

def read_excel_file(contents, filename, skip_rows=0):
    """Read the Excel file using an appropriate engine with optional skiprows."""
    if filename.endswith(".csv"):
        return pd.read_csv(io.BytesIO(contents), skiprows=skip_rows)
    elif filename.endswith(".xlsx"):
        return pd.read_excel(io.BytesIO(contents), engine="openpyxl", skiprows=skip_rows)
    elif filename.endswith(".xls"):
        return pd.read_excel(io.BytesIO(contents), engine="xlrd", skiprows=skip_rows)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")
        
def find_valid_header(df):
    """
    If the DataFrame does not contain required columns,
    search for a row that contains the keywords 'Time', 'Distance', and 'Speed'
    and then use that row as header.
    """
    rows = df.values.tolist()
    header_row_index = None
    for i, row in enumerate(rows):
        row_str = " ".join([str(x) for x in row]).lower()
        if "time" in row_str and "distance" in row_str and "speed" in row_str:
            header_row_index = i
            break
    if header_row_index is None:
        raise HTTPException(status_code=400, detail="Cannot find valid header row.")
    new_header = rows[header_row_index]
    data_rows = rows[header_row_index + 1:]
    new_df = pd.DataFrame(data_rows, columns=new_header)
    new_df.columns = new_df.columns.str.strip()
    return new_df

@app.post("/api/total_distance")
async def total_distance_at_achieved_mps(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        filename = file.filename.lower()
        
        # Read the file, skipping the first 4 rows
        df = read_excel_file(contents, filename, skip_rows=4)
        df.columns = df.columns.str.strip()
        
        # Remove the last row containing event codes
        if len(df) > 0:
            df = df.iloc[:-1]
            
        print("Initial Columns in DataFrame:", df.columns.tolist())
        
        # If "EventGn" exists, drop it.
        if "EventGn" in df.columns:
            df = df.drop(columns=["EventGn"])
            
            
        # Remove unnamed columns
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        
        # Rename alternative column names if necessary.
        if "Speed" not in df.columns:
            for col in df.columns:
                if col.lower().replace(" ", "") in ["speedkm/hr", "speed(km/hr)", "speedkmph"]:
                    df.rename(columns={col: "Speed"}, inplace=True)
                    break
        if "Distance" not in df.columns:
            for col in df.columns:
                if col.lower().replace(" ", "") in ["distancekm", "distance(km)", "km"]:
                    df.rename(columns={col: "Distance"}, inplace=True)
                    break

        # Check if the file appears structured (i.e. header row is correct)
        if df.columns.tolist() == ["Time", "Distance", "Speed"]:
            # Split "Time" into "Date" and "Time" if possible
            if df["Time"].str.contains(" ").any():
                split_df = df["Time"].str.split(" ", n=1, expand=True)
                if split_df.shape[1] == 2:
                    df["Date"] = split_df[0].str.strip()
                    df["Time"] = split_df[1].str.strip()
        elif "Speed" not in df.columns or "Distance" not in df.columns:
            df = pd.read_excel(io.BytesIO(contents), engine="openpyxl", header=None, skiprows=4)
            print("Re-read without headers. Columns:", df.columns.tolist())
            df = find_valid_header(df)
            if len(df.columns) >= 4:
                df = df.rename(columns={
                    df.columns[0]: "Date",
                    df.columns[1]: "Time",
                    df.columns[2]: "Distance",
                    df.columns[3]: "Speed"
                })
            else:
                raise HTTPException(status_code=400, detail="File does not have enough columns after cleaning.")
        
        # Reorder columns to desired order
        desired_order = ["Date", "Time", "Distance", "Speed"]
        df = df[[col for col in desired_order if col in df.columns]]
        
        # Remove extra header rows
        mask_extra = (
            (df["Date"].astype(str).str.strip() == "") &
            (df["Distance"].astype(str).str.strip().str.lower() == "km") &
            (df["Speed"].astype(str).str.strip().str.lower() == "km/hr")
        )
        df = df[~mask_extra]
        
        # Parse Datetime
        if "Date" in df.columns and "Time" in df.columns:
            dt_str = (df["Date"] + " " + df["Time"]).str.strip()
            dt_series = pd.to_datetime(dt_str, format="%d/%m/%y %H:%M:%S", dayfirst=True, errors="coerce")
            if dt_series.isnull().all():
                raise HTTPException(status_code=400, detail="Datetime parsing failed for Date and Time columns.")
            df["Datetime"] = dt_series
        elif "Time" in df.columns:
            dt_series = pd.to_datetime(df["Time"], format="%d/%m/%y %H:%M:%S", dayfirst=True, errors="coerce")
            if dt_series.isnull().all():
                raise HTTPException(status_code=400, detail="Datetime parsing failed for Time column.")
            df["Datetime"] = dt_series
            df["Date"] = df["Datetime"].dt.strftime("%d/%m/%y")
        else:
            raise HTTPException(status_code=400, detail="Missing required date/time information.")
        
        if "Datetime" not in df.columns:
            raise HTTPException(status_code=400, detail="Datetime column not created. Check the file format.")
        
        # Final column order
        final_order = ["Date", "Time", "Distance", "Speed", "Datetime"]
        df = df[[col for col in final_order if col in df.columns]]
        
        # Save cleaned file
        cleaned_file_path = "/home/sr06/Documents/Shravani/my-app-/my-app/backend/cleaned_file_with_dt.xlsx"
        df.to_excel(cleaned_file_path, index=False)
        
        # Re-read and final processing
        df = pd.read_excel(cleaned_file_path, engine="openpyxl")
        df["Distance"] = pd.to_numeric(df["Distance"], errors="coerce")
        df["Speed"] = pd.to_numeric(df["Speed"], errors="coerce")
        df = df.dropna(subset=["Distance", "Speed"])
        
        print("dtypes in DataFrame after re-read:", df.dtypes)
        print("Columns after re-read:", df.columns.tolist())
        
        # -------------------------------
        # Calculate Achieved MPS and Total Distance at Achieved MPS
        # -------------------------------
        mps_achieved = df["Speed"].max()
        if pd.isna(mps_achieved):
            mps_achieved = 0
        print("Achieved MPS:", mps_achieved)
        mps_rows = df[df["Speed"] == mps_achieved]
        if mps_rows.empty:
            total_mps_distance = 0
        else:
            total_mps_distance = mps_rows["Distance"].max() - mps_rows["Distance"].min()
            total_mps_distance = round(total_mps_distance, 2)
        print("Total Distance at Achieved MPS:", total_mps_distance)
        
        # -------------------------------
        # Calculate Distance at near Achieved MPS (95% threshold)
        # -------------------------------
        near_mps_threshold = 0.95 * mps_achieved
        near_mps_rows = df[df["Speed"] > near_mps_threshold].copy()
        if near_mps_rows.empty:
            total_distance_near_mps = 0
        else:
            near_mps_rows["Segment"] = near_mps_rows["Distance"].diff().fillna(0).cumsum()
            try:
                segment_distances = near_mps_rows.groupby("Segment")["Distance"].agg(lambda x: x.max() - x.min())
            except Exception as ex:
                segment_distances = 0
            total_distance_near_mps = round(segment_distances.sum(), 2)
        print("Distance at near Achieved MPS:", total_distance_near_mps)
        
        # -------------------------------
        # Calculate Total Journey Distance
        # -------------------------------
        total_journey_distance = df["Distance"].max() - df["Distance"].min()
        total_journey_distance = round(total_journey_distance, 2)
        print("Total Journey Distance:", total_journey_distance)
        
        # -------------------------------
        # Calculate Total Journey Time (in hours)
        # -------------------------------
        start_time_dt = df["Datetime"].min()
        end_time_dt = df["Datetime"].max()
        total_journey_time = (end_time_dt - start_time_dt).total_seconds() / 3600
        total_journey_time = round(total_journey_time, 2)
        print("Start Time:", start_time_dt, "End Time:", end_time_dt, "Total Journey Time (hours):", total_journey_time)
        if total_journey_time == 0:
            raise HTTPException(status_code=400, detail="Total journey time is computed as 0. Check the Date/Time values in the file.")
        
        # -------------------------------
        # Calculate Average Speed (km/h)
        # -------------------------------
        avg_speed = round(total_journey_distance / total_journey_time, 2) if total_journey_time > 0 else 0
        print("Average Speed:", avg_speed)
        
        # -------------------------------
        # Calculate Average Running Speed (mean of Speed column)
        # -------------------------------
        avg_run_speed = round(df["Speed"].mean(), 2)
        print("Average Running Speed:", avg_run_speed)
        
        # -------------------------------
        # Calculate Brake Feel Test (BFT)
        # -------------------------------
        brake_feel_max_speed = 15
        brake_feel_min_speed = 10
        brake_feel_time = None
        brake_feel_max_index = 0
        for i in range(len(df) - 1):
            current_speed = df.loc[i, "Speed"]
            next_speed = df.loc[i + 1, "Speed"]
            current_time = df.loc[i, "Time"]
            if current_speed >= brake_feel_max_speed and next_speed < current_speed:
                brake_feel_max_speed = current_speed
                brake_feel_time = df.loc[i, "Time"]
                brake_feel_max_index = i
                break
        for i in range(brake_feel_max_index, len(df) - 1):
            current_speed = df.loc[i, "Speed"]
            next_speed = df.loc[i + 1, "Speed"]
            if current_speed <= brake_feel_min_speed and next_speed > current_speed:
                brake_feel_min_speed = current_speed
                break

        # -------------------------------
        # Calculate Brake Power Test (BPT)
        # -------------------------------
        brake_power_max_speed = 60
        brake_power_min_speed = 31
        brake_power_time = None
        brake_power_max_index = 0
        for i in range(len(df) - 1):
            current_speed = df.loc[i, "Speed"]
            next_speed = df.loc[i + 1, "Speed"]
            current_time = df.loc[i, "Time"]
            if current_speed > brake_power_max_speed and next_speed < current_speed:
                brake_power_max_speed = current_speed
                brake_power_time = df.loc[i, "Time"]
                brake_power_max_index = i
                break
        for i in range(brake_power_max_index, len(df) - 1):
            current_speed = df.loc[i, "Speed"]
            next_speed = df.loc[i + 1, "Speed"]
            if current_speed <= brake_power_min_speed and next_speed > current_speed:
                brake_power_min_speed = current_speed
                break

        if pd.isna(mps_achieved):
            mps_achieved = 0

        total_mps_distance = float(safe_float(total_mps_distance))
        mps_achieved = float(safe_float(mps_achieved))
        total_distance_near_mps = float(safe_float(total_distance_near_mps))
        total_journey_distance = float(safe_float(total_journey_distance))
        total_journey_time = float(safe_float(total_journey_time))
        avg_speed = float(safe_float(avg_speed))
        avg_run_speed = float(safe_float(avg_run_speed))
        
        bft_time = brake_feel_time if brake_feel_time is not None else "N/A"
        bpt_time = brake_power_time if brake_power_time is not None else "N/A"
        bft_speed_drop = f"{brake_feel_max_speed} - {brake_feel_min_speed}"
        bpt_speed_drop = f"{brake_power_max_speed} - {brake_power_min_speed}"
        
        # -------------------------------
        # Calculate Number of Stops (rows where Speed is 0)
        # -------------------------------
        no_of_stops = int(df[df["Speed"] == 0].shape[0])
        print("Number of Stops:", no_of_stops)
        
        
        response_dict = {
            "total_mps_distance": total_mps_distance,
            "mps_achieved": mps_achieved,
            "total_distance_near_mps": total_distance_near_mps,
            "total_journey_distance": total_journey_distance,
            "total_journey_time": total_journey_time,
            "avg_speed": avg_speed,
            "avg_run_speed": avg_run_speed,
            "bft_time": bft_time,
            "bft_speed_drop": bft_speed_drop,
            "bpt_time": bpt_time,
            "bpt_speed_drop": bpt_speed_drop,
            "no_of_stops": no_of_stops,
            "start_time": start_time_dt.strftime("%H:%M:%S"),
            "end_time": end_time_dt.strftime("%H:%M:%S"),
        }
        print("Response Dict:", response_dict)
        return JSONResponse(content=jsonable_encoder(response_dict))
    
    except Exception as e:
        print("Error in total_distance endpoint:", str(e))
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

