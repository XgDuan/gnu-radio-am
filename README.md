# Basic information
Comming soon.

# Dependency

## Ubuntu mate
> If you are gonna run the program on your linux pc version, please skip this part.
However, if you are gonna run the program on Windows, we are not sure whether you will encounter some strange problem due to gnuradio.

pls refer to this [site](https://www.raspberrypi.org/downloads/) for more information. You are recommended to install the `ubuntu mate` for that we have test the whole system on it.

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
Sometimes, when you have built the system and try to run a simple demo, the system crashed and says 'No mudule named baz_swig' or some other modules with the `_swig` suffix. On such occasion, just run `swig` first through `sudo apt install swig`, then rebuild and reinstall the gr-baz.

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