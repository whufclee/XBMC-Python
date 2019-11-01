# -*- coding: utf8 -*-

# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details

import xbmc
import xbmcgui
from ..Utils import *
from ..ImageTools import *
from ..TheMovieDB import *
from DialogBaseInfo import DialogBaseInfo
from ..WindowManager import wm
from ..OnClickHandler import OnClickHandler
from .. import VideoPlayer

PLAYER = VideoPlayer.VideoPlayer()
ch = OnClickHandler()


def get_tvshow_window(window_type):

    class DialogTVShowInfo(DialogBaseInfo, window_type):

        def __init__(self, *args, **kwargs):
            super(DialogTVShowInfo, self).__init__(*args, **kwargs)
            self.type = "TVShow"
            data = extended_tvshow_info(tvshow_id=kwargs.get('tmdb_id', False),
                                        dbid=self.dbid)
            if not data:
                return None
            self.info, self.data, self.account_states = data
            if "dbid" not in self.info:
                self.info['poster'] = get_file(self.info.get("poster", ""))
            self.info['ImageFilter'], self.info['ImageColor'] = filter_image(input_img=self.info.get("poster", ""),
                                                                             radius=25)
            self.listitems = [(150, self.data["similar"]),
                              (250, self.data["seasons"]),
                              (1450, self.data["networks"]),
                              (550, self.data["studios"]),
                              (650, merge_with_cert_desc(self.data["certifications"], "tv")),
                              (750, self.data["crew"]),
                              (850, self.data["genres"]),
                              (950, self.data["keywords"]),
                              (1000, self.data["actors"]),
                              (1150, self.data["videos"]),
                              (1250, self.data["images"]),
                              (1350, self.data["backdrops"])]

        def onInit(self):
            self.get_youtube_vids("%s tv" % (self.info['title']))
            super(DialogTVShowInfo, self).onInit()
            pass_dict_to_skin(data=self.info,
                              prefix="movie.",
                              window_id=self.window_id)
            super(DialogTVShowInfo, self).update_states()
            self.fill_lists()

        def onClick(self, control_id):
            super(DialogTVShowInfo, self).onClick(control_id)
            ch.serve(control_id, self)

        @ch.click(120)
        def browse_tvshow(self):
            if self.dbid:
                url = "videodb://tvshows/titles/%s/" % (self.dbid)
            else:
                url = "plugin://plugin.video.metalliq/tv/tvdb/%s" % self.info.get("tvdb_id", "")
            self.close()
            xbmc.executebuiltin("ActivateWindow(videos,%s,return)" % url)

        @ch.click(750)
        @ch.click(1000)
        def credit_dialog(self):
            selection = xbmcgui.Dialog().select(heading=LANG(32151),
                                                list=[LANG(32009), LANG(32147)])
            if selection == 0:
                wm.open_actor_info(prev_window=self,
                                   actor_id=self.listitem.getProperty("id"))
            if selection == 1:
                self.open_credit_dialog(self.listitem.getProperty("credit_id"))

        @ch.click(150)
        def open_tvshow_dialog(self):
            wm.open_tvshow_info(prev_window=self,
                                tvshow_id=self.listitem.getProperty("id"),
                                dbid=self.listitem.getProperty("dbid"))

        @ch.click(250)
        def open_season_dialog(self):
            wm.open_season_info(prev_window=self,
                                tvshow_id=self.info["id"],
                                season=self.listitem.getProperty("season"),
                                tvshow=self.info['title'])

        @ch.click(550)
        def open_company_info(self):
            filters = [{"id": self.listitem.getProperty("id"),
                        "type": "with_companies",
                        "typelabel": LANG(20388),
                        "label": self.listitem.getLabel().decode("utf-8")}]
            wm.open_video_list(prev_window=self,
                               filters=filters)

        @ch.click(950)
        def open_keyword_info(self):
            filters = [{"id": self.listitem.getProperty("id"),
                        "type": "with_keywords",
                        "typelabel": LANG(32114),
                        "label": self.listitem.getLabel().decode("utf-8")}]
            wm.open_video_list(prev_window=self,
                               filters=filters)

        @ch.click(850)
        def open_genre_info(self):
            filters = [{"id": self.listitem.getProperty("id"),
                        "type": "with_genres",
                        "typelabel": LANG(135),
                        "label": self.listitem.getLabel().decode("utf-8")}]
            wm.open_video_list(prev_window=self,
                               filters=filters,
                               media_type="tv")

        @ch.click(1450)
        def open_network_info(self):
            filters = [{"id": self.listitem.getProperty("id"),
                        "type": "with_networks",
                        "typelabel": LANG(32152),
                        "label": self.listitem.getLabel().decode("utf-8")}]
            wm.open_video_list(prev_window=self,
                               filters=filters,
                               media_type="tv")

        @ch.click(13)
        def add_play_tvshow(self):
            title = self.info.get("TVShowTitle", "")
            xbmc.executebuiltin("Skin.SetString(ShowSearch,"+title+")")
            dialog = xbmcgui.Dialog()
            show_id = str(self.info.get("dbid", ""))
            extended_play_list = []
            extended_add_list = []
            chosen_add_addon = "na"
            preseason = "1"
            preepisode = "1"
            if ADDON.getSetting("AddOrPlayTVShow") == "play" and ADDON.getSetting("MainAddonTVShow") != "Trailer" and ADDON.getSetting("MainAddonTVShow") != "iSearch" and ADDON.getSetting("MainAddonTVShow") != "Phoenix":
                preseason = dialog.numeric(0, LANG(32197))
                if preseason == '' or preseason == 0:
                    preseason = "1"
                preepisode = dialog.numeric(0, LANG(32198))
                if preepisode == '' or preepisode == 0:
                    preepisode = "1"
                season = preseason.zfill(2)
                episode = preepisode.zfill(2)
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.1channel)"):
                extended_play_list.append("1Channel")
                extended_add_list.append("1Channel")
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.exodus)"):
                extended_play_list.append("Exodus")
