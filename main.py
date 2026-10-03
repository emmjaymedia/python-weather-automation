from fastapi import FastAPI
import sqlite3
from datetime import datetime

app = FastAPI()

# 1. Initialize the SQLite database with an extra timestamp column
def init_db():
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            temperature TEXT,
            condition TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# 2. Endpoint that checks the real clock and saves it to the database
@app.get("/weather/{city}")
def get_city_weather(city: str):
    # Get the current hour (0 to 23) using Python's datetime module
    current_hour = datetime.now().hour
    
    # Dynamic logic: If it's between 6 AM and 6 PM, it's daytime. Otherwise, it's night!
    if 6 <= current_hour < 18:
        cond = "Sunny"
        temp = "32°C"
    else:
        cond = "Clear Night"
        temp = "24°C"
        
    # Get a clean formatted timestamp string
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Save the record permanently into SQLite with the timestamp
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO weather_records (city, temperature, condition, timestamp) VALUES (?, ?, ?, ?)",
        (city.capitalize(), temp, cond, current_time)
    )
    conn.commit()
    conn.close()

    return {
        "status": "Saved with real-time logic!",
        "location": city.capitalize(),
        "temperature": temp,
        "condition": cond,
        "checked_at": current_time
    }

# 3. View all saved records
@app.get("/records")
def get_all_records():
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, city, temperature, condition, timestamp FROM weather_records")
    rows = cursor.fetchall()
    conn.close()
    
    return {"total_saved_records": len(rows), "records": rows}
    