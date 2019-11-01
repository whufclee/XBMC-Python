# -*- coding: utf8 -*-

# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details

import urllib
import xbmc
import xbmcgui
from ..Utils import *
from ..TheMovieDB import *
from ..omdb import *
from ..ImageTools import *
import threading
from DialogBaseInfo import DialogBaseInfo
from ..WindowManager import wm
from ..OnClickHandler import OnClickHandler
from .. import VideoPlayer

PLAYER = VideoPlayer.VideoPlayer()
ch = OnClickHandler()


def get_movie_window(window_type):

    class DialogVideoInfo(DialogBaseInfo, window_type):

        def __init__(self, *args, **kwargs):
            super(DialogVideoInfo, self).__init__(*args, **kwargs)
            self.type = "Movie"
            data = extended_movie_info(movie_id=kwargs.get('id'),
                                       dbid=self.dbid)
            if not data:
                return None
            self.info, self.data, self.account_states = data
            sets_thread = SetItemsThread(self.info["SetId"])
            self.omdb_thread = FunctionThread(get_omdb_movie_info, self.info["imdb_id"])
            lists_thread = FunctionThread(self.sort_lists, self.data["lists"])
            filter_thread = FilterImageThread(self.info.get("thumb", ""), 25)
            for thread in [self.omdb_thread, sets_thread, lists_thread, filter_thread]:
                thread.start()
            if "dbid" not in self.info:
                self.info['poster'] = get_file(self.info.get("poster", ""))
            sets_thread.join()
            self.setinfo = sets_thread.setinfo
            self.data["similar"] = [i for i in self.data["similar"] if i["id"] not in sets_thread.id_list]
            filter_thread.join()
            self.info['ImageFilter'] = filter_thread.image
            self.info['ImageColor'] = filter_thread.imagecolor
            lists_thread.join()
            self.listitems = [(1000, self.data["actors"]),
                              (150, self.data["similar"]),
                              (250, sets_thread.listitems),
                              (450, lists_thread.listitems),
                              (550, self.data["studios"]),
                              (650, merge_with_cert_desc(self.data["releases"], "movie")),
                              (750, merge_dict_lists(self.data["crew"])),
                              (850, self.data["genres"]),
                              (950, self.data["keywords"]),
                              (1050, self.data["reviews"]),
                              (1150, self.data["videos"]),
                              (1250, self.data["images"]),
                              (1350, self.data["backdrops"])]

        def onInit(self):
            super(DialogVideoInfo, self).onInit()
            pass_dict_to_skin(data=self.info,
                              prefix="movie.",
                              window_id=self.window_id)
            super(DialogVideoInfo, self).update_states()
            self.get_youtube_vids("%s %s, movie" % (self.info["Label"], self.info["year"]))
            self.fill_lists()
            pass_dict_to_skin(data=self.setinfo,
                              prefix="movie.set.",
                              window_id=self.window_id)
            self.join_omdb_async()

        def onClick(self, control_id):
            super(DialogVideoInfo, self).onClick(control_id)
            ch.serve(control_id, self)

        def onAction(self, action):
            super(DialogVideoInfo, self).onAction(action)
            ch.serve_action(action, self.getFocusId(), self)

        @ch.action("contextmenu", 150)
        @ch.action("contextmenu", 250)
        def add_movie_to_account(self):
            movie_id = self.listitem.getProperty("id")
            add_movie_to_list(movie_id)

        @ch.click(10)
        def play_trailer(self):
            PLAYER.play_youtube_video(youtube_id=self.getControl(1150).getListItem(0).getProperty("youtube_id"),
                                      window=self)

        @ch.click(1000)
        @ch.click(750)
        def open_actor_info(self):
            wm.open_actor_info(prev_window=self,
                               actor_id=self.listitem.getProperty("id"))

        @ch.click(150)
        @ch.click(250)
        def open_movie_info(self):
            wm.open_movie_info(prev_window=self,
                               movie_id=self.listitem.getProperty("id"),
                               dbid=self.listitem.getProperty("dbid"))

        @ch.click(10)
        def play_trailer(self):
            PLAYER.play_youtube_video(youtube_id=youtube_id,
                                      listitem=self.getControl(1150).getListItem(0).getProperty("youtube_id"),
                                      window=self)

        @ch.click(350)
        @ch.click(1150)
        def play_youtube_video(self):
            PLAYER.play_youtube_video(youtube_id=self.listitem.getProperty("youtube_id"),
                                      listitem=self.listitem,
                                      window=self)

        @ch.click(550)
        def open_company_list(self):
            filters = [{"id": self.listitem.getProperty("id"),
                        "type": "with_companies",
                        "typelabel": LANG(20388),
                        "label": self.listitem.getLabel().decode("utf-8")}]
            wm.open_video_list(prev_window=self,
                               filters=filters)

        @ch.click(1050)
        def show_review(self):
            author = self.listitem.getProperty("author")
            text = "[B]%s[/B][CR]%s" % (author, clean_text(self.listitem.getProperty("content")))
            wm.open_textviewer(header=LANG(207),
                               text=text,
                               color=self.info['ImageColor'])

        @ch.click(950)
        def open_keyword_list(self):
            filters = [{"id": self.listitem.getProperty("id"),
                        "type": "with_keywords",
                        "typelabel": LANG(32114),
                        "label": self.listitem.getLabel().decode("utf-8")}]
            wm.open_video_list(prev_window=self,
                               filters=filters)

        @ch.click(850)
        def open_genre_list(self):
            filters = [{"id": self.listitem.getProperty("id"),
                        "type": "with_genres",
                        "typelabel": LANG(135),
                        "label": self.listitem.getLabel().decode("utf-8")}]
            print "QQQQQ"+str(filters)
            wm.open_video_list(prev_window=self,
                               filters=filters)

        @ch.click(650)
        def open_cert_list(self):
            filters = [{"id": self.listitem.getProperty("iso_3166_1"),
                        "type": "certification_country",
                        "typelabel": LANG(32153),
                        "label": self.listitem.getProperty("iso_3166_1")},
                       {"id": self.listitem.getProperty("certification"),
                        "type": "certification",
                        "typelabel": LANG(32127),
                        "label": self.listitem.getProperty("certification")},
                       {"id": self.listitem.getProperty("year"),
                        "type": "year",
                        "typelabel": LANG(345),
                        "label": self.listitem.getProperty("year")}]
            wm.open_video_list(prev_window=self,
                               filters=filters)

        @ch.click(450)
        def open_lists_list(self):
            wm.open_video_list(prev_window=self,
                               mode="list",
                               list_id=self.listitem.getProperty("id"),
                               filter_label=self.listitem.getLabel())

        @ch.click(6002)
        def show_list_dialog(self):
            listitems = [LANG(32134), LANG(32135)]
            xbmc.executebuiltin("ActivateWindow(busydialog)")
            account_lists = get_account_lists()
            for item in account_lists:
                listitems.append("%s (%i)" % (item["name"], item["item_count"]))
            xbmc.executebuiltin("Dialog.Close(busydialog)")
            index = xbmcgui.Dialog().select(LANG(32136), listitems)
            if index == -1:
                pass
            elif index == 0:
                wm.open_video_list(prev_window=self,
                                   mode="favorites")
            elif index == 1:
                wm.open_video_list(prev_window=self,
                                   mode="rating")
            else:
                wm.open_video_list(prev_window=self,
                                   mode="list",
                                   list_id=account_lists[index - 2]["id"],
                                   filter_label=account_lists[index - 2]["name"],
                                   force=True)

        @ch.click(132)
        def show_plot(self):
            wm.open_textviewer(header=LANG(207),
                               text=self.info["Plot"],
                               color=self.info['ImageColor'])

        @ch.click(6001)
        def set_rating_dialog(self):
            if set_rating_prompt("movie", self.info["id"]):
                self.update_states()

        @ch.click(6005)
        def add_to_list_dialog(self):
            xbmc.executebuiltin("ActivateWindow(busydialog)")
            account_lists = get_account_lists()
            listitems = ["%s (%i)" % (i["name"], i["item_count"]) for i in account_lists]
            listitems.insert(0, LANG(32139))
            listitems.append(LANG(32138))
            xbmc.executebuiltin("Dialog.Close(busydialog)")
            index = xbmcgui.Dialog().select(heading=LANG(32136),
                                            list=listitems)
            if index == 0:
                listname = xbmcgui.Dialog().input(heading=LANG(32137),
                                                  type=xbmcgui.INPUT_ALPHANUM)
                if not listname:
                    return None
                list_id = create_list(listname)
                xbmc.sleep(1000)
                change_list_status(list_id=list_id,
                                   movie_id=self.info["id"],
                                   status=True)
            elif index == len(listitems) - 1:
                self.remove_list_dialog(account_lists)
            elif index > 0:
                change_list_status(account_lists[index - 1]["id"], self.info["id"], True)
                self.update_states()

        @ch.click(6003)
        def change_list_status(self):
            change_fav_status(media_id=self.info["id"],
                              media_type="movie",
                              status=str(not bool(self.account_states["favorite"])).lower())
            self.update_states()

        @ch.click(6006)
        def open_rating_list(self):
            wm.open_video_list(prev_window=self,
                               mode="rating")

        #@ch.click(9)
        def play_movie_resume(self):
            self.close()
            get_kodi_json(method="Player.Open",
                          params='{"item": {"movieid": %s}, "options":{"resume": %s}}' % (self.info['dbid'], "true"))

        @ch.click(8)
        def play_movie_no_resume(self):
            if self.dbid:
                dbid = self.dbid
                url = "temp"
            else:
                dbid = 0
                url = "plugin://plugin.video.metalliq/movies/play/tmdb/%s/default" % self.info.get("id", "")
            PLAYER.qlickplay(url,
                             listitem=None,
                             window=self,
                             dbid=dbid)

        @ch.click(11)
        def add_play_movie(self):
            title = self.info.get("title", "")
            xbmc.executebuiltin("Skin.SetString(MovieSearch,"+title+")")
            dialog = xbmcgui.Dialog()
            movie_id = str(self.info.get("dbid", ""))
            extended_play_list = []
            extended_add_list = []
            chosen_add_addon = "na"
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
            if xbmc.getCondVisibility("system.hasaddon(plugin.program.super.favourites)"):
                extended_play_list.append("iSearch")
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
            if xbmc.getCondVisibility("system.hasaddon(script.qlickplay)"):
                extended_play_list.append("Trailer")
            if ADDON.getSetting("AddOrPlayMovie") == "add" or ADDON.getSetting("AutoAddMovie") == "true":
                if len(extended_add_list) <= 0:
                    chosen_add_addon = "na"
                elif len(extended_add_list) == 1:
                    chosen_add_addon = extended_add_list[0]
                else:
                    if ADDON.getSetting("LibraryAddonMovie") in extended_add_list:
                        chosen_add_addon = ADDON.getSetting("LibraryAddonMovie")
                    else:
                        dialog = xbmcgui.Dialog()
                        chosen_add_addon_id = dialog.select(LANG(32187), extended_add_list)
                        chosen_add_addon = extended_add_list[chosen_add_addon_id]
            if len(extended_play_list) == 1:
                chosen_play_addon = extended_play_list[0]
            else:
                if ADDON.getSetting("MainAddonMovie") in extended_play_list:
                    chosen_play_addon = ADDON.getSetting("MainAddonMovie")
                else:
                    if ADDON.getSetting("AlternateAddonMovie") in extended_play_list:
                        chosen_play_addon = ADDON.getSetting("AlternateAddonMovie")
                    else:
                        if ADDON.getSetting("AddOrPlayMovie") == "play":
                            dialog = xbmcgui.Dialog()
                            chosen_play_addon_id = dialog.select(LANG(32185), extended_play_list)
                            chosen_play_addon = extended_play_list[chosen_play_addon_id]
                        else:
                            chosen_play_addon = ""
            churl = "na"
            if chosen_add_addon == "na":
                add = "na"
