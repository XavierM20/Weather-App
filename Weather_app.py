from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser
import requests

url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']

#Gets the weather 
def get_weather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()
        # (City, Country, temp_celsisus, temp_fahrenheit, icon, weather)
        city = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp_celsius = temp_kelvin - 273.15
        temp_fahrenheit = (temp_kelvin - 273.15) * 9 / 5 + 32
        icon = json['weather'][0]['icon']
        weather = json['weather'][0]['main']
        final = (city, country, temp_celsius, temp_fahrenheit, icon, weather)
        return final

    else:
        return None
#The search feature to find the city that is being searched
def search():
    city = city_text.get()
    weather = get_weather(city)
    if weather:
        location_label['text'] = '{}, {}'.format(weather[0], weather[1])
        image['bitmap'] = 'weather_icons/{}.png'.format(weather[4])
        temp_label['text'] = '{:.2f}°C, {:.2f}°F'.format(weather[2], weather[3])
        weather_label['text'] = weather[5]
    else:
        messagebox.showinfo("Error", "City not found{}".format(city))

#functions
app = Tk()
app.title("Weather App")
app.geometry("700x350")

city_text = StringVar()
city_entry = Entry(app, textvariable=city_text)
city_entry.pack()

search_button = Button(app, text="Search", width=12, command=search)
search_button.pack()

location_label = Label(app, text="Location")
location_label.pack()

image = Label(app, bitmap='')
image.pack()

temp_label = Label(app, text='')
temp_label.pack()

weather_label = Label(app, text='')
weather_label.pack()

app.mainloop()
