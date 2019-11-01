# -*- coding: utf8 -*-

# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details

import xbmc
import xbmcgui
from WindowManager import wm
from Utils import *


class VideoPlayer(xbmc.Player):

    def __init__(self, *args, **kwargs):
        xbmc.Player.__init__(self)
        self.stopped = False

    def onPlayBackEnded(self):
        self.stopped = True

    def onPlayBackStopped(self):
        self.stopped = True

    def onPlayBackStarted(self):
        self.stopped = False

    def play(self, url, listitem, window=False):
        if window and window.window_type == "dialog":
            wm.add_to_stack(window)
            window.close()
        super(VideoPlayer, self).play(item=url,
                                      listitem=listitem,
                                      windowed=False,
                                      startpos=-1)
        if window and window.window_type == "dialog":
            self.wait_for_video_end()
            wm.pop_stack()

    def qlickplay(self, url, listitem, window=False, dbid=0):
        if ADDON.getSetting("window_mode") == "false":
            if window:
                wm.add_to_stack(window)
                window.close()
        if dbid != 0:
            if RESUME == "false":
                get_kodi_json(method="Player.Open",
                              params='{"item": {"movieid": %s}, "options":{"resume": %s}}' % (dbid, "false"))
            else:
                get_kodi_json(method="Player.Open",
                              params='{"item": {"movieid": %s}, "options":{"resume": %s}}' % (dbid, "true"))
        else:
            super(VideoPlayer, self).play(item=url,
                                          listitem=listitem,
                                          windowed=False,
                                          startpos=-1)
        if ADDON.getSetting("window_mode") == "false":
            while not xbmc.getCondVisibility("player.hasvideo"):
                for i in range(100):
                    xbmc.sleep(1000)
                    if xbmc.getCondVisibility("player.hasvideo"):
                        while xbmc.getCondVisibility('Window.IsActive(busydialog)'):
                            for i in range(50):
                                xbmc.sleep(1000)
                                if not xbmc.getCondVisibility('Window.IsActive(busydialog)'):
                                    break
                            break
                        break
                break
            if xbmc.getCondVisibility("player.hasvideo"):
                self.wait_for_video_end()
                wm.pop_stack()
            else:
                wm.pop_stack()

    def play_youtube_video(self, youtube_id="", listitem=None, window=False):
        """
        play youtube vid with info from *listitem
        """
        url, yt_listitem = self.youtube_info_by_id(youtube_id)
        if not listitem:
            listitem = yt_listitem
        if url:
            self.play(url=url,
                      listitem=listitem,
                      window=window)
        else:
            notify(header=LANG(257),
                   message="no youtube id found")

    @busy_dialog
    def youtube_info_by_id(self, youtube_id):
        import YDStreamExtractor
        vid = YDStreamExtractor.getVideoInfo(youtube_id,
                                             quality=1)
        if not vid:
            return None, None
        listitem = xbmcgui.ListItem(label=vid.title,
                                    thumbnailImage=vid.thumbnail)
        listitem.setInfo(type='video',
                         infoLabels={"genre": vid.sourceName,
                                     "plot": vid.description})
        return vid.streamURL(), listitem

    def wait_for_video_end(self):
        xbmc.sleep(500)
        while not self.stopped:
            xbmc.sleep(200)
        self.stopped = False
