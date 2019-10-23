#!/usr/bin/env python3
import platform
from datetime import datetime
import os
from random import choice, randint, seed
from subprocess import Popen
from time import sleep
from signal import SIGTERM


class FL:
	def __init__(self):
		# Set parameters here
		# both path must start with a r: r'', r'Intervals' etc...
		self.video_path = r'.'  	# path to videos 1.mp4 to 100.mp4 (r'' and r'.' means same directory as python file)
		self.interval_path = r'.'  	# path to interval pics/webms/musics or whatever
		self.interval_length = 10  	# number of seconds of interval
		self.fullscreen = False  	# must be True or False
		self.output_log = False  	# Do you want to output logfile even without errors?

		# accepted filetypes for intervals
		# only file from these types will be played (to avoid trying to play a fucking .docx)
		self.filetypes = ['jpg', 'jpeg', 'png', 'gif', 'webm', 'webp', 'mp4']

		# Do not touch the rest
		self.mpv = ''
		self.messages = []
		self.posLog = [1]
		self.intervals = []
		self.logname = "fl_log0.txt"
		self.myOs = platform.system()
		nb = 0
		while os.path.isfile(self.logname):
			nb += 1
			self.logname = 'fl_log' + str(nb) + '.txt'

	# Script requires each file to be {number}.mp4
	# rename files from original file pool if necessary
	def rename_files_if_necessary(self):
		self.info("Renaming file if necessary")
		if os.path.isfile(os.path.join(self.video_path, "1 - Start.mp4")):
			os.rename(os.path.join(self.video_path, "1 - Start.mp4"), os.path.join(self.video_path, "1.mp4"))
			self.info("    Renamed '1 - Start.mp4' in '1.mp4'")
		if os.path.isfile(os.path.join(self.video_path, "25 - Checkpoint.mp4")):
			os.rename(os.path.join(self.video_path, "25 - Checkpoint.mp4"), os.path.join(self.video_path, "25.mp4"))
			self.info("    Renamed '25 - Checkpoint.mp4' in '25.mp4'")
		if os.path.isfile(os.path.join(self.video_path, "50 - Checkpoint.mp4")):
			os.rename(os.path.join(self.video_path, "50 - Checkpoint.mp4"), os.path.join(self.video_path, "50.mp4"))
			self.info("    Renamed '50 - Checkpoint.mp4' in '50.mp4'")
		if os.path.isfile(os.path.join(self.video_path, "75 - Checkpoint.mp4")):
			os.rename(os.path.join(self.video_path, "75 - Checkpoint.mp4"), os.path.join(self.video_path, "75.mp4"))
			self.info("    Renamed '75 - Checkpoint.mp4' in '75.mp4'")
		if os.path.isfile(os.path.join(self.video_path, "100 - End.mp4")):
			os.rename(os.path.join(self.video_path, "100 - End.mp4"), os.path.join(self.video_path, "100.mp4"))
			self.info("    Renamed '100 - End.mp4' in '100.mp4'")
		self.info("Done")

	# Returns all files (with extension in defined self.filetypes) in a given folder and all its subfolders
	def listdir_rec(self, pth):
		for root, directories, filenames in os.walk(pth):
			for filename in filenames:
				if filename.split('.')[-1] in self.filetypes: yield (os.path.join(root, filename))

	# Prints the message, and adds it to buffer (if we want to write logfile later)
	def info(self, msg):
		print(msg)
		self.messages.append(msg)

	# Checks the configuration
	def check(self):
		checks = True
		self.info('Checking if all 100 videos are found using "self.video_path"')
		videos = os.listdir(self.video_path)
		test = 0
		for f in videos:
			for i in range(1, 101):
				if f == str(i) + '.mp4':
					test += 1
		if test == 0:
			self.info("ERROR")
			self.info('No videos were found in folder "' + self.video_path + '"')
			self.info(
				'		Please change the "video_path" variable to a folder with the required videos (from 1.mp4 to 100.mp4)')
			checks = False
		elif test != 100:
			self.info("ERROR")
			self.info('Not all videos were found in folder "' + self.video_path + '"')
			self.info('		Number of videos with name format 1.mp4, 2.mp4, etc... found : ' + str(test))
			self.info('		Please check you have all required files (from 1.mp4 to 100.mp4) in that folder')
			checks = False
		else:
			self.info('    Done')

		self.info('Trying to find some interval files using "self.interval_path"')
		self.intervals = list(self.listdir_rec(self.interval_path))
		if len(self.intervals) == 0:
			self.info("ERROR")
			self.info('No file found for Intervals')
			self.info('		Either update the "self.interval_path" variable (current: "' + self.interval_path + '")')
			self.info('		Or update the possible filetype list :')
			self.info('		' + str(self.filetypes))
			self.info('		Note : "self.interval_path" will look in all the subfolders as well')
			checks = False
		else:
			self.info('    Done')

		self.info('Checking if mpv can be run')
		test = os.popen('mpv --version').read()
		if test.startswith('mpv'):
			self.info('    mpv is installed')
			self.mpv = 'mpv '
		else:
			if self.myOs == 'Windows':
				self.info('    mpv not installed, trying to revert to static binary')
				self.mpv = 'binaries/Windows/mpv.exe '
			elif self.myOs == 'Darwin':
				self.info('    mpv not installed, trying to revert to static binary')
				self.mpv = 'binaries/OSX/mpv '
			elif self.myOs == 'Linux':
				self.info("ERROR")
				self.info('    No static binary available for Linux')
				self.info('    Please install mpv through your package manager')
				self.info('    or through mpv-build')
				checks = False

		if self.fullscreen: self.mpv += '-fs '
		self.mpv += '-msg-level=all=no '
		return checks

	# Rolls a dice (returns random number between 1 and 6)
	def diceroll(self, pos):
		self.info('Rolling dice')
		roll = randint(1, 6)
		self.info('    Rolled a ' + str(roll))
		newpos = pos + roll
		self.posLog.append(newpos)
		return newpos

	# Plays video given the number
	def video(self, nb):
		file = os.path.join(self.video_path, str(nb) + '.mp4')
		self.info('Playing : "' + file + "'")
		self.info("    " + self.mpv + '"' + file + '"')
		os.system(self.mpv + '"' + file + '"')

	# Plays a random interval in self.intervals
	def interval(self):
		file = choice(self.intervals)
		self.info('Interval : "' + file + '"')
		self.info('    ' + self.mpv + '-loop "' + file + '"')
		if self.myOs == "Windows":
			p = Popen(self.mpv + '-loop "' + file + '"')
			sleep(self.interval_length)
			p.terminate()
		elif self.myOs == 'Darwin':
			p = Popen(self.mpv + '-loop "' + file + '"', shell=True)
			sleep(self.interval_length)
			p.terminate()
		else:
			p = Popen(self.mpv + '-loop "' + file + '"', shell=True, preexec_fn=os.setsid)
			sleep(self.interval_length)
			os.killpg(p.pid, SIGTERM)

	# Play the game
	def start(self):
		self.info('Start')
		self.info('Checking configuration.')
		self.info('')
		self.rename_files_if_necessary()
		if self.check():
			self.info('')
			self.info('Conf ok')
			self.info('Starting the game.')
			self.video(1)
			self.info('')

			pos = 1
			pos = self.diceroll(pos)
			while pos < 100:
				self.video(pos)
				newpos = self.diceroll(pos)
				self.info('Current position: ' + str(newpos))
				if (pos < 25) and (newpos >= 25):
					if newpos != 25: self.video(25)
				elif (pos < 50) and (newpos >= 50):
					if newpos != 50: self.video(50)
				elif (pos < 75) and (newpos >= 75):
					if newpos != 75: self.video(75)
				elif ((pos % 25) != 0) and (newpos < 100):
					print("interval")
					self.interval()
				pos = newpos

				self.info('')

			self.info('Congratulations, you\'ve cleared the game!')
			self.video(100)
			self.info('')
			self.info('Roll history : ')
			self.info(' ' + str(self.posLog))
			if self.output_log:
				file = open(self.logname, 'a')
				for msg in self.messages:
					file.write(msg + '\n')
				file.close()
				print('Log printed to logfile: ' + self.logname)
		else:
			self.info('')
			self.info('Errors found')
			self.info('Please try again')
			file = open(self.logname, 'a')
			for msg in self.messages:
				file.write(msg + '\n')
			file.close()
			print('Log printed to logfile: ' + self.logname)


seed(int(datetime.now().strftime("%Y%m%d%H%M%S")))
game = FL()
game.start()
