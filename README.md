# Timed Shutdown

Forces shutdown once timer runs out or force quits specified applications if timer is interrupted.
Plays sound notifications once timer is almost out.

## Motivation

Every played a video game for way too long in one session? Yeah, me neither *cough*
*cough*. This program allows you to set time till when your system will shutdown. By
default, you will get notified via sound once the time limit is close to hitting zero.
Allowing you to save and quit a singleplayer game before it's too late.

It is not meant to be used on remote servers or to specify a scheduled shutdown. Rather,
it's meant as a timer that will force stop whatever you are doing.

## Prerequisites

### Linux

In order to use all features you need `wmctrl`. On **Debian** like systems run

### Windows

As of now, it's not fully supported. You can not use it to auto close applications.

```
sudo apt install wmctrl
```

## Installtion

To install, simple run


## Usage

To run the script with default settings you can execute

```
python main.py
```

which will shutdown the system after 60 minutes. The output will look something like this

```
Shutting down in:   0%|                        | 2/3600 [00:02<1:00:03,  1.00s/it]
```

You can **cancel** the process with `CTRL + C`. In order to bind applications to the cancellation
process you can add them via `-a <app_name>`. This will **close** the app if you cancel the
shutdown. To list all running apps you can run `-l`.

```
usage: main.py [-h] [-a APP] [-l] [--sound-theme {big-sur,chime,mario,material,pokemon,sonic,zelda}] [minutes]

Shut down the system after the given time period.

positional arguments:
  minutes               time in minutes till shutdown

options:
  -h, --help            show this help message and exit
  -a APP, --app APP     the app that will get closed if the timer is interrupted
  -l, --list-apps       list all running applications and exit.
  --sound-theme {big-sur,chime,mario,material,pokemon,sonic,zelda}
                        the theme to use to play sounds, see chime
```

### Examples

Let's say I want to play minecraft for 45 minutes and I am in a call with a friend.
I could run

```
ftimer 45 -a minecraft -a discord
```

which would bind both minecraft and discord to the cancellation process.
If I cancel the shutdown process, both of them will be **closed**.

Note that for this to work, both `minecraft` and `discord` need to be called this way. In order to get a list of running applications, run

```
ftimer -l
```

which will print out something like

```
('0x01200003', 'xfce4-panel')
('0x01000003', 'Desktop')
('0x02e00003', 'forceful-timer · PyPI - Brave')
```

you don't have to care about the first entry (it's mainly for debugging), all you have to care about is to match the name somewhat closely.

## Development

If you want to contribute to this repo or simple want to develop your own repo locally, then you can install it through

### Linux

```
git clone https://github.com/PraxTube/timed-shutdown.git
cd timed-shutdown
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### Windows

```
git clone https://github.com/PraxTube/timed-shutdown.git
cd timed-shutdown
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
pip install -e .
```

once you installed and set up your virtual environment, you can use the script and make changes to it.

To contribute, feel free to simple fork and open up a pull request.
