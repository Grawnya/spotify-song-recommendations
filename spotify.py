import string
import operator
import regex
import pandas as pd


class Spotify:
    '''docstring'''
    def __init__(self):
        self.spotify_db = self.get_spotify_data()
        self.artists_to_format = self.spotify_db['artist_name'].to_list()
        self.music_artists = self._format_list_values(self.artists_to_format)
        self.genres_to_format = self.spotify_db['genre'].to_list()
        self.genres = self._format_list_values(self.genres_to_format)
        self.tracks_to_format = self.spotify_db['track_name'].to_list()
        self.tracks = self._format_list_values(self.tracks_to_format)

    def get_spotify_data(self):
        '''
        get list of music artists and genres from database and
        also return the database
        '''
        spotify_df = pd.read_csv('SpotifyFeatures.csv')
        spotify_df = spotify_df.drop(columns=['valence', 'time_signature',
                                              'speechiness', 'mode',
                                              'loudness', 'liveness', 'key',
                                              'energy', 'acousticness',
                                              'track_id'])
        return spotify_df

    def _format_list_values(self, list_of_values):
        '''docstring'''
        lower_list = [each.lower() for each in list_of_values]
        replace_and = [each.replace('&', 'and') for each in lower_list]
        replace_apost = [each.replace("'", '') for each in replace_and]
        replace_full_stop = [each.replace('.', '') for each in replace_apost]
        replace_e = [each.replace('é', 'e') for each in replace_full_stop]
        replace_whitespace = [each.strip(' ') for each in replace_e]
        return replace_whitespace

    def _favourite(self, list_of_interest):
        '''docstring'''
        value_of_interest = self._format_list_values([input('\n')])
        while value_of_interest[0] not in list_of_interest \
                or value_of_interest[0] == '':
            value_interest = self._format_list_values([input('Invalid value.'
                                                             ' Enter a new '
                                                             'value:\n')])
        return (value_interest[0])

    def _closed_question_answer_checks(self, y_or_n):
        '''
        Checks if the user inputs a valid y (yes) or n (no) value
        into the terminal
        '''
        remove_whitespace = y_or_n.replace(' ', '')
        while remove_whitespace.isalpha() is False or \
                remove_whitespace.lower() not in ['y', 'yes', 'n', 'no']:
            remove_whitespace = input('\nAnswer not valid. Please enter'
                                      ' y or n:\n')
            remove_whitespace.replace(' ', '')
        if remove_whitespace.lower() == 'yes':
            remove_whitespace = 'y'
        elif remove_whitespace.lower() == 'no':
            remove_whitespace = 'n'
        return remove_whitespace.lower()


class Artist(Spotify):

    def _favourite_artist_exists(self):
        print('\nWelcome to the Spotify Song Recommender!\n'
              'We\'ll help you pick some songs that will '
              'become your new favourites from our database'
              ' of over 200,000 songs!\n\n'
              'Firstly we need to ask you some questions!'
              '\n1. Who is your favourite music artist?\n'
              'Examples include Cardi B, The 1975 and '
              'Beyonce:')
        unique_music_artists = list(set(self.music_artists))
        music_artist = self._favourite(unique_music_artists)
        return music_artist

    def favourite_artist_songs(self):
        '''docstring'''
        music_artist = self._favourite_artist_exists()
        indices_of_songs = []
        for count, value in enumerate(self.music_artists):
            if value == music_artist:
                indices_of_songs.append(count)
        print(indices_of_songs)
        return music_artist, indices_of_songs


class Genre(Spotify):
    '''docstring'''
    def favourite_genre(self):
        '''docstring'''
        print('\nNext up is pick your favourite genre. '
              'Pick from one of the following:\n')
        unique_genres = list(set(self.genres))
        list_of_genres = ', '.join(str(genre) for genre in unique_genres)
        print(list_of_genres + '\n\n')
        genre = self._favourite(unique_genres)
        if genre != 'hip-hop':
            genre = string.capwords(genre)
        else:
            genre = 'Hip-Hop'
        return genre


class Track(Spotify):
    '''docstring'''
    def _song_position(self, artist):
        '''docstring'''
        artists_track_indices = []
        i = 0
        for each in self.music_artists:
            if each == artist:
                artists_track_indices.append(i)
            i += 1
        return artists_track_indices

    def _remove_feature(self, song):
        '''docstring'''
        if '(feat' in song:
            song = song.split('(feat')[0]
        elif 'feat' in song:
            song = song.split('feat')[0]
        if ' (' in song:
            song = song.split(' (')[0]
        if ' -' in song:
            song = song.split(' -')[0]
        song.replace('?', '')
        song = song.strip(' ')
        return song

    def _tracks(self, artist):
        '''docstring'''
        appears_in_db = self._song_position(artist)
        print(f'\n{artist} has {len(appears_in_db)} songs in our database')
        track_names = {}
        for index, song_title in enumerate(self.tracks):
            if index in appears_in_db:
                adjusted_song_title = self._remove_feature(song_title)
                track_names[index] = adjusted_song_title
        return track_names

    def favourite_track(self):
        '''docstring'''
        print('\nNext step is to search for your favourite song!\n'
              'Firstly enter the artist who sings your favourite '
              'song and then we\'ll show you all their songs in '
              'our database. Pick your favourite song or you can '
              'pick another artist if you don\'t like the choice\n'
              'Choose an artist\' discography you want to see:')
        unique_music_artists = list(set(self.music_artists))
        singer = self._favourite(unique_music_artists)
        list_of_tracks_not_unique = self._tracks(singer)
        list_of_tracks = list(set(list_of_tracks_not_unique.values()))
        if len(list_of_tracks) < 11:
            print(f'\nThe following tracks exist from {singer}\n')
            tracks_to_print = ', '.join(str(each) for each in list_of_tracks)
            print(tracks_to_print + '\n\n')
            print('\nType in one of the above songs: '
                  '(Make sure it is spelt correctly)')
        else:
            print('\nThe track list is too long to print.\nGuess a song to see'
                  ' if it is in the list: (Make sure it is spelt correctly)')
        track = self._favourite(list_of_tracks)
        return track, list_of_tracks_not_unique


class Mood(Spotify):
    '''docstring'''
    def _mood_for(self, question, parameter, mood_values_dict):
        '''
        Asks the user about their mood and set it to
        a value comparison
        '''
        task_asked_about = self._closed_question_answer_checks(question)
        if task_asked_about == 'y':
            task_asked_about = '>'
        elif task_asked_about == 'n':
            task_asked_about = '<'
        mood_values_dict[parameter] = task_asked_about
        return mood_values_dict

    def song_style_questions(self):
        '''
        Asks the user if they want to dance,
        focus and listen to something popular
        '''
        print('\n\nWe just need to ask a few more questions to pick out'
              '\nthe perfect songs for you!\n'
              'These ones are more mood based\n\n*******\n\n')
        mood_values = {}
        dancing = self._mood_for(input('1. Do you feel like dancing at the '
                                       'moment? y or n\n'),
                                 'danceability', mood_values)
        focus = self._mood_for(input('\n2. Do you want to focus at the '
                                     'moment? y or n\n'),
                               'instrumentalness', mood_values)
        popular = self._mood_for(input('\n3. Do you want to listen to '
                                       'something popular? y or n\n'),
                                 'popularity', mood_values)
        return mood_values
