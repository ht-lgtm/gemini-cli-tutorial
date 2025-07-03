
import customtkinter
import requests

class WeatherApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Weather App")
        self.geometry("400x300")

        self.city_entry = customtkinter.CTkEntry(self, placeholder_text="Enter city")
        self.city_entry.pack(pady=10)

        self.search_button = customtkinter.CTkButton(self, text="Search", command=self.get_weather)
        self.search_button.pack(pady=10)

        self.city_label = customtkinter.CTkLabel(self, text="", font=("Helvetica", 20))
        self.city_label.pack()

        self.temperature_label = customtkinter.CTkLabel(self, text="", font=("Helvetica", 40))
        self.temperature_label.pack()

        self.description_label = customtkinter.CTkLabel(self, text="", font=("Helvetica", 16))
        self.description_label.pack()

    def get_weather(self):
        city = self.city_entry.get()
        api_key = "d5b59998d220ebf1a647227e5f6cc067"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            data = response.json()

            if data["cod"] == 200:
                self.city_label.configure(text=data["name"])
                self.temperature_label.configure(text=f"{data['main']['temp']}°C")
                self.description_label.configure(text=data["weather"][0]["description"])
            else:
                self.city_label.configure(text="Error")
                self.temperature_label.configure(text="")
                self.description_label.configure(text=data["message"])
        except requests.exceptions.RequestException as e:
            self.city_label.configure(text="Error")
            self.temperature_label.configure(text="")
            self.description_label.configure(text="Network error")

if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()
