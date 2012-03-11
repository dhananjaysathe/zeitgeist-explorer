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

from gi.repository import Gtk, Pango

from datetime import datetime

from templates import BuiltInFilters
from eventwidgets import EventViewer

from zeitgeist.datamodel import Event, Subject, Interpretation, \
    Manifestation, StorageState, ResultType, Symbol
from zeitgeist.client import Monitor

class MonitorViewer(Gtk.VBox):

    def __init__(self, zeitgeist_client):
        super(MonitorViewer, self).__init__()

        self.client = zeitgeist_client
        self.monitor = None
        self.is_running = False
        # The Entry for this MonitorViewer
        self.entry = None

        self.events = {}

        self.spacing = 6
        self.margin = 12
        
        self.builtin = BuiltInFilters()

        #desc_label = Gtk.Label()
        #desc_label.set_alignment(0, 0)
        #desc_label.set_markup("<b>%s</b>" %("Description"))
        #self.pack_start(desc_label, False, False, 6)

        self.desc_entry = Gtk.Label()
        self.desc_entry.set_alignment(0, 0)
        self.desc_entry.set_line_wrap(True)
        self.desc_entry.set_line_wrap_mode(Pango.WrapMode.WORD)
        self.pack_start(self.desc_entry, False, False, 6)


        # ButtonBox
        self.button_box = Gtk.HButtonBox()
        self.button_box.set_homogeneous(False)
        self.button_box.set_layout(Gtk.ButtonBoxStyle.START)
        self.pack_start(self.button_box, False, False, 6)

        self.start = Gtk.Button()
        self.start.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_MEDIA_PLAY, 
                Gtk.IconSize.BUTTON))
        self.start.connect("clicked", self.start_monitor)
        self.button_box.pack_start(self.start, False, False, 6)

        self.stop = Gtk.Button()
        self.stop.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_MEDIA_STOP,
                Gtk.IconSize.BUTTON))
        self.stop.connect("clicked", self.stop_monitor)
        self.stop.set_sensitive(False)
        self.button_box.pack_start(self.stop, False, False, 6)

        self.edit = Gtk.Button()
        self.edit.set_size_request(32, 32)
        self.edit.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_EDIT,
                Gtk.IconSize.BUTTON))
        self.button_box.pack_start(self.edit, False, False, 6)

        self.scroll = Gtk.ScrolledWindow(None, None)
        self.scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scroll.set_shadow_type(Gtk.ShadowType.IN)
        self.scroll.set_border_width(1)
        self.pack_start(self.scroll, True, True, 6)

        # Event Id, TimeStamp, Interpretation, Manifestation, Actor
        self.store = Gtk.ListStore( int, str, str, str, str)
        self.treeview = Gtk.TreeView(self.store)
        self.treeview.connect("cursor-changed", self.on_event_selected)
        self.scroll.add(self.treeview)

        column_id = Gtk.TreeViewColumn("ID")
        self.treeview.append_column(column_id)
        id_rend = Gtk.CellRendererText()
        column_id.pack_start(id_rend, False)
        column_id.add_attribute(id_rend, "markup", 0)
        column_id.set_resizable(True)

        column_time = Gtk.TreeViewColumn("Timestamp")
        self.treeview.append_column(column_time)
        time_rend = Gtk.CellRendererText()
        column_time.pack_start(time_rend, False)
        column_time.add_attribute(time_rend, "markup", 1)
        column_time.set_resizable(True)

        column_inter = Gtk.TreeViewColumn("Interpretation")
        self.treeview.append_column(column_inter)
        inter_rend = Gtk.CellRendererText()
        column_inter.pack_start(inter_rend, False)
        column_inter.add_attribute(inter_rend, "markup", 2)
        column_inter.set_resizable(True)

        column_manif = Gtk.TreeViewColumn("Manifestation")
        self.treeview.append_column(column_manif)
        manif_rend = Gtk.CellRendererText()
        column_manif.pack_start(manif_rend, False)
        column_manif.add_attribute(manif_rend, "markup", 3)
        column_manif.set_resizable(True)

        column_actor = Gtk.TreeViewColumn("Actor")
        self.treeview.append_column(column_actor)
        actor_rend = Gtk.CellRendererText()
        column_actor.pack_start(actor_rend, False)
        column_actor.add_attribute(actor_rend, "markup", 4)
        column_actor.set_resizable(True)

        self.viewer = EventViewer()
        self.pack_start(self.viewer, False, False, 6)

        self.show_all()

    def map(self, index, is_predefined):
        self.entry = self.builtin[index] if is_predefined else None
        if self.entry is not None:
            self.desc_entry.set_text(self.entry[1])

    def monitor_insert(self, time_range, events):
        for event in events:
            self.events[event.get_id()] = event

            timestamp = int(str(event.get_timestamp()))
            time = datetime.fromtimestamp(timestamp/1000).strftime("%Y-%m-%d %I:%M:%S %p")
            
            actor = event.get_actor()

            event_inter = str(event.get_interpretation())
            interpretation = event_inter.split("#")[-1]
            event_manifes = str(event.get_manifestation())
            manifestation = event_manifes.split("#")[-1]

            self.store.append([event.get_id(), time, interpretation, manifestation, actor])

    def monitor_delete(self, time_range, event_ids):
        pass

    def start_monitor(self, button):
        self.start.set_sensitive(False)
        self.stop.set_sensitive(True)
        self.is_running = True
        self.monitor = self.client.install_monitor(self.entry[3], \
            [self.entry[2]], self.monitor_insert, self.monitor_delete)

    def stop_monitor(self, button):
        self.start.set_sensitive(True)
        self.stop.set_sensitive(False)
        self.is_running = False
        self.client.remove_monitor(self.monitor)

    def is_monitor_running(self):
        return self.is_running

    def monitor_stop(self):
        self.stop_monitor(self.stop)

    def on_event_selected(self, treeview):
        selection = self.treeview.get_selection()
        if selection is not None:
            model, _iter = selection.get_selected()
            if _iter is not None:
                event_id = model.get(_iter, 0)[0]
                event = self.events[event_id]
                self.viewer.map(event)
