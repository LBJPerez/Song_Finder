from flask import Flask, render_template, request
import requests
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__, template_folder='/Users/luisjimenez/Desktop/Python_Projects/IST_Project')

client_credentials_manager = SpotifyClientCredentials(client_id='3983eacffb104766ab7c877180c2d32c', client_secret='bd526b40db8d48c78d7e8690fe5f498c')
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":

        lyrics = request.form["lyrics"]

        headers = {
            "Authorization": "Bearer cDdPbXXAzg-rpuNuJ_YYwoRsGBB66OjQr8CsokDYtuXQTOjXOcmbOWdM6_PmfWsv"
        }
        params = {
            "q": lyrics
        }

        response = requests.get("https://api.genius.com/search", params=params, headers=headers)

        data = json.loads(response.text)
        songs = data["response"]["hits"]

        if len(songs) == 0:
            message = "No songs found for the given lyrics."
        else:
            message = f"Found {len(songs)} songs:"
            song_list = []
            for song in songs:
                track_name = song['result']['title']
                artist_name = song['result']['primary_artist']['name']
                preview_url = None
                try:
                    results = spotify.search(q=f"track:{track_name} artist:{artist_name}", type='track')
                    track = results['tracks']['items'][0]
                    preview_url = track['preview_url']
                except:
                    pass
                song_list.append({'name': track_name, 'artist': artist_name, 'preview_url': preview_url})

        return render_template("song.html", message=message, songs=song_list)

    return render_template("song.html")

if __name__ == "__main__":
    app.run(debug=True)



