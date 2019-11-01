# -*- coding: utf8 -*-

# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details

from LastFM import *
from TheAudioDB import *
from TheMovieDB import *
from Utils import *
from local_db import *
from YouTube import *
from Trakt import *
from WindowManager import wm
import VideoPlayer
PLAYER = VideoPlayer.VideoPlayer()


def start_info_actions(infos, params):
	if "artistname" in params:
		params["artistname"] = params.get("artistname", "").split(" feat. ")[0].strip()
		params["artist_mbid"] = fetch_musicbrainz_id(params["artistname"])
	prettyprint(params)
	prettyprint(infos)
	if "prefix" in params and (not params["prefix"].endswith('.')) and (params["prefix"] is not ""):
		params["prefix"] = params["prefix"] + '.'
	# NOTICE: compatibility
	if "imdbid" in params and "imdb_id" not in params:
		params["imdb_id"] = params["imdbid"]
	for info in infos:
		data = [], ""
		#  Images
		if info == 'xkcd':
			from MiscScraper import get_xkcd_images
			data = get_xkcd_images(), "XKCD"
		elif info == 'cyanide':
			from MiscScraper import get_cyanide_images
			data = get_cyanide_images(), "CyanideHappiness"
		elif info == 'dailybabes':
			from MiscScraper import get_babe_images
			data = get_babe_images(), "DailyBabes"
		elif info == 'dailybabe':
			from MiscScraper import get_babe_images
			data = get_babe_images(single=True), "DailyBabe"
		# Audio
		elif info == 'discography':
			discography = get_artist_discography(params["artistname"])
			if not discography:
				discography = get_artist_albums(params.get("artist_mbid"))
			data = discography, "discography"
		elif info == 'mostlovedtracks':
			data = get_most_loved_tracks(params["artistname"]), "MostLovedTracks"
		elif info == 'musicvideos':
			pass
			# if "audiodbid" in artist_details:
			#	 data = get_musicvideos(artist_details["audiodbid"]), "MusicVideos"
		elif info == 'trackdetails':
			if params.get("id", ""):
				data = get_track_details(params.get("id", "")), "Trackinfo"
		elif info == 'albumshouts':
			if params["artistname"] and params["albumname"]:
				data = get_album_shouts(params["artistname"], params["albumname"]), "Shout"
		elif info == 'artistshouts':
			if params["artistname"]:
				data = get_artist_shouts(params["artistname"]), "Shout"
		elif info == 'topartists':
			data = get_top_artists(), "TopArtists"
		elif info == 'hypedartists':
			data = get_hyped_artists(), "HypedArtists"
		elif info == 'latestdbmovies':
			data = get_db_movies('"sort": {"order": "descending", "method": "dateadded"}', params.get("limit", 10)), "LatestMovies"
		elif info == 'randomdbmovies':
			data = get_db_movies('"sort": {"method": "random"}', params.get("limit", 10)), "RandomMovies"
		elif info == 'inprogressdbmovies':
			method = '"sort": {"order": "descending", "method": "lastplayed"}, "filter": {"field": "inprogress", "operator": "true", "value": ""}'
			data = get_db_movies(method, params.get("limit", 10)), "RecommendedMovies"
	#  RottenTomatoesMovies
		elif info == 'intheaters':
			from RottenTomatoes import get_rottentomatoes_movies
			data = get_rottentomatoes_movies("movies/in_theaters"), "InTheatersMovies"
		elif info == 'boxoffice':
			from RottenTomatoes import get_rottentomatoes_movies
			data = get_rottentomatoes_movies("movies/box_office"), "BoxOffice"
		elif info == 'opening':
			from RottenTomatoes import get_rottentomatoes_movies
			data = get_rottentomatoes_movies("movies/opening"), "Opening"
		elif info == 'comingsoon':
			from RottenTomatoes import get_rottentomatoes_movies
			data = get_rottentomatoes_movies("movies/upcoming"), "ComingSoonMovies"
		elif info == 'toprentals':
			from RottenTomatoes import get_rottentomatoes_movies
			data = get_rottentomatoes_movies("dvds/top_rentals"), "TopRentals"
		elif info == 'currentdvdreleases':
			from RottenTomatoes import get_rottentomatoes_movies
			data = get_rottentomatoes_movies("dvds/current_releases"), "CurrentDVDs"
		elif info == 'newdvdreleases':
			from RottenTomatoes import get_rottentomatoes_movies
			data = get_rottentomatoes_movies("dvds/new_releases"), "NewDVDs"
		elif info == 'upcomingdvds':
			from RottenTomatoes import get_rottentomatoes_movies
			data = get_rottentomatoes_movies("dvds/upcoming"), "UpcomingDVDs"
		#  The MovieDB
		elif info == 'incinemas':
			data = get_tmdb_movies("now_playing"), "InCinemasMovies"
		elif info == 'upcoming':
			data = get_tmdb_movies("upcoming"), "UpcomingMovies"
		elif info == 'topratedmovies':
			data = get_tmdb_movies("top_rated"), "TopRatedMovies"
		elif info == 'popularmovies':
			data = get_tmdb_movies("popular"), "PopularMovies"
		elif info == 'ratedmovies':
			data = get_rated_media_items("movies"), "RatedMovies"
		elif info == 'starredmovies':
			data = get_fav_items("movies"), "StarredMovies"
		elif info == 'accountlists':
			account_lists = handle_tmdb_misc(get_account_lists())
			for item in account_lists:
				item["directory"] = True
			data = account_lists, "AccountLists"
		elif info == 'listmovies':
			movies = get_movies_from_list(params["id"])
			data = movies, "AccountLists"
		elif info == 'airingtodaytvshows':
			data = get_tmdb_shows("airing_today"), "AiringTodayTVShows"
		elif info == 'onairtvshows':
			data = get_tmdb_shows("on_the_air"), "OnAirTVShows"
		elif info == 'topratedtvshows':
			data = get_tmdb_shows("top_rated"), "TopRatedTVShows"
		elif info == 'populartvshows':
			data = get_tmdb_shows("popular"), "PopularTVShows"
		elif info == 'ratedtvshows':
			data = get_rated_media_items("tv"), "RatedTVShows"
		elif info == 'starredtvshows':
			data = get_fav_items("tv"), "StarredTVShows"
		elif info == 'similarmovies':
			movie_id = params.get("id", False)
			if not movie_id:
				movie_id = get_movie_tmdb_id(imdb_id=params.get("imdb_id", False),
											 dbid=params.get("dbid", False))
			if movie_id:
				data = get_similar_movies(movie_id), "SimilarMovies"
		elif info == 'similartvshows':
			tvshow_id = None
			dbid = params.get("dbid", False)
			name = params.get("name", False)
			tmdb_id = params.get("tmdb_id", False)
			tvdb_id = params.get("tvdb_id", False)
			imdb_id = params.get("imdb_id", False)
			if tmdb_id:
				tvshow_id = tmdb_id
			elif dbid and int(dbid) > 0:
				tvdb_id = get_imdb_id_from_db("tvshow", dbid)
				if tvdb_id:
					tvshow_id = get_show_tmdb_id(tvdb_id)
			elif tvdb_id:
				tvshow_id = get_show_tmdb_id(tvdb_id)
			elif imdb_id:
				tvshow_id = get_show_tmdb_id(imdb_id)
			elif name:
				tvshow_id = search_media(name, "", "tv")
			if tvshow_id:
				data = get_similar_tvshows(tvshow_id), "SimilarTVShows"
		elif info == 'studio':
			if "id" in params and params["id"]:
				data = get_company_data(params["id"]), "StudioInfo"
			elif "studio" in params and params["studio"]:
				company_data = search_company(params["studio"])
				if company_data:
					data = get_company_data(company_data[0]["id"]), "StudioInfo"
		elif info == 'set':
			if params.get("dbid") and "show" not in str(params.get("type", "")):
				name = get_set_name_from_db(params["dbid"])
				if name:
					params["setid"] = get_set_id(name)
			if params.get("setid"):
				set_data, _ = get_set_movies(params["setid"])
				if set_data:
					data = set_data, "MovieSetItems"
		elif info == 'movielists':
			movie_id = params.get("id", False)
			if not movie_id:
				movie_id = get_movie_tmdb_id(imdb_id=params.get("imdb_id", False),
											 dbid=params.get("dbid", False))
			if movie_id:
				data = get_movie_lists(movie_id), "MovieLists"
		elif info == 'keywords':
			movie_id = params.get("id", False)
			if not movie_id:
				movie_id = get_movie_tmdb_id(imdb_id=params.get("imdb_id", False),
											 dbid=params.get("dbid", False))
			if movie_id:
				data = get_keywords(movie_id), "Keywords"
		elif info == 'popularpeople':
			data = get_popular_actors(), "PopularPeople"
		elif info == 'directormovies':
			if params.get("director"):
				director_info = get_person_info(person_label=params["director"],
												skip_dialog=True)
				if director_info and director_info.get("id"):
					movies = get_person_movies(director_info["id"])
					for item in movies:
						del item["credit_id"]
					data = merge_dict_lists(movies, key="department"), "DirectorMovies"
		elif info == 'writermovies':
			if params.get("writer") and not params["writer"].split(" / ")[0] == params.get("director", "").split(" / ")[0]:
				writer_info = get_person_info(person_label=params["writer"],
											  skip_dialog=True)
				if writer_info and writer_info.get("id"):
					movies = get_person_movies(writer_info["id"])
					for item in movies:
						del item["credit_id"]
					data = merge_dict_lists(movies, key="department"), "WriterMovies"
		elif info == 'similarmoviestrakt':
			if params.get("id", False) or params.get("dbid"):
				if params.get("dbid"):
					movie_id = get_imdb_id_from_db("movie", params["dbid"])
				else:
					movie_id = params.get("id", "")
				data = get_trakt_similar("movie", movie_id), "SimilarMovies"
		elif info == 'similartvshowstrakt':
			if (params.get("id", "") or params["dbid"]):
				if params.get("dbid"):
					if params.get("type") == "episode":
						tvshow_id = get_tvshow_id_from_db_by_episode(params["dbid"])
					else:
						tvshow_id = get_imdb_id_from_db(media_type="tvshow",
														dbid=params["dbid"])
				else:
					tvshow_id = params.get("id", "")
				data = get_trakt_similar("show", tvshow_id), "SimilarTVShows"
		elif info == 'airedyesterday':
			data = get_trakt_calendar_shows("shows"), "AiringShows"
		elif info == 'premieredlastweek':
			data = get_trakt_calendar_shows("premieres"), "PremiereShows"
		elif info == 'trendingshows':
			data = get_trending_shows(), "TrendingShows"
		elif info == 'trendingmovies':
			data = get_trending_movies(), "TrendingMovies"
		elif info == 'similarartistsinlibrary':
			if params.get("artist_mbid"):
				data = get_similar_artists_from_db(params.get("artist_mbid")), "SimilarArtists"
		elif info == 'artistevents':
			if params.get("artist_mbid"):
				data = get_events(params.get("artist_mbid")), "ArtistEvents"
		elif info == 'youtubesearch':
			HOME.setProperty('%sSearchValue' % params.get("prefix", ""), params.get("id", ""))  # set properties
			if params.get("id"):
				listitems = search_youtube(search_str=params.get("id", ""),
										   hd=params.get("hd", ""),
										   orderby=params.get("orderby", "relevance"))
				data = listitems.get("listitems", []), "YoutubeSearch"
		elif info == 'youtubeplaylist':
			if params.get("id"):
				data = get_youtube_playlist_videos(params.get("id", "")), "YoutubePlaylist"
		elif info == 'youtubeusersearch':
			user_name = params.get("id", "")
			if user_name:
				playlists = get_youtube_user_playlists(user_name)
				data = get_youtube_playlist_videos(playlists["uploads"]), "YoutubeUserSearch"
		elif info == 'nearevents':
			eventinfo = get_near_events(tag=params.get("tag", ""),
										festivals_only=params.get("festivalsonly", ""),
										lat=params.get("lat", ""),
										lon=params.get("lon", ""),
										location=params.get("location", ""),
										distance=params.get("distance", ""))
			data = eventinfo, "NearEvents"
		elif info == 'trackinfo':
			HOME.setProperty('%sSummary' % params.get("prefix", ""), "")  # set properties
			if params["artistname"] and params["trackname"]:
				track_info = get_track_info(artist=params["artistname"],
											track=params["trackname"])
				HOME.setProperty('%sSummary' % params.get("prefix", ""), track_info["summary"])  # set properties
		elif info == 'venueevents':
			if params["location"]:
				params["id"] = get_venue_id(params["location"])
			if params.get("id", ""):
				data = get_venue_events(params.get("id", "")), "VenueEvents"
			else:
				notify("Error", "Could not find venue")
		elif info == 'topartistsnearevents':
			artists = get_kodi_artists()
			from MiscScraper import get_artist_near_events
			data = get_artist_near_events(artists["result"]["artists"][0:49]), "TopArtistsNearEvents"
		elif info == 'favourites':
			if params.get("id", ""):
				favs = get_favs_by_type(params.get("id", ""))
			else:
				favs = get_favs()
				HOME.setProperty('favourite.count', str(len(favs)))
				if favs:
					HOME.setProperty('favourite.1.name', favs[-1]["Label"])
			data = favs, "Favourites"
		elif info == 'similarlocal' and "dbid" in params:
			data = get_similar_movies_from_db(params["dbid"]), "SimilarLocalMovies"
		elif info == 'iconpanel':
			data = get_icon_panel(int(params["id"])), "IconPanel" + str(params["id"])
		elif info == 'weather':
			data = get_weather_images(), "WeatherImages"
		elif info == "sortletters":
			data = get_sort_letters(params["path"], params.get("id", "")), "SortLetters"

		# ACTIONS
		elif info == 't9input':
			resolve_url(params.get("handle"))
			from dialogs.T9Search import T9Search
			dialog = T9Search(u'%s-T9Search.xml' % ADDON_ID, ADDON_PATH,
							  call=None,
							  start_value="")
			dialog.doModal()
			get_kodi_json(method="Input.SendText",
						  params='{"text":"%s", "done":true}' % dialog.search_str)

		elif info == 'playmovie':
			resolve_url(params.get("handle"))
			get_kodi_json(method="Player.Open",
						  params='{"item": {"movieid": %s}, "options":{"resume": %s}}' % (params.get("dbid"), params.get("resume", "true")))
		elif info == 'playepisode':
			resolve_url(params.get("handle"))
			get_kodi_json(method="Player.Open",
						  params='{"item": {"episodeid": %s}, "options":{"resume": %s}}' % (params.get("dbid"), params.get("resume", "true")))
		elif info == 'playmusicvideo':
			resolve_url(params.get("handle"))
			get_kodi_json(method="Player.Open",
						  params='{"item": {"musicvideoid": %s}}' % (params.get("dbid")))
		elif info == 'playalbum':
			resolve_url(params.get("handle"))
			get_kodi_json(method="Player.Open",
						  params='{"item": {"albumid": %s}}' % (params.get("dbid")))
		elif info == 'playsong':
			resolve_url(params.get("handle"))
			get_kodi_json(method="Player.Open",
						  params='{"item": {"songid": %s}}' % (params.get("dbid")))
		elif info == "openinfodialog":
			resolve_url(params.get("handle"))
			dbid = xbmc.getInfoLabel("ListItem.DBID")
			if not dbid:
				dbid = xbmc.getInfoLabel("ListItem.Property(dbid)")
			if xbmc.getCondVisibility("Container.Content(movies)"):
				xbmc.executebuiltin("RunScript(script.qlickplay,info=movieinfo,dbid=%s,id=%s)" % (dbid, xbmc.getInfoLabel("ListItem.Property(id)")))
			elif xbmc.getCondVisibility("Container.Content(tvshows)"):
				xbmc.executebuiltin("RunScript(script.qlickplay,info=tvinfo,dbid=%s,id=%s)" % (dbid, xbmc.getInfoLabel("ListItem.Property(id)")))
			elif xbmc.getCondVisibility("Container.Content(seasons)"):
				xbmc.executebuiltin("RunScript(script.qlickplay,info=seasoninfo,tvshow=%s,season=%s)" % (xbmc.getInfoLabel("ListItem.TVShowTitle"), xbmc.getInfoLabel("ListItem.Season")))
			elif xbmc.getCondVisibility("Container.Content(actors) | Container.Content(directors)"):
				xbmc.executebuiltin("RunScript(script.qlickplay,info=actorinfo,name=%s)" % (xbmc.getInfoLabel("ListItem.Label")))
		elif info == "ratedialog":
			resolve_url(params.get("handle"))
			if xbmc.getCondVisibility("Container.Content(movies)"):
				xbmc.executebuiltin("RunScript(script.qlickplay,info=ratemedia,type=movie,dbid=%s,id=%s)" % (xbmc.getInfoLabel("ListItem.DBID"), xbmc.getInfoLabel("ListItem.Property(id)")))
			elif xbmc.getCondVisibility("Container.Content(tvshows)"):
				xbmc.executebuiltin("RunScript(script.qlickplay,info=ratemedia,type=tv,dbid=%s,id=%s)" % (xbmc.getInfoLabel("ListItem.DBID"), xbmc.getInfoLabel("ListItem.Property(id)")))
			elif xbmc.getCondVisibility("Container.Content(episodes)"):
				xbmc.executebuiltin("RunScript(script.qlickplay,info=ratemedia,type=episode,tvshow=%s,season=%s)" % (xbmc.getInfoLabel("ListItem.TVShowTitle"), xbmc.getInfoLabel("ListItem.Season")))
		elif info == 'youtubebrowser':
			from WindowManager import wm
			resolve_url(params.get("handle"))
			wm.open_youtube_list(search_str=params.get("id", ""))
		elif info == 'movieinfo':
			from WindowManager import wm
			resolve_url(params.get("handle"))
			HOME.setProperty('infodialogs.active', "true")
			wm.open_movie_info(movie_id=params.get("id", ""),
							   dbid=params.get("dbid", None),
							   imdb_id=params.get("imdb_id", ""),
							   name=params.get("name", ""))
			HOME.clearProperty('infodialogs.active')
		elif info == 'actorinfo':
			from WindowManager import wm
			resolve_url(params.get("handle"))
			HOME.setProperty('infodialogs.active', "true")
			wm.open_actor_info(actor_id=params.get("id", ""),
							   name=params.get("name", ""))
			HOME.clearProperty('infodialogs.active')
		elif info == 'tvinfo':
			from WindowManager import wm
			resolve_url(params.get("handle"))
			HOME.setProperty('infodialogs.active', "true")
			wm.open_tvshow_info(tvshow_id=params.get("id", ""),
								tvdb_id=params.get("tvdb_id", ""),
								dbid=params.get("dbid", None),
								imdb_id=params.get("imdb_id", ""),
								name=params.get("name", ""))
			HOME.clearProperty('infodialogs.active')
		elif info == 'seasoninfo':
			from WindowManager import wm
			resolve_url(params.get("handle"))
			HOME.setProperty('infodialogs.active', "true")
			wm.open_season_info(tvshow=params.get("tvshow"),
								dbid=params.get("dbid"),
								season=params.get("season"))
			HOME.clearProperty('infodialogs.active')
		elif info == 'episodeinfo':
			from WindowManager import wm
			resolve_url(params.get("handle"))
			HOME.setProperty('infodialogs.active', "true")
			wm.open_episode_info(tvshow=params.get("tvshow"),
								 tvshow_id=params.get("tvshow_id"),
								 dbid=params.get("dbid"),
								 episode=params.get("episode"),
								 season=params.get("season"))
			HOME.clearProperty('infodialogs.active')
		elif info == 'albuminfo':
			from WindowManager import wm
			resolve_url(params.get("handle"))
			if params.get("id", ""):
				album_details = get_album_details(params.get("id", ""))
				pass_dict_to_skin(album_details, params.get("prefix", ""))
		elif info == 'artistdetails':
			resolve_url(params.get("handle"))
			artist_details = get_artist_details(params["artistname"])
			pass_dict_to_skin(artist_details, params.get("prefix", ""))
		elif info == 'ratemedia':
			resolve_url(params.get("handle"))
			media_type = params.get("type", False)
			if media_type:
				if params.get("id") and params["id"]:
					tmdb_id = params["id"]
				elif media_type == "movie":
					tmdb_id = get_movie_tmdb_id(imdb_id=params.get("imdb_id", ""),
												dbid=params.get("dbid", ""),
												name=params.get("name", ""))
				elif media_type == "tv" and params["dbid"]:
					tvdb_id = get_imdb_id_from_db(media_type="tvshow",
												  dbid=params["dbid"])
					tmdb_id = get_show_tmdb_id(tvdb_id=tvdb_id)
				else:
					return False
				set_rating_prompt(media_type=media_type,
								  media_id=tmdb_id)
		elif info == 'updatexbmcdatabasewithartistmbidbg':
			resolve_url(params.get("handle"))
			set_mbids_for_artists(False, False)
		elif info == 'setfocus':
			resolve_url(params.get("handle"))
			xbmc.executebuiltin("SetFocus(22222)")
		elif info == 'playliststats':
			resolve_url(params.get("handle"))
			get_playlist_stats(params.get("id", ""))
		elif info == 'slideshow':
			resolve_url(params.get("handle"))
			window_id = xbmcgui.getCurrentwindow_id()
			window = xbmcgui.Window(window_id)
			# focusid = Window.getFocusId()
			itemlist = window.getFocus()
			num_items = itemlist.getSelectedPosition()
			for i in range(0, num_items):
				notify(item.getProperty("Image"))
		elif info == 'action':
			resolve_url(params.get("handle"))
			for builtin in params.get("id", "").split("$$"):
				xbmc.executebuiltin(builtin)
			return None
		elif info == 'bounce':
			resolve_url(params.get("handle"))
			HOME.setProperty(params.get("name", ""), "True")
			xbmc.sleep(200)
			HOME.clearProperty(params.get("name", ""))
		elif info == "youtubevideo":
			resolve_url(params.get("handle"))
			xbmc.executebuiltin("Dialog.Close(all,true)")
			PLAYER.play_youtube_video(params.get("id", ""))
		elif info == 'playtrailer':
			from WindowManager import wm
			resolve_url(params.get("handle"))
			xbmc.executebuiltin("ActivateWindow(busydialog)")
			if params.get("id", ""):
				movie_id = params.get("id", "")
			elif int(params.get("dbid", -1)) > 0:
				movie_id = get_imdb_id_from_db(media_type="movie",
											   dbid=params["dbid"])
			elif params.get("imdb_id", ""):
				movie_id = get_movie_tmdb_id(params.get("imdb_id", ""))
			else:
				movie_id = ""
			if movie_id:
				trailer = get_trailer(movie_id)
				xbmc.executebuiltin("Dialog.Close(busydialog)")
				xbmc.sleep(100)
				if trailer:
					PLAYER.play_youtube_video(trailer)
				elif params.get("title"):
					wm.open_youtube_list(search_str=params.get("title", ""))
				else:
					xbmc.executebuiltin("Dialog.Close(busydialog)")
		elif info == 'playtvtrailer':
			from WindowManager import wm
			resolve_url(params.get("handle"))
			xbmc.executebuiltin("ActivateWindow(busydialog)")
			if params.get("id", ""):
				tvshow_id = params.get("id", "")
			elif int(params.get("dbid", -1)) > 0:
				tvshow_id = get_imdb_id_from_db(media_type="show",
											   dbid=params["dbid"])
			elif params.get("tvdb_id", ""):
				tvshow_id = get_tvshow_id_from_tvdbid(params.get("tvdb_id", ""))
			else:
				tvshow_id = ""
			if tvshow_id:
				trailer = get_tvtrailer(tvshow_id)
				xbmc.executebuiltin("Dialog.Close(busydialog)")
				xbmc.sleep(100)
				if trailer:
					PLAYER.play_youtube_video(trailer)
				elif params.get("title"):
					wm.open_youtube_list(search_str=params.get("title", ""))
				else:
					xbmc.executebuiltin("Dialog.Close(busydialog)")
		elif info == 'updatexbmcdatabasewithartistmbid':
			resolve_url(params.get("handle"))
			set_mbids_for_artists(True, False)
		elif info == 'deletecache':
			resolve_url(params.get("handle"))
			HOME.clearProperties()
			import shutil
			for rel_path in os.listdir(ADDON_DATA_PATH):
				path = os.path.join(ADDON_DATA_PATH, rel_path)
				try:
					if os.path.isdir(path):
						shutil.rmtree(path)
				except Exception as e:
					log(e)
			notify("Cache deleted")
		elif info == "qustom":
			from WindowManager import wm
			HOME.setProperty('infodialogs.active', "true")
			from resources.lib.WindowManager import wm
			wm.open_video_list(media_type=params.get("type", "tv"),
							   mode="filter")
			HOME.clearProperty('infodialogs.active')
		elif info == "onclicknext":
			mvoption = None
			tvoption = None
			if params.get("type")	 == "movie" :
				mvoption = SETTING('onclick_movies')
			if params.get("type")	 == "tv"	:
				tvoption = SETTING('onclick_tvshows')
			else								 :
				mvoption = SETTING('onclick_movies')
				tvoption = SETTING('onclick_tvshows')
			if mvoption			   != None	:
				if   mvoption == "select" : SET("onclick_movies", "default")
				elif mvoption == "default": SET("onclick_movies", "info")
				elif mvoption == "info"   : SET("onclick_movies", "library")
				elif mvoption == "library": SET("onclick_movies", "context")
				elif mvoption == "context": SET("onclick_movies", "trailer")
				elif mvoption == "trailer": SET("onclick_movies", "select")
			if tvoption			   != None	:
				if   tvoption == "select" : SET("onclick_tvshows", "default")
				elif tvoption == "default": SET("onclick_tvshows", "info")
				elif tvoption == "info"   : SET("onclick_tvshows", "library")
				elif tvoption == "library": SET("onclick_tvshows", "context")
				elif tvoption == "context": SET("onclick_tvshows", "trailer")
				elif tvoption == "trailer": SET("onclick_tvshows", "select")
		elif info == "pathplay":
			from WindowManager import wm
			resolve_url(params.get("handle"))
			HOME.setProperty('infodialogs.active', "true")
			type = params.get("type")
			if type:
				if "qlick" in params: qlick = params.get("qlick")
				else: qlick = SETTING("qlick_"+type)
				if "action" in params: action = params.get("action")
				else: action = SETTING("action_"+type)
				if "player" in params: player = params.get("player")
				else: player = SETTING("player_"+type)
				if "window" in params: window = params.get("window")
				else: window = SETTING("window_"+type)
			else: 
				notify(header="no type",message="available")
				return
			if type == "movie" or type=="tv":
				url			= ""
				dbid		= ""
				tmdb_id		= ""
				imdb_id		= ""
				tvdb_id		= ""
				trakt_id	= ""
				name		= ""
				slug		= ""
			if params.get("db"):
				if not params.get("id") or params.get("id") == "":
					notify(header="no id or title",message="available")
					return
				id = params.get("id")
			db = params.get("db")
			if db:
				if type == "movie":
					if db == "local": movie_id  = get_movie_tmdb_id(imdb_id=get_imdb_id_from_db(media_type=type, dbid=id))
					elif db == "tmdb": movie_id  = id
					elif db == "imdb":
						try: movie_id = get_movie_tmdb_id(imdb_id=id)
						except: name = id
					elif db == "tvdb": 
						notify(header="Error: TVDb-id present", message="So probably not a movie...", time=10000)
						return
					elif db == "name": movie_id = search_media(media_name=id, media_type=type)
					#notify(header="Db: "+str(movie_id),message="Id: "+str(id))
					if imdb_id  == "": imdb_id  = get_imdb_id_from_movie_id(movie_id)
					if trakt_id == "":
						trakt = get_movie_info_min(imdb_id)
						if trakt:
							trakt_id = trakt['ids']['trakt']
							slug = trakt['ids']['slug']
					if name == "": name = get_title_from_id(movie_id=movie_id)
					#notify(header="TMDb-IMDb-Trakt:",message=str(movie_id)+"-"+str(imdb_id).replace("tt","")+"-"+str(trakt_id))
				if type == "tv":
					no_tmdb_id = False
					if db == "local":
						try: tvshow_id = get_show_tmdb_id(get_imdb_id_from_db(media_type="tvshow", dbid=id))
						except:
							tvdb_id = get_imdb_id_from_db(media_type="tvshow", dbid=id)
							no_tmdb_id = True
							#notify(header="No TMDB-id available",message="Using TVDB-id instead")
					elif db == "tmdb": tvshow_id = id
					elif db == "imdb": tvshow_id = get_show_tmdb_id(imdb_id=id)
					elif db == "tvdb": tvshow_id = tvshow_id = get_show_tmdb_id(tvdb_id=id)
					elif db == "name": 
						tvshow_id = search_media(media_name=id, media_type=type)
						#notify(header="Db: "+str(tvshow_id),message="Id: "+str(id))
						if tvshow_id == None:
							name = id.split(" (",1)
							tvshow_id = search_media(media_name=name[0], media_type=type)
							#notify(header="tvshow_id: "+str(tvshow_id),message="Id: "+str(id))
					if tvshow_id: 
						external_ids = get_tvshow_ids(tvshow_id)
						if imdb_id == "": imdb_id = fetch(external_ids, "imdb_id")
						if tvdb_id == "": tvdb_id = fetch(external_ids, "tvdb_id")
						if name == "": name = get_title_from_id(tvshow_id=tvshow_id)
					if imdb_id != "":
						trakt = get_tshow_info_min(imdb_id)
						if trakt:
							trakt_id = trakt['ids']['trakt']
							slug = trakt['ids']['slug']
							if imdb_id == "": imdb_id = trakt['ids']['imdb']
							if tvdb_id == "": tvdb_id = trakt['ids']['tvdb']
							if name	== "": name = trakt['title']
					#else: notify(header="No IMDB-id available",message="Using title instead")
					if params.get("season"): season = params.get("season")
					else: season = ""
					if season == "" or season == None:
						if "pilots" in params: pilots = params.get("pilots")
						else: pilots = SETTING("pilots")
						if pilots   == "first": season = 1
						elif pilots == "last" : season = 1
						elif pilots == "smart": season = 1
						elif pilots == "lazy" : season = 1
					if params.get("episode"): episode = params.get("episode")
					else: episode = ""
					if episode == "" or episode == None:
						if "pilots" in params: pilots = params.get("pilots")
						else: pilots = SETTING("pilots")
						if pilots   == "first": episode = 1
						elif pilots == "last" : episode = 1
						elif pilots == "smart": episode = 1
						elif pilots == "lazy" : episode = 1
					#notify(header="TMDb-IMDb-Trakt-TVDb:",message=str(tvshow_id)+"-"+str(imdb_id).replace("tt","")+"-"+str(trakt_id)+"-"+str(tvdb_id))
			#if type == "music":
			if type == "movie" or type == "tv":
				if qlick == "search":
					if action   == "runplugin"		: url = "%s(plugin://script.qlickplay/?info=list&type=%s&query=%s)" % (action, type, name)
					elif action == "runscript"		: url = "%s(script.qlickplay,info=list,type=%s,query=%s)" % (action, type, name)
					elif action != ""				:
						if type == "movie"			: url = "%s(%s,plugin://plugin.video.metalliq/movies/search_term/%s/1,return)" % (action, window, name)
						elif type == "tv"			: url = "%s(%s,plugin://plugin.video.metalliq/tv/search_term/%s/1,return)" % (action, window, name)
				elif qlick == "youtube":
					if action   == "runscript"		: url = "RunScript(script.qlickplay,info=list,type=channel,query=%s)" % name
					elif action == "activatewindow"	: url = "RunScript(script.qlickplay,info=list,type=video,query=%s)" % name
					elif action == "replacewindow"	: url = "RunScript(script.qlickplay,info=list,type=playlist,query=%s)" % name
					elif action == "runplugin"		: 
						if type == "movie"			: url = "%s(plugin://script.qlickplay/?&info=playtrailer&id=%s&dbid=%s&imdb_id=%s&title=%s)" % (action, movie_id, dbid, imdb_id, name)
						elif type == "tv"			: url = "%s(plugin://script.qlickplay/?&info=playtvtrailer&id=%s&dbid=%s&imdb_id=%s&title=%s)" % (action, tvshow_id, dbid, imdb_id, name)
			if type == "movie":
				if qlick == "info":
					if action   == "runplugin"		: url = "%s(plugin://script.qlickplay/?info=%sinfo&id=%s&dbid=%s&imdb_id=%s&name=%s)" % (action, type, movie_id, dbid, imdb_id, name)
					elif action == "runscript"		: url = "runplugin(plugin://plugin.video.metalliq/movies/add_to_library/tmdb/%s)" % movie_id
					elif action != ""				: url = "%s(%s,plugin://script.qlickplay/?info=%sinfo&id=%s&dbid=%s&imdb_id=%s&name=%s,return)" % (action, window, type, movie_id, dbid, imdb_id, name)
				elif qlick == "play":
					if action   == "runplugin"		: url = "%s(plugin://plugin.video.metalliq/movies/play/tmdb/%s/%s)" % (action, movie_id, player)
					elif action == "runscript"		: url = "runplugin(plugin://plugin.video.metalliq/movies/play_by_name/%s/%s)" % (name, SETTING("LanguageID"))
					elif action != ""				: url = "%s(%s,plugin://plugin.video.metalliq/movies/play/tmdb/%s/%s,return)" % (action, window, movie_id, player)
			elif type == "tv":
				if qlick == "info":
					if action   == "runplugin"		: url = "%s(plugin://script.qlickplay/?info=%sinfo&id=%s&tvdb_id=%s&dbid=%s&imdb_id=%s&name=%s)" % (action, type, tvshow_id, tvdb_id, dbid, imdb_id, name)
					elif action == "runscript"		: url = "runplugin(plugin://plugin.video.metalliq/tv/add_to_library/%s)" % tvdb_id
					elif action == "activatewindow"	:
						if season != ""				: url = "%s(%s,plugin://plugin.video.metalliq/tv/tvdb/%s/%s,return)" % (action, window, tvdb_id, season)
						else						: url = "%s(%s,plugin://plugin.video.metalliq/tv/tvdb/%s/,return)" % (action, window, tvdb_id)
					elif action == "replacewindow"	:
						if season != ""				: url = "%s(%s,plugin://plugin.video.metalliq/tv/tvdb/%s/%s,return)" % (action, window, tvdb_id, season)
						else						: url = "%s(%s,plugin://plugin.video.metalliq/tv/tvdb/%s/,return)" % (action, window, tvdb_id)
				elif qlick == "play":
					if action   == "runplugin"		: url = "%s(plugin://plugin.video.metalliq/tv/play/%s/%s/%s/%s)" % (action, tvdb_id, season, episode, player)
					elif action == "runscript"		: url = "runplugin(plugin://plugin.video.metalliq/tv/play_by_name/%s/%s/%s/%s)" % (name, season, episode, SETTING("LanguageID"))
					elif action != ""				: url = "%s(%s,plugin://plugin.video.metalliq/tv/play/%s/%s/%s/%s)" % (action, window, tvdb_id, season, episode, player)
			xbmc.executebuiltin(url)
			if qlick == "info":
				if action == "runscript":
					xbmc.executebuiltin("RunScript(script.qlickplay,info=afteradd)")
			HOME.clearProperty('infodialogs.active')
		elif info == "clearprops":
			HOME.clearProperties()
		elif info == "afteradd":
			resolve_url(params.get("handle"))
			HOME.clearProperties()
			import shutil
			basepath = os.path.join(ADDON_DATA_PATH, "TheMovieDB")
			path1 = os.path.join(basepath, "0ec735169a3d0b98719c987580e419e5.txt")
			path2 = os.path.join(basepath, "c36fcc8e9da1fe1a16fded10581fcc15.txt")
			try:
				if os.path.exists(path1):
					os.remove(path1)
			except Exception as e:
				log(e)
			try:
				if os.path.exists(path2):
					os.remove(path2)
			except Exception as e:
				log(e)
		elif info == 'list':
			from WindowManager import wm
			resolve_url(params.get("handle"))
			HOME.setProperty('infodialogs.active', "true")
			dialog = xbmcgui.Dialog()
			if params.get("type", "") == "channel" or params.get("type", "") == "playlist" or params.get("type", "") == "video":
				if params.get("query", "") == "qqqqq":
					youtubesearch = dialog.input("YoutubeSearch")
					xbmc.executebuiltin('Skin.SetString(YoutubeSearch,'+youtubesearch+')')
					xbmc.executebuiltin('Container.Refresh')
					wm.open_youtube_list(media_type=params.get("type", ""),
										 search_str=youtubesearch)
				elif params.get("query", "") != "" and params.get("query", "") != "qqqqq":
					wm.open_youtube_list(media_type=params.get("type", ""),
										 search_str=params.get("query", ""))
				elif params.get("id", ""):
					if params.get("type", "") == "channel":
						channel_filter = [{"id": params.get("id", ""),"type": "channelId","typelabel": LANG(19029),"label": params.get("id", "")}]
						wm.open_youtube_list(filters=channel_filter)
					elif params.get("type", "") == "playlist":
						xbmc.executebuiltin('RunPlugin(plugin://script.qlickplay?info=youtubeplaylist&id=%s)' % params.get("id", ""))
				else:
					wm.open_youtube_list(media_type=params.get("type", ""))
			elif params.get("type", "") == "movie" or params.get("type", "") == "tv" or not params.get("type", ""):
				if params.get("query", ""):
					if params.get("query", "") == "qqqqq":
						if params.get("type", "") == "movie":
							searchstring = dialog.input("MovieSearch")
							xbmc.executebuiltin('Skin.SetString(MovieSearch,'+searchstring+')')
						elif params.get("type", "") == "tv":
							searchstring = dialog.input("ShowSearch")
							xbmc.executebuiltin('Skin.SetString(ShowSearch,'+searchstring+')')
						else:
							xbmc.executebuiltin("Notification(Please set a valid type,and try again, 5000, special://home/addons/script.qlickplay/icon.png)")
							return
					else:
						searchstring = params.get("query", "")
					wm.open_custom_list(media_type=params.get("type", ""),
										mode="search",
										search_str=searchstring)
				elif params.get("iquery", ""):
					if params.get("iquery", "") == "qqqqq":
						if params.get("type", "") == "movie":
							searchstring = dialog.input("MovieSearch")
							xbmc.executebuiltin('Skin.SetString(MovieSearch,'+searchstring+')')
							xbmc.executebuiltin('Container.Refresh')
						elif params.get("type", "") == "tv":
							searchstring = dialog.input("ShowSearch")
							xbmc.executebuiltin('Skin.SetString(ShowSearch,'+searchstring+')')
							xbmc.executebuiltin('Container.Refresh')
						else:
							searchstring = dialog.input("TotalSearch")
							xbmc.executebuiltin('Skin.SetString(TotalSearch,'+searchstring+')')
							xbmc.executebuiltin('Container.Refresh')
					else:
						searchstring = params.get("iquery", "")
						if params.get("type", "") == "movie":
							xbmc.executebuiltin('Skin.SetString(MovieSearch,'+searchstring+')')
							xbmc.executebuiltin('Container.Refresh')
						elif params.get("type", "") == "tv":
							xbmc.executebuiltin('Skin.SetString(ShowSearch,'+searchstring+')')
							xbmc.executebuiltin('Container.Refresh')
						else:
							xbmc.executebuiltin('Skin.SetString(TotalSearch,'+searchstring+')')
							xbmc.executebuiltin('Container.Refresh')
					if params.get("type", "") == "movie":
						xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.program.super.favourites/?label=MovieSearch&mode=400&path=special://home/addons/script.qlickplay/resources/extras/movie/)')
						xbmc.executebuiltin("Dialog.Close(all,true)")
					elif params.get("type", "") == "tv":
						xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.program.super.favourites/?label=ShowSearch&mode=400&path=special://home/addons/script.qlickplay/resources/extras/tv/)')
						xbmc.executebuiltin("Dialog.Close(all,true)")
					else:
						xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.program.super.favourites/?label=TotalSearch&mode=400&path=special://home/addons/script.qlickplay/resources/extras/total/)')
						xbmc.executebuiltin("Dialog.Close(all,true)")
				elif params.get("filters", ""):
					filters = str(params.get("filters", "")).replace("%5B","[").replace("%5D","]").replace("%7B","{").replace("%7C","|").replace("%7D","}").replace("%27","'").replace("%2C",",").replace("%3A",":").replace("%20"," ").replace("%3C","<").replace("%3D","=").replace("%3E",">")
					print "QQQQQ"+str(filters)
					wm.open_video_list(media_type=params.get("type", ""),
									   filters=filters,
									   force=True,
									   mode="filter")
				else:
					wm.open_video_list(media_type=params.get("type", ""),
									   mode="filter")
			elif params.get("id", ""):
				wm.open_custom_list(mode="list",
									list_id=params.get("id", ""),
									search_str="",
									force=True)
			else:
				pass
			HOME.clearProperty('infodialogs.active')
		elif info == 'syncwatchlist':
			pass
		elif info == 'audiotest':
			from WindowManager import wm
			wm.open_audio_list(media_type="artist")
		elif info == 'cleartest':
			HOME.clearProperty('infodialogs.active')
		elif info == 'configplay':
			set_next_setting("Movie","Qlick","Info")
			set_next_setting("TV","Qlick","Info")
		elif info == 'setset':
			if params.get("type", ""): type = params.get("type", "")
			else: type = None
			if params.get("name", ""): name = params.get("name", "")
			else: name = None
			if params.get("value", ""): value = params.get("value", "")
			else: value = None
			if type != None: 
				if name != None:
					set_next_setting(type,name,value)
				else:
					for item in TOTALS[1]:
						name = item
						set_next_setting(type,name,value)
			else:
				if name != None:
					for item in TOTALS[0]:
						type = item
						set_next_setting(type,name,value)
				else:
					for total in TOTALS[0]:
						type = total
						for item in TOTALS[1]:
							name = item
							set_next_setting(type,name,value)
		elif info == 'toggleadvanced':
			if SETTING("mode_advanced") == "false": SET("mode_advanced","true")
			elif SETTING("mode_advanced") == "true": SET("mode_advanced","false")
		elif info == 'setold':
			xbmc.executebuiltin("Addon.OpenSettings(script.qlickplay)")
			xbmc.executebuiltin("SetFocus(102)")
			xbmc.executebuiltin("SetFocus(202)")
			xbmc.executebuiltin("SetFocus(201)")
			xbmc.executebuiltin("Control.Message(201,click)")
			xbmc.executebuiltin("Control.Message(201,movedown)")
			xbmc.executebuiltin("Control.Message(3,moveup)")
			xbmc.executebuiltin("Control.Message(5,click)")
		elif info == "testing":
			data = get_top_artists(), "TopArtists"
			from WindowManager import wm
			HOME.setProperty('infodialogs.active', "true")
			from resources.lib.WindowManager import wm
			wm.open_audio_list(media_type=params.get("type", "artist"),
							   mode="filter")
			HOME.clearProperty('infodialogs.active')
		elif info == "widgetdialog":
			resolve_url(params.get("handle"))
			widget_selectdialog()
		listitems, prefix = data
		if params.get("handle"):
			xbmcplugin.addSortMethod(params.get("handle"), xbmcplugin.SORT_METHOD_TITLE)
			xbmcplugin.addSortMethod(params.get("handle"), xbmcplugin.SORT_METHOD_VIDEO_YEAR)
			xbmcplugin.addSortMethod(params.get("handle"), xbmcplugin.SORT_METHOD_DURATION)
			if info.endswith("shows"):
				xbmcplugin.setContent(params.get("handle"), 'tvshows')
			else:
				xbmcplugin.setContent(params.get("handle"), 'movies')
		pass_list_to_skin(name=prefix,
						  data=listitems,
						  prefix=params.get("prefix", ""),
						  handle=params.get("handle", ""),
						  limit=params.get("limit", 20))

def resolve_url(handle):
	if handle:
		xbmcplugin.setResolvedUrl(handle=int(handle),
								  succeeded=False,
								  listitem=xbmcgui.ListItem())
