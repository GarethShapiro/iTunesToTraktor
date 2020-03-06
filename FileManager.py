from __future__ import print_function, unicode_literals

import os
import sys
import shutil

import xml.etree.ElementTree as ET

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

				emptyPlaylistFilePath = self.__createEmptyTempPlaylistFile(playlist)
				playlistsCreated.append(emptyPlaylistFilePath)


				tree = TreeBuilder()
				tree.start("playlist")
				xml = tree.close()

				

				for track in playlist.tracks:

					Terminal.info(f"{playlist.name} :: {track.name} - {track.artist} [{track.genre}] [{track.location}]")

		else:

			Terminal.warning("However the list of iTunesPlaylists passed was empty")

		Terminal.ok(f"iTunesPlaylistFileManager created {len(playlistsCreated)} empty temporary playlists:")

		#for createdPlaylist in playlistsCreated:
			

	def __createEmptyTempPlaylistFile(self, playlist):

		fileName = playlist.name.lower().replace(" ", "-")
		filePath = self.outputPlaylistsFolderPath + "/" + fileName + ".xml"

		open(filePath, 'w').close()

		Terminal.ok(f"	{filePath}")

		return filePath

	# Copying Files
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

	def diffTunes(self, pathList, iTunesPlaylists, traktorPlaylists):

		if 'itunes_parent_folder' not in pathList or 'traktor_parent_folder' not in pathList:
			Terminal.fail("Either the iTunes or the Traktor parent folder missing.")
			sys.exit()

		iTunesParentFolder = pathList

		Terminal.info(pathList)



