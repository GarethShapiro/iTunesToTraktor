import xml.etree.ElementTree as ET
import os

#from iTunesTrack import iTunesTrack

class iTunesPlaylistParser:

	iTunesTree = None
	trackRepository = dict()

	outputPlaylistsFolderPath = "./output-playlists"

	def __init__(self, *args):

		iTunesLibraryPath = self.getiTunesLibraryPath(args)

		if self.validateInput(iTunesLibraryPath):

			self.iTunesTree = self.getTree(iTunesLibraryPath)
			playlists = self.getPlaylists(self.iTunesTree)

			self.preparePlaylistsFolder()
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

		print("iTunesParser is starting to parse the xml tree for playlists.")

		root = tree.getroot()
		targetPlaylistList = []

		for playlist in root.findall("./dict/array/dict[key='Playlist ID']"):
			
			self.resetPlaylistFlags()

			for element in playlist:

				if element.tag == "key" and element.text == "Distinguished Kind":
					self.isDistinguishedKind = True

				if element.tag == "key" and element.text == "Master":
					self.isMaster = True

				if element.tag == "key" and element.text == "Folder":
					self.isFolder = True

				if element.tag == "key" and element.text == "Smart Info":
					self.isSmartInfo = True


			if (self.isDistinguishedKind == False and 
			    self.isMaster == False and 
			    self.isFolder == False and 
			    self.isSmartInfo == False):

				targetPlaylistList.append(playlist)

		return targetPlaylistList

	def preparePlaylistsFolder(self):

		os.mkdir(self.outputPlaylistsFolderPath, 0o755)

	def printPlaylist(self, playlistList, showTunes = False):

		for playlist in playlistList:

			self.resetPlaylistFlags()

			for element in playlist:

				if self.isNameNext == True:
					
					nameHighlight = ""

					for i in range(len(element.text)):
						nameHighlight += "-"

					print(nameHighlight)
					print(element.text)
					print(nameHighlight)

					if showTunes == True:
						
						playlistTracks = self.getPlaylistTracks(playlist)

						if playlistTracks is not None:
							for trackName in playlistTracks:
								print(trackName)

				self.resetPlaylistFlags()

				if element.tag == "key" and element.text == "Name":
					self.isNameNext = True

	def resetPlaylistFlags(self):

		self.isMaster = False
		self.isDistinguishedKind = False
		self.isFolder = False
		self.isSmartInfo = False

		self.isNameNext = False

	def getPlaylistTracks(self, playlist):

		playlistTracks = []

		for track in playlist.findall("./array/dict[key='Track ID']"):
			
			trackId = track.find("integer").text
			trackName = self.trackNameFromTrackRepository(trackId)

			if trackName is not None:
				playlistTracks.append(trackName)
			else:
				trackName = self.getTrack(self.iTunesTree, trackId)

				if trackName is not None:
					playlistTracks.append(trackName)

		if len(playlistTracks) > 0:
			return playlistTracks

		return None

	def trackNameFromTrackRepository(self, trackId):

		try:
			return self.trackRepository[trackId]
		except KeyError: 
			return None

	def getTrack(self, tree, trackId):

		root = tree.getroot()
		targetPlaylistList = []

		for track in root.findall("./dict/dict/dict[key='Track ID']"):
			
			self.resetTracksFlags()

			trackName = ""
			id = ""

			for element in track:

				if self.isNameNext == True:
					trackName = element.text

				if self.isIdNext == True:
					id = element.text

				self.resetTracksFlags()

				if element.tag == "key" and element.text == "Name":
					self.isNameNext = True

				if element.tag == "key" and element.text == "Track ID":
					self.isIdNext = True

			if id == trackId:

				targetPlaylistList.append(trackName)

		if len(targetPlaylistList) > 0:
			return targetPlaylistList

		return None

	def resetTracksFlags(self):

		self.isIdNext = False
		self.isNameNext = False

