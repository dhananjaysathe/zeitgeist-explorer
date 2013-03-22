#! /usr/bin/env python
# -.- coding: utf-8 -.-
#
# Zeitgeist Explorer
#
# Copyright © 2012 Manish Sinha <manishsinha@ubuntu.com>
# Copyright © 2012 Dhananjay Sathe <dhananjaysathe@gmail.com>
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.";

import codecs
from datetime import datetime
from gi.repository import Gtk, Gdk, Gio
from zeitgeist.datamodel import Event, Subject, Manifestation, \
    Interpretation, StorageState, Symbol, ResultType

from lookupdata import *
from date_widgets2 import TimeRangeViewer

# workaround for Gtk ComboBoxText Widgets
def get_active_text(combobox):
      model = combobox.get_model()
      active = combobox.get_active()
      if active < 0:
          return ''
      return model[active][0]




class EventViewer(Gtk.VBox):

    def __init__(self):

        super(EventViewer, self).__init__()

        self.table = Gtk.Table(18, 4, False,border_width=1)
        self.pack_start(self.table, False, False, 6)

        id_label = Gtk.Label(xalign=0,yalign=0.5)
        id_label.set_markup("<b>%s</b>" %("Event ID"))

        self.id_entry = Gtk.Label(xalign=0,yalign=0.5)

        time_label = Gtk.Label(xalign=0,yalign=0.5)
        time_label.set_markup("<b>%s</b>" %("Timestamp"))

        self.time_entry = Gtk.Label(xalign=0,yalign=0.5)

        event_int_label = Gtk.Label(xalign=0,yalign=0.5)
        event_int_label.set_markup("<b>%s</b>" %("Interpretation"))

        self.event_int_entry = Gtk.Label(xalign=0,yalign=0.5)

        event_manifes_label = Gtk.Label(xalign=0,yalign=0.5)
        event_manifes_label.set_markup("<b>%s</b>" %("Manifestation"))

        self.event_manifes_entry = Gtk.Label(xalign=0,yalign=0.5)

        actor_label = Gtk.Label(xalign=0,yalign=0.5)
        actor_label.set_markup("<b>%s</b>" %("Actor"))

        self.actor_entry = Gtk.Label(xalign=0,yalign=0.5)

        actor_box = Gtk.HBox()
        self.image_entry = Gtk.Image(xalign=0,yalign=0.5)
        actor_box.pack_start(self.image_entry, False, False, 6)
        self.actor_name_entry = Gtk.Label(xalign=0,yalign=0.5)
        actor_box.pack_start(self.actor_name_entry, False, False, 6)

        uri_label = Gtk.Label(xalign=0,yalign=0.5)
        uri_label.set_markup("<b>%s</b>" %("URI"))

        self.uri_entry = Gtk.Label(xalign=0,yalign=0.5)

        current_uri_label = Gtk.Label(xalign=0,yalign=0.5)
        current_uri_label.set_markup("<b>%s</b>" %("Current URI"))

        self.current_uri_entry = Gtk.Label(xalign=0,yalign=0.5)

        subj_int_label = Gtk.Label(xalign=0,yalign=0.5)
        subj_int_label.set_markup("<b>%s</b>" %("Interpretation"))

        self.subj_int_entry = Gtk.Label(xalign=0,yalign=0.5)

        subj_manifes_label = Gtk.Label(xalign=0,yalign=0.5)
        subj_manifes_label.set_markup("<b>%s</b>" %("Manifestation"))

        self.subj_manifes_entry = Gtk.Label(xalign=0,yalign=0.5)


        origin_label = Gtk.Label(xalign=0,yalign=0.5)
        origin_label.set_markup("<b>%s</b>" %("Origin"))

        self.origin_entry = Gtk.Label(xalign=0,yalign=0.5)

        mimetype_label = Gtk.Label(xalign=0,yalign=0.5)
        mimetype_label.set_markup("<b>%s</b>" %("Mimetype"))

        self.mime_entry = Gtk.Label(xalign=0,yalign=0.5)

        text_label = Gtk.Label(xalign=0,yalign=0.5)
        text_label.set_markup("<b>%s</b>" %("Text"))

        self.text_entry = Gtk.Label(xalign=0,yalign=0.5)

        storage_label = Gtk.Label(xalign=0,yalign=0.5)
        storage_label.set_markup("<b>%s</b>" %("Storage"))

        self.storage_entry = Gtk.Label(xalign=0,yalign=0.5)

        attach_list = (
            (id_label,(0, 1, 0, 1)),
            (self.id_entry,(1, 2, 0, 1)),
            (time_label,(2, 3, 0, 1)),
            (self.time_entry,(3, 4, 0, 1)),
            (event_int_label,(0, 1, 1, 2)),
            (self.event_int_entry,(1, 4, 1, 2)),
            (event_manifes_label,(0, 1, 2, 3)),
            (self.event_manifes_entry,(1, 4, 2, 3)),
            (actor_label,(0, 1, 3, 4)),
            (self.actor_entry,(1, 2, 3, 4)),
            (actor_box,(2, 4, 3, 4)),
            (uri_label,(0, 1, 4, 5)),
            (self.uri_entry,(1, 4, 4, 5)),
            (current_uri_label,(0, 1, 5, 6)),
            (self.current_uri_entry,(1, 4, 5, 6)),
            (subj_int_label,(0, 1, 6, 7)),
            (self.subj_int_entry,(1, 4, 6, 7)),
            (subj_manifes_label,(0, 1, 7, 8)),
            (self.subj_manifes_entry,(1, 4, 7, 8)),
            (origin_label,(0, 1, 8, 9)),
            (self.origin_entry,(1, 2, 8, 9)),
            (mimetype_label,(2, 3, 8, 9)),
            (self.mime_entry,(3, 4, 8, 9)),
            (text_label,(0, 1, 9, 10)),
            (self.text_entry,(1, 2, 9, 10)),
            (storage_label,(2, 3, 9, 10)),
            (self.storage_entry,(3, 4, 9, 10))
         )
        for widget_entry in attach_list:
           widget,pos = widget_entry
           self.table.attach(widget,pos[0],pos[1], pos[2], pos[3], xpadding=6, ypadding=6)

    def map(self, event):
        try:
            id_val = int(event.get_id())
            self.id_entry.set_text(str(id_val) if id_val > 0 else "")

            timestamp = int(str(event.get_timestamp()))
            time = datetime.fromtimestamp(timestamp/1000).strftime("%Y-%m-%d %I:%M:%S %p")
            self.time_entry.set_text(time if id_val > 0 else "")
        except:
            self.id_entry.set_text("")
            self.time_entry.set_text("")

        self.event_int_entry.set_text(str(event.get_interpretation()))
        self.event_manifes_entry.set_text(str(event.get_manifestation()))

        actor = str(event.get_actor())
        self.actor_entry.set_label(actor)

        if actor.startswith("application://"):
            app_info = Gio.DesktopAppInfo.new(actor.replace("application://", ""))
            self.image_entry.set_from_gicon(app_info.get_icon(), Gtk.IconSize.DIALOG)
            self.actor_name_entry.set_text(app_info.get_display_name())
        else:
            self.image_entry.clear()
            self.actor_name_entry.set_text("")

        if len(event.subjects) > 0:
            subj = event.subjects[0]

            self.uri_entry.set_text(str(subj.get_uri()))
            self.current_uri_entry.set_text(str(subj.get_current_uri()))

            self.subj_int_entry.set_text(str(subj.get_interpretation()))
            self.subj_manifes_entry.set_text(str(subj.get_manifestation()))

            self.origin_entry.set_text(str(subj.get_origin()))
            self.mime_entry.set_text(subj.get_mimetype())
            try:
                txt = str(subj.get_text())
                self.text_entry.set_text(txt)
            except:
                #print unicode(subj.get_text().strip(codecs.BOM_UTF8), 'utf-8')
                self.text_entry.set_text("")
            self.storage_entry.set_text(str(subj.get_storage()))