#            if xbmc.getCondVisibility("system.hasaddon(plugin.video.genesis)"):
#                extended_play_list.append("Genesis")
#                extended_add_list.append("Genesis")
            if xbmc.getCondVisibility("system.hasaddon(script.icechannel)"):
                extended_play_list.append("iSTREAM")
                extended_add_list.append("iSTREAM")
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.phstreams)"):
                extended_play_list.append("Phoenix")
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.pulsar)"):
                extended_play_list.append("Pulsar")
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.quasar)"):
                extended_play_list.append("Quasar")
                extended_add_list.append("Quasar")
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.salts)"):
                extended_play_list.append("SALTS")
                extended_add_list.append("SALTS")
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.saltshd.lite)"):
                extended_play_list.append("Salts HD Lite")
                extended_add_list.append("Salts HD Lite")
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.saltsrd.lite)"):
                extended_play_list.append("Salts RD Lite")
                extended_add_list.append("Salts RD Lite")
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.specto)"):
                extended_play_list.append("Specto")
                extended_add_list.append("Specto")
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.theroyalwe)"):
                extended_play_list.append("The Royal We")
            if xbmc.getCondVisibility("system.hasaddon(plugin.program.ump)"):
                extended_play_list.append("UMP")
            if xbmc.getCondVisibility("system.hasaddon(plugin.program.super.favourites)"):
                extended_play_list.append("iSearch")
            if xbmc.getCondVisibility("system.hasaddon(script.qlickplay)"):
                extended_play_list.append("Trailer")
            if ADDON.getSetting("AddOrPlayTVShow") == "add" or ADDON.getSetting("AutoAddTVShow") == "true":
                if len(extended_add_list) <= 0:
                    chosen_add_addon = "na"
                elif len(extended_add_list) == 1:
                    chosen_add_addon = extended_add_list[0]
                else:
                    if ADDON.getSetting("LibraryAddonTVShow") in extended_add_list:
                        chosen_add_addon = ADDON.getSetting("LibraryAddonTVShow")
                    else:
                        dialog = xbmcgui.Dialog()
                        chosen_add_addon_id = dialog.select(LANG(32187), extended_add_list)
                        chosen_add_addon = extended_add_list[chosen_add_addon_id]
            if len(extended_play_list) == 1:
                chosen_play_addon = extended_play_list[0]
            else:
                if ADDON.getSetting("MainAddonTVShow") in extended_play_list:
                    chosen_play_addon = ADDON.getSetting("MainAddonTVShow")
                else:
                    if ADDON.getSetting("AlternateAddonTVShow") in extended_play_list:
                        chosen_play_addon = ADDON.getSetting("AlternateAddonTVShow")
                    else:
                        if ADDON.getSetting("AddOrPlayTVShow") == "play":
                            dialog = xbmcgui.Dialog()
                            chosen_play_addon_id = dialog.select(LANG(32185), extended_play_list)
                            chosen_play_addon = extended_play_list[chosen_play_addon_id]
                        else:
                            chosen_play_addon = ""
            churl = "na"
            if chosen_add_addon == "na":
                add = "na"
