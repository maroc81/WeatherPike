# WeatherPike
Internet Weather Station for Raspberry Pi

![Screenshot](/screenshots/480_320.png)

## Overview

Weather Pike is a multi-platform internet weather station but designed with a Raspberry Pi and a 3.5" LCD in mind. Weather Pike is built on the Kivy Python framework with forecast data provided by DarkSky.

Weather Pike includes features such as

- Current time
- Current temperature
- Current conditions
- Multi-day forecast with lo/high temperatures and precipitation percentage

Planned features include

- Hourly forecast
- Detailed forecast
- Configuration UI
- Web based configuration
- Dynamic scaling UI for different resolutions and pixel density

## Kivy

Weather Pike is built using the [Kivy Python framework](https://kivy.org/).  Kivy is a cross platform toolkit for making multi-touch user interfaces on desktop and mobile devices. Kivy provides separation of application logic and user interface through its Kv design language making it simple to create complete graphical applications with minimal straight forward code.

The UI for Weather Pike is defined in weatherpike.kv while the logic is located in weatherpike.py.  Due to the simplicity of Kivy, the two files make up the entire (basic for now) application and are less than 400 lines total.

The UI can be easily modified (with an understanding of the Kv language and Kivy widgets) to your liking by changing the kv file and updating the python code (if needed).


## Usage

1. Register for an API key from [Dark Sky](https://darksky.net/dev)
2. Install python (version 3.5+ recommended)
3. Follow instructions to [Download and Install Kivy](https://kivy.org/#download) for your platform
4. Install the darkskylib python library
```bash
$ python3 -m pip install --user darkskylib
```
4. Clone this repository
5. Edit `config.ini` and enter your API key, desired GPS coordinates, etc
6. Run weatherpike.py
```bash
$ python3 weatherpike.py
```

The above directions should work for your desired platform.  For detailed steps, see DEVELOP.md

TODO: Provide package for Raspbery Pi

## Acknowledgements

 - [PiWeatherRock](https://github.com/genebean/PiWeatherRock): The UI for Weather Pike was (heavily) inspired by this project.  Which in turn was based on the original (as far as I know) Weather Pi written by Jim Kemp.  While Weather Pike's UI is heavily influenced by these projects, all code is original due to Weather Pike's dependency on Kivy
 - [Weather Underground Icons](https://github.com/manifestinteractive/weather-underground-icons)
