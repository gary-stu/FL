# FL

## Introduction

This script was created as a support to a board game.

The rules are the following:

- You start at spot 1
- You roll a six faced dice to know how many spots you have to move
- You play the video of the spot you ended to, and do what it says
- You have to reach spot 100 to win the game

## Prerequisites

Obviously, you need Python.

You also need mpv accessible through your PATH, but Windows and OSX binaries are packaged with the release in case you don't have it installed

## Installing

1. You extract the release somewhere you want
2. You edit FL.py to enter your own settings
```
	self.video_path = r'.'
	self.interval_path = r'Intervals'
	self.interval_length = 1
	self.fullscreen = '-fs'
	self.output_log = False
```
   - self.video_path: the path to your "rounds", or "spot" video. They number from 1.mp4 to 100.mp4
   - self.interval_path: Path to some files to play in between the rounds. Path will be explored recursively, so all subfolders in this path will be explored as well
   - self.interval_length: Length, in seconds, between the rounds
   - self.fullscreen: if you want to start mpv in fullscreen, put '-fs', else put ''
   - self.output_log: Do you want to create a verbose log, even if there are no errors? True for yes, False for no
3. You may also edit, in FL.py, self.filetypes
```
	self.filetypes = ['jpg', 'jpeg', 'png', 'gif', 'webm', 'webp']
```
   - self.filetypes is the list of possible extensions for interval files
4. You are now good to go

## How to play

If your OS allows you to run python scripts from clicking them, you can do that.

Else, you'll have to start the script from your terminal (or cmd)

On Linux and OSX (note that you can replace python by python3):
```
	cd (your folder with FL.py in it)
	python FL.py
```

On Windows :
```
	cd (your folder with FL.py in it)
	py FL.py
```
But a double click on file should be enough for windows. You can then set up self.output_log to True if you want to see what's going on

## License

This code is licensed under [the Unlicense](https://github.com/gary-stu/FL/blob/master/LICENSE)
