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
        self.pack_start(timerange_label, False, False, 12)

        self.always_radio = Gtk.RadioButton()
        self.always_radio.set_label("Always")
        self.always_radio.set_margin_left(24)
        self.pack_start(self.always_radio, False, False, 12)

        self.custom_radio = Gtk.RadioButton.new_from_widget(self.always_radio)
        self.custom_radio.set_label("Custom")
        self.custom_radio.set_margin_left(24)
        self.pack_start(self.custom_radio, False, False, 12)



class TemplateViewer(Gtk.VBox):
    def __init__(self):
       super(TemplateViewer, self).__init__()

       self.table = Gtk.Table(10, 2, False)
       self.table.set_border_width(1)
       self.pack_start(self.table, True, True, 0)

       event_label = Gtk.Label()
       event_label.set_markup("Event")
       self.table.attach(event_label, 0, 2, 0, 1, xpadding=6, ypadding=6)

       # Event Interpretation
       event_inter_label = Gtk.Label("Interpretation")
       self.table.attach(event_inter_label, 0, 1, 1, 2, xpadding=6, ypadding=6)
       self.event_inter_entry = Gtk.Entry()
       self.event_inter_entry.set_width_chars(40)
       self.table.attach(self.event_inter_entry, 1, 2, 1, 2, xpadding=6, ypadding=6)

       # Event Manifesation
       event_manifes_label = Gtk.Label("Manifestation")
       self.table.attach(event_manifes_label, 0, 1, 2, 3, xpadding=6, ypadding=6)
       self.event_manifes_entry = Gtk.Entry()
       self.event_manifes_entry.set_width_chars(40)
       self.table.attach(self.event_manifes_entry, 1, 2, 2, 3, xpadding=6, ypadding=6)
 
       # Event Actor
       #actor_hbox = Gtk.HBox()
       #actor_hbox.set_margin_bottom(6)
       #self.table.attach(actor_hbox, 0, 2, 3, 4)

       actor_label = Gtk.Label("Actor")
       self.table.attach(actor_label, 0, 1, 3, 4, xpadding=6, ypadding=6)
       self.actor_entry = Gtk.Entry()
       self.table.attach(self.actor_entry, 1, 2, 3, 4, xpadding=6, ypadding=6)
       
       actor_hbox = Gtk.HBox()
       actor_hbox.set_margin_bottom(6)
       self.table.attach(actor_hbox, 1, 2, 4, 5, xpadding=6, ypadding=6)
       self.actor_button = Gtk.Button()
       self.actor_button.set_size_request(32, 32)
       actor_hbox.pack_start(self.actor_button, False, False, 12)
       self.actor_value = Gtk.Label()
       actor_hbox.pack_start(self.actor_value, False, False, 12)

       subj_label = Gtk.Label()
       subj_label.set_markup("Subject")
       self.table.attach(subj_label, 0, 2, 5, 6, xpadding=6, ypadding=6)


       # Subject Interpretation
       subj_inter_label = Gtk.Label("Interpretation")
       self.table.attach(subj_inter_label, 0, 1, 6, 7, xpadding=6, ypadding=6)
       self.subj_inter_entry = Gtk.Entry()
       self.subj_inter_entry.set_width_chars(40)
       self.table.attach(self.subj_inter_entry, 1, 2, 6, 7, xpadding=6, ypadding=6)

       # Subject Manifesation
       subj_manifes_label = Gtk.Label("Manifestation")
       self.table.attach(subj_manifes_label, 0, 1, 7, 8, xpadding=6, ypadding=6)
       self.subj_manifes_entry = Gtk.Entry()
       self.subj_manifes_entry.set_width_chars(40)
       self.table.attach(self.subj_manifes_entry, 1, 2, 7, 8, xpadding=6, ypadding=6)

       # Mimetype
       mimetype_label = Gtk.Label("Mimetype")
       self.table.attach(mimetype_label, 0, 1, 8, 9, xpadding=6, ypadding=6)
       self.mimetype_entry = Gtk.Entry()
       self.mimetype_entry.set_width_chars(40)
       self.table.attach(self.mimetype_entry, 1, 2, 8, 9, xpadding=6, ypadding=6)
 
       # Storage
       storage_label = Gtk.Label("Storage")
       self.table.attach(storage_label, 0, 1, 9, 10, xpadding=6, ypadding=6)
       self.storage_entry = Gtk.Entry()
       self.storage_entry.set_width_chars(40)
       self.table.attach(self.storage_entry, 1, 2, 9, 10, xpadding=6, ypadding=6)
 
       self.show_all()

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

        self.table = Gtk.Table(18, 4, False)
        self.pack_start(self.table, False, False, 6)
        self.table.set_border_width(1)

        id_label = Gtk.Label()
        id_label.set_markup("<b>%s</b>" %("Event ID"))
        id_label.set_alignment(0, 0.5)
        self.table.attach(id_label, 0, 1, 0, 1, xpadding = 6, ypadding =6 )

        self.id_entry = Gtk.Label()
        self.id_entry.set_alignment(0, 0.5)
        self.table.attach(self.id_entry, 1, 2, 0, 1, xpadding = 6, ypadding =6)

        time_label = Gtk.Label()
        time_label.set_markup("<b>%s</b>" %("Timestamp"))
        time_label.set_alignment(0, 0.5)
        self.table.attach(time_label, 2, 3, 0, 1, xpadding = 6, ypadding = 6)

        self.time_entry = Gtk.Label()
        self.time_entry.set_alignment(0, 0.5)
        self.table.attach(self.time_entry, 3, 4, 0, 1, xpadding = 6, ypadding = 6)

        event_int_label = Gtk.Label()
        event_int_label.set_markup("<b>%s</b>" %("Interpretation"))
        event_int_label.set_alignment(0, 0.5)
        self.table.attach(event_int_label, 0, 1, 1, 2, xpadding = 6, ypadding = 6)

        self.event_int_entry = Gtk.Label()
        self.event_int_entry.set_alignment(0, 0.5)
        self.table.attach(self.event_int_entry, 1, 4, 1, 2, xpadding = 6, ypadding = 6)

        event_manifes_label = Gtk.Label()
        event_manifes_label.set_markup("<b>%s</b>" %("Manifestation"))
        event_manifes_label.set_alignment(0, 0.5)
        self.table.attach(event_manifes_label, 0, 1, 2, 3, xpadding = 6, ypadding = 6)

        self.event_manifes_entry = Gtk.Label()
        self.event_manifes_entry.set_alignment(0, 0.5)
        self.table.attach(self.event_manifes_entry, 1, 4, 2, 3, xpadding = 6, ypadding = 6)

        actor_label = Gtk.Label()
        actor_label.set_markup("<b>%s</b>" %("Actor"))
        actor_label.set_alignment(0, 0.5)
        self.table.attach(actor_label, 0, 1, 3, 4, xpadding = 6, ypadding = 6)

        self.actor_entry = Gtk.Label()
        self.actor_entry.set_alignment(0, 0.5)
        self.table.attach(self.actor_entry, 1, 2, 3, 4, xpadding = 6, ypadding =6)

        actor_box = Gtk.HBox()
        self.table.attach(actor_box, 2, 4, 3, 4, xpadding = 6, ypadding = 6)
        self.image_entry = Gtk.Image()
        self.image_entry.set_alignment(0, 0.5)
        actor_box.pack_start(self.image_entry, False, False, 6)
        self.actor_name_entry = Gtk.Label()
        self.actor_name_entry.set_alignment(0, 0.5)
        actor_box.pack_start(self.actor_name_entry, False, False, 6)

        uri_label = Gtk.Label()
        uri_label.set_markup("<b>%s</b>" %("URI"))
        uri_label.set_alignment(0, 0.5)
        self.table.attach(uri_label, 0, 1, 4, 5, xpadding = 6, ypadding = 6)

        self.uri_entry = Gtk.Label()
        self.uri_entry.set_alignment(0, 0.5)
        self.table.attach(self.uri_entry, 1, 4, 4, 5, xpadding = 6, ypadding = 6)

        current_uri_label = Gtk.Label()
        current_uri_label.set_markup("<b>%s</b>" %("Current URI"))
        current_uri_label.set_alignment(0, 0.5)
        self.table.attach(current_uri_label, 0, 1, 5, 6, xpadding = 6, ypadding = 6)
        
        self.current_uri_entry = Gtk.Label()
        self.current_uri_entry.set_alignment(0, 0.5)
        self.table.attach(self.current_uri_entry, 1, 4, 5, 6, xpadding = 6, ypadding = 6)

        subj_int_label = Gtk.Label()
        subj_int_label.set_markup("<b>%s</b>" %("Interpretation"))
        subj_int_label.set_alignment(0, 0.5)
        self.table.attach(subj_int_label, 0, 1, 6, 7, xpadding = 6, ypadding = 6)

        self.subj_int_entry = Gtk.Label()
        self.subj_int_entry.set_alignment(0, 0.5)
        self.table.attach(self.subj_int_entry, 1, 4, 6, 7, xpadding = 6, ypadding = 6)

        subj_manifes_label = Gtk.Label()
        subj_manifes_label.set_markup("<b>%s</b>" %("Manifestation"))
        subj_manifes_label.set_alignment(0, 0.5)
        self.table.attach(subj_manifes_label, 0, 1, 7, 8, xpadding = 6, ypadding = 6)

        self.subj_manifes_entry = Gtk.Label()
        self.subj_manifes_entry.set_alignment(0, 0.5)
        self.table.attach(self.subj_manifes_entry, 1, 4, 7, 8, xpadding = 6, ypadding = 6)


        origin_label = Gtk.Label()
        origin_label.set_markup("<b>%s</b>" %("Origin"))
        origin_label.set_alignment(0, 0.5)
        self.table.attach(origin_label, 0, 1, 8, 9, xpadding = 6, ypadding = 6)

        self.origin_entry = Gtk.Label()
        self.origin_entry.set_alignment(0, 0.5)
        self.table.attach(self.origin_entry, 1, 2, 8, 9, xpadding = 6, ypadding =6)

        mimetype_label = Gtk.Label()
        mimetype_label.set_markup("<b>%s</b>" %("Mimetype"))
        mimetype_label.set_alignment(0, 0.5)
        self.table.attach(mimetype_label, 2, 3, 8, 9, xpadding = 6, ypadding = 6)

        self.mime_entry = Gtk.Label()
        self.mime_entry.set_alignment(0, 0.5)
        self.table.attach(self.mime_entry, 3, 4, 8, 9, xpadding = 6, ypadding = 6)

        text_label = Gtk.Label()
        text_label.set_markup("<b>%s</b>" %("Text"))
        text_label.set_alignment(0, 0.5)
        self.table.attach(text_label, 0, 1, 9, 10, xpadding = 6, ypadding = 6)

        self.text_entry = Gtk.Label()
        self.text_entry.set_alignment(0, 0.5)
        self.table.attach(self.text_entry, 1, 2, 9, 10, xpadding = 6, ypadding =6)

        storage_label = Gtk.Label()
        storage_label.set_markup("<b>%s</b>" %("Storage"))
        storage_label.set_alignment(0, 0.5)
        self.table.attach(storage_label, 2, 3, 9, 10, xpadding = 6, ypadding = 6)
        
        self.storage_entry = Gtk.Label()
        self.storage_entry.set_alignment(0, 0.5)
        self.table.attach(self.storage_entry, 3, 4, 9, 10, xpadding = 6, ypadding = 6)


    def map(self, event):
        self.id_entry.set_text(str(event.get_id()))

        timestamp = int(str(event.get_timestamp()))
        time = datetime.fromtimestamp(timestamp/1000).strftime("%Y-%m-%d %I:%M:%S %p")
        self.time_entry.set_text(time)
        
        self.event_int_entry.set_text(str(event.get_interpretation()))
        self.event_manifes_entry.set_text(str(event.get_manifestation()))

        actor = str(event.get_actor())
        self.actor_entry.set_label(actor)

        app_info = Gio.DesktopAppInfo.new(actor.replace("application://", ""))
        self.image_entry.set_from_gicon(app_info.get_icon(), Gtk.IconSize.DIALOG)
        self.actor_name_entry.set_text(app_info.get_display_name())

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
