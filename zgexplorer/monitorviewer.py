#! /usr/bin/env python
# -.- coding: utf-8 -.-
#
# Zeitgeist Explorer
#
# Copyright © 2012 Manish Sinha <manishsinha@ubuntu.com>.
# Copyright © 2011-2012 Collabora Ltd.
#             By Siegfried-A. Gevatter Pujals <siegfried@gevatter.com>
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk, Gdk, Pango

from datetime import datetime

from templates import BuiltInFilters
from eventwidgets import EventDetailsViewer, EventsTreeView
from remote import get_zeitgeist

from zeitgeist.datamodel import Event, Subject, Interpretation, \
    Manifestation, StorageState, ResultType, Symbol

class MonitorViewer(Gtk.VBox):

    _client = None
    _is_running = False

    def __init__(self):
        super(MonitorViewer, self).__init__()

        self.ids = [] 
        self._client = get_zeitgeist()
        self.monitor = None
        # The Entry for this MonitorViewer
        self.entry = None

        self.events = {}

        self.spacing = 6
        self.margin = 12

        self.desc_entry = Gtk.Label(xalign=0,yalign=0,wrap=True)
        self.pack_start(self.desc_entry, False, False, 6)

        # ButtonBox
        self.hbox = Gtk.HBox(True)
        self.button_box = Gtk.HButtonBox(False)

        self.hbox.pack_start(Gtk.Label(), False, False, 6)
        self.hbox.pack_start(self.button_box, False, False, 6)
        self.hbox.pack_start(Gtk.Label(), False, False, 6)
        
        self.button_box.set_layout(Gtk.ButtonBoxStyle.START)
        self.pack_start(self.hbox, False, False, 6)

        self.start_button = Gtk.Button(image=Gtk.Image.new_from_stock(
            Gtk.STOCK_MEDIA_PLAY,Gtk.IconSize.BUTTON))
        self.start_button.connect("clicked", self.start_monitor)
        self.button_box.pack_start(self.start_button, False, False, 6)

        self.stop_button = Gtk.Button(image= Gtk.Image.new_from_stock(
            Gtk.STOCK_MEDIA_STOP,Gtk.IconSize.BUTTON))
        self.stop_button.connect("clicked", self.stop_monitor)
        self.stop_button.set_sensitive(False)
        self.button_box.pack_start(self.stop_button, False, False, 6)

        self.clear = Gtk.Button(image=Gtk.Image.new_from_stock(
            Gtk.STOCK_CLEAR,Gtk.IconSize.BUTTON))
        self.clear.connect("clicked", self.clear_events)
        self.button_box.pack_start(self.clear, False, False, 6)

        self.scroll = Gtk.ScrolledWindow(None, None,border_width=1,shadow_type=Gtk.ShadowType.IN)
        self.scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.pack_start(self.scroll, True, True, 6)

        self.treeview = EventsTreeView()
        self.treeview.set_selection_changed_cb(self.on_event_selected)
        self.scroll.add(self.treeview)

        self.viewer = EventDetailsViewer()
        self.pack_start(self.viewer, False, False, 6)

        self.show_all()

    def map(self, template):
        self.entry = template

    def monitor_insert(self, time_range, events):
        for event in events:
            if event.id not in self.ids:
                self.events[event.id] = event
                self.ids.append(event.id)
        self.treeview.add_events(events)

    def monitor_delete(self, time_range, event_ids):
        # FIXME: change row background to red or something
        pass

    def clear_events(self, button):
        self.events.clear()
        self.viewer.map(Event.new_for_values(subjects=[Subject()]))
        self.treeview.set_events([])
        # FIXME:
        wtf = """
        model = self.treeview.get_model()
        print type(model)
        _iter = model.get_iter_first()
        while _iter is not None:
            print model.get(_iter, 0)[0]
            self.store.remove(_iter)
            _iter = model.iter_next(_iter)

        _iter = model.get_iter_first()
        if _iter is not None:
            self.store.remove(_iter)
            """

    def start(self):
        self.start_monitor(None)

    def start_monitor(self, button):
        self.start_button.set_sensitive(False)
        self.stop_button.set_sensitive(True)
        self._is_running = True
        self.monitor = self._client.install_monitor(self.entry[3], \
            [self.entry[2]], self.monitor_insert, self.monitor_delete)

    def stop_monitor(self, button):
        self.start_button.set_sensitive(True)
        self.stop_button.set_sensitive(False)
        self._is_running = False
        self._client.remove_monitor(self.monitor)
        self.ids = []

    def monitor_clear(self, button):
        pass

    def is_monitor_running(self):
        return self._is_running

    def monitor_stop(self):
        self.stop_monitor(self.stop)

    def on_event_selected(self, event_id):
        event = self.events[event_id]
        self.viewer.map(event)


