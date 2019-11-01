# -*- coding: utf8 -*-

# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details

import xbmcgui
from ..Utils import *
from ..LastFM import *
from ..YouTube import *
from DialogBaseList import DialogBaseList
from ..WindowManager import wm
from .. import VideoPlayer
from ..OnClickHandler import OnClickHandler

PLAYER = VideoPlayer.VideoPlayer()
ch = OnClickHandler()


TRANSLATIONS = {"track": "track",
                "album": "album",
                "artist": "artist"}
SORTS = {"track": {"date": LANG(552),
                   "rating": LANG(563),
                   "relevance": LANG(32060),
                   "title": LANG(369),
                   "viewCount": LANG(567)},
         "album": {"date": LANG(552),
                   "rating": LANG(563),
                   "relevance": LANG(32060),
                   "title": LANG(369),
                   "videoCount": LANG(32068),
                   "viewCount": LANG(567)},
         "artist": {"date": LANG(552),
                    "rating": LANG(563),
                    "relevance": LANG(32060),
                    "title": LANG(369),
                    "videoCount": LANG(32068),
                    "viewCount": LANG(567)}}


def get_audio_window(window_type):

    class DialogAudioList(DialogBaseList, window_type):

        @busy_dialog
        def __init__(self, *args, **kwargs):
            super(DialogAudioList, self).__init__(*args, **kwargs)
            self.type = kwargs.get('type', "artist")
            self.filter_url = ""
            self.page_token = ""
            self.next_page_token = ""
            self.prev_page_token = ""
            self.sort = kwargs.get('sort', "relevance")
            self.sort_label = kwargs.get('sort_label', LANG(32060))
            self.order = kwargs.get('order', "desc")
            force = kwargs.get('force', False)
            self.update_content(force_update=force)

        def onClick(self, control_id):
            super(DialogAudioList, self).onClick(control_id)
            ch.serve(control_id, self)

        def onAction(self, action):
            super(DialogAudioList, self).onAction(action)
            ch.serve_action(action, self.getFocusId(), self)

        @ch.click(500)
        def main_list_click(self):
            self.last_position = self.control.getSelectedPosition()
            youtube_id = self.listitem.getProperty("youtube_id")
            if self.type == "artist":
                channel_filter = [{"id": youtube_id,
                                   "type": "channelId",
                                   "typelabel": LANG(19029),
                                   "label": youtube_id}]
                wm.open_youtube_list(filters=channel_filter)
            else:
                PLAYER.play_youtube_video(youtube_id=youtube_id,
                                          listitem=self.listitem,
                                          window=self)

        @ch.click(5002)
        def set_published_filter(self):
            label_list = [LANG(32062), LANG(32063), LANG(32064), LANG(32065), LANG(636)]
            deltas = [1, 7, 31, 365, "custom"]
            index = xbmcgui.Dialog().select(heading=LANG(32151),
                                            list=label_list)
            if index == -1:
                return None
            delta = deltas[index]
            if delta == "custom":
                delta = xbmcgui.Dialog().input(heading=LANG(32067),
                                               type=xbmcgui.INPUT_NUMERIC)
            if delta:
                d = datetime.datetime.now() - datetime.timedelta(int(delta))
                date_str = d.isoformat('T')[:-7] + "Z"
                self.add_filter("publishedAfter", date_str, LANG(172), str(label_list[index]))
                self.update()

        @ch.click(5003)
        def set_language_filter(self):
            label_list = ["en", "de", "fr"]
            index = xbmcgui.Dialog().select(heading=LANG(32151),
                                            list=label_list)
            if index > -1:
                self.add_filter("regionCode", label_list[index], LANG(248), str(label_list[index]))
                self.update()

        @ch.click(5006)
        def set_dimension_filter(self):
            value_list = ["2d", "3d", "any"]
            label_list = ["2D", "3D", LANG(593)]
            index = xbmcgui.Dialog().select(heading=LANG(32151),
                                            list=label_list)
            if index > -1:
                self.add_filter("videoDimension", value_list[index], "Dimensions", str(label_list[index]))
                self.update()

        @ch.click(5008)
        def set_duration_filter(self):
            value_list = ["long", "medium", "short", "any"]
            label_list = [LANG(33013), LANG(601), LANG(33012), LANG(593)]
            index = xbmcgui.Dialog().select(heading=LANG(32151),
                                            list=label_list)
            if index > -1:
                self.add_filter("videoDuration", value_list[index], LANG(180), str(label_list[index]))
                self.update()

        @ch.click(5009)
        def set_caption_filter(self):
            value_list = ["closedCaption", "none", "any"]
            label_list = [LANG(107), LANG(106), LANG(593)]
            index = xbmcgui.Dialog().select(heading=LANG(287),
                                            list=label_list)
            if index > -1:
                self.add_filter("videoCaption", value_list[index], LANG(287), str(label_list[index]))
                self.update()

        @ch.click(5012)
        def set_definition_filter(self):
            value_list = ["high", "standard", "any"]
            label_list = [LANG(419), LANG(602), LANG(593)]
            index = xbmcgui.Dialog().select(heading=LANG(169),
                                            list=label_list)
            if index > -1:
                self.add_filter("videoDefinition", value_list[index], LANG(169), str(label_list[index]))
                self.update()

        @ch.click(5007)
        def toggle_type(self):
            self.filters = []
            self.page = 1
            self.mode = "filter"
            types = {"track": "album",
                     "album": "artist",
                     "artist": "track"}
            if self.type in types:
                self.type = types[self.type]
            if self.sort not in SORTS[self.type].keys():
                self.sort = "relevance"
                self.sort_label = LANG(32060)
            self.update()

        def update_ui(self):
            self.window.setProperty("Type", TRANSLATIONS[self.type])
            if self.type == "track":
                self.window.getControl(5006).setVisible(True)
                self.window.getControl(5008).setVisible(True)
                self.window.getControl(5009).setVisible(True)
                self.window.getControl(5012).setVisible(True)
            elif self.type == "album":
                self.window.getControl(5006).setVisible(False)
                self.window.getControl(5008).setVisible(False)
                self.window.getControl(5009).setVisible(False)
                self.window.getControl(5012).setVisible(False)
            elif self.type == "artist":
                self.window.getControl(5006).setVisible(False)
                self.window.getControl(5008).setVisible(False)
                self.window.getControl(5009).setVisible(False)
                self.window.getControl(5012).setVisible(False)
            super(DialogAudioList, self).update_ui()

        def go_to_next_page(self):
            if self.page < self.total_pages:
                self.page += 1
                self.prev_page_token = self.page_token
                self.page_token = self.next_page_token

        def go_to_prev_page(self):
            if self.page > 1:
                self.page -= 1
                self.next_page_token = self.page_token
                self.page_token = self.prev_page_token

        @ch.click(5001)
        def get_sort_type(self):
            sort_key = self.type
            listitems = [key for key in SORTS[sort_key].values()]
            sort_strings = [value for value in SORTS[sort_key].keys()]
            index = xbmcgui.Dialog().select(heading=LANG(32104),
                                            list=listitems)
            if index == -1:
                return None
            self.sort = sort_strings[index]
            self.sort_label = listitems[index]
            self.update()

        @ch.action("contextmenu", 500)
        def context_menu(self):
            if self.type == "track":
                more_vids = "%s [B]%s[/B]" % (ADDON.getLocalizedString(32081), self.listitem.getProperty("channel_title"))
                listitems = [LANG(32069), more_vids]
                selection = xbmcgui.Dialog().select(heading=LANG(32151),
                                                    list=listitems)
                if selection < 0:
                    return None
                elif selection == 0:
                    related_filter = [{"id": self.listitem.getProperty("youtube_id"),
                                       "type": "relatedToVideoId",
                                       "typelabel": "Related",
                                       "label": self.listitem.getLabel()}]
                    wm.open_youtube_list(filters=related_filter)
                elif selection == 1:
                    channel_filter = [{"id": self.listitem.getProperty("channel_id"),
                                       "type": "channelId",
                                       "typelabel": "Related",
                                       "label": self.listitem.getProperty("channel_title")}]
                    wm.open_youtube_list(filters=channel_filter)

        def add_filter(self, key, value, typelabel, label):
            super(DialogAudioList, self).add_filter(key=key,
                                                      value=value,
                                                      typelabel=typelabel,
                                                      label=label,
                                                      force_overwrite=True)
            self.mode = "filter"
            self.page = 1

        def fetch_data(self, force=False):  # TODO: rewrite
            if self.type == "artist":
                temp = "artist"
                rated = LANG(32145)
                starred = LANG(32144)
            elif self.type == "album":
                temp = "album"
                rated = LANG(32135)
                starred = LANG(32134)
            else:
                temp = "track"
                rated = LANG(32135)
                starred = LANG(32134)
            if self.type == "artist":
                self.set_filter_url()
                self.set_filter_label()
                url = "method=Chart.getTopArtists&limit=100"
            elif self.type == "track":
                self.set_filter_url()
                self.set_filter_label()
                url = "method=Chart.getTopTracks&limit=100"
            if force:
                response = get_lastfm_data(url=url,
                                         cache_days=0,
                                         folder="LastFM")
            else:
                response = get_lastfm_data(url=url,
                                         cache_days=2,
                                         folder="LastFM")
            if not response:
                return None
            if self.type == "artist":
                listitems = handle_lastfm_artists(results=response["artists"])
            elif self.type == "album":
                listitems = handle_lastfm_albums(results=response["topalbums"])
            elif self.type == "track":
                listitems = handle_lastfm_top_tracks(results=response["tracks"])
            info = {"listitems": listitems,
                    "results_per_page": 100,
                    "total_results": 100}
            return info
    return DialogAudioList
