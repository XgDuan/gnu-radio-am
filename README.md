# eewls(Electronic Engineering WireLess)

## Basic information

The eewls(Electronic Engineering WireLess)project provides a SOC(System on Chip) solution for AM/FM audio dcoder and some other modules for you to build an audio decoder or learn gnu-raido through our code.

All runnable codes are under `example/`. Those `*.grc`s are grc files that show the system structure and `*.py`s are python files that can be run directly with `python *.py`. More specifically, those ones end with `_0`  are mostly built upon raw gnuradio module and **gr-baz**. Those ones end with `_1` are built with `gr-eewls`, which packs the whole system into a single module.

## Dependency

In the following part, a **Respberry pi** and a **rtl-sdr** hardware are required.

> If you are gonna run the program on your linux pc version, everything will be fine.
However, if you are gonna run the program on `Windows`, we are not sure whether you will encounter any strange problems or not.

### Ubuntu mate

pls refer to this [site](https://www.raspberrypi.org/downloads/) for more information. You are recommended to install the `ubuntu mate`  on which we have tested the whole system.

### Python

The whole system is built upon **python 2.7.\***, and is not tested on **python 3** or earlier python 2 version.

### gnuradio

```powershell
sudo apt install gnuradio
```

### gr-baz

#### install from source

```powershell
git clone https://github.com/balint256/gr-baz.git
cd gr-eewls
mkdir build
cd build
cmake ../
make
sudo make install
sudo ldconfig
```

Sometimes, when you have built the system and try to run a simple demo, the system crashed and says 'No mudule named baz_swig' or some other modules with the `_swig` suffix. On such occasion, just install `swig` first with `sudo apt install swig`, then rebuild and reinstall `gr-baz`.

Also `libusb` is required to build gr-baz(`sudo apt install libusb-1.0-0-dev`).

Other dependency: [`armadillo`](https://github.com/conradsnicta/armadillo-code), [`uhd`](https://github.com/EttusResearch/uhd)(neglectable, but will bring some performance gain).

```powershell
# install uhd through apt-get
sudo apt-get install libuhd-dev libuhd003 uhd-host
# install armadillo(we assume you are in the armadillo folder)
cmake .
make
sudo make install
```

## Build

```powershell
git clone https://github.com/XgDuan/gnu-radio-am.git
cd gr-eewls
mkdir build
cd build
cmake ../
make
sudo make install
sudo ldconfig
```
