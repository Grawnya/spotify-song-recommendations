import gspread
import readline
from tracks import *
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
    music_artists = format_list_values(spotify_df['artist_name'].to_list())
    genres = format_list_values(spotify_df['genre'].to_list())
    tracks = format_list_values(spotify_df['track_name'].to_list())
    return spotify_df, music_artists, genres, tracks


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
    unique_music_artists = list(set(music_artists))
    music_artist = favourite(unique_music_artists)
    return music_artist
    

def favourite_genre(genres):
    '''docstring'''
    print('\nNext up is pick your favourite genre. '
          'Pick from one of the following:\n')
    unique_genres = list(set(genres))
    list_of_genres = ', '.join(str(genre) for genre in unique_genres)
    print(list_of_genres + '\n\n')
    genre = favourite(unique_genres)
    return genre


def favourite_track(list_of_all_artists, tracks):
    '''docstring'''
    print('\nNext step is to search for your favourite song!\n'
          'Firstly enter the artist who sings your favourite '
          'song and then we\'ll show you all their songs in '
          'our database. Pick your favourite song or you can '
          'pick another artist if you don\'t like the choice\n'
          'Choose an artist\' discography you want to see:)
    unique_music_artists = list(set(list_of_all_artists))
    artist_who_sings = favourite(unique_music_artists)
    picked_track = Track(artist_who_sings, tracks)
    


# ask mood questions - check if valid y or n

# pick all songs from their favourite artist and all songs that are from that genre and meet the mood criteria

# randomly select up to 20 to be returned

# paste name and some details of each on terminal 1 at a time - use Track class to save details

# ask for another one

# paste them into google sheet

# open the link in separate tab

# ask to play again
def main():
    spotify, music_artists, genres, tracks = get_spotify_data()
    singer = favourite_artist(music_artists)
    genre = favourite_genre(genres)

main()