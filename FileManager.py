from __future__ import print_function, unicode_literals

import pdb

import os
import sys
import shutil

from urllib.parse import urlparse
from urllib.parse import unquote

from collections import namedtuple

from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement
from xml.dom import minidom

from PyInquirer import prompt, print_json
from Utilities.Terminal import Terminal

ITunesPathData = namedtuple('ITunesPathData', ['path', 'file'])

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

		#assume for now that all iTunes tracks are under the same parent folder, called Music
		#just map the path to the corresponding Traktor folder once

		for playlist in tempPlaylists:

			playlistRoot = self.__getTree(playlist).getroot()
			
			for track in playlistRoot.findall("./track"):

				lastPath = ""

				for element in track:
				
					if element.tag == "location":
						
						targetTraktorPath = self.__targetTraktorPath(element.text, traktorParentFolder)
						lastPath = targetTraktorPath

						# this is where the folder creating is going to happen
						breakpoint()

	def __getTree(self, xmlFilePath):

		try:
			return ET.parse(xmlFilePath)

		except FileNotFoundError:
			Terminal.fail("There doesn't seem to be a file at {xmlFilePath}", True)
			sys.exit()

	def __targetTraktorPath(self, iTunesPath, traktorParentFolder):

		#dev data
		traktorParentFolder = "/Users/garethshapiro/Music/Tunes"
		#iTunesPath = "/None/No"

		noProtocolPath = os.path.relpath(iTunesPath, "file:///")
		iTunesPathItems = noProtocolPath.split("/")

		traktorPathItems = traktorParentFolder.split("/")
		traktorPathItems = self.__cleanPathItems(traktorPathItems)

		#iTunes seems to url encode urls
		return unquote(self.__syncPaths(iTunesPathItems, traktorPathItems))

	def __cleanPathItems(self, pathItems):

		itemsToRemove = [""]

		for remove in itemsToRemove:

			if remove in pathItems:
				pathItems.remove(remove)

		return pathItems

	def __syncPaths(self, iTunesPathItems, traktorPathItems):

		iTunesPathData = self.__iTunesPathData(iTunesPathItems)
		trimmedTraktorPathItems = self.__trimTraktorPath(traktorPathItems)

		syncedPathItems = trimmedTraktorPathItems + iTunesPathData.path

		return "".join(["/" + item for item in syncedPathItems]) + "/"
		
	def __iTunesPathData(self, iTunesPathItems):

		try:
			iTunesMusicIndex = iTunesPathItems.index("Music") # TODO: This needs to be more sophisticated 
		except ValueError:

			constructPath = "".join(["/" + item for item in iTunesPathItems if item != '..'])
			Terminal.fail(f"There doesn't appear to be a 'Music' folder in the iTunes path: \n{constructPath}", True)
			sys.exit()

		numiTunesPathItems = len(iTunesPathItems)

		# Remove the file from the path
		if numiTunesPathItems > 0:

			numiTunesPathItems -= 1
			return ITunesPathData(file = "", path = iTunesPathItems[iTunesMusicIndex:numiTunesPathItems])

		else:

			# if for some reason the file was found in the top folder. 
			# TODO: This needs testing
			Terminal.fail(f"Unhandled iTunes file at the top folder.")
			sys.exit()

	def __trimTraktorPath(self, traktorPathItems):

		try:
			traktorMusicIndex = traktorPathItems.index("Music") # TODO: This needs to be more sophisticated 
		except ValueError:

			constructPath = "".join(["/" + item for item in traktorPathItems if item != '..'])
			Terminal.fail(f"There doesn't appear to be a 'Music' folder in the Traktor path: \n{constructPath}", True)
			sys.exit()

		return traktorPathItems[0:traktorMusicIndex]