munin-1wire
===========

Munin plugin for reading from Dallas 1Wire temperature sensors. Specifically tested using DS18B20 sensors on a RaspberryPi running Raspbian Wheezy. May work on other platforms as well

Requires samuel/python-munin

Installation
============

Ensure that you are running a kernel that supports the w1-gpio and w1-therm modules, and that these modules are loaded (`modprobe w1-gpio w1-therm`). This should create folders in `/sys/bus/w1/devices` for each sensor. These folders should contain a file called `w1-slave`.

Clone somewhere convenient, then copy 1wire.py to `/usr/share/munin/plugins`, then symlink it into `/etc/munin/plugins` (`ln -s /usr/share/munin/plugins/1wire.py /etc/munin/plugins/1wire`). Restart munin-node, and the master should start picking up sensors

Configuration
=============

By default, the plugin will use the sensors serial number as its label on the graph. This isn't very human-friendly, so aliases can be configured. This is done by using munins' `plugin-conf.d` folder to set environment variables. The plugin will look for environment variables called `alias_[sensor serial]`, and use the value of this variable as the label instead of the id. For example:

    [1wire]
    env.alias_00000437ddab Tank
    env.alias_000004371f3c Ambient

Note that the family ID ('28-') is not included.
For more information on plugin-conf.d, see [the munin wiki](http://munin-monitoring.org/wiki/plugin-conf.d)


-- Will Hughes, 2013