#            elif chosen_add_addon == 'Genesis':
#                add = "plugin://plugin.video.genesis/?action=tvshowToLibrary&tvshowtitle=%s&year=%s&imdb=%s&tmdb=%s&tvdb=%s&tvrage=%s" % (urllib.quote_plus(self.info.get("TVShowTitle", "")), self.info.get("year", ""), self.info.get("imdb_id", ""), self.info.get("tmdb_id", ""), self.info.get("tvdb_id", ""), self.info.get("tvrage_id", ""))
            elif chosen_add_addon == '1Channel':
                churl='http://www.primewire.ag/'
                link = requests.get(churl).content
                key=regex_from_to(link,'"hidden" name="key" value="', '"')
                churl='http://www.primewire.ag/index.php?search_keywords=%s&key=%s&search_section=1' % (title,key)
                link = requests.get(churl).content
                churl=regex_from_to(link,'index_item index_item_ie"><a href="','"').replace('-online-free','')
                add = "plugin://plugin.video.1channel/?img=http%%3A%%2F%%2Fimages.primewire.ag%%2Fthumbs%%2F%s_%s_59.jpg&title=%s&url=%%2F%s&video_type=tvshow&mode=add_to_library&year=%s" % (churl.replace('watch-',''), self.info.get("year", ""), urllib.quote_plus(self.info.get("TVShowTitle", "")), churl, self.info.get("year", ""))
            elif chosen_add_addon == "iSTREAM":
                add = "plugin://script.icechannel/?indexer_id=IMDb&episode=&name=%s&img=&title=%s&item_title=%s&season=&section=&video_type=tvshow&indexer=tv_shows&imdb_id=%s&fanart=&url=%s&year=%s&item_mode=content&type=tv_seasons&mode=add_to_library" % (urllib.quote_plus(self.info.get("title", "")), urllib.quote_plus(self.info.get("title", "") + '  (' + self.info.get("year", "") + ')'), urllib.quote_plus(self.info.get("title", "") + '  (' + self.info.get("year", "") + ')'), self.info.get("imdb_id", ""), urllib.quote_plus("http://imdb.com/title/" + self.info.get("imdb_id", "")), self.info.get("year", ""))
            elif chosen_add_addon == "Quasar":
                add = "plugin://plugin.video.quasar/library/show/add/%s" % self.info.get("tmdb_id", "")
            elif chosen_add_addon == "SALTS":
                add = "plugin://plugin.video.salts/?trakt_id=%s&year=%s&mode=add_to_library&video_type=TV+Show&title=%s" % (self.info.get("trakt_id", ""), self.info.get("year", ""), urllib.quote_plus(self.info.get("title", "")))
            elif chosen_add_addon == "Salts HD Lite":
                add = "plugin://plugin.video.saltshd.lite/?trakt_id=%s&year=%s&mode=add_to_library&video_type=TV+Show&title=%s" % (self.info.get("trakt_id", ""), self.info.get("year", ""), urllib.quote_plus(self.info.get("title", "")))
            elif chosen_add_addon == "Salts RD Lite":
                add = "plugin://plugin.video.saltsrd.lite/?trakt_id=%s&year=%s&mode=add_to_library&video_type=TV+Show&title=%s" % (self.info.get("trakt_id", ""), self.info.get("year", ""), urllib.quote_plus(self.info.get("title", "")))
            elif chosen_add_addon == 'Specto':
                add = "plugin://plugin.video.specto/?action=tvshowToLibrary&tvshowtitle=%s&year=%s&imdb=%s&tmdb=%s&tvdb=%s&tvrage=%s" % (urllib.quote_plus(self.info.get("TVShowTitle", "")), self.info.get("year", ""), self.info.get("imdb_id", ""), self.info.get("tmdb_id", ""), self.info.get("tvdb_id", ""), self.info.get("tvrage_id", ""))
            if chosen_play_addon == '1Channel':
                if churl != "na":
                    churl = churl.replace('watch-','tv-')
                else:
                    churl='http://www.primewire.ag/'
                    link = requests.get(churl).content
                    key=regex_from_to(link,'"hidden" name="key" value="', '"')
                    churl='http://www.primewire.ag/index.php?search_keywords=%s&key=%s&search_section=1' % (title,key)
                    link = requests.get(churl).content
                    churl=regex_from_to(link,'index_item index_item_ie"><a href="','"').replace('-online-free','').replace('watch-','tv-')
                url = "plugin://plugin.video.1channel/?img=&imdbnum=&url=%s/season-%s-episode-%s&title=%s&video_type=episode&mode=GetSources&dialog=1" % (urllib.quote(churl), preseason, preepisode, urllib.quote_plus(self.info.get("TVShowTitle", "")))
            elif chosen_play_addon == 'Exodus':
                url = "plugin://plugin.video.exodus/?action=play&title=%s&year=%s&imdb=%s&tvdb=%s&season=%s&episode=%s&tvshowtitle=%s&premiered=&meta=" % (urllib.quote_plus(self.info.get("TVShowTitle", "") + " S%.2dE%.2d" % (int(preseason), int(preepisode))), self.info.get("year", ""), self.info.get("imdb_id", ""), self.info.get("tvdb_id", ""), preseason, preepisode, urllib.quote_plus(self.info.get("TVShowTitle", "")))
