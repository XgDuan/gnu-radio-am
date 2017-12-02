# Basic information

The eewls(Electronic Engineering WireLess)project provides a SOC(System on Chip) for am audio decoding as long as a fm dcoder and some other modules for you to build an am audio decoder or learn gnu-raido through our lucid code.

Also, all runnable codes are under `example/`. those `*.grc`s are grc files that show the system structure and those `*.py`s are python files that can be run directly with `python *.py`. More specifically, those end with `_0`  are mostly built upon raw gnuradio module and **gr-baz**. those ene with `_1` are built with `gr-eewls`, which package the swollen system into a single module.

# Dependency

## Ubuntu mate
In the following part, we assume that you have a **Respberry pi** and a **rtl-sdr** hardware.

> If you are gonna run the program on your linux pc version, please skip this part.
However, if you are gonna run the program on Windows, we are not sure whether you will encounter any stranges problem due to gnuradio.

pls refer to this [site](https://www.raspberrypi.org/downloads/) for more information. You are recommended to install the `ubuntu mate` for that we have test the whole system on it.
## Python
The whole system is built upon **python 2.7.\***, and we have not tested them on **python 3** or early python 2 version.

## gnuradio
```powershell
sudo apt install gnuradio
```

## gr-baz
### install from source
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
Sometimes, when you have built the system and try to run a simple demo, the system crashed and says 'No mudule named baz_swig' or some other modules with the `_swig` suffix. On such occasion, just install `swig` first with `sudo apt install swig`, then rebuild and reinstall gr-baz.

# Build

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