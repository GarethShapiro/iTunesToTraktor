import os
import shutil

from Utilities.Terminal import Terminal

class iTunesPlaylistFileManager:

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

	def createTempPlaylists(self, iTunesPlaylists, traktorPlaylists):

		Terminal.info(f"iTunesPlaylistFileManager is starting to create temp playlists.")

		numberOfPlaylists = 0

		if iTunesPlaylists != None:

			for playlist in iTunesPlaylists:

				tNames = [tPlaylist.name for tPlaylist in traktorPlaylists]
				
				if playlist.name in tNames:
					
					self.__createEmptyTempPlaylistFile(playlist)
					numberOfPlaylists += 1

		else:
			
			Terminal.warning("However the list of playlists passed was empty")

		Terminal.ok(f"iTunesPlaylistFileManager created {numberOfPlaylists} empty temporary playlists.")

	def __createEmptyTempPlaylistFile(self, playlist):

		fileName = playlist.name.lower().replace(" ", "-")
		filePath = self.outputPlaylistsFolderPath + "/" + fileName + ".xml"

		open(filePath, 'w').close()
