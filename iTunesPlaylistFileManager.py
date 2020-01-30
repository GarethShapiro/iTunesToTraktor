import os

#from iTunesTrack import iTunesTrack

class iTunesPlaylistFileManager:

	outputPlaylistsFolderPath = "./output-playlists"

	def prepareTempPlaylistsFolder(self):

		print(f"iTunesPlaylistFileManager is attempting to make a folder {self.outputPlaylistsFolderPath}.")

		if not os.path.exists(self.outputPlaylistsFolderPath):
			os.mkdir(self.outputPlaylistsFolderPath, 0o755)

	def createTempPlaylists(self, playlists):

		print("iTunesPlaylistFileManager is starting to create temp playlists.")

		if playlists != None:

			for playlist in playlists:
				self.createEmptyTempPlaylistFile(playlist)

		else:
			print("However the list of playlists passed was empty")
			
	def createEmptyTempPlaylistFile(self, playlist):

		fileName = playlist.name.lower().replace(" ", "-")
		filePath = self.outputPlaylistsFolderPath + "/" + fileName + ".xml"

		print(f"iTunesPlaylistFileManager is attempting to create {filePath}")

		open(filePath, 'w').close()
