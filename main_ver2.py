from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import pandas as pd
from haversine import haversine
from typing import List
import os
import tqdm
import argparse

app = FastAPI()

def parse_arguments():
    parser = argparse.ArgumentParser(description="Asset Report Generation API")
    parser.add_argument("--csv", required=True, help="Path to the Trip-Info CSV file")
    parser.add_argument("--csv_directory", required=True, help="Path to the directory containing vehicle trail CSV files")
    return parser.parse_args()

args = parse_arguments()

@app.get("/")
async def root():
    # generate_asset_report(1527597396,1527618569 )
    return {"message": "Hello World"}

def load_data():
    file_path = args.csv

    # Load CSV file into a DataFrame
    trip_info_df = pd.read_csv(file_path)
    print("Successfully loaded trip data")

    csv_directory = args.csv_directory

    # List to store individual DataFrames
    dataframes = []

    # Loop through CSV files in the directory
    for filename in tqdm.tqdm(os.listdir(csv_directory)):
        if filename.endswith('.csv'):
            file_path = os.path.join(csv_directory, filename)
            df = pd.read_csv(file_path, low_memory=False)
            dataframes.append(df)

    # Concatenate the DataFrames into a single DataFrame
    combined_df = pd.concat(dataframes, ignore_index=True)
    print("Successfully loaded vehicle trail data")
    return combined_df, trip_info_df


# Calculate distance using Haversine formula
def calculate_distance(lat1, lon1, lat2, lon2):
    return haversine((lat1, lon1), (lat2, lon2))

# Generate asset report
def generate_asset_report(start_time, end_time):
    vehicle_trails_df, trip_info_df = load_data()

    # Filter data based on start and end time
    filtered_trails = vehicle_trails_df[(vehicle_trails_df['tis'] >= start_time) & (vehicle_trails_df['tis'] <= end_time)]
    

    if filtered_trails.empty:
        return None

    
    # Calculate distances between consecutive points
    filtered_trails['prev_lat'] = filtered_trails['lat'].shift()
    filtered_trails['prev_lon'] = filtered_trails['lon'].shift()
    filtered_trails['distance'] = filtered_trails.apply(
        lambda row: calculate_distance(row['lat'], row['lon'], row['prev_lat'], row['prev_lon'])
        if pd.notnull(row['lat']) and pd.notnull(row['lon']) and pd.notnull(row['prev_lat']) and pd.notnull(row['prev_lon'])
        else 0,
        axis=1
    )

    # Calculate total distance for each vehicle
    distance_per_vehicle = filtered_trails.groupby('lic_plate_no')['distance'].sum()
    
    

    # Calculate the number of trips completed for each vehicle
    
    trips_per_vehicle = trip_info_df.groupby('vehicle_number')['trip_id'].count()
    
    plate_to_transporter = trip_info_df.set_index('vehicle_number')['transporter_name'].to_dict()
    
    
    # Calculate average speed for each vehicle
    avg_speed_per_vehicle = filtered_trails.groupby('lic_plate_no')['spd'].mean()
    
    # Calculate the number of speed violations for each vehicle
    num_speed_violations_per_vehicle = filtered_trails.groupby('lic_plate_no')['osf'].sum()
    

    # Merge all calculated values into a report DataFrame
    report_df = pd.DataFrame({
        'License plate number': distance_per_vehicle.index,
        'Distance': distance_per_vehicle.values,
        'Number of Trips Completed': trips_per_vehicle.get(distance_per_vehicle.index, 0),
        'Average Speed': avg_speed_per_vehicle.values,
        'Transporter Name': distance_per_vehicle.index.map(plate_to_transporter),
        'Number of Speed Violations': num_speed_violations_per_vehicle.values
    })
    print("Sucessfully generated data")
    

    return report_df

@app.get("/generate_report/")
async def api_generate_report(start_time: int, end_time: int):
    report_df = generate_asset_report(start_time, end_time)

    if report_df is None:
        raise HTTPException(status_code=404, detail="No data available for the specified time period.")

    # Create Excel file and return it as a response
    excel_file_path = 'asset_report.xlsx'
    report_df.to_excel(excel_file_path, index=False)

    return FileResponse(excel_file_path, headers={"Content-Disposition": "attachment; filename=asset_report.xlsx"})


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
