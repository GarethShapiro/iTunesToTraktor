import pdb;
from Utilities.Terminal import Terminal

import xml.etree.ElementTree as ET
from iTunesPlaylist import iTunesPlaylist

class iTunesPlaylistParser:

	playlists = None
	iTunesTree = None
	trackRepository = dict()

	def __init__(self, *args):

		iTunesLibraryPath = self.getiTunesLibraryPath(args)

		if self.validateInput(iTunesLibraryPath):

			self.iTunesTree = self.getTree(iTunesLibraryPath)
			self.playlists = self.createPlaylists(self.iTunesTree)

			Terminal.ok(f"iTunesParser found {len(self.playlists)} playlists.")

	def getiTunesLibraryPath(self, args):

		numberOfArgs = len(args)

		if(numberOfArgs == 1):
			return str(args[0])

		else:

			Terminal.fail(f"iTunesPlaylistParser was expecting 1 argument and {numberOfArgs} was recieved.", True)
			sys.exit()

	def validateInput(self, iTunesLibraryPath):

		if len(iTunesLibraryPath) < 1:

			Terminal.fail("Implausible path to iTunes Library.", True)
			sys.exit()

		return True

	def getTree(self, iTunesLibraryPath):

		Terminal.info("iTunesParser is starting to get the XML tree.")
		
		try:
			return ET.parse(iTunesLibraryPath)

		except FileNotFoundError:
			Terminal.fail("There doesn't seem to be a file at {iTunesLibraryPath}", True)
			sys.exit()

	def createPlaylists (self, tree):

		Terminal.info("iTunesParser is starting to parse the xml tree for playlists.")

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

				iTunesPlaylist = self.createiTunesPlaylist(playlist)
				targetPlaylistList.append(iTunesPlaylist)

		return targetPlaylistList

	def resetPlaylistFlags(self):

		self.isMaster = False
		self.isDistinguishedKind = False
		self.isFolder = False
		self.isSmartInfo = False

		self.isNameNext = False

	def createiTunesPlaylist(self, playlist):

		self.resetPlaylistFlags()

		newPlaylist = iTunesPlaylist()

		for element in playlist:

			if self.isNameNext == True:
				
				newPlaylist.name = element.text

				break

			if element.tag == "key" and element.text == "Name":

				self.isNameNext = True

		return newPlaylist

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

