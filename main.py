from iTunesPlaylistParser import iTunesPlaylistParser
from iTunesPlaylistFileManager import iTunesPlaylistFileManager

parser = iTunesPlaylistParser("./iTunes.xml")
playlists = parser.playlists

fileManager = iTunesPlaylistFileManager()
fileManager.prepareTempPlaylistsFolder()
fileManager.createTempPlaylists(playlists)