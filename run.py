import gspread
import readline
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


def format_list_values(list_of_values):
    '''docstring'''
    lower_list = [each.lower() for each in list_of_values]
    replace_and = [each.replace('&', 'and') for each in lower_list]
    replace_apostrophe = [each.replace("'", '') for each in replace_and]
    replace_full_stop = [each.replace('.', '') for each in replace_apostrophe]
    replace_e = [each.replace('é', 'e') for each in replace_full_stop]
    return replace_e

def get_spotify_data():
    '''
    get list of music artists and genres from database and
    also return the database
    '''
    spotify_df = pd.read_csv('SpotifyFeatures.csv')
    music_artists = format_list_values(spotify_df['artist_name'].unique())
    genres = format_list_values(spotify_df['genre'].unique())
    return spotify_df, music_artists, genres


def favourite(list_of_interest):
    '''docstring'''
    value_of_interest = format_list_values([input('\n')])
    while value_of_interest[0] not in list_of_interest \
            and value_of_interest[0] != '':
        value_of_interest = format_list_values([input('Invalid value. Enter'
                                                 ' a new value:\n')])
    return (value_of_interest[0])


def favourite_artist(music_artists):
    '''docstring'''
    print('Welcome to the Spotify Song Recommender!\n'
          'We\'ll help you picksome songs that will '
          'become your new favourites!\n\n'
          'Firstly we need to ask you some questions!'
          '\n1. Who is your favourite music artist?\n'
          'Examples include Cardi B, The 1975 and '
           'Beyonce:\n')
    music_artist = favourite(music_artists)
    return music_artist
    
def favourite_genre(genres):
    '''docstring'''
    print('\nNext up is pick your favourite genre. '
          'Pick from one of the following:\n')
    list_of_genres = ', '.join(str(genre) for genre in genres)
    print(list_of_genres + '\n\n')
    genre = favourite(genres)
    return genre
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
    singer = favourite_artist(music_artists)
    genre = favourite_genre(genres)

main()