import re
from random import choice
    

#todo: use Proper Nouns & Numbers off text
#todo: use some parts-of-speech (e.g. -ing)
#todo: read tuples off preprocessed dictionary
#todo: improve parsing (end of sentense)
class MarkovGenerator(object):

  def __init__(self, n, max, min=5):
    self.words = []
    self.n = n # order (length) of ngrams
    self.max = max # maximum number of elements to generate
    self.min = min # minimum number of elements to generate
    self.ngrams = dict() # ngrams as keys; next elements as values
    self.beginnings = list() # beginning ngram of every line
    self.names = set()
    for line in open("namesAll.txt"):
    	self.names.add(line.strip())
    self.nouns = set()
    for line in open("listNouns.txt"):
    	self.nouns.add(line.strip())
    self.verbs = set()
    for line in open("listVerbs.txt"):
    	self.verbs.add(line.strip())
    lines = []
    for line in open("PoemLinesNew.txt"):
    	lines.append(line)
    self.createNgrams(lines)
    self.localbeginings = list()
    self.localNgrams = dict()
    self.article = []
    self.articleWords = []
    self.articleWordPositions = dict()
    self.bt = {}
    for line in open('brownList.txt'):
    	words = line.split()
    	tag = words[0]
    	self.bt[tag] = set()
    	for word in words[1:]:
    		self.bt[tag].add(word)
    self.bt["VD"] = self.bt["VD"].union(self.bt["VN"])
    
    self.debug = 0
  	
  def setWords(self,words):
  	 self.words = words
  	
  	
  def tokenizePoems(self, text):#expecting preparsed text
  	lines = []
  	for line in text:
  		lines.append(line.split())
  	return lines
  	
  	
  def getHTMLarray(self): #done
  	return self.words
  		

  def tokenizeArticle(self, articleArray): #done
    words = []
    positions = {}
    singleCharWords = ['a','i','m','s','d','t']
    i = -1
    for element in articleArray:
      i = i + 1
      #Error happens here sometimes: TypeError: expected str or unicode but got <type 'instance'>
      try:
        terms = re.findall(r'\w+',element)
      except:
        print "finding terms failed"
      if len(terms) == 1:
        word = terms[0]
        if len(word) > 1 or word in singleCharWords:
          words.append(word)
          if word not in positions:
            positions[word] = []
  				#print word + " " + str(i) 
          positions[word].append(i)
    self.articleWords = words
    self.articleWordPositions = positions
    self.makeTagLists()
  
  
  def makeTagLists(self):
  		newline = []
  		for word in self.articleWordPositions.keys():
  			tags = []
  			
  			#if word.isdigit():
			#	tags.append('<Num>')
			if word[0].isupper() and word.lower() in self.names:
				tags.append('<Name>')
			#elif pos == 'NNP' and i > 1:
			#	tag = '<NNP>'
			if word in self.nouns and word in self.bt["N"]:
				tags.append('<NN>')
			if word[len(word)-1] == "s" and word[0:len(word)-1] in self.nouns and word in self.bt["N"]:
				tags.append('<NNS>')
			if word[len(word)-3:] == "ing" and word[0:len(word)-3] in self.verbs and word in self.bt["VG"]:
				tags.append('<VBG>')
			if word[len(word)-2:] == "ed" and word[0:len(word)-2] in self.verbs and word in self.bt["VD"]:
				tags.append('<VBD>')
			if word in self.verbs and word in self.bt["V"]:
				tags.append('<VB>')
			if word[len(word)-2] == "ly" and word in self.bt["ADV"]:
				newline.append('<ADV>')
			if word in self.bt["ADJ"]:
				newline.append('<ADJ>')
			
			if tags != []:
				for tag in tags:
					if tag not in self.articleWordPositions:
  						self.articleWordPositions[tag] = []
  					self.articleWordPositions[tag].extend(self.articleWordPositions[word])
  					self.articleWordPositions[tag].sort()
  					if self.debug:
  						print "word: " + word + ", tag " + tag

  def createNgrams(self, text): #done
  	for line in self.tokenizePoems(text):
  		if len(line) >= self.n:
  			beginning = tuple(line[:self.n])
    		self.beginnings.append(beginning)
    		for i in range(len(line) - self.n):
      			gram = tuple(line[i:i+self.n])
      			next = line[i+self.n] # get the element after the gram

      		# if we've already seen this ngram, append; otherwise, set the
      		# value for this key as a new list
      		if gram in self.ngrams:
      			#todo: illiminate duplicates
        		self.ngrams[gram].append(next)
      		else:
        		self.ngrams[gram] = [next]
        		#self.beginnings.append(gram)

  def pruneNgrams(self): #done
  	self.localNgrams = dict()
  	self.localbeginings = list()
  	for gram in self.ngrams:
  		allgood = True
  		for element in gram:
  			if element not in self.articleWordPositions:
  				allgood = False
  				break
  		
  		if allgood:
  			for word in self.ngrams[gram]:
  				allsame = True
  				for member in gram:
  					if word != member:
  						allsame = False
  						break
  				'''for member in gram:
  					alltags 
  					if member[0] == '<':
  						for g in gram:
  							if g[0] != '<';
  								break
  						allsame = False'''
  						
  				if not allsame:
  					if word in self.articleWordPositions:
  				 		if gram not in self.localNgrams:
  				 			self.localNgrams[gram] = []
  				 		self.localNgrams[gram].append(word)
  						self.localbeginings.append(gram)
  				#else:
  					#print "-> (" + word + ") ", 
  					#print gram
  	for gram in self.localNgrams:
  		results = set(self.localNgrams[gram])
  		self.localNgrams[gram] = list(results)

  # called from generate() to join together generated elements
  def concatenate(self, source):
    return " ".join(source)
    
  def generateFromText(self,numlines): #done

    #lines = []
    #for line in open("Poems.txt"):
    #	lines.append(line)
    #self.createNgrams(lines)
    self.article = self.getHTMLarray() #output  output_diabetes output_speech_lost output_melanoma 
    self.tokenizeArticle(self.article)
    self.pruneNgrams()
    if self.debug ==1:
    	print self.localNgrams
    output = []
    for n in range(0,numlines):
    	iter = 0
    	line = self.generateFromTextOld()
    	longestline = line
    	while len(line.split()) < self.min and iter < 1000:
    		iter += 1
    		line = self.generateFromTextOld()
    		if len(line) > len(longestline):
    			longestline = line
    	
    	newline = self.makeLocationsArray(longestline) 
    	if newline !=[]:
    		output.append(newline)
    return output
    
  def makeLocationsArray(self,line):
      output = []
      curpos = -1
      prev = ""
      curr = ""
      for word in line.split():
          if word in self.articleWordPositions:
              list = self.articleWordPositions[word]
              if list[len(list)-1] < curpos:
                  curpos = list[0]
              else:
                  for loc in list:
                      if loc > curpos:
                          curpos = loc
                          break
              if prev == "a" or prev == "an":
                  curr = self.article[curpos]
                  if prev == "a" and curr[0] in ("aeiou"):
                      for loc in list:
                          if self.article[loc][0] not in ("aeiou"):
                              curpos = loc
                              if self.debug:
                                  print "prev = " + prev + ", curr = " + curr + ", curr[0] = " + curr[0] + ", self.article[loc] = " + self.article[loc] + ", self.article[loc][0] not in (\"aeiou\") = " + str(self.article[loc][0] not in ("aeiou")) 
                              break
                      if self.article[curpos][0] in ("aeiou"):
                          #error
                          print "error"
                  if prev == "an" and curr[0] not in ("aeiou"):
                      for loc in list:
                          if self.article[loc][0] in ("aeiou"):
                              curpos = loc
                              if self.debug:
                                  print "prev = " + prev + ", curr = " + curr + ", curr[0] = " + curr[0] + ", self.article[loc] = " + self.article[loc] + ", self.article[loc][0] in (\"aeiou\") = " + str(self.article[loc][0] in ("aeiou")) 
                              break
                      if self.article[curpos][0] not in ("aeiou"):
                          #error
                          print "error"
              output.append(curpos)
              prev=self.article[curpos]
      return output    			
    				

    
  # generate a text from the information in self.ngrams
  def generateFromTextOld(self): #done

    from random import choice
    
    if len(self.localbeginings) == 0:
      return "Sorry, empty"
    
    # get a random line beginning; convert to a list. 
    current = choice(self.localbeginings)
    output = list(current)

    for i in range(self.max):
      if current in self.localNgrams:
        possible_next = self.localNgrams[current]
        next = choice(possible_next)
        output.append(next)
        # get the last N entries of the output; we'll use this to look up
        # an ngram in the next iteration of the loop
        current = tuple(output[-self.n:])
      else:
        break

    output_str = self.concatenate(output)
    return output_str
    
  def arrayToWords(self,arrays):
  	lines = []
  	for line in arrays:
  		tmp = []
  		for position in line:
  			tmp.append(self.article[position])
  		lines.append(" ".join(tmp))
  	return lines

if __name__ == '__main__':

  import sys
  generator2 = MarkovGenerator(n=3, max=30, min=4)
  lines =  generator2.generateFromText(14)
  print generator2.arrayToWords(lines)
