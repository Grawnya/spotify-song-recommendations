import gspread
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
          'Choose an artist\' discography you want to see:')
    unique_music_artists = list(set(list_of_all_artists))
    artist_who_sings = favourite(unique_music_artists)
    picked_track = Spotify(artist_who_sings, tracks)
    


# ask mood questions - check if valid y or n

# pick all songs from their favourite artist and all songs that are from that genre and meet the mood criteria

# randomly select up to 20 to be returned

# paste name and some details of each on terminal 1 at a time - use Track class to save details

# ask for another one

# paste them into google sheet

# open the link in separate tab

# ask to play again
def main():
    singer = Artist().favourite_artist_exists()
    print(singer)

main()