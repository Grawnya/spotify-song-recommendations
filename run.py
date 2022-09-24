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

def operation(df, mood_keyword, operator_value, equal):
    '''docstring'''
    if operator_value == ">":
        mood_dataframe = df[operator.gt(df[mood_keyword], equal)]
    elif operator_value == "<":
        mood_dataframe = df[operator.lt(df[mood_keyword], equal)]
    return mood_dataframe

def make_song_recommendations(favourite_singer, singer_song_indices, favourite_genre, favourite_track, tracks_similar, mood):
    '''docstring'''
    df = Spotify().get_spotify_data()
    # get all from singer
    singer_songs = df.loc[singer_song_indices]
    # get all from genre
    genre_songs = df.loc[df['genre'] == favourite_genre]
    # get all from similar track
    indices_of_songs_tracks = tracks_similar.keys()
    track_songs = df.loc[indices_of_songs_tracks]
    list_of_songs_to_choose_from = pd.concat([singer_songs, genre_songs, track_songs], ignore_index=True, axis=0)
    moods = list(mood.keys())
    how_you_feel = list(mood.values())
    dance_songs = operation(list_of_songs_to_choose_from, moods[0], how_you_feel[0], 0.5)
    focus_songs = operation(dance_songs, moods[1], how_you_feel[1], 0.5)
    recommendations = operation(focus_songs, moods[2], how_you_feel[2], 50)
    # recommendations = pd.concat([dance_songs, focus_songs, popular_songs], ignore_index=True, axis=0)
    if recommendations.shape[0] > 20:
        recommendations = recommendations.sample(20)
    print(recommendations)

# paste name and some details of each on terminal 1 at a time - use Track class to save details

# ask for another one

# paste them into google sheet

# open the link in separate tab

# ask to play again
def main():
    singer, their_song_indices_in_db = Artist().favourite_artist_songs()
    genre = Genre().favourite_genre()
    if genre != 'hip-hop':
        genre = string.capwords(genre)
    else:
        genre = 'Hip-Hop'
    track, similar_tracks = Track().favourite_track()
    mood = Mood().song_style_questions()
    songs = make_song_recommendations(singer, their_song_indices_in_db, genre, track, similar_tracks, mood)

main()