import gspread
import readline
import operator
import pandas as pd
from spotify import *
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPE_CREDENTIALS = CREDS.with_scopes(SCOPE)
GSPREAD_AUTHORIZATION = gspread.authorize(SCOPE_CREDENTIALS)
SHEET = GSPREAD_AUTHORIZATION.open('song_recs')


def operation(df, mood_keyword, operator_value, equal):
    '''
    Selects all rows in a dataframe where values in column mood_keyword
    are less than or greater than the equal value e.g. df['danceability'] < 0.5
    where the user doesn't want to dance, so low danceable songs selected.

    Parameters:
    df (dataframe): A Pandas dataframe type - similar to a database
    mood_keyword (str): df column name that matches a mood
    operator_value (str): Type of operator as a string - either "<" or ">"
    equal (int): median possible value of the mood type -
                 0.5 for danceability, instrumentalness and 50 for popular

    Returns:
    mood_dataframe (dataframe): Dataframe with mood criteria met
    '''
    if operator_value == ">":
        mood_dataframe = df[operator.gt(df[mood_keyword], equal)]
    elif operator_value == "<":
        mood_dataframe = df[operator.lt(df[mood_keyword], equal)]
    return mood_dataframe


def make_song_recommendations(favourite_singer, singer_song_indices,
                              favourite_genre, favourite_track,
                              tracks_similar, mood):
    '''
    Outputs a dataframe of 20 songs based on inputted singer, genre,
    track and mood values.

    Parameters:
    favourite_singer (str): Inputted favourite singer value
    singer_song_indices (list): List of indices of all songs the favourite
                                singer has sang from spotify dataset
    favourite_genre (str): Inputted favourite genre value
    favourite_track (str): Inputted favourite track value
    tracks_similar (list): List of all tracks similar to the favourite
                            track from spotify dataset
    mood (dict): Dictionary where keys are the mood value column name and
                 the values are the operator based on how they feel

    Returns:
    recommendations (dataframe): Dataframe of up to 20 recommended songs
    '''
    df = Spotify().get_spotify_data()
    # get all from singer
    singer_songs = df.loc[singer_song_indices]
    # get all from genre
    genre_songs = df.loc[df['genre'] == favourite_genre]
    # get all from similar track
    indices_of_songs_tracks = tracks_similar.keys()
    track_songs = df.loc[indices_of_songs_tracks]
    list_of_songs_to_choose_from = pd.concat([singer_songs,
                                              genre_songs,
                                              track_songs],
                                             ignore_index=True, axis=0)
    moods = list(mood.keys())
    how_you_feel = list(mood.values())
    dance_songs = operation(list_of_songs_to_choose_from, moods[0],
                            how_you_feel[0], 0.5)
    dance_and_focus_songs = operation(dance_songs, moods[1],
                                      how_you_feel[1], 0.5)
    recommendations = operation(dance_and_focus_songs, moods[2],
                                how_you_feel[2], 50)
    if recommendations.shape[0] == 0:
        recommendations = list_of_songs_to_choose_from
    if recommendations.shape[0] > 20:
        recommendations = recommendations.sample(20)
    recommendations = recommendations.reset_index()
    return recommendations


def print_values(recommendations_df, play_again):
    '''
    Prints the songs one by one on the terminal.

    Parameters:
    recommendations_df (dataframe): Up to 20 recommended songs dataframe
    play_again (bool): Original Value if user wants to play again.
                       Default is True

    Returns:
    play_again (bool): Newly inputted value if user wants to play again
    '''
    print('\nHere is the first recommendation:\n')
    for index, row in recommendations_df.iterrows():
        print(f'Song Name: {row.track_name}')
        print(f'Artist Name: {row.artist_name}')
        minutes = row.duration_ms // 60000
        seconds = round((row.duration_ms % 60000)/1000)
        print(f'Song Duration: {minutes} minutes and {seconds} seconds\n')
        if index != recommendations_df.shape[0] - 1:
            ask = input('Another one?...That is song recommendation: y or n\n')
            another_one = Spotify()._closed_question_answer_checks(ask)
            if another_one == 'y':
                print('\n')
            else:
                break
    playing_again = input('\nThanks for playing! Do you want to play again: '
                          'y or n\n')
    play_again_check = Spotify()._closed_question_answer_checks(playing_again)
    if play_again_check == 'n':
        play_again = False
    return play_again


def add_to_worksheet(recommendations_df):
    '''
    Adds recommended songs dataframe to a list that the user can access.

    Parameters:
    recommendations_df (dataframe): Up to 20 recommended songs dataframe
    '''
    song_worksheet = SHEET.worksheet('Songs')
    song_worksheet.clear()
    song_worksheet.update([recommendations_df.columns.values.tolist()] +
                          recommendations_df.values.tolist())
    print('\nHere is a list of all the recommended songs:')
    print('To select the link below, do not click on it, but highlight '
          'it and right click, then select "copy" and then paste the link'
          ' into a new tab')
    link_to_google_sheet = r'https://docs.google.com/spreadsheets/d/19APnfM8o7hUttAOnIaQ-mHoGC5tH-BnegAzFkqZ6FLk/edit?usp=sharing'  # noqa
    print(link_to_google_sheet)


def main():
    play_again = True
    while play_again:
        singer, their_song_indices_in_db = Artist().favourite_artist_songs()
        genre = Genre().favourite_genre()
        track, similar_tracks = Track().favourite_track()
        mood = Mood().song_style_questions()
        songs = make_song_recommendations(singer, their_song_indices_in_db,
                                          genre, track, similar_tracks, mood)
        play_again = print_values(songs, play_again)
    add_to_worksheet(songs)
    print('\nThanks for playing! If you have any suggestions '
          'please send them to https://www.linkedin.com/in/grainne-donegan/')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n\n*****\nYou interrupted the game, lets play again\n*****\n')
        main()
