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

from filtermanager import FilterManagerDialog
from monitorviewer import MonitorViewer
from editwizard import TemplateEditWizard
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

    #monitor_builtin = {}
    #monitor_custom = {}
    #selected_monitor_view = None

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

class ConfirmMonitorStop(Gtk.Dialog):

    def __init__(self):
        super(ConfirmMonitorStop, self).__init__()
        self.set_properties('margin',6,'padding',12,'title',
            "Confirm Monitor Stop",'resizable',False,'modal',True,'decorated',False)
        self.set_size_request(100, 50)

        self.add_button(Gtk.STOCK_DELETE, Gtk.ResponseType.YES)
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.NO)

        box = self.get_content_area()

        label1 = Gtk.Label(xalign=0,yalign=0.5,margin_top=12,
                            margin_right=12,margin_left=12)
        label1.set_markup("<b>%s</b>"
        %("The monitor which you are trying to remove is still running"))

        label2 = Gtk.Label(xalign=0,yalign=0.5,margin_top=12,
                            margin_right=12,margin_left=12)
        label2.set_markup("Going ahead will stop the monitor before removing it")

        box.pack_start(label1, False, False, 6)
        box.pack_start(label2, False, False, 6)

        self.show_all()