#            elif chosen_add_addon == 'Genesis':
#                add = "plugin://plugin.video.genesis/?action=movieToLibrary&name=%s&title=%s&year=%s&imdb=%s&tmdb=%s" % (urllib.quote_plus(self.info.get("title", "") + ' (' + self.info.get("year", "") + ')'), urllib.quote_plus(self.info.get("title", "")), self.info.get("year", ""), self.info.get("imdb_id", ""), self.info.get("tmdb_id", ""))
            elif chosen_add_addon == "iSTREAM":
                add = "plugin://script.icechannel/?name=%s&title=%s&item_title=%s&video_type=movie&indexer=movies&imdb_id=%s&mode=add_to_library&url=%s&year=%s&item_mode=file_hosts&type=movies&library=true" % (urllib.quote_plus(self.info.get("title", "") + ' '), urllib.quote_plus(self.info.get("title", "") + '  (' + self.info.get("year", "") + ')'), urllib.quote_plus(self.info.get("title", "") + '  (' + self.info.get("year", "") + ')'), self.info.get("imdb_id", ""), urllib.quote_plus("http://imdb.com/title/" + self.info.get("imdb_id", "")), self.info.get("year", ""))
            elif chosen_add_addon == "Quasar":
                add = "plugin://plugin.video.quasar/library/movie/add/%s" % self.info.get("tmdb_id", "")
            elif chosen_add_addon == "SALTS":
                add = "plugin://plugin.video.salts/?title=%s&video_type=Movie&trakt_id=%s&mode=add_to_library&dialog=True&year=%s" % (urllib.quote_plus(self.info.get("title", "")), self.info.get("trakt_id", ""), self.info.get("year", ""))
            elif chosen_add_addon == "Salts HD Lite":
                add = "plugin://plugin.video.saltshd.lite/?title=%s&video_type=Movie&trakt_id=%s&mode=add_to_library&dialog=True&year=%s" % (urllib.quote_plus(self.info.get("title", "")), self.info.get("trakt_id", ""), self.info.get("year", ""))
            elif chosen_add_addon == "Salts RD Lite":
                add = "plugin://plugin.video.saltsrd.lite/?title=%s&video_type=Movie&trakt_id=%s&mode=add_to_library&dialog=True&year=%s" % (urllib.quote_plus(self.info.get("title", "")), self.info.get("trakt_id", ""), self.info.get("year", ""))
            elif chosen_add_addon == 'Specto':
                add = "plugin://plugin.video.specto/?action=movieToLibrary&name=%s&title=%s&year=%s&imdb=%s&tmdb=%s" % (urllib.quote_plus(self.info.get("title", "") + ' (' + self.info.get("year", "") + ')'), urllib.quote_plus(self.info.get("title", "")), self.info.get("year", ""), self.info.get("imdb_id", ""), self.info.get("tmdb_id", ""))
            elif chosen_add_addon == '1Channel':
                churl='http://www.primewire.ag/'
                link = requests.get(churl).content
                key=regex_from_to(link,'"hidden" name="key" value="', '"')
                churl='http://www.primewire.ag/index.php?search_keywords=%s&key=%s&search_section=1' % (title,key)
                link = requests.get(churl).content
                churl=regex_from_to(link,'index_item index_item_ie"><a href="','"').replace('-online-free','')
                add = "plugin://plugin.video.1channel/?img=http%%3A%%2F%%2Fimages.primewire.ag%%2Fthumbs%%2F2%s_%s.jpg&title=%s&url=%%2F%s&video_type=movie&mode=add_to_library&year=%s" % (churl.replace('watch-',''), self.info.get("year", ""), urllib.quote_plus(self.info.get("title", "")), churl, self.info.get("year", ""))
            if chosen_play_addon == 'Exodus':
                url = "plugin://plugin.video.exodus/?action=play&title=%s&year=%s&imdb=%s&tmdb=%s&meta=" % (urllib.quote_plus(self.info.get("title", "")), self.info.get("year", ""), self.info.get("imdb_id", ""), self.info.get("tmdb_id", ""))
