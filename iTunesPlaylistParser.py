import xml.etree.ElementTree as ET
#from iTunesTrack import iTunesTrack

class iTunesPlaylistParser:

	def __init__(self, *args):

		iTunesLibraryPath = self.getiTunesLibraryPath(args)

		if self.validateInput(iTunesLibraryPath):

			tree = self.getTree(iTunesLibraryPath)
			playlists = self.getPlaylists(tree)

			self.printPlaylist(playlists, True)

	def getiTunesLibraryPath(self, args):

		numberOfArgs = len(args)

		if(numberOfArgs == 1):
			return str(args[0])

		else:

			print (f"iTunesPlaylistParser was expecting 1 argument and {numberOfArgs} was recieved. \n")
			return ""

	def validateInput(self, iTunesLibraryPath):

		if len(iTunesLibraryPath) < 1:

			print ("\nImplausible path to iTunes playlist.\n")
			return False

		return True

	def getTree(self, iTunesLibraryPath):

		print("iTunesParser is starting to get the XML tree.")
		
		try:
			return ET.parse(iTunesLibraryPath)

		except FileNotFoundError:
			print(f"There doesn't seem to be a file at {iTunesLibraryPath}")

	def getPlaylists (self, tree):

		print("iTunesParser is starting to parse the xml tree.")

		root = tree.getroot()
		targetPlaylistList = []

		for playlist in root.findall("./dict/array/dict[key='Playlist ID']"):
			
			self.resetPlaylistFlags()

			for element in playlist:

				if element.tag == "key" and element.text == "Distinguished Kind":
					self.isDistinguishedKind = True

				if element.tag == "key" and element.text == "Master":
					self.isMaster = True

			if self.isDistinguishedKind == False and self.isMaster == False:
				targetPlaylistList.append(playlist)

		return targetPlaylistList

	def printPlaylist(self, playlistList, showTunes = False):

		for playlist in playlistList:

			self.resetPlaylistFlags()

			for element in playlist:

				if self.isNameNext == True:
					print(element.text)

				if self.isNameNext == True and showTunes == True:
					print("----------")
					self.getTracks(playlist)

				self.resetPlaylistFlags()

				if element.tag == "key" and element.text == "Name":
					self.isNameNext = True

	def resetPlaylistFlags(self):

		self.isMaster = False
		self.isDistinguishedKind = False

		self.isNameNext = False


	def getTracks(self, playlist):

		for track in playlist.findall("./array/dict[key='Track ID']"):
			trackId = track.find("integer").text
			print(f"Track ID = {trackId}")

	def resetTracksFlags(self):

		self
	'''

		for track in root.findall("./dict/dict/dict[key='Track ID']"):

			targetTrack = iTunesTrack()
			self.resetPlaylistFlags()

			for element in track:

				if self.isNameNext == True:
					targetTrack.name = element.text
			
				if self.isDateAddedNext == True:
					targetTrack.dateAdded = element.text
			
				if self.isPlayCountNext == True:
					targetTrack.playCount = element.text
			
				if self.isPlayDateNext == True:
					targetTrack.playDate = element.text

				if self.isRatingNext == True:
					targetTrack.rating = element.text

				if self.isRatingComputedNext == True:
					if element.tag == "true":
						targetTrack.rating = 0

				if self.isLocationNext == True:
					targetTrack.location = element.text
			
				self.resetPlaylistFlags()

				if element.tag == "key" and element.text == "Name":
					self.isNameNext = True

				if element.tag == "key" and element.text == "Date Added":
					self.isDateAddedNext = True

				if element.tag == "key" and element.text == "Play Count":
					self.isPlayCountNext = True

				if element.tag == "key" and element.text == "Play Date":
					self.isPlayDateNext = True

				if element.tag == "key" and element.text == "Rating":
					self.isRatingNext = True

				if element.tag == "key" and element.text == "Rating Computed":
					self.isRatingComputedNext = True

				if element.tag == "key" and element.text == "Location":
					self.isLocationNext = True

			if ".Trash" not in targetTrack.location:
				targetTrackList.append(targetTrack) 

		print("iTunesParser has finished parsing the xml file")
		return targetTrackList

	resetPlaylistFlags()

	def resetPlaylistFlags(self):
		self.isNameNext = False
		self.isDateAddedNext = False
		self.isPlayCountNext = False
		self.isPlayDateNext = False
		self.isRatingNext = False
		self.isRatingComputedNext = False
		self.isLocationNext = False
'''
