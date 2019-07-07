from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock
from kivy.config import Config

from datetime import datetime, timezone
import configparser
import os, sys

import darksky

# class for weather details used by our application
# any future weather providers just need to map
# details into this class
class WeatherDetails():
    def __init__(self):
        self.dt = datetime.now()
        self.temp = 0.0
        self.temp_min = 0.0
        self.temp_max = 0.0
        self.temp_apparent = 0.0
        self.temp_high = 0.0
        self.temp_low = 0.0
        self.status = ""
        self.detailed_status = ""
        self.img_url = ""
        self.sunrise = 0
        self.sunset = 0
        self.pressure = 0
        self.humidity = 0
        self.wind_speed = 0
        self.wind_dir = ""
        self.precip_probability = 0.0

# Dark Sky weather provider class for translating the
# dark sky library data into our weather details
class DarkSky():

    def __init__(self):
        self.fcast = None
        self.icons_root = "%s/icons/256x256" % os.path.dirname(os.path.abspath(__file__))
        self.key = "00000000"
        self.lat = 51.0
        self.lon = 0.0
        self.units = "auto"
        self.daily_forecasts = []
        self.cur_weather = WeatherDetails()
        self.weather = None
        self.default_weather = WeatherDetails()
        self.default_weather.img_url = self.convertIconDesc("")

    def setConfig(self, key, lat, lon, units):
        try:
            self.key = key
            self.lat = lat
            self.lon = lon
            self.units = units
        except Exception as e:
            print("Failed to read config file")
            print(e)

    def setKey(self, key):
        self.key = key

    def setLocation(self, lat, lon, units):
        self.lat = lat
        self.lon = lon
        self.units = units

    def update(self):
        try:
            self.weather = darksky.forecast(self.key, self.lat, self.lon, exclude="minutely", units=self.units)
            self.cur_weather = self.populateWeather(self.weather.currently)
        except Exception as e:
            self.cur_weather.img_url =  self.convertIconDesc("")
            print("Error getting weather")
            print(e)

    def populateWeather(self, weather):
        wd = WeatherDetails()
        wd.dt = datetime.fromtimestamp(weather.time)
        wd.temp = weather.temperature
        wd.temp_apparent = weather.apparentTemperature
        wd.status = weather.summary
        wd.img_url = self.convertIconDesc(weather.icon)
        wd.humidity = weather.humidity * 100
        wd.pressure = weather.pressure
        return wd

    def populateForecast(self, data):
        wd = WeatherDetails()
        wd.dt = datetime.fromtimestamp(data.time)
        wd.temp_high = data.temperatureHigh
        wd.temp_low = data.temperatureLow
        wd.img_url = self.convertIconDesc(data.icon)
        wd.precip_probability = data.precipProbability * 100
        return wd

    def getCurWeather(self):
        if self.cur_weather is None:
            return self.default_weather
        return self.cur_weather

    def getForecast(self, idx):
        if self.weather is None or len(self.weather.daily.data) <= idx:
            return self.default_weather
        fcast = self.weather.daily.data
        day = self.populateForecast(fcast[idx])
        return day

    def convertIconDesc(self, desc):
        if desc is None:
            desc = "unknown"
        if "day" in desc:
            name = desc.replace("day", "").replace("-", "")
            img = "%s/%s.png" % (self.icons_root, name)
        elif "night" in desc:
            name = desc.replace("night", "").replace("-", "")
            img = "%s/nt_%s.png" % (self.icons_root, name)
        else:
            img = "%s/%s.png" % (self.icons_root, desc)
        if not os.path.exists(img):
            img = "%s/unknown.png" % self.icons_root
        return img

# Widget holding temperature, current condition summary,
# and current condition image
class TemperatureWidget(BoxLayout):
    cur_temp = ObjectProperty()
    cur_conditions = ObjectProperty()
    cur_image = ObjectProperty(None)

    def update(self, details):
        self.cur_temp.markup = True
        self.cur_temp.text = "%.2f[sup]o[/sup]" % details.temp
        self.cur_conditions.text = details.status
        self.cur_image.source = details.img_url

# Widget holding current weather details
class CurrentWeatherWidget(GridLayout):
    feels_like = ObjectProperty()
    humidity = ObjectProperty()
    pressure = ObjectProperty()

    def update(self, details):
        self.feels_like.markup = True
        self.feels_like.text = "%.2f[sup]o[sup]"  % details.temp_apparent
        self.humidity.text = "%d%%" % details.humidity
        self.pressure.text = "%d" % details.pressure

# Widget holding a forecast
class ForecastWidget(BoxLayout):
    title = ObjectProperty(None)
    img = ObjectProperty(None)
    temps = ObjectProperty(None)
    percent = ObjectProperty(None)

    def update(self, details):
        #self.title.text = details.dt.strftime("%-I %p")
        self.title.text = details.dt.strftime("%A")
        self.img.source = details.img_url
        self.temps.markup = True
        self.temps.text = "%d[sup]o[/sup] / %d[sup]o[/sup]" % (details.temp_low, details.temp_high)
        self.percent.text = "%d%%" % details.precip_probability


# The root widget of our app
class WeatherPike(Widget):
    txt_time = ObjectProperty(None)
    cur_temp = ObjectProperty(None)
    cur_weather = ObjectProperty(None)
    forecast1 = ObjectProperty(None)
    forecast2 = ObjectProperty(None)
    forecast3 = ObjectProperty(None)
    forecast4 = ObjectProperty(None)

    def updateTime(self, clockDt):
        dt = datetime.now()
        tz = datetime.now(timezone.utc).astimezone().tzinfo
        self.txt_time.markup = True
        dtStr = dt.strftime("%a, %b %d   %I:%M:%S %p")
        self.txt_time.text = "[b]%s[/b] [color=00FFFF][sup]%s[sup][/color]" % (dtStr, tz)

    def updateCurrentConditions(self, clockDt):
        global provider
        provider.update()
        self.cur_temp.update(provider.getCurWeather())
        self.cur_weather.update(provider.getCurWeather())
        self.forecast1.update(provider.getForecast(0))
        self.forecast2.update(provider.getForecast(1))
        self.forecast3.update(provider.getForecast(2))
        self.forecast4.update(provider.getForecast(3))


# The App class required by Kivy which will look for
# a file named weatherpike.kv
class WeatherPikeApp(App):
    def build(self):
        # create an instance of the root widget
        weather = WeatherPike()
        # update current conditions now
        weather.updateCurrentConditions(datetime.now())
        # schedule time update for every second
        Clock.schedule_interval(weather.updateTime, 1)
        # schedule weather update every 5 minutes
        # TODO: put the interval in the config
        Clock.schedule_interval(weather.updateCurrentConditions, 60 * 5)
        return weather


if __name__ == '__main__':

    provider = None
    appConfig = configparser.ConfigParser()
    try:
        appConfig.read("config.ini")
        provider = DarkSky()
        provider.setKey(appConfig["weather"]["key"])
        provider.setLocation(appConfig["location"]["lat"],
                             appConfig["location"]["lon"],
                             appConfig["location"]["units"])
    except Exception as e:
        print("Error reading config file")
        print(e)
        sys.exit()

    Config.set('graphics', 'width', appConfig["app"]["width"])
    Config.set('graphics', 'height', appConfig["app"]["height"])
    WeatherPikeApp().run()
