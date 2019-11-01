
List of possible [COLOR ff0084ff]Q[/COLOR]lick[COLOR ff0084ff]P[/COLOR]lay calls.
All calls can also be done by using a plugin path.

Example:
<content>plugin://script.qlickplay?info=discography&artistname=INSERT_ARTIST_NAME_HERE</content>
- keep Attention to the parameter separator: "&" some places it may need to be "&amp;"

### Custom (added by OpenELEQ)

RunScript(script.qlickplay,info=list,type=movie)     --> Starts script with movie-type
  - optional additional parameter: query=
    - set query to "qqqqq" to force keyboard
  - optional additional parameter: iquery=              --> Executes custom iSearch using movie-list (~/resources/extras/movie/favourites.xml)
    - set iquery to "qqqqq" to force keyboard

RunScript(script.qlickplay,info=list,type=tv)        --> Starts script with tv-type
  - optional additional parameter: query=
    - set query to "qqqqq" to force keyboard
  - optional additional parameter: iquery=              --> Executes custom iSearch using tv-list (~/resources/extras/tv/favourites.xml)
    - set iquery to "qqqqq" to force keyboard

RunScript(script.qlickplay,info=list,iquery=)        --> Executes custom iSearch using total list (~/resources/extras/total/favourites.xml)
  - set iquery to "qqqqq" to force keyboard

RunScript(script.qlickplay,info=list,type=channel)   --> Starts youtube-browser with channel-type
  - optional additional parameter: query=

RunScript(script.qlickplay,info=list,type=playlist)  --> Starts youtube-browser with playlist-type
  - optional additional parameter: query=

RunScript(script.qlickplay,info=list,type=video)     --> Starts youtube-browser with video-type
  - optional additional parameter: query=

RunScript(script.qlickplay,info=list,id=)            --> Starts script using listid
  - TMDb login required

RunScript(script.qlickplay,info=string)              --> Sets SkinString (TotalSearch) and refreshes container
  - optional additional parameter: type=
    - if type=tv                                        --> Sets SkinString (ShowSearch) and refreshes container
    - if type=movie                                     --> Sets SkinString (MovieSearch) and refreshes container
    - if type=music                                     --> Sets SkinString (MusicSearch) and refreshes container
    - if type=youtube                                   --> Sets SkinString (YoutubeSearch) and refreshes container

### Rotten Tomatoes
RunScript(script.qlickplay,info=intheaters)          --> InTheatersMovies.%d.xxx
RunScript(script.qlickplay,info=comingsoon)          --> ComingSoonMovies.%d.xxx
RunScript(script.qlickplay,info=opening)             --> Opening.%d.xxx
RunScript(script.qlickplay,info=boxoffice)           --> BoxOffice.%d.xxx
RunScript(script.qlickplay,info=toprentals)          --> TopRentals.%d.xxx
RunScript(script.qlickplay,info=currentdvdreleases)  --> CurrentDVDs.%d.xxx
RunScript(script.qlickplay,info=newdvdreleases)      --> NewDVDs.%d.xxx
RunScript(script.qlickplay,info=upcomingdvds)        --> UpcomingDVDs.%d.xxx

Available Properties:
- 'Title':        Movie Title
- 'imdb_id':      IMDB ID
- 'duration':     Movie duration
- 'Year':         Release Year
- 'Premiered':    Release Date
- 'mpaa':         MPAA Rating
- 'Rating':       Audience Rating (0-10)
- 'Plot':         Movie Plot

Available Art:
- 'Poster':       Movie Poster

### TheMovieDB
RunScript(script.qlickplay,info=incinemas)           --> InCinemasMovies.%d
RunScript(script.qlickplay,info=upcoming)            --> UpcomingMovies.%d
RunScript(script.qlickplay,info=popularmovies)       --> PopularMovies.%d
RunScript(script.qlickplay,info=topratedmovies)      --> TopRatedMovies.%d
RunScript(script.qlickplay,info=similarmovies)       --> SimilarMovies.%d
  - required additional parameters: dbid=
RunScript(script.qlickplay,info=set)                 --> MovieSetItems.%d
- fetches a list of movies from the same Set
  - required additional parameters: dbid=
RunScript(script.qlickplay,info=directormovies)      --> DirectorMovies.%d
  - required additional parameters: director=
