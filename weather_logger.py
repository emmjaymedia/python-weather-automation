import csv
from datetime import datetime
import requests


def fetch_and_save_weather():
  # We are pulling live weather data for Doha, Qatar from a free public API
  url = "https://api.open-meteo.com/v1/forecast?latitude=25.2854&longitude=51.5310&current=temperature_2m,relative_humidity_2m,wind_speed_10m"

  print("Connecting to weather API...")
  response = requests.get(url)

  # Check if the connection was successful (Status 200 means OK)
  if response.status_code == 200:
    data = response.json()
    current = data["current"]

    # Grab the specific values we want
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    temp = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]
    wind_speed = current["wind_speed_10m"]

    # Check if our CSV file already exists
    file_name = "weather_log.csv"
    file_exists = False
    try:
      with open(file_name, "r"):
        file_exists = True
    except FileNotFoundError:
      pass

    # Open the CSV file and save the data
    with open(file_name, mode="a", newline="", encoding="utf-8") as f:
      writer = csv.writer(f)

      # If the file is brand new, write the title headers first
      if not file_exists:
        writer.writerow(
            ["Timestamp", "Temperature (°C)", "Humidity (%)", "Wind Speed"]
        )

      # Write the actual weather row
      writer.writerow([timestamp, temp, humidity, wind_speed])

    print(
        f"Success! Logged -> Temp: {temp}°C | Humidity: {humidity}% | Wind:"
        f" {wind_speed} km/h"
    )
  else:
    print(f"Failed to fetch data. Status code: {response.status_code}")


if __name__ == "__main__":
  fetch_and_save_weather()
  