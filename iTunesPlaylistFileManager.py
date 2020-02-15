import os
from Utilities.Terminal import Terminal

class iTunesPlaylistFileManager:

	outputPlaylistsFolderPath = "./output-playlists"

	def prepareTempPlaylistsFolder(self):

		Terminal.info(f"iTunesPlaylistFileManager is attempting to make a folder {self.outputPlaylistsFolderPath}.")

		if not os.path.exists(self.outputPlaylistsFolderPath):
			os.mkdir(self.outputPlaylistsFolderPath, 0o755)

	def createTempPlaylists(self, playlists):

		Terminal.info(f"iTunesPlaylistFileManager is starting to create temp playlists.")

		if playlists != None:

			for playlist in playlists:
				self.createEmptyTempPlaylistFile(playlist)

		else:
			Terminal.warning("However the list of playlists passed was empty")

		Terminal.ok(f"iTunesPlaylistFileManager created {len(playlists)} empty temporary playlists.")

	def createEmptyTempPlaylistFile(self, playlist):

		fileName = playlist.name.lower().replace(" ", "-")
		filePath = self.outputPlaylistsFolderPath + "/" + fileName + ".xml"

		open(filePath, 'w').close()
