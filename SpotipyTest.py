import configparser
from sense_hat import SenseHat
import spotipy
import spotipy.oauth2 as oauth2
import spotipy.util as util

sense = SenseHat()

config = configparser.ConfigParser()
config.read('config.cfg')
client_id = config.get('SPOTIFY', 'CLIENT_ID')
client_secret = config.get('SPOTIFY', 'CLIENT_SECRET')
client_uri = config.get('SPOTIFY', 'CLIENT_URI')

auth = oauth2.SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
)

username="plpkacper"
scope = "user-read-playback-state"

#token = auth.get_access_token()
token = util.prompt_for_user_token(username, scope, client_id, client_secret, client_uri)
spotify = spotipy.Spotify(auth=token)

currentTrack = spotify.current_user_playing_track()
#Song Name
sense.show_message(currentTrack.get("item").get("name"))
#Album Name
sense.show_message(currentTrack.get("item").get("album").get("name"))
#Artist Name
sense.show_message(currentTrack.get("item").get("artists")[0].get("name"))















