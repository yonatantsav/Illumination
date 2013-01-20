"""
  illumination.py
  
  by Jack Kalish and Yonatan Ben-Simhon
  NYU ITP 2011
"""

import processing.video.Capture as Capture
import commands, subprocess, math, re, os, shutil, glob, random, time
from BeautifulSoup import BeautifulSoup
#from markov import MarkovGenerator
import imageadjuster.ImageAdjuster as ImageAdjuster;
from threading import Thread
from MarkovGenerator import MarkovGenerator
#from ArduinoSerialProcessing import ArduinoSerial

imgPath = 'captures/Capture_00001.JPG'

class Illuminate(object):
	def setup(self):
		#~~CONTROL VARS~~#
		self.fadeAlpha = 4
		self.fadeSpeed = 15
		self.lightColor = [255,230,182]
		self.speed = 300 #overall speed of showing each word
		self.wordMargin = 3 #controls size of the box around the word

		#instantiate class vars
		self.makePoems = False
		self.flipImage = False
		
		#self.lightColor = 0xFFEF91
		self.calibrate = False
		self.showImg = 1
		self.boxList = []
		self.currentBoxNum = [0]
		self.lastTime = [0]
		self.mt = []
		self.words = []
		self.loading = 0
		self.thread = None
		self.generator = None
		self.lightOn = True
		self.img = PImage()
		#self.sensors = ArduinoSerial()
		#TRAIN THE MARKOV GENERATOR
		print "reading and getting inspiration..."
		self.generator = MarkovGenerator(n=3, max=30, min=4)
		self.showTime = 1000
		# calibrate
		f = open('config.txt')
		str = f.read()
		print "str: "+str
		calib = str.split(',')
		print calib
		try:
			self.imgPos = [int(calib[0]),int(calib[1])]
		except:
			#set default calib value
			calib = [507,324,535,297,0]
		self.imgPos = [int(calib[0]),int(calib[1])]
		self.imgSize = [int(calib[2]),int(calib[3])]
		self.imgRot = int(calib[4])
		self.saveCalib();
		#set screen		
		size(1680,1050)
		fill(255, 5000)
		noStroke()
		self.adjust = ImageAdjuster(this)
		self.line = []
		self.lines = []
		self.lineCnt = 0
		self.wordCnt = 0
		noCursor()
	
	def init(self):
		print "init called - jack kalish"
	
	def clearPhotos(self):
		#delete all but the latest available file
		#delete the capture.tif if there is one
		try:
			commands.getstatusoutput('rm -f captures/capture.tif')
		except:
			print "failed to delete capture.tif"
		files = glob.glob('captures/*')
		fileCnt = 0
		for file in files:
			if fileCnt < len(files):
				#delete the file
				commands.getstatusoutput('rm -f '+file)
			fileCnt += 1
		
		
	def loadNewImage(self):
		print "loadNewImage"
		#self.clearPhotos()
		#self.tryLoadImage(imgPath)
		self.img = None
		print "BEFORE LOAD ATTEMPT self.img: ",
		print self.img
		#if you fail, try again
		lastPixelColor = -8355712
		files = glob.glob('captures/*')
		loadSuccess = False
		imageIndex = 0
		while loadSuccess == False:
			print "Try to load image"
			files = glob.glob('captures/*')
			print "len(files): ",
			print len(files)
			if len(files) > imageIndex:
				imgPath = files[imageIndex]
				firstLetter = imgPath.split('/')[1][0]
				print "imgPath: ",
				print imgPath
				print "firstLetter: ",
				print firstLetter
				if firstLetter == "C": 
					#load image
					try:
						self.img = loadImage(imgPath)
					except:
						loadSuccess = False
					try:
						lastPixelColor = self.img.pixels[len(self.img.pixels)-1]
						print "color of last pixel: ",
						print lastPixelColor
					except:
						loadSuccess = False
					if lastPixelColor != 0:
						if lastPixelColor != -8355712:
							#full image has loaded
							loadSuccess = True
				else:
					imageIndex = imageIndex+1
		self.capture() #convert to tiff
		
	def draw(self):
		#check the sensors
		#self.checkSensors()
		
		if self.lightOn:
			self.light()
		if self.loading == 1:
			if self.thread and self.thread.isAlive():
				self.showLoader()
			else:
				self.loading = 0
				if self.onThreadComplete != None:
					self.onThreadComplete()
			
		#print "self.lines: ",
		#print self.lines
		
		#set the rotation of the stage
		pushMatrix();
		rotate(float(radians(self.imgRot)))

		if self.calibrate:
			image(self.img, self.imgPos[0], self.imgPos[1], self.imgSize[0], self.imgSize[1])

		popMatrix();

		
		if self.makePoems:
			if len(self.lines)>0:
				#background(0)
				if self.lineCnt < len(self.lines)-1:
					'''print "len(self.line): ",
					print len(self.line)
					print "len(self.words): ",
					print len(self.words)
					print "self.wordCnt: ",
					print self.wordCnt'''
					
					if millis() - self.lastTime[0] > self.showTime:
						if self.wordCnt >= len(self.line):
							#background(0)
							#go to next line
							self.wordCnt = 0
							self.lineCnt += 1
							self.line = self.lines[self.lineCnt]
							self.showTime = 1500
							self.fadeAlpha = self.fadeSpeed
							print ""
							#print "new line length:"
							#print len(self.line)
							#print " ".join(self.line)
							#print len(self.mt[self.currentBoxNum[0]])*100
						else:
							#background(0,10)
							#lightRandomWord()
							#print "self.wordCnt: ",
							#print self.wordCnt
							#print "line[self.wordCnt] ",
							#print self.line[self.wordCnt]

                            #draw boxes for words
							try:
								pushMatrix();
								rotate(float(radians(self.imgRot)))
								self.lightWord(self.line[self.wordCnt])
								popMatrix();
								self.showTime = math.sqrt(self.getCurrentWordLength())*self.speed
							except:
								print "word out of range!"
							self.wordCnt += 1
							self.fadeAlpha = 2
						self.lastTime[0] = millis()
					fill(0,0,0,self.fadeAlpha)
                    #fade out
					rect(0,0,width,height)
				else:
					#we gotta end it here, no more lines!
					self.end()

					

	def light(self):
		background(self.lightColor[0],self.lightColor[1],self.lightColor[2])
	
	def end(self):
		print "***THE END***"
		self.runThreadOn(self.makeNewPoem)
		#now delete all but the most recent photo
		#self.clearPhotos()
		
	
	def makeNewPoem(self):
		print "thinking of a new poem...",
		#make a new poem between 3 and 14 lines long
		self.lineCnt = 0
		self.wordCnt = 0
		numLines = round(random.random()*11)+3
		print "it will be ",
		print numLines,
		print "lines long"
		print "***THE START***"
		lines =  self.generator.generateFromText(numLines)
		self.lines = lines
		self.line = lines[0]
		self.showTime = 5000
	
	def getCurrentWordLength(self):
		return len(self.words[self.line[self.wordCnt]])
	
	def runThreadOn(self, method, callback=None):
		if self.thread and self.thread.isAlive():
			print "thread already running"
			return
		self.onThreadComplete = callback
		self.thread = Thread(target=method)
		self.thread.start()
		self.loading = 1
		self.calibrate = False
		
	
	def runThread(self):
		if self.thread and self.thread.isAlive():
			print "thread already running"
			return
		self.thread = Thread(target=self.run)
		self.thread.start()
		self.loading = 1
		self.calibrate = False
	
	def showLoader(self):
		randomness = 3.0
		background(self.lightColor[0], self.lightColor[1], self.lightColor[2])
		'''if self.img:
			tint(self.lightColor[0],self.lightColor[1],self.lightColor[2],150)
			image(self.img, self.getWiggle(self.imgPos[0], randomness), self.getWiggle(self.imgPos[1], randomness), self.getWiggle(self.imgSize[0], randomness), self.getWiggle(self.imgSize[1], randomness))
		'''
		#background(self.lightColor,random.random()*255)
		fill(0, random.random()*25)
		rect(0,0,width,height)
		#image(self.img, self.imgPos[0], self.imgPos[1], self.imgSize[0], self.imgSize[1])
		#image(self.img, self.imgPos[0]*random(randomness*-1, randomness), self.imgPos[1]*random(randomness*-1, randomness), self.imgSize[0]*random(randomness*-1, randomness), self.imgSize[1]*random(randomness*-1, randomness))
	
	def getWiggle(self, val, r):
		#print 'input val:',
		#print val
		val +=  (random.random()*r*2) - r
		#print 'output val',
		#print val
		return val
		
	def run(self):
		#stop current poem
		self.makePoems = False
		#clear screen
		background(0)
		self.img = None
		self.loadNewImage()
		self.showImg = 0
		#colorMode(HSB, 100);
		#tint(0,0)
		#adjust contrast
		#img.adjust.contrast(g, 2)
		#flip the image?
		if self.flipImage:
			rotate(180)
		#self.clearPhotos()
		self.performOCR()
		self.words = self.parseWords()
		self.generator.setWords(words=self.words)
	
	def onOCRComplete(self):
		print "finished reading!"
		self.makePoems = True
		self.lightOn = False
		self.runThreadOn(self.makeNewPoem)
		#now get generate the poetry from the text...
		#doMarkov()
		
	def performOCR(self):
		print "reading text..."
		subprocess.call(['tesseract',r'captures/capture.tif', 'output', '-l', 'eng' ,'+hocr.txt'])
		#commands.getstatusoutput('tesseract capture.tif output -l eng +ocr/hocr.txt')
		#commands.getstatusoutput('tesseract captures/capture.tif output -l eng +hocr.txt')
		#commands.getstatusoutput('tesseract ocr/article.tif output -l eng +ocr/hocr.txt')
		
	
	def lightRandomWord(self):
		self.lightWord(random.randint(0,len(boxList)))
	
	def lightWord(self,id):
		#print "light word: ",
		print self.words[id],
		self.lightBox(self.boxList[id])
	
	def lightNextBox(self):
		#background(0)
		#print 'light next word:'
		#print boxList[currentBoxNum[0]]
		self.lightBox(self.boxList[self.currentBoxNum[0]])
		self.currentBoxNum[0] += 1
		
	def lightBox(self,r):
		xScale = self.imgSize[0]/float(self.img.width)
		yScale = self.imgSize[1]/float(self.img.height)
		#print r
		#fill(255,10)
		fill(self.lightColor[0],self.lightColor[1],self.lightColor[2])
		rect((float(r[0]))*xScale+self.imgPos[0]-(self.wordMargin), (float(r[1]))*yScale+self.imgPos[1]-(self.wordMargin), float(r[2])*xScale+(self.wordMargin*2), float(r[3])*yScale+(self.wordMargin*2))
		#delay(1000)
			
	def moveImage(self,x,y):
		self.imgPos[0] += x
		self.imgPos[1] += y
		self.saveCalib()
		
	def scale(self,x,y):
		self.imgSize[0] += x
		self.imgSize[1] += y
		self.saveCalib()

	def rotateStage(self,r):
		self.imgRot += r
		self.saveCalib()
		
	def saveCalib(self):
		print "save calib"
		f = open('config.txt', 'r+')
		f.truncate()
		calib = str(self.imgPos[0])+","+str(self.imgPos[1])+","+str(self.imgSize[0])+","+str(self.imgSize[1])+","+str(self.imgRot)
		print "calib: "+calib
		f.write(calib)
		f.close()	
		
	def clearCaptures(self):
		print "clear captures dir"
		files = glob.glob('captures/*')
		print "files:"
		print files
		for f in files:
			print f
			os.remove(f)
					
	def capture(self):
		print "save tif"
		self.img.save("captures/capture.tif");
	
	def parseWords(self):
		soup = BeautifulSoup(open('output.html'))
		print "parsing words..."
		boxes = soup.findAll('span', { "class" : "ocr_word" })
		cnt = 0
		words = []
		self.boxList = []
		print boxes
		for word in boxes:
			#generate arrary of only words
			print word
			w = ""
			if len(word.contents) > 0 and len(word.contents[0].contents) > 0:
			    w = word.contents[0].contents[0]
			words.append(w)
			title = word['title']
			#print "title: " + title
			r = title.split(' ')
			r.pop(0)
			#generate another array of box data
			#convert array to processing rect object coords (x,y,W,H)
			r[2] = float(r[2]) - float(r[0])
			r[3] = float(r[3]) - float(r[1])
			self.boxList.append([r[0], r[1], r[2], r[3]])
			cnt += 1
		print "words:",
		print words
		return words
		#print "words array: "
		#print words
		
	def keyPressed(self):
		print "keypressed: "
		print key
		if key == CODED:
			if keyCode == UP:
				self.moveImage(0,-1)
			elif keyCode == DOWN:
				self.moveImage(0,1)
			elif keyCode == LEFT:
				self.moveImage(-1,0)
			elif keyCode == RIGHT:
				self.moveImage(1,0)
		elif key==61:
			self.scale(1,0);
		elif key==45:
			self.scale(-1,0);
		elif key==93:
			self.scale(0,1);
		elif key==91:
			self.scale(0,-1);
		elif key==44:
			#scale x and y together (maintain ratio)
			self.scale(-1,-1);
		elif key==46:
			self.scale(1,1);
		elif key==99:
			#c - switch calibration mode
			if not self.calibrate:
				tint(255)
				self.loadNewImage()
			self.calibrate = not self.calibrate	
		elif key==32:
			#spacebar - run
			self.onClick()
		elif key==48:
			#rotate right
			self.rotateStage(-1);
		elif key==57:
			#rotate right
			self.rotateStage(+1);
		elif key=="i":
			#display image toggle
			self.calibrate = not self.calibrate	

	def mousePressed(self):
		print "mouse pressed"
		#self.onClick()
			
	def processNewText(self):
		time.sleep(3)

		self.runThreadOn(self.run, self.onOCRComplete)
		
	def onClick(self):
		#switch between "light" and poetry
		if self.makePoems:
			self.lightOn = True
			self.makePoems = False
		else:
			self.processNewText()
		
	def stop(self):
		self.loading=0
		if self.makePoems:
			self.lightOn = True
			self.makePoems = False
		#kill any running threads
		if self.thread:
			self.thread._Thread__stop()

illuminate = Illuminate()
	
def setup(): illuminate.setup()
def draw(): illuminate.draw()
def mousePressed(): illuminate.mousePressed()
def keyPressed(): illuminate.keyPressed()
def init(): illuminate.init()