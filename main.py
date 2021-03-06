from iTunesPlaylistParser import iTunesPlaylistParser
from TraktorPlaylistParser import TraktorPlaylistParser

from FileManager import FileManager

iTunesParser = iTunesPlaylistParser("./iTunes.xml")
traktorParser = TraktorPlaylistParser("./collection.nml")
traktorPlaylists = traktorParser.playlists

iTunesParser.removePlaylistsWithoutTraktorEquivalent(traktorPlaylists)
iTunesParser.loadTracksIntoPlaylists()
iTunesPlaylists = iTunesParser.playlists

fileManager = FileManager()
fileManager.prepareTempPlaylistsFolder()
tempPlaylists = fileManager.createTempPlaylists(iTunesPlaylists)

parentFolderPaths = fileManager.getPaths()
fileManager.copyTunestoTraktorPath(parentFolderPaths, tempPlaylists)