#            elif chosen_play_addon == 'Genesis':
#                url = "plugin://plugin.video.genesis/?action=play&name=%s&title=%s&year=%s&imdb=%s&tmdb=%s&tvdb=%s&tvrage=%s&season=%s&episode=%s&tvshowtitle=%s&alter=0&date=" % (urllib.quote_plus(self.info.get("TVShowTitle", "") + " S%.2dE%.2d" % (int(preseason), int(preepisode))), urllib.quote_plus(self.info.get("TVShowTitle", "")), self.info.get("year", ""), self.info.get("imdb_id", ""), self.info.get("tmdb_id", ""), self.info.get("tvdb_id", ""), self.info.get("tvrage_id", ""), preseason, preepisode, urllib.quote_plus(self.info.get("TVShowTitle", "")))
            elif chosen_play_addon == "iSTREAM":
                url = "plugin://script.icechannel/?episode=%s&name=%s&title=%s&season=%s&section=&indexer=tv_shows&library=true&imdb_id=%s&video_type=episode&url=%s&year=%s&type=tv_episodes&mode=file_hosts" % (preepisode, urllib.quote_plus(self.info.get("TVShowTitle", "")), urllib.quote_plus(self.info.get("TVShowTitle", "") + " S%.2dE%.2d" % (int(preseason), int(preepisode))), preseason, self.info.get("imdb_id", ""), urllib.quote_plus("http://imdb.com/title/" + self.info.get("imdb_id", "")), self.info.get("year", ""))
            elif chosen_play_addon == "SALTS":
                url = "plugin://plugin.video.salts/?ep_airdate=&trakt_id=%s&episode=%s&mode=get_sources&dialog=True&title=%s&ep_title=%s&season=%s&year=%s&video_type=Episode" % (self.info.get("trakt_id", ""), preepisode, urllib.quote_plus(self.info.get("TVShowTitle", "")), urllib.quote_plus(self.info.get("TVShowTitle", "") + " S%.2dE%.2d" % (int(preseason), int(preepisode))), preseason, self.info.get("year", ""))
            elif chosen_play_addon == "Salts HD Lite":
                url = "plugin://plugin.video.saltshd.lite/?ep_airdate=&trakt_id=%s&episode=%s&mode=get_sources&dialog=True&title=%s&ep_title=%s&season=%s&year=%s&video_type=Episode" % (self.info.get("trakt_id", ""), preepisode, urllib.quote_plus(self.info.get("TVShowTitle", "")), urllib.quote_plus(self.info.get("TVShowTitle", "") + " S%.2dE%.2d" % (int(preseason), int(preepisode))), preseason, self.info.get("year", ""))
            elif chosen_play_addon == "Salts RD Lite":
                url = "plugin://plugin.video.saltsrd.lite/?ep_airdate=&trakt_id=%s&episode=%s&mode=get_sources&dialog=True&title=%s&ep_title=%s&season=%s&year=%s&video_type=Episode" % (self.info.get("trakt_id", ""), preepisode, urllib.quote_plus(self.info.get("TVShowTitle", "")), urllib.quote_plus(self.info.get("TVShowTitle", "") + " S%.2dE%.2d" % (int(preseason), int(preepisode))), preseason, self.info.get("year", ""))
            elif chosen_play_addon == 'Specto':
                url = "plugin://plugin.video.specto/?action=play&name=%s&title=%s&year=%s&imdb=%s&tmdb=%s&tvdb=%s&tvrage=%s&season=%s&episode=%s&tvshowtitle=%s&alter=0&date=" % (urllib.quote_plus(self.info.get("TVShowTitle", "") + " S%.2dE%.2d" % (int(preseason), int(preepisode))), urllib.quote_plus(self.info.get("TVShowTitle", "")), self.info.get("year", ""), self.info.get("imdb_id", ""), self.info.get("tmdb_id", ""), self.info.get("tvdb_id", ""), self.info.get("tvrage_id", ""), preseason, preepisode, urllib.quote_plus(self.info.get("TVShowTitle", "")))
            elif chosen_play_addon == "Phoenix":
                url = "plugin://plugin.video.phstreams/?action=addSearch&url=%s" % self.info.get("TVShowTitle", "")
            elif chosen_play_addon == "Pulsar":
                url = "plugin://plugin.video.pulsar/show/%s/season/%s/episode/%s/%s" % (self.info.get("tmdb_id", ""), preseason, preepisode, ADDON.getSetting("PulsarModeTVShow"))
            elif chosen_play_addon == "Quasar":
                url = "plugin://plugin.video.quasar/show/%s/season/%s/episode/%s/%s" % (self.info.get("id", ""), preseason, preepisode, ADDON.getSetting("PulsarModeTVShow"))
            elif chosen_play_addon == 'The Royal We':
                url = "plugin://plugin.video.theroyalwe/?trakt_id=%s&episode=%s&mode=play_episode&tmdb_id=%s&year=%s&season=%s&display=%s&showtitle=%s&imdb_id=%s" % (self.info.get("trakt_id", ""), int(preepisode), self.info.get("id", ""), self.info.get("year", ""), int(preseason), urllib.quote_plus(self.info.get("TVShowTitle", "") + " S%.2dE%.2d" % (int(preseason), int(preepisode))), urllib.quote_plus(self.info.get("TVShowTitle", "")), self.info.get("imdb_id", ""))
            elif chosen_play_addon == 'UMP':
                url = "plugin://plugin.program.ump/?info=%%7B%%22rating%%22%%3A+%%22%%22%%2C+%%22aired%%22%%3A+%%22%%22%%2C+%%22code%%22%%3A+%%22%s%%22%%2C+%%22Language%%22%%3A+%%22%s%%22%%2C+%%22EpisodeNumber%%22%%3A+%s%%2C+%%22season%%22%%3A+%s%%2C+%%22tvshowtitle%%22%%3A+%%22%s%%22%%2C+%%22code2%%22%%3A+%%22%s%%22%%2C+%%22director%%22%%3A+%%22%%22%%2C+%%22localtitle%%22%%3A+%%22%s%%22%%2C+%%22studio%%22%%3A+%%22%%22%%2C+%%22year%%22%%3A+%s%%2C+%%22genre%%22%%3A+%%22%%22%%2C+%%22episode%%22%%3A+%s%%2C+%%22code10%%22%%3A+%%22%%22%%2C+%%22alternates%%22%%3A+%%5B%%22%%22%%5D%%2C+%%22GuestStars%%22%%3A+%%22%%22%%2C+%%22plot%%22%%3A+%%22%%22%%2C+%%22votes%%22%%3A+%%22%%22%%2C+%%22dateadded%%22%%3A+%%22%%22%%2C+%%22SeasonNumber%%22%%3A+%s%%2C+%%22title%%22%%3A+%%22%%22%%2C+%%22mpaa%%22%%3A+%%22%%22%%2C+%%22writer%%22%%3A+%%22%%7C%%7C%%22%%2C+%%22originaltitle%%22%%3A+%%22%s%%22%%2C+%%22cast%%22%%3A+%%5B%%22%%22%%5D%%2C+%%22absolute_number%%22%%3A+%%22%%22%%2C+%%22EpImgFlag%%22%%3A+2%%7D&art=%%7B%%22thumb%%22%%3A+%%22%%22%%2C+%%22fanart%%22%%3A+%%22%%22%%2C+%%22poster%%22%%3A+%%22%%22%%2C+%%22clearlogo%%22%%3A+%%22%%22%%2C+%%22landscape%%22%%3A+%%22%%22%%2C+%%22banner%%22%%3A+%%22%%22%%2C+%%22clearart%%22%%3A+%%22%%22%%7D&args=%%7B%%7D&module=tvdb&content_type=video&page=urlselect" % (self.info.get("imdb_id", ""), SETTING("LanguageID"), preepisode, preseason, urllib.quote_plus(self.info.get("TVShowTitle", "")), self.info.get("tvdb_id", ""), urllib.quote_plus(self.info.get("TVShowTitle", "")), self.info.get("year", ""), preepisode, preseason, urllib.quote_plus(self.info.get("TVShowTitle", "")))
            elif chosen_play_addon == "iSearch" and ADDON.getSetting("CustomIsearchShow") == "true":
                url = "plugin://plugin.program.super.favourites/?label=ShowSearch&mode=400&path=special://home/addons/script.qlickplay/resources/extras/tv/"
            elif chosen_play_addon == "iSearch" and ADDON.getSetting("CustomIsearchShow") == "false":
                url = "plugin://plugin.program.super.favourites/?mode=0&keyword=%s" % self.info.get("TVShowTitle", "")
            elif chosen_play_addon == "Trailer":
                url = "plugin://script.qlickplay/?info=playtvtrailer&id=%s" % self.info.get("id", "")
            if ADDON.getSetting("AddOrPlayTVShow") == "add" or ADDON.getSetting("AutoAddTVShow") == "true":
                if add == "na":
                    xbmc.executebuiltin("Notification(Install SALTS(HD/RD lite)/Specto/iSTREAM,To Add To Library,8000,special://home/addons/script.qlickplay/icon.png)")
                else:
                    xbmc.executebuiltin("RunPlugin(%s)" % add)
