import gspread
import readline
import pandas as pd
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


def make_song_recommendations(favourite_singer, singer_song_indices,
                              favourite_genre, favourite_track,
                              tracks_similar, mood):
    '''docstring'''
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
    return recommendations.reset_index()


def print_values(recommendations_df, play_again):
    '''docstring'''
    print('Here is the first recommendation:\n')
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
    playing_again = input('Thanks for playing! Do you want to play again: '
                          'y or n\n')
    play_again_check = Spotify()._closed_question_answer_checks(playing_again)
    if play_again_check == 'n':
        play_again = False
    return play_again


def add_to_worksheet(recommendations_df):
    '''docstrings'''
    song_worksheet = SHEET.worksheet('Songs')
    song_worksheet.clear()
    song_worksheet.update([recommendations_df.columns.values.tolist()] +
                          recommendations_df.values.tolist())
    print('\nHere is a list of all the recommended songs:\n')
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
