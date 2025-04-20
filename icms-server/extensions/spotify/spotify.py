from extension import Extension
from threading import Thread
import asyncio
import time
import json as Json
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class Spotify(Extension):
    def __init__(self, server):
        super().__init__(server)

        self.clientID = ""
        self.clientSecret = ""
        self.sp = None

        credentials_path = os.getcwd() + "/extensions/spotify/credentials.json"

        with open(credentials_path) as credentials:
            json = Json.load(credentials)
            self.clientID = json["clientID"]
            self.clientSecret = json["clientSecret"]

        scope = "user-read-currently-playing user-modify-playback-state"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=self.clientID, client_secret=self.clientSecret, redirect_uri="https://0.0.0.0:8080/auth"))

        self.volume = 0
        self.register_function(self.change_volume, {
            "volume": "int"
        })
        self.register_function(self.next_track)
        self.register_function(self.previous_track)
        self.register_function(self.get_current_track)

    async def get_current_track(self):
        if self.sp is None:
            return "ERROR: Spotipy Failed To Intialise"

        song = self.sp.current_user_playing_track()['item']['name']
        return f"SUCCESS: Song Is: {song}"
        
    async def next_track(self):
        if self.sp is None:
            return "ERROR: Spotipy Failed To Intialise"

        self.sp.next_track()
        return f'SUCCESS: New Track: {self.sp.current_user_playing_track()['item']['name']}'

    async def previous_track(self):
        if self.sp is None:
            return "ERROR: Spotipy Failed To Intialise"
        
        self.sp.previous_track()
        return f'SUCCESS: New Track: {self.sp.current_user_playing_track()['item']['name']}'

    async def change_volume(self, volume: int):
        if self.sp is None:
            return "ERROR: Spotipy Failed To Intialise"
        
        self.sp.volume(volume_percent=volume)
        return f"SUCCESS: Set Volume: {volume}"


def initialise(server) -> Extension:
    spotify = Spotify(server)
    return spotify