#                    if show_id:
#                        pass
#                    else:
#                        xbmc.executebuiltin("RunScript(script.qlickplay,info=deletecache)")
            if ADDON.getSetting("AddOrPlayTVShow") == "play":
                PLAYER.qlickplay(chosen_play_addon,
                                 url,
                                 listitem=None,
                                 window=self)

        @ch.click(21)
        def appintegration_show(self):
            dbid = str(self.info.get("dbid", ""))
            imdb_id = str(self.info.get("shimdb_id", ""))
            tvdb_id = str(self.info.get("tvdb_id", ""))
            premocktitle = self.info.get("TVShowTitle", "")
            mocktitle = premocktitle.replace("&", "%26")
            title = mocktitle.encode('utf-8')
            manage_list = []
            if dbid:
                if xbmc.getCondVisibility("system.hasaddon(script.artwork.downloader)"):
                    manage_list.append(["Download Artwork", "RunScript(script.artwork.downloader,mediatype=tvshow,dbid="+dbid+")||Notification(Artwork Downloader:,"+title+",5000,special://home/addons/script.artwork.downloader/icon.png)"])
            if not dbid and xbmc.getCondVisibility("system.hasaddon(plugin.video.sickrage)"):
                manage_list.append([LANG(32166), "RunPlugin(plugin://plugin.video.sickrage/?action=addshow&tvdb_id="+tvdb_id+")||Notification(SickRage,"+premocktitle+",5000,special://home/addons//plugin.video.sickrage/icon.png))"])
            if xbmc.getCondVisibility("system.hasaddon(script.qlickplay)"):
                manage_list.append(["Search Youtube Videos", "RunScript(script.qlickplay,info=list,type=video,query="+title+")||Notification(YouTube Videos:,"+title+",5000,special://home/addons/script.qlickplay/resources/skins/Default/media/common/youtube.png)"])
            if xbmc.getCondVisibility("system.hasaddon(script.qlickplay)") and ADDON.getSetting("ExtendedYoutubeShow") == "true":
                manage_list.append(["Search Youtube Channels", "RunScript(script.qlickplay,info=list,type=channel,query="+title+")||Notification(YouTube Channels:,"+title+",5000,special://home/addons/script.qlickplay/resources/skins/Default/media/common/youtube.png)"])
            if xbmc.getCondVisibility("system.hasaddon(script.qlickplay)") and ADDON.getSetting("ExtendedYoutubeShow") == "true":
                manage_list.append(["Search Youtube Playlists", "RunScript(script.qlickplay,info=list,type=playlist,query="+title+")||Notification(YouTube Playlists:,"+title+",5000,special://home/addons/script.qlickplay/resources/skins/Default/media/common/youtube.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.1channel)"):
                manage_list.append(["Search 1Channel", "ActivateWindow(10025,&quot;plugin://plugin.video.1channel/?mode=Search&amp;section=movies&amp;query="+title+",return)||Notification(1Channel:,"+title+",5000,special://home/addons/plugin.video.1channel/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.exodus)"):
                manage_list.append(["Search Exodus", "ActivateWindow(10025,plugin://plugin.video.exodus/?action=tvSearch&query="+title+",return)||Notification(Exodus:,"+premocktitle+",5000,special://home/addons/plugin.video.exodus/icon.png)"])
#            if xbmc.getCondVisibility("system.hasaddon(plugin.video.genesis)"):
#                manage_list.append(["Search Genesis", "ActivateWindow(10025,plugin://plugin.video.genesis/?action=tvSearch&query="+title+",return)||Notification(Genesis:,"+premocktitle+",5000,special://home/addons/plugin.video.genesis/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(script.icechannel)"):
                manage_list.append(["Search iSTREAM", "ActivateWindow(10025,plugin://script.icechannel/?indexer=tv_shows&indexer_id&mode=search&search_term="+title+"&section=search&type=tv_seasons)||Notification(iSTREAM:,"+premocktitle+",5000,special://home/addons/script.icechannel/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.kmediatorrent)"):
                manage_list.append(["Search K-Media (ExtraTorrent)", "ActivateWindow(10025,plugin://plugin.video.kmediatorrent/extratorrent/search/?query="+title+",return)||Notification(K-Media:,"+premocktitle+",5000,special://home/addons/plugin.video.kmediatorrent/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.phstreams)"):
                manage_list.append(["Search Phoenix", "ActivateWindow(10025,plugin://plugin.video.phstreams/?action=addSearch&url="+premocktitle+",return)||Notification(Phoenix:,"+premocktitle+",5000,special://home/addons/plugin.video.phstreams/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.salts)"):
                manage_list.append(["Search SALTS", "ActivateWindow(10025,plugin://plugin.video.salts/?query="+title+"&section=TV&mode=search_results,return)||Notification(SALTS:,"+premocktitle+",5000,special://home/addons/plugin.video.salts/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.saltshd.lite)"):
                manage_list.append(["Search Salts HD Lite", "ActivateWindow(10025,plugin://plugin.video.saltshd.lite/?query="+title+"&section=TV&mode=search_results,return)||Notification(Salts HD Lite:,"+premocktitle+",5000,special://home/addons/plugin.video.saltshd.lite/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.saltsrd.lite)"):
                manage_list.append(["Search Salts RD Lite", "ActivateWindow(10025,plugin://plugin.video.saltsrd.lite/?query="+title+"&section=TV&mode=search_results,return)||Notification(Salts RD Lite:,"+premocktitle+",5000,special://home/addons/plugin.video.saltsrd.lite/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.specto)"):
                manage_list.append(["Search Specto", "ActivateWindow(10025,plugin://plugin.video.specto/?action=tvSearch&query="+title+",return)||Notification(Specto:,"+premocktitle+",5000,special://home/addons/plugin.video.specto/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.program.super.favourites)"):
                manage_list.append(["iSearch (Super Favourites)", "ActivateWindow(10025,plugin://plugin.program.super.favourites/?mode=0&keyword="+title+",return)||Notification(iSearch:,"+premocktitle+",5000,special://home/addons/plugin.program.super.favourites/icon.png)"])
            selection = xbmcgui.Dialog().select(heading=LANG(32188),
                                                list=[item[0] for item in manage_list])
            if dbid:
                if selection == 0 and xbmc.getCondVisibility("system.hasaddon(script.artwork.downloader)"):
                    artwork_list = []
                    artwork_call = "RunScript(script.artwork.downloader,%s)"
                    artwork_list += [[LANG(413), artwork_call % " mode=gui, mediatype=tvshow, dbid=%s" % dbid],
                                    [LANG(14061), artwork_call % " mediatype=tvshow, dbid=%s" % dbid],
                                    [LANG(32101), artwork_call % " mode=custom, mediatype=tvshow, dbid=%s, extrathumbs" % dbid],
                                    [LANG(32100), artwork_call % " mode=custom, mediatype=tvshow, dbid=%s, extrafanart" % dbid]]
                    selection = xbmcgui.Dialog().select(heading=LANG(32191),
                                    list=[i[0] for i in artwork_list])
                    if selection > -1:
                        for item in artwork_list[selection][1].split("||"):
                            xbmc.executebuiltin(item)
                elif selection > -1:
                    for item in manage_list[selection][1].split("||"):
                        self.close()
                        xbmc.executebuiltin(item)
            else:
                if selection > -1:
                    for item in manage_list[selection][1].split("||"):
                        if selection == 0 and xbmc.getCondVisibility("system.hasaddon(plugin.video.sickrage)"):
                            xbmc.executebuiltin(item)
                        else:
                            self.close()
                            xbmc.executebuiltin(item)

        @ch.click(445)
        def show_manage_dialog(self):
            manage_list = []
            title = self.info.get("TVShowTitle", "")
            # if xbmc.getCondVisibility("system.hasaddon(script.tvtunes)") and self.dbid:
            #     manage_list.append([LANG(32102), "RunScript(script.tvtunes,mode=solo&amp;tvpath=$ESCINFO[Window.Property(movie.FilenameAndPath)]&amp;tvname=$INFO[Window.Property(movie.TVShowTitle)])"])
            #if xbmc.getCondVisibility("system.hasaddon(script.libraryeditor)") and self.dbid:
            #    manage_list.append([LANG(32103), "RunScript(script.libraryeditor,DBID=" + self.dbid + ")"])
            manage_list.append([xbmc.getInfoLabel('System.AddonTitle(script.qlickplay)') + " " + LANG(32133), "Addon.OpenSettings(script.qlickplay)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.metalliq)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(plugin.video.metalliq)') + " " + LANG(32133), "Addon.OpenSettings(plugin.video.metalliq)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.1channel)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(plugin.video.1channel)') + " " + LANG(32133), "Addon.OpenSettings(plugin.video.1channel)"])
            if xbmc.getCondVisibility("system.hasaddon(script.artworkdownloader)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(script.artworkdownloader)') + " " + LANG(32133), "Addon.OpenSettings(script.artworkdownloader)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.couchpotato_manager)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(plugin.video.couchpotato_manager)') + " " + LANG(32133), "Addon.OpenSettings(plugin.video.couchpotato_manager)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.exodus)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(plugin.video.exodus)') + " " + LANG(32133), "Addon.OpenSettings(plugin.video.exodus)"])
#            if xbmc.getCondVisibility("system.hasaddon(plugin.video.genesis)"):
#                manage_list.append(["Genesis", "Addon.OpenSettings(plugin.video.genesis)"])
            if xbmc.getCondVisibility("system.hasaddon(script.icechannel)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(script.icechannel)') + " " + LANG(32133), "Addon.OpenSettings(script.icechannel)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.kmediatorrent)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(plugin.video.kmediatorrent)') + " " + LANG(32133), "Addon.OpenSettings(plugin.video.kmediatorrent)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.salts)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(plugin.video.salts)') + " " + LANG(32133), "Addon.OpenSettings(plugin.video.salts)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.pulsar)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(plugin.video.pulsar)') + " " + LANG(32133), "Addon.OpenSettings(plugin.video.pulsar)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.quasar)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(plugin.video.quasar)') + " " + LANG(32133), "Addon.OpenSettings(plugin.video.quasar)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.saltshd.lite)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(plugin.video.saltshd.lite)') + " " + LANG(32133), "Addon.OpenSettings(plugin.video.saltshd.lite)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.saltsrd.lite)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(plugin.video.saltsrd.lite)') + " " + LANG(32133), "Addon.OpenSettings(plugin.video.saltsrd.lite)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.theroyalwe)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(plugin.video.theroyalwe)') + " " + LANG(32133), "Addon.OpenSettings(plugin.video.theroyalwe)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.program.super.favourites)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(plugin.program.super.favourites)') + " " + LANG(32133), "Addon.OpenSettings(plugin.program.super.favourites)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.tv4me)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(plugin.video.tv4me)') + " " + LANG(32133), "Addon.OpenSettings(plugin.video.tv4me)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.phstreams)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(plugin.video.phstreams)') + " " + LANG(32133), "Addon.OpenSettings(plugin.video.phstreams)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.specto)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(plugin.video.specto)') + " " + LANG(32133), "Addon.OpenSettings(plugin.video.specto)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.whatthefurk)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(plugin.video.whatthefurk)') + " " + LANG(32133), "Addon.OpenSettings(plugin.video.whatthefurk)"])
            selection = xbmcgui.Dialog().select(heading=LANG(10004),
                                                list=[item[0] for item in manage_list])
            if selection == -1:
                return None
            for item in manage_list[selection][1].split("||"):
                xbmc.executebuiltin(item)

        @ch.click(6001)
        def set_rating(self):
            if set_rating_prompt(media_type="tv",
                                 media_id=self.info["id"]):
                self.update_states()

        @ch.click(6002)
        def open_list(self):
            index = xbmcgui.Dialog().select(heading=LANG(32136),
                                            list=[LANG(32144), LANG(32145)])
            if index == 0:
                wm.open_video_list(prev_window=self,
                                   media_type="tv",
                                   mode="favorites")
            elif index == 1:
                wm.open_video_list(prev_window=self,
                                   mode="rating",
                                   media_type="tv")
            else:
                wm.open_video_list(prev_window=self,
                                   mode="list",
                                   list_id=account_lists[index - 2]["id"],
                                   filter_label=account_lists[index - 2]["name"],
                                   force=True)

        @ch.click(6003)
        def toggle_fav_status(self):
            change_fav_status(media_id=self.info["id"],
                              media_type="tv",
                              status=str(not bool(self.account_states["favorite"])).lower())
            self.update_states()

        @ch.click(6006)
        def open_rated_items(self):
            wm.open_video_list(prev_window=self,
                               mode="rating",
                               media_type="tv")

        @ch.click(9)
        def play_tvshow_no_resume(self):
            if self.dbid:
                url = "special://profile/playlists/video/MetalliQ/TVShows/%s.xsp" % self.info.get("tvdb_id", "")
            else:
                url = "plugin://plugin.video.metalliq/tv/play/%s/1/1/default" % self.info.get("tvdb_id", "")
            PLAYER.qlickplay(url,
                             listitem=None,
                             window=self,
                             dbid=0)

        @ch.click(132)
        def open_text(self):
            wm.open_textviewer(header=LANG(32037),
                               text=self.info["Plot"],
                               color=self.info['ImageColor'])

        @ch.click(350)
        @ch.click(1150)
        def play_youtube_video(self):
            PLAYER.play_youtube_video(youtube_id=self.listitem.getProperty("youtube_id"),
                                      listitem=self.listitem,
                                      window=self)

        def update_states(self):
            xbmc.sleep(2000)  # delay because MovieDB takes some time to update
            _, __, self.account_states = extended_tvshow_info(tvshow_id=self.info["id"],
                                                              cache_time=0,
                                                              dbid=self.dbid)
            super(DialogTVShowInfo, self).update_states()

    return DialogTVShowInfo
