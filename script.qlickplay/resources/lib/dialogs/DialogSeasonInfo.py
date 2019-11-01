# -*- coding: utf8 -*-

# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details

from ..Utils import *
from ..TheMovieDB import *
from ..ImageTools import *
from DialogBaseInfo import DialogBaseInfo
from ..WindowManager import wm
from ..OnClickHandler import OnClickHandler
from .. import VideoPlayer

ch = OnClickHandler()
PLAYER = VideoPlayer.VideoPlayer()


def get_season_window(window_type):

    class DialogSeasonInfo(DialogBaseInfo, window_type):

        def __init__(self, *args, **kwargs):
            super(DialogSeasonInfo, self).__init__(*args, **kwargs)
            self.type = "Season"
            self.tvshow_id = kwargs.get('id')
            data = extended_season_info(tvshow_id=self.tvshow_id,
                                        season_number=kwargs.get('season'))
            if not data:
                return None
            self.info, self.data = data
            if "dbid" not in self.info:  # need to add comparing for seasons
                self.info['poster'] = get_file(url=self.info.get("poster", ""))
            self.info['ImageFilter'], self.info['ImageColor'] = filter_image(input_img=self.info.get("poster", ""),
                                                                             radius=25)
            self.listitems = [(1000, self.data["actors"]),
                              (750, self.data["crew"]),
                              (2000, self.data["episodes"]),
                              (1150, self.data["videos"]),
                              (1250, self.data["images"]),
                              (1350, self.data["backdrops"])]

        def onInit(self):
            self.get_youtube_vids("%s %s tv" % (self.info["TVShowTitle"], self.info['title']))
            super(DialogSeasonInfo, self).onInit()
            pass_dict_to_skin(data=self.info,
                              prefix="movie.",
                              window_id=self.window_id)
            self.fill_lists()

        def onClick(self, control_id):
            super(DialogSeasonInfo, self).onClick(control_id)
            ch.serve(control_id, self)

        @ch.click(121)
        def browse_season(self):
            if self.dbid:
                url = "videodb://tvshows/titles/%s/%s/" % ((self.dbid), self.info.get("season", ""))
            else:
                tvdb_id = fetch(get_tvshow_ids(self.tvshow_id), "tvdb_id")
                url = "plugin://plugin.video.metalliq/tv/tvdb/%s/%s/" % (tvdb_id, self.info.get("season", ""))
            self.close()
            xbmc.executebuiltin("ActivateWindow(videos,%s,return)" % url)

        @ch.click(750)
        @ch.click(1000)
        def open_actor_info(self):
            wm.open_actor_info(prev_window=self,
                               actor_id=self.listitem.getProperty("id"))

        @ch.click(2000)
        def open_episode_info(self):
            wm.open_episode_info(prev_window=self,
                                 tvshow=self.info["TVShowTitle"],
                                 tvshow_id=self.tvshow_id,
                                 season=self.listitem.getProperty("season"),
                                 episode=self.listitem.getProperty("episode"))

        @ch.click(10)
        def play_season_no_resume(self):
            if self.dbid:
                url = "special://profile/playlists/video/MetalliQ/TVShows/%s.xsp" % self.info.get("tvdb_id", "")
            else:
                url = "plugin://plugin.video.metalliq/tv/play/%s/%s/1/%s" % (self.info.get("tvdb_id", ""), self.info.get("season", ""), SETTING("player_main"))
            PLAYER.qlickplay(url,
                             listitem=None,
                             window=self,
                             dbid=0)

        @ch.click(132)
        def open_text(self):
            wm.open_textviewer(header=LANG(32037),
                               text=self.info["Plot"],
                               color=self.info['ImageColor'])

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


        @ch.click(350)
        @ch.click(1150)
        def play_youtube_video(self):
            PLAYER.play_youtube_video(youtube_id=self.listitem.getProperty("youtube_id"),
                                      listitem=self.listitem,
                                      window=self)
    return DialogSeasonInfo
