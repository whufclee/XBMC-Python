# -*- coding: utf8 -*-

# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details

import xbmc
from ..Utils import *
from ..TheMovieDB import *
from ..ImageTools import *
from DialogBaseInfo import DialogBaseInfo
from ..WindowManager import wm
from ..OnClickHandler import OnClickHandler
from .. import VideoPlayer

PLAYER = VideoPlayer.VideoPlayer()
ch = OnClickHandler()


def get_episode_window(window_type):

    class DialogEpisodeInfo(DialogBaseInfo, window_type):

        @busy_dialog
        def __init__(self, *args, **kwargs):
            super(DialogEpisodeInfo, self).__init__(*args, **kwargs)
            self.type = "Episode"
            self.tvshow_id = kwargs.get('show_id')
            data = extended_episode_info(tvshow_id=self.tvshow_id,
                                         season=kwargs.get('season'),
                                         episode=kwargs.get('episode'))
            if not data:
                return None
            self.info, self.data, self.account_states = data
            self.info['ImageFilter'], self.info['ImageColor'] = filter_image(input_img=self.info.get("thumb", ""),
                                                                             radius=25)
            self.listitems = [(1000, self.data["actors"] + self.data["guest_stars"]),
                              (750, self.data["crew"]),
                              (1150, self.data["videos"]),
                              (1350, self.data["images"])]

        def onInit(self):
            super(DialogEpisodeInfo, self).onInit()
            pass_dict_to_skin(self.info, "movie.", False, False, self.window_id)
            super(DialogEpisodeInfo, self).update_states()
            self.get_youtube_vids("%s tv" % (self.info['title']))
            self.fill_lists()

        def onClick(self, control_id):
            super(DialogEpisodeInfo, self).onClick(control_id)
            ch.serve(control_id, self)

        @ch.click(750)
        @ch.click(1000)
        def open_actor_info(self):
            wm.open_actor_info(prev_window=self,
                               actor_id=self.listitem.getProperty("id"))

        @ch.click(132)
        def open_text(self):
            wm.open_textviewer(header=LANG(32037),
                               text=self.info["Plot"],
                               color=self.info['ImageColor'])

        @ch.click(6001)
        def set_rating_dialog(self):
            if set_rating_prompt(media_type="episode",
                                 media_id=[self.tvshow_id, self.info["season"], self.info["episode"]]):
                self.update_states()

        @ch.click(6006)
        def open_rating_list(self):
            xbmc.executebuiltin("ActivateWindow(busydialog)")
            listitems = get_rated_media_items("tv/episodes")
            xbmc.executebuiltin("Dialog.Close(busydialog)")
            wm.open_video_list(prev_window=self,
                               listitems=listitems)

        @ch.click(350)
        @ch.click(1150)
        def play_youtube_video(self):
            PLAYER.play_youtube_video(youtube_id=self.listitem.getProperty("youtube_id"),
                                      listitem=self.listitem,
                                      window=self)

        @ch.click(11)
        def play_episode_no_resume(self):
            if self.dbid:
                url = "special://profile/playlists/video/MetalliQ/TVShows/%s.xsp" % self.info.get("tvdb_id", "")
            else:
                dbid = 0
                tvdb_id = fetch(get_tvshow_ids(self.tvshow_id), "tvdb_id")
                notify(header=str(tvdb_id))
                url = "plugin://plugin.video.metalliq/tv/play/%s/%s/%s/%s" % (tvdb_id, self.info["season"], self.info["episode"], SETTING("player_main"))
            PLAYER.qlickplay(url,
                             listitem=None,
                             window=self,
                             dbid=dbid)


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


        def update_states(self):
            xbmc.sleep(2000)  # delay because MovieDB takes some time to update
            _, __, self.account_states = extended_episode_info(tvshow_id=self.tvshow_id,
                                                               season=self.info["season"],
                                                               episode=self.info["episode"],
                                                               cache_time=0)
            super(DialogEpisodeInfo, self).update_states()

    return DialogEpisodeInfo
