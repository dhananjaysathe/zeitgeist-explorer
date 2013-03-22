#! /usr/bin/env python
# -.- coding: utf-8 -.-
#
# Zeitgeist Explorer
#
# Copyright © 2012 Manish Sinha <manishsinha@ubuntu.com>
# Copyright © 2012 Dhananjay Sathe <dhananjaysathe@gmail.com>
# Copyright © 2012 Collabora Ltd.
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
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk, Pango

from monitorviewer import MonitorViewer
from datamodel import MonitorData
from templates import all_events

class ExplorerMainWindow(Gtk.Window):

    filter_manager = None

    def __init__(self):
        super(ExplorerMainWindow, self).__init__()
        self.connect("destroy", Gtk.main_quit)
        self.set_title("Zeitgeist Explorer")
        self.set_default_size(800, 600)

        main_box = Gtk.VBox()
        main_box.spacing = 6
        main_box.margin = 12
        self.add(main_box)

        # Create tabs
        self.notebook = Gtk.Notebook()
        main_box.pack_start(self.notebook, True, True, 12)

        self.monitor_window = MonitorWindow(self)
        self.notebook.append_page(self.monitor_window, Gtk.Label("Monitor Events"))
        self.explorer_window = ExplorerWindow()
        self.notebook.append_page(self.explorer_window, Gtk.Label("Explorer Events"))

        self.show_all()


class MonitorWindow(Gtk.VBox):

    monitor_inst = None
    main_window = None

    def __init__(self, window):
        super(MonitorWindow, self).__init__()

        self.main_window = window

        self.hbox = Gtk.HBox()
        self.pack_start(self.hbox, True, True, 12)

        self.monitor_inst = MonitorViewer()
        self.monitor_inst.map(all_events)
        self.hbox.pack_start(self.monitor_inst, True, True, 12)
        self.monitor_inst.start()


class ExplorerWindow(Gtk.VBox):

    def __init__(self):
        super(ExplorerWindow, self).__init__()

