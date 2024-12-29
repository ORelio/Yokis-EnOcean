![Yokis-EnOcean](images/yokis-enocean-logo.png)

_This tool is an example of how the [Rabbit Home](http://github.com/ORelio/Rabbit-Home) framework can be reused to make other projects. It's not maintained actively, but contributions are welcome._

Yokis-EnOcean allows driving an existing [Yokis shutter system](https://www.yokis.fr/radio/radio-ouvrant/volet-roulant-radio/) using [EnOcean](https://en.wikipedia.org/wiki/EnOcean) switches instead of the stock ones. [Yokis wall switches](https://www.yokis.fr/radio/emetteurs/telecommandes-murales/) have pretty bad autonomy, requiring to change the CR2032 battery way too often. [EnOcean switches](https://www.enocean-alliance.org/products/?_sft_enocean_frequency=868&_sft_enocean_product_category=wall-switch) are batteryless and offer more features.

**Note that this project is not authorized nor endorsed by Yokis or EnOcean.**

## How it works

The project is a custom Python service intended to run on a Linux system, on which both a [Yokis-Hack](https://github.com/nmaupu/yokis-hack) board and [EnOcean USB dongle](https://www.enocean.com/en/product/usb-300/) are connected. It translates EnOcean switch events into Yokis-Hack serial commands to drive the shutters.

If given exclusive control of the shutters (i.e. not using Yokis switches or remotes anymore) and fine-tuning timings in configuration, Yokis-EnOcean can keep track of shutter movements and adjust them to intermediate heights.

## Installing

These instructions are for advanced users with sufficient knowledge of Linux command-line.

1. Install utilities : `shuttercmd` and `enoceanserial`.
    * See [Rabbit-Home/utilities](http://github.com/ORelio/Rabbit-Home/tree/master/utilities) for instructions.
2. Install python dependency for `enocean.py`:
    * `pip install 'crc8>=0.2.1'`
2. Upload the `yokis-enocean` folder to your home directory:
    * `/home/USERNAME/yokis-enocean` should contain `yokis-enocean.py`
4. Enable lingering services for your account:
    * `sudo loginctl enable-linger USERNAME`
5. Create the `yokisenocean` service: 
    * `mkdir -p ~/.config/systemd/user`
    * `editor ~/.config/systemd/user/yokisenocean.service`
    * Paste the following, adjusting your `USERNAME`:
```ini
[Unit]
Description=Yokis EnOcean
After=local-fs.target network.target systemd-tmpfiles-setup.service

[Service]
ExecStart=/usr/bin/env python3 /home/USERNAME/yokis-enocean/yokis-enocean.py
Restart=always
Type=simple

[Install]
WantedBy=default.target
```

6. Start service:
```
systemctl --user unmask yokisenocean
systemctl --user enable yokisenocean
systemctl --user restart yokisenocean
systemctl --user status yokisenocean
```

## Configuring

It is assumed that your [Yokis-Hack](https://github.com/nmaupu/yokis-hack) device already has your shutters registered at this point. If not, see [Firmware usage](https://github.com/nmaupu/yokis-hack?tab=readme-ov-file#firmware-usage).

Go to `config` folder and edit `shutters.ini` to configue your shutters, then `enocean.ini` to configure your switches.

If you need logs to diagnose what is going on or print EnOcean device IDs, edit `logs.ini` to enable debug and logging to file.

After changing configuration files, restart the service to apply your changes:
```
systemctl --user restart yokisenocean
```

## License

The [Rabbit Home](http://github.com/ORelio/Rabbit-Home) framework, including this example project, is provided under [CDDL-1.0](http://opensource.org/licenses/CDDL-1.0) ([Why?](http://qstuff.blogspot.fr/2007/04/why-cddl.html)).

Basically, you can use it or its source for any project, free or commercial, but if you improve it or fix issues,
the license requires you to contribute back by submitting a pull request with your improved version of the code.
Also, credit must be given to the original project, and license notices may not be removed from the code.
