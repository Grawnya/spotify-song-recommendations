import string
import gspread
import pandas as pd
import readline
from spotify import *
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDENTIALS = Credentials.from_service_account_file('credentials.json')
SCOPE_CREDENTIALS = CREDENTIALS.with_scopes(SCOPE)
GSPREAD_AUTHORIZATION = gspread.authorize(SCOPE_CREDENTIALS)
SHEET = GSPREAD_AUTHORIZATION.open('song_recs')

def make_song_recommendations(favourite_singer, favourite_genre, favourite_track, tracks_similar, mood):
    '''docstring'''
    df = Spotify().get_spotify_data()
    # get all from genre
    genre_songs = df.loc[df['genre'] == favourite_genre]
    # get all from singer
    indics_of_songs = tracks_similar.keys()
    artist_songs = df.loc[indics_of_songs]
    list_of_songs_to_choose_from = pd.concat([genre_songs, artist_songs], ignore_index=True, axis=0)
    # from those rows, get all that fit mood
    # remove favourite track
# randomly select up to 20 to be returned

# paste name and some details of each on terminal 1 at a time - use Track class to save details

# ask for another one

# paste them into google sheet

# open the link in separate tab

# ask to play again
def main():
    singer = Artist().favourite_artist_exists()
    genre = Genre().favourite_genre()
    if genre != 'hip-hop':
        genre = string.capwords(genre)
    else:
        genre = 'Hip-Hop'
    track, similar_tracks = Track().favourite_track()
    mood = Mood().song_style_questions()
    songs = make_song_recommendations(singer, genre, track, similar_tracks, mood)

main()