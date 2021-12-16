![readme_top.jpg](img/readme_top.jpg?raw=true)

# ep-cal-jp * ePaper Japanese calendar with Raspberry pi

Beautiful, simple, electric, ePaper, Japanese calendar without glare.


## Sample image

ePaper draw like this.

![sample.png](img/sample.png?raw=true)


## Information

The calendar will show Japanese holidays. https://en.wikipedia.org/wiki/Public_holidays_in_Japan
Holidays data will get from https://holidays-jp.github.io .

If you want to show another country holiday data, rewrite source code.


## Required hardware

- Raspberry Pi Series
    - Zero is good.
- Waveshare 7.5inch E-Paper E-Ink Display (Red / Black / White): https://www.waveshare.com/product/displays/e-paper/epaper-1/7.5inch-e-paper-hat-b.htm
    - If you buy another models, change import library (ex. `epd7in5b_V2` ), some parameters in `ep-cal.py`.
- Photo frame
    - 2L is not bad.
- USB cable for Raspberry Pi power


## How to build

1. Install https://www.raspberrypi.com/software/operating-systems/ to Raspberry Pi, and settings you need. (packages update, change pi user passwd, enable ssh, ntp...)
2. Install below packages. (`python` command needs to be 3.x)
```
$ sudo apt-get install git python3-spidev python3-pil python3-rpi.gpio python3-pip
```
3. Enable SPI (GPIO) Interface.
```
$ sudo raspi-config nonint do_spi 0
```
4. Reboot Raspberry Pi.
5. `git clone` of this repository.
6. `git clone` https://github.com/waveshare/e-Paper to somewhere.
7. Make symbolic link in `/path/to/e-Paper/RaspberryPi_JetsonNano/python/lib/` to `/path/to/ep-cal-jp/lib/.`
```
$ ln -s /path/to/e-Paper/RaspberryPi_JetsonNano/python/lib/ /path/to/ep-cal-jp/lib/.
```
8. Add execute permission to `ep-cal.sh`
9. Add your crontab.
```
0 0 * * *       /path/to/ep-cal-jp/ep-cal.sh >> /tmp/ep-cal.log 2>&1
```
10. Wait for next day. (If can not wait, execute `ep-cal.sh`)


## Lovely, respectful

-  speedyg0nz / MagInkCal: https://github.com/speedyg0nz/MagInkCal/tree/main/render
    - Everyone enchanted, greatly product.
- Android Experiments OBJECT グランプリ : Magic Calendar: https://www.youtube.com/watch?v=2KDkFgOHZ5I
    - And, everyone enchanted so.
