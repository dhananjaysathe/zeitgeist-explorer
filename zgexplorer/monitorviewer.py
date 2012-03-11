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

from templates import BuiltInFilters
from eventwidgets import EventViewer

from zeitgeist.datamodel import Event, Subject, Interpretation, \
    Manifestation, StorageState, ResultType
from zeitgeist.client import Monitor

class MonitorViewer(Gtk.VBox):

    def __init__(self, zeitgeist_client):
        super(MonitorViewer, self).__init__()

        self.client = zeitgeist_client
        self.monitor = None

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

        # Array Index, Event Id, TimeStamp, Interpretation, Manifestation
        self.store = Gtk.ListStore(int, int, str, str, str)
        self.treeview = Gtk.TreeView(self.store)
        self.scroll.add(self.treeview)

        column_id = Gtk.TreeViewColumn("ID")
        self.treeview.append_column(column_id)
        id_rend = Gtk.CellRendererText()
        id_rend.set_property("ellipsize", Pango.EllipsizeMode.END)
        column_id.pack_start(id_rend, False)
        column_id.add_attribute(id_rend, "markup", 1)
        column_id.set_resizable(True)

        self.viewer = EventViewer()
        self.pack_start(self.viewer, False, False, 6)

        self.show_all()

    def map(self, index, is_predefined):
        entry = self.builtin[index] if is_predefined else None
        if entry is not None:
            self.desc_entry.set_text(entry[1])


        self.monitor = Monitor(entry[3], [entry[2]], self.monitor_insert, None)

    def monitor_insert(self, time_range, events):
        pass

    def start_monitor(self, button):
        self.start.set_sensitive(False)
        self.stop.set_sensitive(True)

    def stop_monitor(self, button):
        self.start.set_sensitive(True)
        self.stop.set_sensitive(False)
