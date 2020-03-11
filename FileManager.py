from __future__ import print_function, unicode_literals

import pdb

import os
import sys
import shutil

from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement
from xml.dom import minidom

from PyInquirer import prompt, print_json
from Utilities.Terminal import Terminal


class FileManager:

	# Temp Playlist
	outputPlaylistsFolderPath = "./output-playlists"

	def prepareTempPlaylistsFolder(self):

		Terminal.info(f"iTunesPlaylistFileManager is attempting to make a folder {self.outputPlaylistsFolderPath}.")

		if not os.path.exists(self.outputPlaylistsFolderPath):
			os.mkdir(self.outputPlaylistsFolderPath, 0o755)
		else:
			self.__emptyPlaylistsFolder()

	def __emptyPlaylistsFolder(self):

		for root, dirs, files in os.walk(self.outputPlaylistsFolderPath):

		    for f in files:
		        os.unlink(os.path.join(root, f))

		    for d in dirs:
		        shutil.rmtree(os.path.join(root, d))

	def createTempPlaylists(self, iTunesPlaylists):

		Terminal.info(f"iTunesPlaylistFileManager is starting to create temp playlists.")

		playlistsCreated = []
		
		if iTunesPlaylists != None:

			for playlist in iTunesPlaylists:

				emptyPlaylistFilePath = self.__createEmptyTempPlaylistFilePath(playlist)

				playlistXML = Element('playlist')
				
				for track in playlist.tracks:

					trackXML = SubElement(playlistXML, 'track')
					nameXML = SubElement(trackXML, 'name')
					nameXML.text = track.name
					artistXML = SubElement(trackXML, 'artist')
					artistXML.text = track.artist
					genreXML = SubElement(trackXML, 'genre')
					genreXML.text = track.genre
					locationXML = SubElement(trackXML, 'location')
					locationXML.text = track.location

				prettyXMLString = self.__prettifyXml(playlistXML)

				with open(emptyPlaylistFilePath, "w") as newPlaylistFile:
					print(prettyXMLString, file=newPlaylistFile)

				playlistsCreated.append(emptyPlaylistFilePath)

		else:

			Terminal.warning("However the list of iTunesPlaylists passed was empty")

		Terminal.ok(f"iTunesPlaylistFileManager created {len(playlistsCreated)} empty temporary playlists:")

		return playlistsCreated

	def __prettifyXml(self, topElement):

		rough_string = ET.tostring(topElement, 'utf-8')
		reparsed = minidom.parseString(rough_string)
		return reparsed.toprettyxml(indent="  ")

	def __createEmptyTempPlaylistFilePath(self, playlist):

		fileName = playlist.name.lower().replace(" ", "-")
		filePath = self.outputPlaylistsFolderPath + "/" + fileName + ".xml"

		return filePath

	def getPaths(self):

		questions = [
			{
				'type': 'input',
 				'name': 'itunes_parent_folder',
				'message': 'What is the parent iTunes folder?',
			}
			,
			{
				'type': 'input',
				'name': 'traktor_parent_folder',
				'message': 'What is the parent Traktor folder?',
			}
		]

		return prompt(questions)

	def copyTunestoTraktorPath(self, pathList, tempPlaylists):

		if 'itunes_parent_folder' not in pathList or 'traktor_parent_folder' not in pathList:
			Terminal.fail("Either the iTunes or the Traktor parent folder missing.")
			sys.exit()

		iTunesParentFolder = pathList["itunes_parent_folder"]
		traktorParentFolder = pathList["traktor_parent_folder"]

		#assume for now that all iTunes tracks are under the same parent folder so 
		#just map the path to the corresponding Traktor folder once


		for playlist in tempPlaylists:

			playlistRoot = self.__getTree(playlist).getroot()
			
			for track in playlistRoot.findall("./track"):

				for element in track:
				
					if element.tag == "location":
						Terminal.info(self.__mapTraktorPath(element.text, traktorParentFolder))

	def __getTree(self, xmlFilePath):

		try:
			return ET.parse(xmlFilePath)

		except FileNotFoundError:
			Terminal.fail("There doesn't seem to be a file at {xmlFilePath}", True)
			sys.exit()

	def __mapTraktorPath(self, iTunesPath, traktorParentFolder):

		traktorParentFolder = "/Users/garethshapiro/Music/Tunes"

		noProtocolPath = os.path.relpath(iTunesPath, "file:///")
		iTunesPathItems = noProtocolPath.split("/")

		tracktorPathItems = traktorParentFolder.split("/")

		breakpoint()

	#def __mappediTunesParentFolder(self):