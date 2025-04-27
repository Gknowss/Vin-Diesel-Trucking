import requests
import sqlite3
import pandas as pd
import time
from datetime import datetime

# API Endpoint
API_URL = "https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvaluesbatch/"

# Read VINs from CSV file (Replace with your data source)
def get_vins_from_csv(file_path="vin_list.csv"):
    df = pd.read_csv(file_path)
    return df["VIN"].tolist()  # Assuming the CSV has a column named "VIN"

# Fetch VIN details from NHTSA
def fetch_trailer_vins(vins):
    payload = {"format": "json", "data": ";".join(vins)}
    response = requests.post(API_URL, data=payload)
    data = response.json().get("Results", [])

    # Filter only trailers
    return [
        {
            "vin": item["VIN"],
            "make": item["Make"],
            "model": item["Model"],
            "year": item["ModelYear"],
            "vehicle_type": item["VehicleType"]
        }
        for item in data if "trailer" in item["VehicleType"].lower()
    ]

# Save to SQLite
def save_to_database(trailers):
    conn = sqlite3.connect("trailers.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trailers (
            vin TEXT PRIMARY KEY,
            make TEXT,
            model TEXT,
            year INTEGER,
            vehicle_type TEXT
        )
    """)

    for trailer in trailers:
        cursor.execute("INSERT OR IGNORE INTO trailers (vin, make, model, year, vehicle_type) VALUES (?, ?, ?, ?, ?)", 
                       (trailer["vin"], trailer["make"], trailer["model"], trailer["year"], trailer["vehicle_type"]))

    conn.commit()
    conn.close()

# Export to Excel
def export_to_excel(trailers, filename="trailers.xlsx"):
    df = pd.DataFrame(trailers)
    df.to_excel(filename, index=False)

# Run automation
def run_automation():
    vins = get_vins_from_csv()
    if not vins:
        print("No VINs found.")
        return

    print(f"Fetching data for {len(vins)} VINs...")
    trailers = fetch_trailer_vins(vins)
    if not trailers:
        print("No trailers found.")
        return

    save_to_database(trailers)
    export_to_excel(trailers)
    
    print(f"Stored {len(trailers)} trailer VINs successfully at {datetime.now()}")

# Schedule automation (Run daily)
if __name__ == "__main__":
    run_automation()
