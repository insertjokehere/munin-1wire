#!/usr/bin/python

import os
from munin import MuninPlugin

#temps = {"Tank 1":"28-00000437ddab","Tank 2":"28-000004371f3c", "Ambient":" "}

BUSPATH = "/sys/bus/w1/devices/"
ALIAS_SUFFIX = "alias_"

class TemperaturePlugin(MuninPlugin):
	title = "Temperature"
	args = "-l 0"
	vlabel = "DegC"
	scaled = False
	category = "sensors"


	def _findSensors(self):
		#find the IDs of all sensors on the bus
		if not os.path.exists(BUSPATH):
			sensors = []
		else:
			sensors = [f for f in os.listdir(BUSPATH) if os.path.isdir(os.path.join(BUSPATH,f)) and os.path.exists(os.path.join(BUSPATH,f,w1_slave))]

		#map the alias' to the sensor ID
		smap = {}
		for s in sensors:
			alias = ALIAS_SUFFIX+s
			if alias in os.environ and not alias in smap.keys():
				smap[os.environ[alias]] = s
			else:
				smap[s] = s

		return smap

	def _safeName(self, name):
		return name.lower().replace(" ","")


	@property
	def fields(self):
		sensors = self._findSensors()

		f = []

		for name in sensors.keys():
			f.append((self._safeName(name),dict(
				label = name,
				info = "Temperature of "+name,
				type = "GAUGE",
				min = 0)))
	
		return f

	def execute(self):
		sensors = self._findSensors()

		for name, sensor in sensors.items():
			f = open(os.path.join(BUSPATH,sensor,"w1_slave"),"r")
			l = f.readlines()
			f.close()
			temp = int(l[-1].split()[-1].split("=")[-1]) / 1000.0
			if temp < 85.0 and "YES" in l[0]:
				print "%s.value %.3f" % (self._safeName(name),temp)

if __name__ == "__main__":
	TemperaturePlugin().run()
		