#            elif chosen_play_addon == 'Genesis':
#                url = "plugin://plugin.video.genesis/?action=play&name=%s&title=%s&year=%s&imdb=%s&tmdb=%s" % (urllib.quote_plus(self.info.get("title", "") + ' (' + self.info.get("year", "") + ')'), urllib.quote_plus(self.info.get("title", "")), self.info.get("year", ""), self.info.get("imdb_id", ""), self.info.get("tmdb_id", ""))
            elif chosen_play_addon == "iSTREAM":
                url = "plugin://script.icechannel/?name=%s&title=%s&item_title=%s&video_type=movie&indexer=movies&imdb_id=%s&mode=file_hosts&url=%s&year=%s&item_mode=file_hosts&type=movies&library=true" % (urllib.quote_plus(self.info.get("title", "") + ' '), urllib.quote_plus(self.info.get("title", "") + '  (' + self.info.get("year", "") + ')'), urllib.quote_plus(self.info.get("title", "") + '  (' + self.info.get("year", "") + ')'), self.info.get("imdb_id", ""), urllib.quote_plus("http://imdb.com/title/" + self.info.get("imdb_id", "")), self.info.get("year", ""))
            elif chosen_play_addon == "SALTS":
                url = "plugin://plugin.video.salts/?title=%s&video_type=Movie&trakt_id=%s&mode=get_sources&dialog=True&year=%s" % (urllib.quote_plus(self.info.get("title", "")), self.info.get("trakt_id", ""), self.info.get("year", ""))
            elif chosen_play_addon == "Salts HD Lite":
                url = "plugin://plugin.video.saltshd.lite/?title=%s&video_type=Movie&trakt_id=%s&mode=get_sources&dialog=True&year=%s" % (urllib.quote_plus(self.info.get("title", "")), self.info.get("trakt_id", ""), self.info.get("year", ""))
            elif chosen_play_addon == "Salts RD Lite":
                url = "plugin://plugin.video.saltsrd.lite/?title=%s&video_type=Movie&trakt_id=%s&mode=get_sources&dialog=True&year=%s" % (urllib.quote_plus(self.info.get("title", "")), self.info.get("trakt_id", ""), self.info.get("year", ""))
            elif chosen_play_addon == "Phoenix":
                url = "plugin://plugin.video.phstreams/?action=addSearch&url=%s" % self.info.get("title", "")
            elif chosen_play_addon == "Pulsar":
                url = "plugin://plugin.video.pulsar/movie/%s/%s" % (self.info.get("imdb_id", ""), ADDON.getSetting("PulsarModeMovie"))
            elif chosen_play_addon == "Quasar":
                url = "plugin://plugin.video.quasar/movie/%s/%s" % (self.info.get("id", ""), ADDON.getSetting("PulsarModeMovie"))
            elif chosen_play_addon == 'Specto':
                url = "plugin://plugin.video.specto/?action=play&name=%s&title=%s&year=%s&imdb=%s&tmdb=%s" % (urllib.quote_plus(self.info.get("title", "") + ' (' + self.info.get("year", "") + ')'), urllib.quote_plus(self.info.get("title", "")), self.info.get("year", ""), self.info.get("imdb_id", ""), self.info.get("tmdb_id", ""))
            elif chosen_play_addon == '1Channel':
                if churl != "na":
                    pass
                else:
                    churl='http://www.primewire.ag/'
                    link = requests.get(churl).content
                    key=regex_from_to(link,'"hidden" name="key" value="', '"')
                    churl='http://www.primewire.ag/index.php?search_keywords=%s&key=%s&search_section=1' % (title,key)
                    link = requests.get(churl).content
                    churl=regex_from_to(link,'index_item index_item_ie"><a href="','"').replace('-online-free','')
                url = "plugin://plugin.video.1channel/?img=http%%3A%%2F%%2Fimages.primewire.ag%%2Fthumbs%%2F%s_%s.jpg&title=%s&url=%%2F%s&imdbnum=&video_type=movie&mode=GetSources&dialog=1&year=%s" % (churl.replace('watch-',''), self.info.get("year", ""), urllib.quote_plus(self.info.get("title", "")), churl, self.info.get("year", ""))
            elif chosen_play_addon == 'UMP':
                url = "plugin://plugin.program.ump/?info=%%7B%%22status%%22%%3A+%%22%%22%%2C+%%22rating%%22%%3A+%%22%%22%%2C+%%22plotoutline%%22%%3A+%%22%%22%%2C+%%22code%%22%%3A+%%22%s%%22%%2C+%%22tagline%%22%%3A+%%22%%22%%2C+%%22season%%22%%3A+-1%%2C+%%22tvshowtitle%%22%%3A+%%22%%22%%2C+%%22artist%%22%%3A+%%5B%%5D%%2C+%%22aired%%22%%3A+%%22%%22%%2C+%%22tvshowalias%%22%%3A+%%22%%22%%2C+%%22director%%22%%3A+%%22%%22%%2C+%%22duration%%22%%3A+%%22%%22%%2C+%%22localtitle%%22%%3A+%%22%s%%22%%2C+%%22studio%%22%%3A+%%22%%22%%2C+%%22year%%22%%3A+%s%%2C+%%22genre%%22%%3A+%%22%%22%%2C+%%22tracknumber%%22%%3A+-1%%2C+%%22lastplayed%%22%%3A+%%22%%22%%2C+%%22album%%22%%3A+%%22%%22%%2C+%%22alternates%%22%%3A+%%5B%%22%%22%%5D%%2C+%%22count%%22%%3A+1%%2C+%%22plot%%22%%3A+%%22%%22%%2C+%%22votes%%22%%3A+%%22%%22%%2C+%%22castandrole%%22%%3A+%%5B%%22%%22%%5D%%2C+%%22episode%%22%%3A+-1%%2C+%%22overlay%%22%%3A+0%%2C+%%22credits%%22%%3A+%%22%%22%%2C+%%22mpaa%%22%%3A+%%22%%22%%2C+%%22title%%22%%3A+%%22%s%%22%%2C+%%22premiered%%22%%3A+%%22%%22%%2C+%%22originaltitle%%22%%3A+%%22%s%%22%%2C+%%22cast%%22%%3A+%%5B%%22%%22%%5D%%2C+%%22write%%22%%3A+%%22%%22%%2C+%%22sorttitle%%22%%3A+%%22%%22%%2C+%%22playcount%%22%%3A+-1%%2C+%%22size%%22%%3A+0%%2C+%%22top250%%22%%3A+-1%%2C+%%22trailer%%22%%3A+%%22%%22%%2C+%%22dateadded%%22%%3A+%%22%%22%%7D&art=%%7B%%22thumb%%22%%3A+%%22%%22%%2C+%%22fanart%%22%%3A+%%22%%22%%2C+%%22poster%%22%%3A+%%22%%22%%2C+%%22clearlogo%%22%%3A+%%22%%22%%2C+%%22landscape%%22%%3A+%%22%%22%%2C+%%22banner%%22%%3A+%%22%%22%%2C+%%22clearart%%22%%3A+%%22%%22%%7D&args=%%7B%%7D&module=imdb&content_type=video&page=urlselect" % (self.info.get("imdb_id", ""), urllib.quote_plus(self.info.get("title", "")), self.info.get("year", ""), urllib.quote_plus(self.info.get("title", "")), urllib.quote_plus(self.info.get("title", "")))
            elif chosen_play_addon == 'The Royal We':
                url = "plugin://plugin.video.theroyalwe/?title=%s&year=%s&mode=play_movie&tmdb_id=%s&imdb_id=%s" % (urllib.quote_plus(self.info.get("title", "")), self.info.get("year", ""), self.info.get("id", ""), self.info.get("imdb_id", ""))
            elif chosen_play_addon == "iSearch" and ADDON.getSetting("CustomIsearchMovie") == "true":
                url = "plugin://plugin.program.super.favourites/?label=MovieSearch&mode=400&path=special://home/addons/script.qlickplay/resources/extras/movie/"
            elif chosen_play_addon == "iSearch" and ADDON.getSetting("CustomIsearchMovie") == "false":
                url = "plugin://plugin.program.super.favourites/?mode=0&keyword=%s" % self.info.get("title", "")
            elif chosen_play_addon == "Trailer":
                url = "plugin://script.qlickplay/?info=playtrailer&id=%s" % self.info.get("id", "")
            if ADDON.getSetting("AddOrPlayMovie") == "add" or ADDON.getSetting("AutoAddMovie") == "true":
                if add == "na":
                    xbmc.executebuiltin("Notification(Install SALTS (HD/RD lite)/iSTREAM/Specto,To Add To Library,8000,special://home/addons/script.qlickplay/icon.png)")
                else:
                    xbmc.executebuiltin("RunPlugin(%s)" % add)
