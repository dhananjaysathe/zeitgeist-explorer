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

from gi.repository import Gtk
from zeitgeist.datamodel import Event, Subject, Manifestation, \
    Interpretation, StorageState

class TimeRangeViewer(Gtk.VBox):
    def __init__(self):
        super(TimeRangeViewer, self).__init__()



class TemplateViewer(Gtk.VBox):
    def __init__(self):
       super(TemplateViewer, self).__init__()

       self.table = Gtk.Table(9, 2, True)
       self.table.set_border_width(1)
       self.pack_start(self.table, True, True, 0)

       event_label = Gtk.Label()
       event_label.set_markup("Event")
       self.table.attach(event_label, 0, 2, 0, 1)

       # Event Interpretation
       event_inter_hbox = Gtk.HBox()
       event_inter_hbox.set_margin_bottom(6)
       self.table.attach(event_inter_hbox, 0, 2, 1, 2)
       event_inter_label = Gtk.Label("Interpretation")
       event_inter_hbox.pack_start(event_inter_label, False, False, 12)
       self.event_inter_entry = Gtk.Entry()
       self.event_inter_entry.set_width_chars(40)
       event_inter_hbox.pack_start(self.event_inter_entry, True, True, 12)

       # Event Manifesation
       event_manifes_hbox = Gtk.HBox()
       event_manifes_hbox.set_margin_bottom(6)
       self.table.attach(event_manifes_hbox, 0, 2, 2, 3)
       event_manifes_label = Gtk.Label("Manifestation")
       event_manifes_hbox.pack_start(event_manifes_label, False, False, 12)
       self.event_manifes_entry = Gtk.Entry()
       self.event_manifes_entry.set_width_chars(40)
       event_manifes_hbox.pack_start(self.event_manifes_entry, True, True, 12)
 
       # Event Actor
       actor_hbox = Gtk.HBox()
       actor_hbox.set_margin_bottom(6)
       self.table.attach(actor_hbox, 0, 2, 3, 4)

       actor_label = Gtk.Label("Actor")
       actor_label.set_margin_right(60)
       actor_hbox.pack_start(actor_label, False, False, 12)
       self.actor_entry = Gtk.Entry()
       actor_hbox.pack_start(self.actor_entry, True, True, 12)
       self.actor_button = Gtk.Button()
       self.actor_button.set_size_request(32, 32)
       actor_hbox.pack_start(self.actor_button, False, False, 12)
       self.actor_value = Gtk.Label()
       actor_hbox.pack_start(self.actor_value, False, False, 12)

       subj_label = Gtk.Label()
       subj_label.set_markup("Subject")
       self.table.attach(subj_label, 0, 2, 4, 5)


       # Subject Interpretation
       subj_inter_hbox = Gtk.HBox()
       subj_inter_hbox.set_margin_bottom(6)
       self.table.attach(subj_inter_hbox, 0, 2, 5, 6)
       subj_inter_label = Gtk.Label("Interpretation")
       subj_inter_hbox.pack_start(subj_inter_label, False, False, 12)
       self.subj_inter_entry = Gtk.Entry()
       self.subj_inter_entry.set_width_chars(40)
       subj_inter_hbox.pack_start(self.subj_inter_entry, True, True, 12)

       # Subject Manifesation
       subj_manifes_hbox = Gtk.HBox()
       subj_manifes_hbox.set_margin_bottom(6)
       self.table.attach(subj_manifes_hbox, 0, 2, 6, 7)
       subj_manifes_label = Gtk.Label("Manifestation")
       subj_manifes_hbox.pack_start(subj_manifes_label, False, False, 12)
       self.subj_manifes_entry = Gtk.Entry()
       self.subj_manifes_entry.set_width_chars(40)
       subj_manifes_hbox.pack_start(self.subj_manifes_entry, True, True, 12)

       # Mimetype
       mimetype_hbox = Gtk.HBox()
       mimetype_hbox.set_margin_bottom(6)
       self.table.attach(mimetype_hbox, 0, 2, 7, 8)
       mimetype_label = Gtk.Label("Mimetype")
       mimetype_label.set_margin_right(30)
       mimetype_hbox.pack_start(mimetype_label, False, False, 12)
       self.mimetype_entry = Gtk.Entry()
       self.mimetype_entry.set_width_chars(40)
       mimetype_hbox.pack_start(self.mimetype_entry, True, True, 12)
 
       # Storage
       storage_hbox = Gtk.HBox()
       storage_hbox.set_margin_bottom(6)
       self.table.attach(storage_hbox, 0, 2, 8, 9)
       storage_label = Gtk.Label("Storage")
       storage_label.set_margin_right(40)
       storage_hbox.pack_start(storage_label, False, False, 12)
       self.storage_entry = Gtk.Entry()
       self.storage_entry.set_width_chars(40)
       storage_hbox.pack_start(self.storage_entry, True, True, 12)
 
       self.show_all()
