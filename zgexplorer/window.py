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

from filtermanager import FilterManagerDialog

class ExplorerMainWindow(Gtk.Window):

    filter_manager = None

    def __init__(self):
        super(ExplorerMainWindow, self).__init__()
        self.connect("destroy", Gtk.main_quit)
        self.set_title("Zeitgeist Explorer")
        self.set_size_request(1000, 800)
        #self.spacing = 6
        #self.margin = 12
        
        main_box = Gtk.VBox()
        main_box.spacing = 6
        main_box.margin = 12
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
        
        #main_box.pack_start(toolbar, False, True, 0)

        self.filter_manager = FilterManagerDialog()

        # Create tabs
        self.notebook = Gtk.Notebook()
        main_box.pack_start(self.notebook, True, True, 12)

        self.monitor_window = MonitorWindow()
        self.notebook.append_page(self.monitor_window, Gtk.Label("Monitor Events"))
        self.explorer_window = ExplorerWindow()
        self.notebook.append_page(self.explorer_window, Gtk.Label("Explore Events"))

        self.show_all()

    def toolitem_new_clicked(self, button):
        print("New Tool Item Clicked")

    def toolitem_load_clicked(self, button):
        res = self.filter_manager.run()
        self.filter_manager.hide()
        if res == Gtk.ResponseType.OK:
            print("Accepted")


class MonitorWindow(Gtk.VBox):

    def __init__(self):
        super(MonitorWindow, self).__init__()

        hbox = Gtk.HBox()
        self.pack_start(hbox, True, True, 12)

        list_vbox = Gtk.VBox()
        hbox.pack_start(list_vbox, False, False, 0)

        monitor_vbox = Gtk.VBox()
        list_vbox.pack_start(monitor_vbox, True, True, 0)
        self.monitors = Gtk.ListStore(int, str)
        self.monitor_tree = Gtk.TreeView(self.monitors)
        self.monitor_tree.set_size_request(200, 600)
        self.monitor_tree.set_border_width(1)
        self.monitor_tree.set_visible(True)
        self.monitor_tree.set_rules_hint(True)
        self.monitor_tree.set_headers_visible(False)

        scroll = Gtk.ScrolledWindow(None, None)
        scroll.add(self.monitor_tree)
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.set_border_width(1)
        monitor_vbox.pack_start(scroll, True, True, 0)

        column_pix_name = Gtk.TreeViewColumn(_('Name'))
        self.monitor_tree.append_column(column_pix_name)
        name_rend = Gtk.CellRendererText()
        name_rend.set_property("ellipsize", Pango.EllipsizeMode.END)
        column_pix_name.pack_start(name_rend, False)
        column_pix_name.add_attribute(name_rend, "markup", 1)
        column_pix_name.set_resizable(True)

        self.toolbar = Gtk.Toolbar()
        self.toolbar.set_style(Gtk.ToolbarStyle.ICONS)
        self.toolbar.set_icon_size(1)
        self.toolbar.get_style_context().add_class(Gtk.STYLE_CLASS_INLINE_TOOLBAR)
        self.toolbar.get_style_context().set_junction_sides(Gtk.JunctionSides.TOP)
        list_vbox.pack_start(self.toolbar, False, False, 0)

        filter_add = Gtk.ToolButton.new(None, "Add Filter")
        filter_add.set_icon_name("list-add-symbolic")
        filter_add.connect("clicked", self.on_add_clicked)
        self.toolbar.insert(filter_add, 0)

        filter_remove = Gtk.ToolButton.new(None, "Remove Filter")
        filter_remove.set_icon_name("list-remove-symbolic")
        self.toolbar.insert(filter_remove, 1)

    def on_add_clicked(self, button):
        print "Add Clicked"

    def on_remove_clicked(self, button):
        print "Remove Clicked"


class ExplorerWindow(Gtk.VBox):

    def __init__(self):
        super(ExplorerWindow, self).__init__()
