from iTunesPlaylistParser import iTunesPlaylistParser
from iTunesPlaylistFileManager import iTunesPlaylistFileManager

from TraktorPlaylistParser import TraktorPlaylistParser

iTunesParser = iTunesPlaylistParser("./iTunes.xml")
iTunesPlaylists = iTunesParser.playlists

traktorParser = TraktorPlaylistParser("./collection.nml")
traktorPlaylists = traktorParser.playlists

fileManager = iTunesPlaylistFileManager()
fileManager.prepareTempPlaylistsFolder()
fileManager.createTempPlaylists(iTunesPlaylists, traktorPlaylists)