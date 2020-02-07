from iTunesPlaylistParser import iTunesPlaylistParser
from iTunesPlaylistFileManager import iTunesPlaylistFileManager

from TraktorPlaylistParser import TraktorPlaylistParser

iTunesParser = iTunesPlaylistParser("./iTunes.xml")
iTunesPlaylists = iTunesParser.playlists

fileManager = iTunesPlaylistFileManager()
fileManager.prepareTempPlaylistsFolder()
fileManager.createTempPlaylists(iTunesPlaylists)

traktorParser = TraktorPlaylistParser("./collection.nml", iTunesPlaylists)