RunScript(script.qlickplay,info=writermovies)        --> WriterMovies.%d
  - required additional parameters: writer=
RunScript(script.qlickplay,info=studio)              --> StudioInfo.%d
- fetches a list of movies from the same studio
  - required additional parameters: studio=

Available Properties:
- 'Title':            Movie Title
- 'OriginalTitle':    Movie OriginalTitle
- 'ID':               TheMovieDB ID
- 'Rating':           Movie Rating (0-10)
- 'Votes':            Vote Count for Rating
- 'Year':             Release Year
- 'Premiered':        Release Date

Available Art:
- 'Fanart':      Movie Fanart
- 'Poster':      Movie Poster

RunScript(script.qlickplay,info=populartvshows)      --> PopularTVShows.%d
RunScript(script.qlickplay,info=topratedtvshows)     --> TopRatedTVShows.%d
RunScript(script.qlickplay,info=onairtvshows)        --> OnAirTVShows.%d
RunScript(script.qlickplay,info=airingtodaytvshows)  --> AiringTodayTVShows.%d

Available Properties:
- 'Title':            TVShow Title
- 'ID':               TVShow MovieDB ID
- 'OriginalTitle':    TVShow OriginalTitle
- 'Rating':           TVShow Rating
- 'Votes':            Number of Votes for Rating
- 'Premiered':        TV Show First Air Date

Available Art:
- 'Poster':           TVShow Poster
- 'Fanart':           TVShow Fanart

### Trakt.tv
RunScript(script.qlickplay,info=trendingmovies)      --> TrendingMovies.%d
RunScript(script.qlickplay,info=similarmoviestrakt)  --> SimilarMovies.%d
  - required additional parameters: dbid= (database id) or id= (imdb id)

Available Properties:
- 'Title'
- 'Plot'
- 'Tagline'
- 'Genre'
- 'Rating'
- 'mpaa'
- 'Year'
- 'Premiered'
- 'Runtime'
- 'Trailer'

Available Art:
- 'Poster'
- 'Fanart'

RunScript(script.qlickplay,info=trendingshows)         --> TrendingShows.%d
RunScript(script.qlickplay,info=similartvshowstrakt)   --> SimilarTVShows.%d
  - required additional parameters: dbid= (database id) or id= (tvdb id)

Available Properties:
- 'TVShowTitle':      TVShow Title
- 'duration':         Duration (?)
- 'Plot':             Plot
- 'ID':               ID
- 'Genre':            Genre
- 'Rating':           Rating
- 'mpaa':             mpaa
- 'Year':             Release Year
- 'Premiered':        First Air Date
- 'Status':           TVShow Status
- 'Studio':           TVShow Studio
- 'Country':          Production Country
- 'Votes':            Amount of Votes
- 'Watchers':         Amount of Watchers
- 'AirDay':           Day episode is aired
- 'AirShortTime':     Time episode is aired

Available Art:
- 'Poster':      TVShow Poster
- 'Banner':      TVShow Banner
- 'Fanart':      TVShow Fanart

RunScript(script.qlickplay,info=airingshows)         --> AiringShows.%d
RunScript(script.qlickplay,info=premiereshows)       --> PremiereShows.%d

Available Properties:
- 'Title':         Episode Title
- 'TVShowTitle':   TVShow Title
- 'Plot':          Episode Plot
- 'Genre':         TVShow Genre
- 'Runtime':       Episode Duration
- 'Year':          Episode Release Year
- 'Certification': TVShow Mpaa Rating
- 'Studio':        TVShow Studio
- 'Thumb':         Episode Thumb

Available Art:
- 'Poster':   TVShow Poster
- 'Banner':   TVShow Banner
- 'Fanart':   TVShow Fanart


### TheAudioDB
RunScript(script.qlickplay,info=discography)         --> Discography.%d
- fetches the artist discography (Last.FM)
  - required additional parameters: artistname=

Available Properties:
- 'Label':           Album Title
- 'artist':          Album Artist
- 'mbid':            Album MBID
- 'id':              Album AudioDB ID
- 'Description':     Album Description
- 'Genre':           Album Genre
- 'Mood':            Album Mood
- 'Speed':           Album Speed
- 'Theme':           Album Theme
- 'Type':            Album Type
- 'thumb':           Album Thumb
- 'year':            Album Release Year
- 'Sales':           Album Sales

