#! /usr/bin/env python
# -.- coding: utf-8 -.-
#
# Zeitgeist Explorer
#
# Copyright © 2012 Manish Sinha <manishsinha@ubuntu.com>
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
#

import codecs
from datetime import datetime
from gi.repository import Gtk, Gio
from zeitgeist.datamodel import Event, Subject, Manifestation, \
    Interpretation, StorageState, Symbol

class TimeRangeViewer(Gtk.VBox):
    def __init__(self):
        super(TimeRangeViewer, self).__init__()

        timerange_label = Gtk.Label("Time Range")
        self.pack_start(timerange_label,False,False,12)

        self.always_radio = Gtk.RadioButton(label= "Always",margin_left= 24)
        self.pack_start(self.always_radio,False,False,12)

        self.custom_radio = Gtk.RadioButton(label= "Custom",margin_left= 24)
        self.custom_radio.join_group(self.always_radio)
        self.pack_start(self.custom_radio,False,False,12)


class TemplateViewer(Gtk.VBox):
    def __init__(self):
       super(TemplateViewer, self).__init__()

       self.table = Gtk.Table(10, 2, False,border_width=1)
       self.pack_start(self.table, True, True, 0)

       event_label = Gtk.Label()
       event_label.set_markup("Event")

       # Event Interpretation
       event_inter_label = Gtk.Label("Interpretation")
       self.event_inter_entry = Gtk.Entry(width_chars=40)

       # Event Manifesation
       event_manifes_label = Gtk.Label("Manifestation")
       self.event_manifes_entry = Gtk.Entry(width_chars=40)

       actor_label = Gtk.Label("Actor")
       self.actor_entry = Gtk.Entry(width_chars=40)

       actor_hbox = Gtk.HBox(margin_bottom=6)
       self.actor_button = Gtk.Button()
       self.actor_button.set_size_request(32, 32)
       actor_hbox.pack_start(self.actor_button, False, False, 12)
       self.actor_value = Gtk.Label()
       actor_hbox.pack_start(self.actor_value, False, False, 12)

       subj_label = Gtk.Label()
       subj_label.set_markup("Subject")


       # Subject Interpretation
       subj_inter_label = Gtk.Label("Interpretation")
       self.subj_inter_entry = Gtk.Entry(width_chars=40)

       # Subject Manifesation
       subj_manifes_label = Gtk.Label("Manifestation")
       self.subj_manifes_entry = Gtk.Entry(width_chars=40)

       # Mimetype
       mimetype_label = Gtk.Label("Mimetype")
       self.mimetype_entry = Gtk.Entry(width_chars=40)

       # Storage
       storage_label = Gtk.Label("Storage")
       self.storage_entry = Gtk.Entry(width_chars=40)

       attach_list = (
            (event_label,(0, 2, 0, 1)),
            (event_inter_label,(0, 1, 1, 2)),
            (self.event_inter_entry,(1, 2, 1, 2)),
            (event_manifes_label,(0, 1, 2, 3)),
            (self.event_manifes_entry,(1, 2, 2, 3)),
            (actor_label,(0, 1, 3, 4)),
            (self.actor_entry,(1, 2, 3, 4)),
            (actor_hbox,(1, 2, 4, 5)),
            (subj_label,(0, 2, 5, 6)),
            (subj_inter_label,(0, 1, 6, 7)),
            (self.subj_inter_entry,(1, 2, 6, 7)),
            (subj_manifes_label,(0, 1, 7, 8)),
            (self.subj_manifes_entry,(1, 2, 7, 8)),
            (mimetype_label,(0, 1, 8, 9)),
            (self.mimetype_entry,(1, 2, 8, 9)),
            (storage_label,(0, 1, 9, 10)),
            (self.storage_entry,(1, 2, 9, 10))
        )
       for widget_entry in attach_list :
           widget,pos = widget_entry
           self.table.attach(widget,pos[0],pos[1], pos[2], pos[3], xpadding=6, ypadding=6)

    def set_fields_enable(self, enable):
        self.event_inter_entry.set_sensitive(enable)
        self.event_manifes_entry.set_sensitive(enable)
        self.actor_entry.set_sensitive(enable)
        self.actor_button.set_sensitive(enable)
        self.subj_inter_entry.set_sensitive(enable)
        self.subj_manifes_entry.set_sensitive(enable)
        self.mimetype_entry.set_sensitive(enable)
        self.storage_entry.set_sensitive(enable)

    def set_values(self, values):
        ev = values[2]

        # Event Interpretation
        ev_inter = ev.get_interpretation()
        self.event_inter_entry.set_text(ev_inter.name \
                if type(ev_inter) is Symbol else "")
        self.event_inter_entry.set_tooltip_text(ev_inter.doc \
                if type(ev_inter) is Symbol else "")

        # Event Manifestation
        ev_manifes = ev.get_manifestation()
        self.event_manifes_entry.set_text(ev_manifes.name \
                if type(ev_manifes) is Symbol else "")
        self.event_manifes_entry.set_tooltip_text(ev_manifes.doc \
                if type(ev_manifes) is Symbol else "")

        actor = ev.get_actor()
        self.actor_entry.set_text(actor)
        if actor is not "" and actor.startswith("application://"):
            actor =  actor.replace("application://", "")
            try:
                app_info = Gio.DesktopAppInfo.new(actor)
                self.actor_value.set_text(app_info.get_display_name())
                image = Gtk.Image.new_from_gicon(app_info.get_icon(), Gtk.IconSize.BUTTON)
                self.actor_button.set_image(image)
            except TypeError:
                print("Wrong actor string: %s" %(actor))
        else:
            self.actor_value.set_text("")
            self.actor_button.set_image(Gtk.Image())

        subj = None
        if len(ev.get_subjects()) > 0:
            subj = ev.get_subjects()[0]
        else:
            subj = Subject()

        # Subject Interpretation
        subj_inter =  subj.get_interpretation()
        self.subj_inter_entry.set_text(subj_inter.name \
                if type(subj_inter) is Symbol else "")
        self.subj_inter_entry.set_tooltip_text(subj_inter.doc \
                if type(subj_inter) is Symbol else "")

        # Event Manifestation
        subj_manifes =  subj.get_manifestation()
        self.subj_manifes_entry.set_text(subj_manifes.name
                if type(subj_manifes) is Symbol else "")
        self.subj_manifes_entry.set_tooltip_text(subj_manifes.doc \
                if type(subj_manifes) is Symbol else "")

        self.mimetype_entry.set_text(subj.get_mimetype())
        self.storage_entry.set_text(subj.get_storage())

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
        for widget_entry in attach_list :
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
