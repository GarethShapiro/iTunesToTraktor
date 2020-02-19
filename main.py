from iTunesPlaylistParser import iTunesPlaylistParser
from TraktorPlaylistParser import TraktorPlaylistParser

from FileManager import FileManager

iTunesParser = iTunesPlaylistParser("./iTunes.xml")
iTunesPlaylists = iTunesParser.playlists

traktorParser = TraktorPlaylistParser("./collection.nml")
traktorPlaylists = traktorParser.playlists

fileManager = FileManager()
fileManager.prepareTempPlaylistsFolder()
fileManager.createTempPlaylists(iTunesPlaylists, traktorPlaylists)

parentFolderPaths = fileManager.getPaths()

fileManager.diffTunes(parentFolderPaths, iTunesPlaylists, traktorPlaylists)