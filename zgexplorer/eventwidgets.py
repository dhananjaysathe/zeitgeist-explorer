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
