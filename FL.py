#!/usr/bin/env python3
from os import walk, path, listdir, system, popen
from datetime import datetime
from random import choice, randint, seed
from subprocess import Popen
from datetime import datetime
from time import sleep
import platform
		
class FL:
	def __init__(self):
		# Set parameters here
		
		# both path must start with a r: r'', r'Intervals' etc...
		self.video_path = r'.' 		# path to videos 1.mp4 to 100.mp4 (r'' and r'.' means same directory as python file)
		self.interval_path = r'Intervals' # path to interval pics/webms/musics or whatever
		self.interval_length = 1 	# number of seconds of interval
		self.fullscreen = '' 		# must be '-fs' (in fullscreen) or '' (not)
		self.output_log = False 	# Do you want to output logfile even without errors? 
		
		# accepted filetypes for intervals
		# only file from these types will be played (to avoid trying to play a fucking .docx)
		self.filetypes = ['jpg', 'jpeg', 'png', 'gif', 'webm', 'webp', 'mp4']
		
		
		# Do not touch the rest
		self.mpv = ''
		self.messages = []
		self.rolls = [0, 0, 0, 0, 0, 0]
		self.intervals = []
		self.logname = "fl_log0.txt"
		nb = 0
		while path.isfile(self.logname):
			nb += 1
			self.logname = 'fl_log' + str(nb) + '.txt'

	# Prints the message, and adds it to buffer (if we want to write logfile later)
	def info(self, str):
		print(str)
		self.messages.append(str)

	# Rolls a dice (returns random number between 1 and 6)
	def diceroll(self, pos):
		roll = randint(1, 6)
		self.info('Rolled a ' + str(roll))
		self.rolls[roll - 1] += 1
		newpos = pos + roll
		return newpos

	# Returns all files (with extension in defined self.filetypes) in a given folder and all its subfolders
	def listdir_rec(self, pth):
		for root, directories, filenames in walk(pth):
			for filename in filenames:
				if filename.split('.')[-1] in self.filetypes : yield (path.join(root, filename))
		
	# Checks the configuration
	def check(self):
		checks = True
		
		self.info('Checking if "self.fullscreen" has correct value')
		if self.fullscreen != '' and self.fullscreen != '-fs':
			self.info('"fullscreen" variable must either be "-fs" (fullscreen) or "" (windowed)')
			self.info('		current : "' + self.fullscreen + '"')
			checks = False
		else:
			self.info('    Done')
		
		self.info('Checking if all 100 videos are found using "self.video_path"')
		vids = listdir(self.video_path)
		test = 0
		for f in vids:
			for i in range(1, 101):
				if f == str(i) + '.mp4':
					test += 1
		if test == 0:
			self.info('No videos were found in folder "' + self.video_path + '"')
			self.info('		Please change the "video_path" variable to a folder with the required videos (from 1.mp4 to 100.mp4)')
			checks = False
		elif test != 100:
			self.info('Not all videos were found in folder "' + self.video_path + '"')
			self.info('		Number of videos with name format 1.mp4, 2.mp4, etc... found : ' + str(len(test)))
			self.info('		Maybe rename files "1 - Start.mp4" (and 25, 50, 75, 100) to 1.mp4 etc...')
			self.info('		Or check you have all the required files (1.mp4 to 100.mp4)')
			checks = False
		else:
			self.info('    Done')
		
		self.info('Trying to find some interval files using "self.interval_path"')
		self.intervals = list(self.listdir_rec(self.interval_path))
		if len(self.intervals) == 0:
			self.info('No file found for Intervals')
			self.info('		Either update the "self.interval_path" variable (current: "' + self.interval_path + '")')
			self.info('		Or update the possible filetype list :')
			self.info('		' + str(self.filetypes))
			self.info('		Note : "self.interval_path" will look in all the subfolders as well')
			checks = False
		else:
			self.info('    Done')
		
		self.info('Checking if mpv can be run')
		test = popen('mpv --version').read()
		if test.startswith('mpv'):
			self.info('    mpv is installed')
			self.mpv = 'mpv '
		else:
			myOs = platform.system()
			if myOs == 'Windows':
				self.info('    mpv not installed, trying to revert to static binary')
				self.mpv = 'exes/mpv_win.exe '
			elif myOs == 'Darwin':
				self.info('    mpv not installed, trying to revert to static binary')
				self.mpv = 'exes/mpv_osx '
			elif myOs == 'Linux':
				self.info('    No static binary available for Linux')
				self.info('    Please install mpv through your package manager')
				self.info('    or through mpv-build') 
				checks = False
			
		return checks
		
	# Plays video given the number
	def video(self, nb):
		file = path.join(self.video_path, str(nb) + '.mp4')
		self.info('Playing "' + file + '"')
		system(self.mpv + self.fullscreen + ' -msg-level=all=no "' + file + '"')
	
	# Plays a random interval in self.intervals
	def interval(self):
		file = choice(self.intervals)
		self.info('Interval : "' + file + '"')
		p = Popen(self.mpv + self.fullscreen + ' -msg-level=all=no -loop "' + file + '"', shell=True)
		sleep(self.interval_length)
		p.terminate()
	
	# Play the game
	def start(self):
		self.info('Start')
		self.info('Checking configuration.')
		self.info('')
		if self.check():
			self.info('')
			self.info('Conf ok')
			self.info('Starting the game.')
			self.video(1)
			self.info('')
			
			pos = 1
			pos = self.diceroll(pos)
			newpos = 0
			while (pos < 100):
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
					self.interval()
				pos = newpos
				
				self.info('')
	
			self.info('Congratulations, you\'ve cleared the game!')
			self.video(100)
			self.info('Number of rolls :')
			self.info('	1 : ' + str(self.rolls[0]))
			self.info('	2 : ' + str(self.rolls[1]))
			self.info('	3 : ' + str(self.rolls[2]))
			self.info('	4 : ' + str(self.rolls[3]))
			self.info('	5 : ' + str(self.rolls[4]))
			self.info('	6 : ' + str(self.rolls[5]))
			
			if self.output_log:
				file = open(self.logname,'a')
				for msg in self.messages:
					file.write(msg + '\n')
				file.close()
				print('Log printed to logfile: ' + self.logname)
		else:
			self.info('')
			self.info('Errors found')
			self.info('Please try again')
			file = open(self.logname,'a')
			for msg in self.messages:
				file.write(msg + '\n')
			file.close()
			print('Log printed to logfile: ' + self.logname)

seed(int(datetime.now().strftime("%Y%m%d%H%M%S")))
game = FL()
game.start()