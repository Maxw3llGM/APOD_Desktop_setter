import time
import nasapy
import requests
import json
import ctypes
from pathlib import Path
from sys import platform
from appscript import app, mactypes
from datetime import datetime


API_KEY = "add your own api key"
nasa = nasapy.Nasa(key=API_KEY)

d = datetime.today().strftime('%Y-%m-%d')
apod = nasa.picture_of_the_day(date=d, hd=True)
r = requests.get(apod.get("hdurl"))

dirName = Path.home() / 'Pictures/APOD'
dirName = dirName.resolve()
jSON_pathname = (dirName / 'potd.json').resolve()
jPEG_pathname = (dirName / 'potd.jpg').resolve()

try:
    Path.mkdir(dirName)
    print("Directory", dirName, " created. ")
except FileExistsError:
    print("Directory", dirName, " already exists. ")

json_Apod = json.dumps(apod, indent=4)
with open(jSON_pathname, 'w') as outfile:
    json.dump(json_Apod, outfile)
with open(jSON_pathname) as json_file:
    data = json.load(json_file)
    print(data)

open(jPEG_pathname, 'wb').write(r.content)

if platform == "Darwin":
    app('Finder').desktop_picture.set(mactypes.File('/System/Library/Desktop Pictures/Solid Colors/Black.png'))
    time.sleep(1)
    app('Finder').desktop_picture.set(mactypes.File(jPEG_pathname))
elif platform == "win32":
    ctypes.windll.user32.SystemParametersInfoW(20, 0, jPEG_pathname, 0)


