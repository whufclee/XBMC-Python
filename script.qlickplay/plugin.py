# -*- coding: utf8 -*-

# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details

import sys
import xbmc
import xbmcplugin
import xbmcgui
from resources.lib.process import start_info_actions
from resources.lib.Utils import *


class Main:

    def __init__(self):
        xbmc.log("version %s started" % ADDON_VERSION)
        xbmc.executebuiltin('SetProperty(qlickplay_running,True,home)')
        self._parse_argv()
        if self.infos:
            start_info_actions(self.infos, self.params)
        else:
            video = {"list&type=video": "yt - %s [I](Youtube)[/I]" % LANG(32231),
                     "list&type=channel": "yt - %s [I](Youtube)[/I]" % LANG(32229),
                     "list&type=playlist": "yt - %s [I](Youtube)[/I]" % LANG(32230),
                    }
            movie = {"intheaters": "rt - %s [I](RottenTomatoes)[/I]" % LANG(32042),
                     "boxoffice": "rt - %s [I](RottenTomatoes)[/I]" % LANG(32055),
                     "opening": "rt - %s [I](RottenTomatoes)[/I]" % LANG(32048),
                     "comingsoon": "rt - %s [I](RottenTomatoes)[/I]" % LANG(32043),
                     "toprentals": "rt - %s [I](RottenTomatoes)[/I]" % LANG(32056),
                     "currentdvdreleases": "rt - %s [I](RottenTomatoes)[/I]" % LANG(32049),
                     "newdvdreleases": "rt - %s [I](RottenTomatoes)[/I]" % LANG(32053),
                     "upcomingdvds": "rt - %s [I](RottenTomatoes)[/I]" % LANG(32054),
                     # tmdb
                     "incinemas": "tm - %s [I](TheMovieDB)[/I]" % LANG(32042),
                     "upcoming": "tm - %s [I](TheMovieDB)[/I]" % LANG(32043),
                     "topratedmovies": "tm - %s [I](TheMovieDB)[/I]" % LANG(32046),
                     "popularmovies": "tm - %s [I](TheMovieDB)[/I]" % LANG(32044),
                     "accountlists": "tm - %s [I](TheMovieDB)[/I]" % LANG(32045),
                     # trakt
                     "trendingmovies": "tr - %s [I](Trakt.tv)[/I]" % LANG(32047),
                     # tmdb
                     "starredmovies": "tm - %s [I](TheMovieDB)[/I]" % LANG(32134),
                     "ratedmovies": "tm - %s [I](TheMovieDB)[/I]" % LANG(32135),
                     }
            tvshow = {"airingshows": "tr - %s [I](Trakt.tv)[/I]" % LANG(32028),
                      "premiereshows": "tr - %s [I](Trakt.tv)[/I]" % LANG(32029),
                      "trendingshows": "tr - %s [I](Trakt.tv)[/I]" % LANG(32032),
                      "airingtodaytvshows": "tm - %s [I](TheMovieDB)[/I]" % LANG(32038),
                      "onairtvshows": "tm - %s [I](TheMovieDB)[/I]" % LANG(32039),
                      "topratedtvshows": "tm - %s [I](TheMovieDB)[/I]" % LANG(32040),
                      "populartvshows": "tm - %s [I](TheMovieDB)[/I]" % LANG(32041),
                      "starredtvshows": "tm - %s [I](TheMovieDB)[/I]" % LANG(32144),
                      "ratedtvshows": "tm - %s [I](TheMovieDB)[/I]" % LANG(32145),
                      }
            xbmcplugin.setContent(self.handle, 'files')
            items = merge_dicts(video, movie, tvshow)
            for key, value in items.iteritems():
                temp = {}
                temp['value'] = value
                image_code = temp['value'][:2]
                label = temp['value'][5:]
                li = xbmcgui.ListItem(label, iconImage="special://home/addons/script.qlickplay/resources/skins/Default/media/%s.png" % image_code)
                li.setProperty('fanart_image', "special://home/addons/script.qlickplay/resources/skins/Default/media/%s-fanart.jpg" % image_code)
                url = 'plugin://script.qlickplay?info=%s' % key
                xbmcplugin.addDirectoryItem(handle=self.handle, url=url,
                                            listitem=li, isFolder=True)
            xbmcplugin.endOfDirectory(self.handle)
        xbmc.executebuiltin('ClearProperty(qlickplay_running,home)')

    def _parse_argv(self):
        args = sys.argv[2][1:]
        self.handle = int(sys.argv[1])
        self.control = "plugin"
        self.infos = []
        self.params = {"handle": self.handle,
                       "control": self.control}
        if args.startswith("---"):
            delimiter = "&"
            args = args[3:]
        else:
            delimiter = "&"
        for arg in args.split(delimiter):
            param = arg.replace('"', '').replace("'", " ")
            if param.startswith('info='):
                self.infos.append(param[5:])
            else:
                try:
                    self.params[param.split("=")[0].lower()] = "=".join(param.split("=")[1:]).strip()
                except:
                    pass

if (__name__ == "__main__"):
    Main()
xbmc.log('finished')