RunScript(script.qlickplay,info=mostlovedtracks)         --> MostLovedTracks.%d
- fetches most loved tracks for the given artist (TheAudioDB)
  - required additional parameters: artistname=
RunScript(script.qlickplay,info=albuminfo)               --> TrackInfo.%d
  - required additional parameters: id= ???

Available Properties:
- 'Label':       Track Name
- 'Artist':      Artist Name
- 'mbid':        Track MBID
- 'Album':       Album Title
- 'Thumb':       Album Thumb
- 'Path':        Link to Youtube Video

RunScript(script.qlickplay,info=artistdetails) ???

### LastFM
RunScript(script.qlickplay,info=albumshouts)
- fetches twitter shouts for given album
  - required additional parameters: artistname=, albumname=
RunScript(script.qlickplay,info=artistshouts)
- fetches twitter shouts for given artist
  - required additional parameters: artistname=

- 'comment':  Tweet Content
- 'author':   Tweet Author
- 'date':     Tweet Date

RunScript(script.qlickplay,info=topartists)
- fetches a lists of the most popular artists
RunScript(script.qlickplay,info=hypedartists)

Available Properties:
- 'Title':        Artist Name
- 'mbid':         Artist MBID
- 'Thumb':        Artist Thumb
- 'Listeners':    actual Listeners

RunScript(script.qlickplay,info=nearevents)       --> NearEvents.%d
  - optional parameters: lat=, lon=, location=, distance=, festivalsonly=, tag=

Available Properties:
- 'date':         Event Date
- 'name':         Venue Name
- 'venue_id':     Venue ID
- 'event_id':     Event ID
- 'street':       Venue Street
- 'eventname':    Event Title
- 'website':      Event Website
- 'description':  Event description
- 'postalcode':   Venue PostalCode
- 'city':         Venue city
- 'country':      Venue country
- 'lat':          Venue latitude
- 'lon':          Venue longitude
- 'artists':      Event artists
- 'headliner':    Event Headliner
- 'googlemap':    GoogleMap of venue location
- 'artist_image': Artist image
- 'venue_image':  Venue image

### YouTube
RunScript(script.qlickplay,info=youtubesearch)           --> YoutubeSearch.%d
  - required additional parameters: id=
RunScript(script.qlickplay,info=youtubeplaylist)         --> YoutubePlaylist.%d
  - required additional parameters: id=
RunScript(script.qlickplay,info=youtubeusersearch)       --> YoutubeUserSearch.%d
  - required additional parameters: id=

Available Properties:
- 'Thumb':        Video Thumbnail
- 'Description':  Video Description
- 'Title':        Video Title
- 'Date':         Video Upload Date

### Misc Images
RunScript(script.qlickplay,info=xkcd)                   --> XKCD.%d
- fetches a daily random list of XKCD webcomics
RunScript(script.qlickplay,info=cyanide)                --> CyanideHappiness.%d
- fetches a daily random list of Cyanide & Happiness webcomics
RunScript(script.qlickplay,info=dailybabe)              --> DailyBabe.%d
RunScript(script.qlickplay,info=dailybabes)             --> DailyBabes.%d

Available Properties:
- 'Thumb':        Image
- 'Title':        Image Title
- 'Description':  Image Description (only XKCD)

info=similarlocal
    Property Prefix: SimilarLocalMovies
    needed parameters:
    -dbid: DBID of any movie in your library
fetches similar movies from local database

### Misc Calls:
info=artistdetails
    needed parameters:
        artistname: Artist to search for
- also fetches Discography and MusicVideos ATM
info=albuminfo ## todo
    needed parameters:
        artistname: Artist to search for
- also fetches Discography and MusicVideos ATM

### ActorInfo / MovieInfo Dialogs (script.metadata.actors replacement)
possible script call for Actor Info Dialog:
RunScript(script.qlickplay,info=actorinfo,name=ACTORNAME)
RunScript(script.qlickplay,info=actorinfo,id=ACTOR_TMDB_ID)

possible script calls for Movie Info Dialog:
RunScript(script.qlickplay,info=movieinfo,name=MOVIENAME)
RunScript(script.qlickplay,info=movieinfo,id=MOVIE_TMDB_ID)
RunScript(script.qlickplay,info=movieinfo,dbid=MOVIE_DBID)
RunScript(script.qlickplay,info=movieinfo,imdb_id=IMDB_ID)

