import streamlit as st
import pandas as pd
import pickle
import requests
import time

movie_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies_df = pd.DataFrame(movie_dict)
movie_list = movies_df["title"]

similar_score = pickle.load(open("similar_score.pkl", "rb"))

poster_dict = pickle.load(open("poster.pkl", "rb"))
poster_df = pd.DataFrame(poster_dict)

def recommended(movie):
    movie_index = movies_df[movies_df.title == movie].index[0]
    distance_of_the_selected_movie = similar_score[movie_index]
    movie_list = sorted(list(enumerate(distance_of_the_selected_movie)), reverse=True, key=lambda x: x[1])[1:6]


    movie_id = []
    title = []
    for i in movie_list:
        movie_id.append(movies_df.iloc[i[0]].id)
        title.append(movies_df.iloc[i[0]].title)

    return movie_id, title

def fetch_path(id):
    list_of_urls = []
    for i in id:
        try:
            api = f"https://api.themoviedb.org/3/movie/{i}?api_key=fa3dea095ba8fc716dd8810c92199b1e&language=en-US"
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json",
                "Connection": "close"
            }
            response = requests.get(api, headers=headers, timeout=10)
            data = response.json()
            url = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
            list_of_urls.append(url)
            time.sleep(1)

        except requests.exceptions.Timeout:
            #st.warning("The request timed out")
            time.sleep(1)
        except requests.exceptions.ConnectionError as e:
            #st.warning(f"Connection error occurred: {e}")
            time.sleep(2)
    return list_of_urls



st.title("Movie Recommender")
selected = st.selectbox("Pick One Movie form this list which you liked :",movie_list)

recc = st.button("Recommend", key= "recc")

if recc:
    id, title = recommended(selected)
    paths = fetch_path(id)
    
    try:
        for i in range(len(title)):
            st.image(paths[i], caption=title[i])
    except IndexError:
        st.warning("There is some error in fetching Posters, titles may be differ")
        st.header("Here is some recommended titles below")
        st.write(title)
    
