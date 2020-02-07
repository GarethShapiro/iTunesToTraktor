import pdb;

import xml.etree.ElementTree as ET
from TraktorPlaylist import TraktorPlaylist

class TraktorPlaylistParser:

	playlists = None
	traktorTree = None

	def __init__(self, *args):
	
		numberOfArgs = len(args)

		if(numberOfArgs == 2):

			traktorLibraryPath = str(args[0])
			playlists = list(args[1])

#			if playlists != None:
			#for playlist in playlists:
			#	print(f"playlist.name == {playlist.name}")

			if len(traktorLibraryPath) > 1:

				try:
					self.traktorTree = self.getTree(traktorLibraryPath)
					self.playlists = self.createPlaylists(self.traktorTree)

					if self.playlists != None:
						for playlist in self.playlists:

							print(f"-- {playlist.attrib.get('NAME')}")

				except FileNotFoundError:

					print(f"There doesn't seem to be a file at {traktorLibraryPath}")

			else:

				print ("\nImplausible path to Traktor Library.\n")

		else:

			print (f"TraktorPlaylistParser was expecting 2 argument and {numberOfArgs} was recieved.\n")

	def getTree(self, traktorLibraryPath):

		print("TraktorPlaylist is starting to get the XML tree.")
		
		return ET.parse(traktorLibraryPath)

	def createPlaylists (self, tree):

		print("TraktorPlaylistParser is starting to parse the xml tree for playlists.")

		root = tree.getroot()
		targetPlaylistList = []

		for playlist in root.findall("./PLAYLISTS/NODE/SUBNODES/NODE[@TYPE='PLAYLIST'].."):

			for element in playlist:

				name = element.attrib.get("NAME")

				if name[:1] != "_":

					targetPlaylistList.append(element)

		return targetPlaylistList

		