----

## SKINNING ADD-ON DIALOGS:
Please have a look at reference implementation, too much to cover. Consider the following docs as outdated, needs some updating.

#### List of Built In Controls for add-on dialogs :
 - MOVIES, TVSHOWS, SEASONS, EPISODES: script.qlickplay-DialogVideoInfo.xml
 - ACTORS: script.qlickplay-DialogInfo.xml

| IDS     | MOVIES    | TVSHOWS   | SEASONS   | EPISODES | ACTORS      |
|---------|-----------|-----------|-----------|----------|-------------|
| 150     | Similar   | Similar   | ---       | ---      | Movie Roles |
| 250     | Sets      | Seasons   | ---       | ---      | TV Roles    |
| 350     | Youtube   | Youtube   | Youtube   | Youtube  | Youtube     |
| 450     | Lists     | ---       | ---       | ---      | Images      |
| 550     | Studios   | Studios   | ---       | ---      | Movie Crew  |
| 650     | Releases  | Certific  | ---       | ---      | TV Crew     |
| 750     | Crew      | Crew      | Crew      | Crew     | Tagged Img  |
| 850     | Genres    | Genres    | ---       | ---      | ---         |
| 950     | Keywords  | Keywords  | ---       | ---      | ---         |
| 1000    | Actors    | Actors    | Actors    | Actors   | ---         |
| 1050    | Reviews   | ---       | ---       | ---      | ---         |
| 1150    | Videos    | Videos    | Videos    | Videos   | ---         |
| 1250    | Images    | Images    | Images    | ---      | ---         |
| 1350    | Backdrops | Backdrops | Backdrops | Images   | ---         |
| 1450    | ---       | Networks  | ---       | ---      | ---         |
| 2000    | ---       | ---       | Episodes  | ---      | ---         |

#### Labels Available In script-Actors-DialogInfo.xml:

Labels of the currently selected actor / director / writer / artist.
- Window(home).Property(Title) ----------> Name
- Window(home).Property(Label) ----------> Same as Title
- Window(home).Property(Poster)----------> Poster
- Window(home).Property(Plot)------------> Biography
- Window(home).Property(Biography) ------> Same as Plot
- Window(home).Property(TotalMovies) ----> Total of Known Movies (acting / directing / writing)
- Window(home).Property(Birthday) -------> Date of Birthday
- Window(home).Property(HappyBirthday) --> return true or empty
- Window(home).Property(Age) ------------> Age (30)
- Window(home).Property(AgeLong) --------> Age long format (age 30)
- Window(home).Property(Deathday) -------> Date of Deathday
- Window(home).Property(PlaceOfBirth) ---> Place of birth
- Window(home).Property(AlsoKnownAs) ----> Also Known Name
- Window(home).Property(Homepage) -------> Link of homepage
- Window(home).Property(Adult) ----------> Is Adult Actor (no / yes)
- Window(home).Property(fanart) ---------> Fanart

Labels of Known Movies list
- Container(150).ListItem.Label ---------------------> Title of movie
- Container(150).ListItem.Title ---------------------> same as label
- Container(150).ListItem.originaltitle -------------> originaltitle
- Container(150).ListItem.Year ----------------------> year
- Container(150).Listitem.Icon ----------------------> icon of movie
- Container(150).ListItem.Property(role) ------------> role in currently slected movie
- Container(150).ListItem.Property(job) -------------> job in currently slected movie (director / writer / etc)
- Container(150).ListItem.Property(release_date) -----> release date of movie
- Container(150).ListItem.Property(year) ------------> same as year, but not return empty
- Container(150).ListItem.Property(DBID)             -> return 1 or empty, if movie exists in library
- Container(150).ListItem.Property(Playcount) -------> Playcount of movie (default is 0)
- Container(150).ListItem.Property(file) ------------> media to play

Labels of thumbs list
- Container(250).ListItem.Label --------------------> Image résolution (512x720)
- Container(250).Listitem.Icon ---------------------> Image
- Container(250).ListItem.Property(aspect_ratio) ---> Aspect Ratio (0.66)

[...](WIP)

#### Labels Available In script-Actors-DialogVideoInfo.xml:

[...](WIP)
