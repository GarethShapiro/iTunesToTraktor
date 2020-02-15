import sys
from Utilities.Terminal import Terminal

import xml.etree.ElementTree as ET

from TraktorPlaylist import TraktorPlaylist

class TraktorPlaylistParser:

	traktorLibraryPath = None
	playlists = []
	traktorTree = None

	def __init__(self, *args):
	
		self.validateInput(args)

		try:

			self.traktorTree = self.getTree(self.traktorLibraryPath)
			
		except FileNotFoundError:

			Terminal.fail(f"There doesn't seem to be a file at {self.traktorLibraryPath}", True)
			sys.exit()

		self.playlists = self.createPlaylists(self.traktorTree)
		Terminal.ok(f"TraktorPlaylistParser found {len(self.playlists)} playlists.")

	def validateInput(self, args):

		numberOfArgs = len(args)

		if(numberOfArgs == 1):

			traktorLibraryPath = str(args[0])

			if len(traktorLibraryPath) > 1:

				self.traktorLibraryPath = traktorLibraryPath

			else:

				Terminal.fail("Implausible path to Traktor Library.", True)
				sys.exit()
		else:

			Terminal.fail("TraktorPlaylistParser was expecting 2 argument and {numberOfArgs} was recieved.", True)
			sys.exit()

	def getTree(self, traktorLibraryPath):

		Terminal.info("TraktorPlaylist is starting to get the XML tree.")
		return ET.parse(traktorLibraryPath)

	def createPlaylists (self, tree):

		Terminal.info("TraktorPlaylistParser is starting to parse the xml tree for playlists.")

		root = tree.getroot()
		targetPlaylistList = []

		for playlist in root.findall("./PLAYLISTS/NODE/SUBNODES/NODE[@TYPE='PLAYLIST'].."):

			for element in playlist:

				name = element.attrib.get("NAME")

				if name[:1] != "_":

					traktorPlaylist = TraktorPlaylist()
					traktorPlaylist.name = element.attrib.get('NAME')

					targetPlaylistList.append(traktorPlaylist)

		return targetPlaylistList

		