# Development

In order to build and run Weather Pike you need the following:

- Development platform
  - Computer running Linux, Windows, or Mac
  - Or a Raspberry PI
- Python 3.5+ (recommended) or Python 2.7
- Python PIP module for installing dependencies
- Dark Sky API key


## Linux
For development on a Linux system including the Raspbery Pi

1. Install System dependencies

```bash
$ sudo apt update
$ sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
   pkg-config libgl1-mesa-dev libgles2-mesa-dev \
   python-setuptools libgstreamer1.0-dev git-core \
   gstreamer1.0-plugins-{bad,base,good,ugly} \
   gstreamer1.0-{omx,alsa} python-dev libmtdev-dev \
   xclip xsel libjpeg-dev
```

2. Install Python dependencies using PIP

```bash
python3 -m pip install --upgrade --user pip setuptools
python3 -m pip install --upgrade --user Cython==0.29.10 pillow
```

3. Install Kivy
```bash
python3 -m pip install --user kivy
```

## Packaging

1. Install python3 virtual env
```bash
sudo apt update
sudo apt install python3-virtualenv
```
2. Create virtual environment
```bash
python3 -m virtualenv -p python3 kivy_package
```
3. Activate the virtual environment

```bash
cd kivy_package
source bin/activate
```
4. Install dependencies
```bash
python3 -m pip install pip setuptools
python3 -m pip install Cython==0.29.10 pillow
```
5. Install kivy
```bash
python3 -m pip install kivy
```
6. Install pyinstaller
```bash
python3 -m pip install pyinstaller
```
7. Build pyinstaller bootloader for 32 bit arm
```bash
git clone https://github.com/pyinstaller/pyinstaller
cd pyinstaller/bootloader/
python3 ./waf all
cp -r ../PyInstaller/bootloader/Linux-32bit-arm/ lib/python3.5/site-packages/PyInstaller/bootloader/
```
8. Run pyinstaller and wait to finish (will take several minutes)
```bash
pyinstaller weatherpike.py
```
9. Tar/Zip up dist directory