#                    if movie_id:
#                        pass
#                    else:
#                        xbmc.executebuiltin("RunScript(script.qlickplay,info=deletecache)")
            if ADDON.getSetting("AddOrPlayMovie") == "play":
                PLAYER.qlickplay(chosen_play_addon,
                                 url,
                                 listitem=None,
                                 window=self)

        @ch.click(19)
        def appintegration_movie(self):
            manage_list = []
            movie_id = str(self.info.get("dbid", ""))
            tmdb_id = str(self.info.get("id", ""))
            imdb_id = str(self.info.get("imdb_id", ""))
            year = str(self.info.get("year", ""))
            premocktitle = self.info.get("title", "")
            mocktitle = premocktitle.replace("&", "%26")
            title = mocktitle.encode('utf-8')
            language = xbmc.getLanguage()
            if movie_id:
                if xbmc.getCondVisibility("system.hasaddon(script.artwork.downloader)"):
                    manage_list.append(["Download Artwork", "RunScript(script.artwork.downloader,mediatype=movie,dbid="+movie_id+")||Notification(Artwork Downloader:,"+title+",5000,special://home/addons/script.artwork.downloader/icon.png)"])
            if not movie_id and xbmc.getCondVisibility("system.hasaddon(plugin.video.couchpotato_manager)"):
                manage_list.append([LANG(32165), "RunPlugin(plugin://plugin.video.couchpotato_manager/movies/add?imdb_id="+imdb_id+")||Notification(Couch Potato,"+title+",5000,special://home/addons/plugin.video.couchpotato_manager/icon.png))"])
            if xbmc.getCondVisibility("system.hasaddon(script.qlickplay)"):
                manage_list.append(["Search Youtube Videos", "RunScript(script.qlickplay,info=list,type=video,query="+title+")||Notification(YouTube Videos:,"+title+",5000,special://home/addons/script.qlickplay/resources/skins/Default/media/common/youtube.png)"])
            if xbmc.getCondVisibility("system.hasaddon(script.qlickplay)") and ADDON.getSetting("ExtendedYoutubeMovie") == "true":
                manage_list.append(["Search Youtube Channels", "RunScript(script.qlickplay,info=list,type=channel,query="+title+")||Notification(YouTube Channels:,"+title+",5000,special://home/addons/script.qlickplay/resources/skins/Default/media/common/youtube.png)"])
            if xbmc.getCondVisibility("system.hasaddon(script.qlickplay)") and ADDON.getSetting("ExtendedYoutubeMovie") == "true":
                manage_list.append(["Search Youtube Playlists", "RunScript(script.qlickplay,info=list,type=playlist,query="+title+")||Notification(YouTube Playlists:,"+title+",5000,special://home/addons/script.qlickplay/resources/skins/Default/media/common/youtube.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.exodus)"):
                manage_list.append(["Search Exodus", "ActivateWindow(10025,plugin://plugin.video.exodus/?action=movieSearch&query="+title+",return)||Notification(Exodus:,"+title+",5000,special://home/addons/plugin.video.exodus/icon.png)"])
#            if xbmc.getCondVisibility("system.hasaddon(plugin.video.genesis)"):
#                manage_list.append(["Search Genesis", "ActivateWindow(10025,plugin://plugin.video.genesis/?action=movieSearch&query="+title+",return)||Notification(Genesis:,"+title+",5000,special://home/addons/plugin.video.genesis/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(script.icechannel)"):
                manage_list.append(["Search iSTREAM", "ActivateWindow(10025,plugin://script.icechannel/?indexer=movies&indexer_id&mode=search&search_term="+title+"&section=search&type=movies)||Notification(iSTREAM:,"+title+",5000,special://home/addons/script.icechannel/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.salts)"):
                manage_list.append(["Search SALTS", "ActivateWindow(10025,plugin://plugin.video.salts/?query="+title+"&section=Movies&mode=search_results,return)||Notification(SALTS:,"+title+",5000,special://home/addons/plugin.video.salts/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.saltshd.lite)"):
                manage_list.append(["Search Salts HD Lite", "ActivateWindow(10025,plugin://plugin.video.saltshd.lite/?query="+title+"&section=Movies&mode=search_results,return)||Notification(Salts HD Lite:,"+title+",5000,special://home/addons/plugin.video.saltshd.lite/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.saltsrd.lite)"):
                manage_list.append(["Search Salts RD Lite", "ActivateWindow(10025,plugin://plugin.video.saltsrd.lite/?query="+title+"&section=Movies&mode=search_results,return)||Notification(Salts RD Lite:,"+title+",5000,special://home/addons/plugin.video.saltsrd.lite/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.specto)"):
                manage_list.append(["Search Specto", "ActivateWindow(10025,plugin://plugin.video.specto/?action=movieSearch&query="+title+",return)||Notification(Specto:,"+title+",5000,special://home/addons/plugin.video.specto/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.1channel)"):
                manage_list.append(["Search 1Channel", "ActivateWindow(10025,&quot;plugin://plugin.video.1channel/?mode=Search&amp;section=movies&amp;query="+title+",return)||Notification(1Channel:,"+title+",5000,special://home/addons/plugin.video.1channel/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.theroyalwe)"):
                manage_list.append(["Search The Royal We", "ActivateWindow(10025,plugin://plugin.video.theroyalwe/?query="+title+"&section=Movies&mode=search_results,return)||Notification(The Royal We:,"+title+",5000,special://home/addons/plugin.video.theroyalwe/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.phstreams)"):
                manage_list.append(["Search Phoenix", "ActivateWindow(10025,plugin://plugin.video.phstreams/?action=addSearch&url="+title+",return)||Notification(Phoenix:,"+title+",5000,special://home/addons/plugin.video.phstreams/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.pulsar)"):
                manage_list.append(["Search Pulsar", "PlayMedia(plugin://plugin.video.pulsar/movie/"+imdb_id+"/links)||Notification(Pulsar:,"+title+",5000,special://home/addons/plugin.video.pulsar/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.quasar)"):
                manage_list.append(["Search Quasar", "PlayMedia(plugin://plugin.video.quasar/movie/"+tmdb_id+"/links)||Notification(Quasar:,"+title+",5000,special://home/addons/plugin.video.quasar/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(script.search.play2kd)") and language == 'Dutch':
                manage_list.append(["NL [COLOR FFF35C9F]Search+Play[/COLOR]2KD", "RunScript(script.search.play2kd,type=1,query="+title+" gesproken)||Notification([COLOR FFF35C9F]Search+Play[/COLOR]2KD:,"+title+",5000,special://home/addons/script.search.play2kd/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(script.search.play2kd)"):
                manage_list.append(["[COLOR FFF35C9F]Search+Play[/COLOR]2KD", "RunScript(script.search.play2kd,type=1,query="+title+")||Notification([COLOR FFF35C9F]Search+Play[/COLOR]2KD:,"+title+",5000,special://home/addons/script.search.play2kd/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.kmediatorrent)") and language == 'Dutch':
                manage_list.append(["NL K-Search (KickAss)", "ActivateWindow(10025,plugin://plugin.video.kmediatorrent/kat/browse/usearch/"+title+"%2520gesproken%2520%2520verified%253A1/1/seeders/desc,return)||Notification(K-Search NL:,"+title+",5000,special://home/addons/plugin.video.kmediatorrent/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.kmediatorrent)"):
                manage_list.append(["K-Search (KickAss)", "ActivateWindow(10025,plugin://plugin.video.kmediatorrent/kat/browse/usearch/"+title+"2520verified%253A1/1/seeders/desc,return)||Notification(K-Search KickAss:,"+title+",5000,special://home/addons/plugin.video.kmediatorrent/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.kmediatorrent)"):
                manage_list.append(["K-Search Yify", "ActivateWindow(10025,plugin://plugin.video.kmediatorrent/yify/search/"+title+"/1,return)||Notification(K-Search Yify:,"+title+",5000,special://home/addons/plugin.video.kmediatorrent/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.kmediatorrent)"):
                manage_list.append(["K-Search ExtraTorrent", "ActivateWindow(10025,plugin://plugin.video.kmediatorrent/extratorrent/search/?query="+title+",return)||Notification(K-Search ExtraTorrent:,"+title+",5000,special://home/addons/plugin.video.kmediatorrent/icon.png)"])
            #if xbmc.getCondVisibility("system.hasaddon(plugin.video.filmdictator)"):
            #    manage_list.append(["FilmDictator", "ActivateWindow(10025,plugin://plugin.video.filmdictator/?mode=5&url=url&query="+title+",return)||Notification(FilmDictator:,"+title+",5000,special://home/addons/plugin.video.filmdictator/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.yifymovies.hd)"):
                manage_list.append(["Search Yifymovies HD", "ActivateWindow(10025,plugin://plugin.video.yifymovies.hd/?action=movies_search&query="+title+",return)||Notification(YifyFind:,"+title+",5000,special://home/addons/plugin.video.yifymovies.hd/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.program.super.favourites)"):
                manage_list.append(["iSearch (Super Favourites)", "ActivateWindow(10025,plugin://plugin.program.super.favourites/?mode=0&keyword="+title+",return)||Notification(iSearch:,"+title+",5000,special://home/addons/plugin.program.super.favourites/icon.png)"])
            selection = xbmcgui.Dialog().select(heading=LANG(32188),
                                                list=[i[0] for i in manage_list])
            if movie_id:
                if selection == 0 and xbmc.getCondVisibility("system.hasaddon(script.artwork.downloader)"):
                    artwork_list = []
                    artwork_call = "RunScript(script.artwork.downloader,%s)"
                    artwork_list += [[LANG(413), artwork_call % " mode=gui, mediatype=movie, dbid=%s" % movie_id],
                                    [LANG(14061), artwork_call % " mediatype=movie, dbid=%s" % movie_id],
                                    [LANG(32101), artwork_call % " mode=custom, mediatype=movie, dbid=%s, extrathumbs" % movie_id],
                                    [LANG(32100), artwork_call % " mode=custom, mediatype=movie, dbid=%s, extrafanart" % movie_id]]
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
                        if selection == 0 and xbmc.getCondVisibility("system.hasaddon(plugin.video.couchpotato_manager)"):
                            xbmc.executebuiltin(item)
                        else:
                            self.close()
                            xbmc.executebuiltin(item)

        @ch.click(445)
        def show_manage_dialog(self):
            manage_list = []
            movie_id = str(self.info.get("dbid", ""))
            imdb_id = str(self.info.get("imdb_id", ""))
            #if movie_id:
            #    artwork_call = "RunScript(script.artwork.downloader,%s)"
            #    manage_list += [[LANG(413), artwork_call % " mode=gui, mediatype=movie, dbid=%s" % movie_id],
            #                    [LANG(14061), artwork_call % " mediatype=movie, dbid=%s" % movie_id],
            #                    [LANG(32101), artwork_call % " mode=custom, mediatype=movie, dbid=%s, extrathumbs" % movie_id],
            #                    [LANG(32100), artwork_call % " mode=custom, mediatype=movie, dbid=%s, extrafanart" % movie_id]]
            #else:
            #    manage_list += [[LANG(32165), "RunPlugin(plugin://plugin.video.couchpotato_manager/movies/add?imdb_id=" + imdb_id + ")||Notification(script.qlickplay,%s))" % LANG(32059)]]
            #if xbmc.getCondVisibility("system.hasaddon(script.libraryeditor)") and movie_id:
            #    manage_list.append([LANG(32103), "RunScript(script.libraryeditor,DBID=" + movie_id + ")"])
            manage_list.append([xbmc.getInfoLabel('System.AddonTitle(script.qlickplay)') + " " + LANG(32133), "Addon.OpenSettings(script.qlickplay)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.metalliq)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(plugin.video.metalliq)') + " " + LANG(32133), "Addon.OpenSettings(plugin.video.metalliq)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.exodus)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(plugin.video.exodus)') + " " + LANG(32133), "Addon.OpenSettings(plugin.video.exodus)"])
#            if xbmc.getCondVisibility("system.hasaddon(plugin.video.genesis)"):
#                manage_list.append(["Genesis", "Addon.OpenSettings(plugin.video.genesis)"])
            if xbmc.getCondVisibility("system.hasaddon(script.icechannel)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(script.icechannel)') + " " + LANG(32133), "Addon.OpenSettings(script.icechannel)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.salts)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(plugin.video.salts)') + " " + LANG(32133), "Addon.OpenSettings(plugin.video.salts)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.saltshd.lite)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(plugin.video.saltshd.lite)') + " " + LANG(32133), "Addon.OpenSettings(plugin.video.saltshd.lite)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.saltsrd.lite)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(plugin.video.saltsrd.lite)') + " " + LANG(32133), "Addon.OpenSettings(plugin.video.saltsrd.lite)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.theroyalwe)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(plugin.video.theroyalwe)') + " " + LANG(32133), "Addon.OpenSettings(plugin.video.theroyalwe)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.pulsar)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(plugin.video.pulsar)') + " " + LANG(32133), "Addon.OpenSettings(plugin.video.pulsar)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.quasar)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(plugin.video.quasar)') + " " + LANG(32133), "Addon.OpenSettings(plugin.video.quasar)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.specto)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(plugin.video.specto)') + " " + LANG(32133), "Addon.OpenSettings(plugin.video.specto)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.1channel)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(plugin.video.1channel)') + " " + LANG(32133), "Addon.OpenSettings(plugin.video.1channel)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.program.super.favourites)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(plugin.program.super.favourites)') + " " + LANG(32133), "Addon.OpenSettings(plugin.program.super.favourites)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.phstreams)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(plugin.video.phstreams)') + " " + LANG(32133), "Addon.OpenSettings(plugin.video.phstreams)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.yifymovies.hd)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(plugin.video.yifymovies.hd)') + " " + LANG(32133), "Addon.OpenSettings(plugin.video.yifymovies.hd)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.whatthefurk)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(plugin.video.whatthefurk)') + " " + LANG(32133), "Addon.OpenSettings(plugin.video.whatthefurk)"])
            if xbmc.getCondVisibility("system.hasaddon(script.artworkdownloader)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(script.artworkdownloader)') + " " + LANG(32133), "Addon.OpenSettings(script.artworkdownloader)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.couchpotato_manager)"):
                manage_list.append([xbmc.getInfoLabel('System.AddonTitle(plugin.video.couchpotate_manager)') + " " + LANG(32133), "Addon.OpenSettings(plugin.video.couchpotato_manager)"])
            selection = xbmcgui.Dialog().select(heading=LANG(10004),
                                                list=[i[0] for i in manage_list])
            if selection > -1:
                for item in manage_list[selection][1].split("||"):
                    xbmc.executebuiltin(item)

        def sort_lists(self, lists):
            if not self.logged_in:
                return lists
            account_list = get_account_lists(10)  # use caching here, forceupdate everywhere else
            id_list = [item["id"] for item in account_list]
            own_lists = [item for item in lists if item["id"] in id_list]
            own_lists = [dict({"account": "True"}, **item) for item in own_lists]
            misc_lists = [item for item in lists if item["id"] not in id_list]
            return own_lists + misc_lists

        def update_states(self):
            xbmc.sleep(2000)  # delay because MovieDB takes some time to update
            _, __, self.account_states = extended_movie_info(self.info["id"], self.dbid, 0)
            super(DialogVideoInfo, self).update_states()

        def remove_list_dialog(self, account_lists):
            listitems = ["%s (%i)" % (d["name"], d["item_count"]) for d in account_lists]
            index = xbmcgui.Dialog().select(LANG(32138), listitems)
            if index >= 0:
                remove_list(account_lists[index]["id"])
                self.update_states()

        @run_async
        def join_omdb_async(self):
            self.omdb_thread.join()
            pass_dict_to_skin(data=self.omdb_thread.listitems,
                              prefix="movie.omdb.",
                              window_id=self.window_id)

    class SetItemsThread(threading.Thread):

        def __init__(self, set_id=""):
            threading.Thread.__init__(self)
            self.set_id = set_id

        def run(self):
            if self.set_id:
                self.listitems, self.setinfo = get_set_movies(self.set_id)
                self.id_list = [item["id"] for item in self.listitems]
            else:
                self.id_list = []
                self.listitems = []
                self.setinfo = {}

    return DialogVideoInfo
