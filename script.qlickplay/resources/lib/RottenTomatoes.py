# -*- coding: utf8 -*-

# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details

from Utils import *
from Trakt import get_movie_images
from local_db import merge_with_local_movie_info

RT_KEY = '63sbsudx936yedd2wdmt6tkn'
BASE_URL = "http://api.rottentomatoes.com/api/public/v1.0/lists/"


def get_rottentomatoes_movies(movietype):
    movies = []
    url = movietype + '.json?apikey=%s' % (RT_KEY)
    results = get_JSON_response(BASE_URL + url, folder="RottenTomatoes")
    if not results or "movies" not in results:
        return []
    for item in results["movies"]:
        thumb = ""
        poster = ""
        fanart = ""
        if "alternate_ids" in item:
            imdb_id = "tt"+str(item["alternate_ids"]["imdb"])
            try:
                trakt = get_movie_images(imdb_id)
                if trakt["images"]["fanart"]["full"] != "" or trakt["images"]["fanart"]["full"] != None: fanart = trakt["images"]["fanart"]["full"]
                elif trakt["images"]["fanart"]["medium"] != "" or trakt["images"]["fanart"]["medium"] != None: fanart = trakt["images"]["fanart"]["medium"]
                elif trakt["images"]["fanart"]["thumb"] != "" or trakt["images"]["fanart"]["thumb"] != None: fanart = trakt["images"]["fanart"]["thumb"]
                else: fanart = ""
                if trakt["images"]["poster"]["full"] != "" or trakt["images"]["poster"]["full"] != None: poster = trakt["images"]["poster"]["full"]
                elif trakt["images"]["poster"]["full"] != "" or trakt["images"]["poster"]["full"] != None: poster = trakt["images"]["poster"]["medium"]
                elif trakt["images"]["poster"]["full"] != "" or trakt["images"]["poster"]["full"] != None: poster = trakt["images"]["poster"]["thumb"]
                else: poster = item["posters"]["original"]
                if trakt["images"]["poster"]["thumb"] != "" or trakt["images"]["poster"]["thumb"] != None: thumb = trakt["images"]["poster"]["thumb"]
                else: thumb = item["posters"]["original"]
            except: pass
        else:
            imdb_id = ""
            poster = item["posters"]["original"]
            thumb = poster
            fanart = ""
        if imdb_id != "":
            path = 'plugin://script.qlickplay/?info=pathplay&type=movie&db=imdb&id=%s' % imdb_id
            trailer = 'plugin://script.qlickplay/?info=playtrailer&imdb_id=%s' % imdb_id
        else:
            path = 'plugin://script.qlickplay/?info=pathplay&type=movie&db=name&id=%s' % item["title"]
            trailer = 'plugin://script.qlickplay/?info=playtrailer&name=%s' % item["title"]
        movie = {'title': item["title"],
                 'imdb_id': imdb_id,
                 'thumb': thumb,
                 'poster': poster,
                 'fanart': fanart,
                 'Runtime': item["runtime"] * 60,
                 'duration': item["runtime"] * 60,
                 'duration(h)': format_time(item["runtime"], "h"),
                 'duration(m)': format_time(item["runtime"], "m"),
                 'Trailer': trailer,
                 'year': item["year"],
                 'path': path,
                 'Premiered': item["release_dates"].get("theater", ""),
                 'mpaa': item["mpaa_rating"],
                 'Rating': item["ratings"]["audience_score"] / 10.0,
                 'Plot': item["synopsis"]}
        if imdb_id != "":
            movies.append(movie)
    return merge_with_local_movie_info(movies, False)
