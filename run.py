import gspread
import pandas as pd
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

def get_spotify_data():
    '''
    get list of music artists and genres from database and
    also return the database
    '''
    spotify_df = pd.read_csv('SpotifyFeatures.csv')
    music_artists = spotify_df['artist_name'].unique()
    music_artists = [each.lower() for each in music_artists]
    genres = spotify_df['genre'].unique()
    return spotify_df, music_artists, genres


def favourite_artist(database):
    '''docstring'''
    print('Welcome to the Spotify Song Recommender!\n'
          'We\'ll help you picksome songs that will '
          'become your new favourites!\n\n'
          'Firstly we need to ask you some questions!'
          '1. Who is your favourite music artist?\n')
# ask questions re favourite song, genre, song of all time 
# (for song ask for artist first and then print all of their songs on console)

# ask mood questions - check if valid y or n

# pick all songs from their favourite artist and all songs that are from that genre and meet the mood criteria

# randomly select up to 20 to be returned

# paste name and some details of each on terminal 1 at a time - use Track class to save details

# ask for another one

# paste them into google sheet

# open the link in separate tab

# ask to play again
def main():
    spotify, music_artists, genres = get_spotify_data()

main()