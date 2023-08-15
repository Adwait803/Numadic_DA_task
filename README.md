# Numadic_DA_task
# Asset Report Generation API
This FastAPI-based API allows you to generate an asset report for a fleet of vehicles based on their trip data and GPS coordinates. The generated report provides insights into the distance traveled, trips completed, average speed, and number of speed violations for each vehicle within a specified time range.

# Features
Generate Asset Report: This API endpoint allows you to generate an asset report for a specific time period. The report includes the following information for each vehicle:
License plate number
Distance traveled
Number of trips completed
Average speed
Transporter name
Number of speed violations

# Getting Started
Install the required dependencies by running the following command:


pip install fastapi uvicorn pandas haversine tqdm openpyxl

Place your trip data CSV file named Trip-Info.csv in the project directory.(Or change path in the file_path variable)

Organize your vehicle trail CSV files in the test/EOL-dump directory. Each CSV file should contain GPS coordinates and other relevant data for the vehicles.
or Just change the path in the code (csv_directory variable)

Run the API using the following command:


uvicorn main:app --host 0.0.0.0 --port 8000


Access the API documentation at http://127.0.0.1:8000/docs to interact with the API and generate reports.

# API Endpoints
Generate Asset Report
Endpoint: /generate_report/

Method: GET

# Query Parameters:

start_time (int): Start timestamp of the desired time range.
end_time (int): End timestamp of the desired time range.
Response: The API returns an Excel file containing the asset report for the specified time range. The Excel file includes columns for license plate number, distance, trips completed, average speed, transporter name, and number of speed violations.

# Notes
The API uses the Haversine formula to calculate distances between GPS coordinates.
If no data is available for the specified time range, a 404 error is returned.
The generated Excel file is attached to the response and can be downloaded.
Example Usage
Assuming the API is running locally:

Access the API documentation at http://127.0.0.1:8000/docs.
Choose the /generate_report/ endpoint.
Enter the start_time and end_time parameters to specify the desired time range.
Click "Try it out!" and then "Execute".
The API will return an Excel file containing the asset report for the specified time range.
If using main_ver2.py

Run:

python3 main_ver2.py --csv path/to/csv_file --csv_directory path/to/directory



Conclusion
This API provides a convenient way to generate asset reports for a fleet of vehicles based on their trip data and GPS coordinates. It offers valuable insights into vehicle performance and compliance during a specific time period. Feel free to customize the code and endpoints to suit your specific use case and requirements.
