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

class ExplorerMainWindow(Gtk.Window):

    def __init__(self):
        super(ExplorerMainWindow, self).__init__()
        self.connect("destroy", Gtk.main_quit)
        self.set_title("Zeitgeist Explorer")
        self.set_size_request(800, 400)
        self.spacing = 6
        self.margin = 12
        
        main_box = Gtk.VBox()
        self.add(main_box)

        toolbar = Gtk.Toolbar()

        # New Tool Item
        toolitem_new = Gtk.ToolButton()
        toolitem_new.set_label("New")
        toolitem_new.set_icon_name("add")
        toolitem_new.connect("clicked", self.toolitem_new_clicked)
        toolbar.insert(toolitem_new, -1)

        # Load Tool Item
        toolitem_load = Gtk.ToolButton()
        toolitem_load.set_stock_id(Gtk.STOCK_OPEN)
        toolitem_load.set_label("Load")
        toolitem_load.connect("clicked", self.toolitem_load_clicked) 
        toolbar.insert(toolitem_load, -1)
        
        main_box.pack_start(toolbar, False, True, 0)

        self.show_all()

    def toolitem_new_clicked(self, button):
        print("New Tool Item Clicked")

    def toolitem_load_clicked(self, button):
        print("Load tool Item clicked")
