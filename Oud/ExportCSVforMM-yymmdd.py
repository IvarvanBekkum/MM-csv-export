#!/usr/bin/python

import math
import os
import re
import string
import time
import csv
import codecs
from datetime import datetime, timedelta, tzinfo
from dateutil.tz import *
import dateutil.parser

from Foundation import *
from ScriptingBridge import *
from Tkinter import *
from tkFileDialog import asksaveasfilename

class App:
	def __init__(self,parent):
		self.frame = Frame(parent)
		self.frame.pack(padx=2,pady=2)

   		self.entry = Label(self.frame,width=110, text="This script will save the track points of the currently selected tracks as CSV file for the MilkMachine Plugin for QGIS-yymmdd.")
		self.entry.pack(side=TOP,padx=2,pady=2)

	def go(self, filename):
		myTracks = SBApplication.applicationWithBundleIdentifier_("info.stichling.myTracks")

		timeFormat = "%H:%M:%S"
		dateFormat = "%Y/%m/%d"

		with codecs.open(filename, "w") as csvfile:
			writer = csv.writer(csvfile, delimiter=',', quotechar='\\', quoting=csv.QUOTE_MINIMAL)
			writer.writerow(['date', 'time', 'y', 'x', 'altitude'])

			for track in myTracks.selectedTracks():
				timezone = track.timezone()
				print timezone
				count = 0
				for point in track.points():
					count = count + 1
					latitude = point.latitudeString()
					longitude = point.longitudeString()
					timestamp = time.localtime(point.timeIntervalSinceReferenceDate() + 978307200 + timezone*60) #point.timeIntervalSinceReferenceDate()
					elevation = point.elevation()
					speed = point.speed()
					writer.writerow([time.strftime(dateFormat, timestamp).encode("utf-8"), time.strftime(timeFormat, timestamp).encode("utf-8"), latitude, longitude, elevation])
					#("%.3f" % length).encode("utf-8"), tags, desc, count, waypointCount, photoCount])

root = Tk()
root.title('myTracks Scripts')
app = App(root)

os.system("/usr/bin/osascript -e 'tell app \"Finder\" to set frontmost of process \"Python\" to true'")
filename = asksaveasfilename(filetypes=[("csv","*.csv")],defaultextension="csv")
app.go(filename)
