import argparse
import requests
import json
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class WeatherApp:
    def __init__(self, api_key):
        self.api_key = api_key
        self.favorites = self.load_favorites()  # Load favorites from the file

    def load_favorites(self):
        try:
            with open("favorites.txt", "r") as file:
                return [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            return []

    def save_favorites(self):
        with open("favorites.txt", "w") as file:
            for location in self.favorites:
                file.write(location + "\n")

    def get_weather(self, location):
        base_url = "https://api.weatherapi.com/v1/current.json"
        params = {
            "key": self.api_key,
            "q": location,
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()

            if "error" in data:
                print("Error:", data["error"]["message"])
                return None
            else:
                return data["current"]
        except requests.exceptions.RequestException as e:
            print("Request Error:", e)
            return None
        except json.JSONDecodeError as e:
            print("JSON Decode Error:", e)
            return None

    def add_to_favorites(self, location):
        if location not in self.favorites:
            self.favorites.append(location)
            self.save_favorites()  # Save updated favorites to the file
            print(f"{location} added to favorites.")
        else:
            print(f"{location} is already in favorites.")

    def remove_from_favorites(self, location):
        if location in self.favorites:
            self.favorites.remove(location)
            self.save_favorites()  # Save updated favorites to the file
            print(f"{location} removed from favorites.")
        else:
            print(f"{location} is not in favorites.")

    def show_favorites(self):
        if not self.favorites:
            print("Favorites list is empty.")
        else:
            print("Favorites list:")
            for location in self.favorites:
                print(location)

    def refresh_weather(self, location, interval=30):
        while True:
            weather_info = self.get_weather(location)
            if weather_info:
                print(f"Weather in {location}:")
                print(f"Temperature: {weather_info['temp_c']}°C")
                print(f"Condition: {weather_info['condition']['text']}")
                print(f"Wind Speed: {weather_info['wind_kph']} km/h")
                print(f"Pressure: {weather_info['pressure_mb']} mb")
                print(f"Humidity: {weather_info['humidity']}%")
            time.sleep(interval)  # Refresh every 'interval' seconds

def main():
    parser = argparse.ArgumentParser(description="Weather App CLI")
    parser.add_argument("action", nargs="?", default="check", choices=["check", "add", "remove", "list", "refresh","update"], help="Action to perform")
    parser.add_argument("location", nargs="*", help="Location (city name or coordinates)")
    args = parser.parse_args()

    api_key = "368d1f626a9347b8a40141900230909"  # Replace with your API key
    weather_app = WeatherApp(api_key)

    if args.action == "check":
        if args.location:
            for location in args.location:
                weather_info = weather_app.get_weather(location)
                if weather_info:
                    print(f"Weather in {location}:")
                    print(f"Temperature: {weather_info['temp_c']}°C")
                    print(f"Condition: {weather_info['condition']['text']}")
                    print(f"Wind Speed: {weather_info['wind_kph']} km/h")
                    print(f"Pressure: {weather_info['pressure_mb']} mb")
                    print(f"Humidity: {weather_info['humidity']}%")
    elif args.action == "add":
        for location in args.location:
            weather_app.add_to_favorites(location)
    elif args.action == "remove":
        for location in args.location:
            weather_app.remove_from_favorites(location)
    elif args.action == "list":
        weather_app.show_favorites()
    elif args.action == "refresh":
        if args.location:
            for location in args.location:
                weather_app.refresh_weather(location)
    elif args.action == "update":
        if args.location:
            for location in args.location:
                weather_app.refresh_weather(location)

if __name__ == "__main__":
    main()
