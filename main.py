import os
import requests
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

nltk_data_path = '/Users/mitul/Desktop/Mime/nltk_data'

if nltk_data_path not in nltk.data.path:
    nltk.data.path.append(nltk_data_path)

def get_book_description(title):
    url = f'https://openlibrary.org/search.json?title={title}'
    response = requests.get(url)
    data = response.json()
    if 'docs' in data and data['docs']:
        return data['docs'][0].get('first_sentence', {}).get('value', 'No description available')
    return 'No description available'

def identify_keywords(text):
    stop_words_set = set(stopwords.words('english'))
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t.isalnum()]
    filtered_tokens = [t for t in tokens if t not in stop_words_set]
    word_count = Counter(filtered_tokens)
    return word_count.most_common(10)

CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

spotify_client = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                           client_secret=CLIENT_SECRET,
                                                           redirect_uri=REDIRECT_URI,
                                                           scope="user-read-playback-state,user-modify-playback-state"))

def find_song(query):
    results = spotify_client.search(q=query, limit=1, type='track')
    tracks = results['tracks']['items']
    if tracks:
        return tracks[0]['uri']
    return None

def start_song(uri):
    spotify_client.start_playback(uris=[uri])

book_title = input("Enter the title of the book: ")
description = get_book_description(book_title)
print(f'Book Description: {description}')

keywords = identify_keywords(description)
print(f'Extracted keywords: {keywords}')

for keyword, _ in keywords:
    song_uri = find_song(keyword)
    if song_uri:
        print(f'Playing song for keyword: {keyword}')
        start_song(song_uri)
        break


