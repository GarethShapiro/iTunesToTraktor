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

		playlistsCreated = []
		playlistsSkipped = []

		if iTunesPlaylists != None:

			for playlist in iTunesPlaylists:

				tNames = [tPlaylist.name for tPlaylist in traktorPlaylists]

				if playlist.name in tNames:

					emptyPlaylistFilePath = self.__createEmptyTempPlaylistFile(playlist)
					playlistsCreated.append(emptyPlaylistFilePath)

				else:

					playlistsSkipped.append(playlist.name)

		else:

			Terminal.warning("However the list of playlists passed was empty")

		Terminal.ok(f"iTunesPlaylistFileManager created {len(playlistsCreated)} empty temporary playlists:")

		for createdPlaylist in playlistsCreated:
			Terminal.ok(f"	{createdPlaylist}")

		if len(playlistsSkipped) > 0:

			Terminal.warning(f"iTunesPlaylistFileManager skipped {len(playlistsSkipped)} iTunes playlists that weren't in the Traktor DB:")

			for skippedPlaylist in playlistsSkipped:
				Terminal.warning(f"	{skippedPlaylist}")

	def __createEmptyTempPlaylistFile(self, playlist):

		fileName = playlist.name.lower().replace(" ", "-")
		filePath = self.outputPlaylistsFolderPath + "/" + fileName + ".xml"

		open(filePath, 'w').close()

		return filePath
