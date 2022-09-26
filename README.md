# Spotify Song Recommendations

# Introduction

# Aim of the Application
Welcome to a website dedicated to providing song recommendations for the user using a dataset consisting of Spotify song data. The aim is to provide the user with up to 20 song suggestions based on answers given to the questions asked and then to print them onto a Google Sheet so they can access the song details independently from the Terminal interface.

[Visit the Website Here](https://spotify-db-recommendations.herokuapp.com/)

[Visit the Project's GitHub Repository Here]( https://github.com/Grawnya/spotify-song-recommendations)

![Responsive Display](documentation/responsive_screens.png)


# How to Use
The user can interact with the application by going into the website and answering the questions on the screen. The user will be asked for:
* Their favourite music artist
* Their favourite genre from a list provided
* The music artist who sings their favourite track or song
* The title of their favourite track
* If they feel like dancing?
* If they want to focus?
* If they want to listen to something popular?

These questions will enable the programme to pick up to 20 songs, returning them one by one in the form of:

Song Name
Artist Name
Duration

The user will be asked to play again, restarting the game if they opt to play again. Otherwise, if they don’t want to play again, a link to the most recent recommendations on a Google Sheet is printed out onto the terminal.

# Table of Contents

* [UX](#ux "UX")
    * [User Goals](#user-goals "User Goals")
    * [User Stories](#user-stories "User Stories")
    * [User Requirements and Expectations](#user-requirements-and-expectations)
         * [Requirements](#requirements)
         * [Expectations](#expectations)
* [Initial Planning](#initial-planning "Initial Planning")
* [Features](#features "Features")
    * [Existing Features](#existing-features "Existing Features")
         * [Start Application Screen]#start-application-screen "Start Application Screen")


# UX

## User Goals
* Provide song recommendations based on existing taste
* Questions asked to grasp an accurate sense of mood and taste
* Logical flow to the game so no confusion about what to do next at any point
* Answer questions with minimal errors i.e. constant invalid artist names or misspelling.
* Ability to review recommendations when the game is finished so the user can log them elsewhere or put them into their own Spotify playlists.

## User Stories
* As a user, I want to get song recommendations from the application based on songs and artists I like.
* As a user, I want to answer questions that will accurately predict songs that I will like.
* As a user, I want to easily use the application and not get confused at any stage of what to do next.
* As a user, I don’t want to constantly input answers to the questions if they are invalid, as the application might be too difficult to use and I could become bored with it.
* As a user, when the game is finished, I want to see my song recommendations in one place so I can add them to an existing playlist or create a new one.

## User Requirements and Expectations
### Requirements
* Easy to navigate or use the application, to prevent confusion.
* Present introductory sentences in basic English to make the application more accessible.
* Let the user know if the artist, genre or track value entered into the terminal exists in the dataset.
* Entice the user to play again due to the excitement associated with getting new track recommendations.

### Expectations
* I expect the application to flow nicely with a clear, logical progression of the application.
* I expect the website to be completely responsive to all inputs, whether they are values in the dataset or answers to closed yes or no questions.
* I anticipate that the user might want to play again and will build that functionality into the application.


\
&nbsp;
[Back to Top](#table-of-contents)
\
&nbsp;

# Initial Planning
In order to efficiently start creating the application, a basic flow diagram was created. It was used to dictate the flow of the application and to build the functionality as quickly as possible into the programme:


![Starting Flow Chart](documentation/basic_song_recommendation_chart.png "Starting Flow Chart")

As the application began to take a shape, a more in-depth flow chart was created and can be found via the link below:

### [Final Flow Chart](documentation/song-recommendations.pdf "Final Flow Chart")



\
&nbsp;
[Back to Top](#table-of-contents)
\
&nbsp;

# Features

## Existing Features
### Start Application Screen
The application starts by welcoming the user and letting them know that there is an extensive database of songs that the programme can select from, which will effectively make suggested recommendations. It tells the user that in order to make recommendations, they must answer some questions.

The first questions asks the user to enter the name of their favourite artist, while providing some examples to get them started, as seen below.

![Start Application Screen](documentation/start_app_screen.png)
\
&nbsp;
