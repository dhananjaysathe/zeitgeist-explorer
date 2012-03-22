#! /usr/bin/env python
# -.- coding: utf-8 -.-
#
# Zeitgeist Explorer
#
# Copyright © 2012 Manish Sinha <manishsinha@ubuntu.com>
# Copyright © 2012 Dhananjay Sathe <dhananjaysathe@gmail.com>
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
from eventwidgets import TemplateViewer, TimeRangeViewer

class FilterManagerDialog(Gtk.Dialog):

    def __init__(self):
        super(FilterManagerDialog, self).__init__()
        self.set_destroy_with_parent(True)
        self.set_properties('title',"Filter Manager",'margin',12,'content-area-spacing',6) #Check Value
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.set_size_request(600, 700)

        box = self.get_content_area()

        self.notebook = Gtk.Notebook()
        box.pack_start(self.notebook, True, True, 0)

        self.add_predefined_tab()
        self.add_custom_tab()

        box.show_all()

    def add_predefined_tab(self):
        self.predefined_box = Gtk.VBox()
        self.notebook.append_page(self.predefined_box, Gtk.Label("Predefined Filter"))

        self.predefined_store = Gtk.ListStore(int, str)
        self.builtin = BuiltInFilters()
        for i in self.builtin:
            self.predefined_store.append([i, self.builtin[i][0]])

        self.predefined_view = Gtk.TreeView(model=self.predefined_store)
        self.predefined_view.connect("cursor-changed", self.on_cursor_changed)
        column_pix_name = Gtk.TreeViewColumn(_('Name'))
        self.predefined_view.append_column(column_pix_name)
        name_rend = Gtk.CellRendererText(ellipsize=Pango.EllipsizeMode.END)
        column_pix_name.pack_start(name_rend, False)
        column_pix_name.add_attribute(name_rend, "markup", 1)
        column_pix_name.set_resizable(True)

        self.predefined_view.set_properties('headers-visible',False,'rules-hint',True)

        self.predefined_scroll = Gtk.ScrolledWindow(shadow_type=Gtk.ShadowType.IN,border_width=1)
        self.predefined_scroll.add(self.predefined_view)
        self.predefined_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.predefined_box.pack_start(self.predefined_scroll, True, True, 6)

        # See the Template values
        self.predefined_viewer = TemplateViewer()
        self.predefined_viewer.set_fields_enable(False)
        self.predefined_box.pack_start(self.predefined_viewer, False, False, 0)

    def add_custom_tab(self):
        self.custom_box = Gtk.VBox()
        self.notebook.append_page(self.custom_box, Gtk.Label("Custom Filter"))

        self.custom_store = Gtk.ListStore(int, str)

        self.custom_view = Gtk.TreeView(model=self.custom_store)
        self.custom_view.connect("cursor-changed", self.on_custom_cursor_changed)

        column_pix_name = Gtk.TreeViewColumn(_('Name'))
        self.custom_view.append_column(column_pix_name)
        name_rend = Gtk.CellRendererText(ellipsize=Pango.EllipsizeMode.END)
        column_pix_name.pack_start(name_rend, False)
        column_pix_name.add_attribute(name_rend, "markup", 1)
        column_pix_name.set_resizable(True)

        self.custom_view.set_properties('headers-visible',False,'rules-hint',True)

        self.custom_scroll = Gtk.ScrolledWindow(shadow_type=Gtk.ShadowType.IN,border_width=1)
        self.custom_scroll.add(self.custom_view)
        self.custom_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.custom_box.pack_start(self.custom_scroll, True, True, 6)

        # See the Template values
        self.custom_viewer = TemplateViewer()
        self.custom_viewer.set_fields_enable(False)
        self.custom_box.pack_start(self.custom_viewer, False, False, 0)


    def get_selected_index(self):
        selection = self.predefined_view.get_selection()
        model, _iter = selection.get_selected()
        if _iter is not None:
            app_index = model.get(_iter, 0)
            return app_index[0]
        else:
            return None

    def get_selected_entry(self):
        index = self.get_selected_index()
        is_predefined = True
        if index is not None:
            return index,self.builtin[index], is_predefined

        return None

    def on_button_toggled(self, button, name):
        if button.get_active():
            state = "on"
        else:
            state = "off"
        print "Button", name, "was turned", state

    def on_cursor_changed(self, treeview):
        index = self.get_selected_index()
        if index is not None:
            self.predefined_viewer.set_values(self.builtin[index])

    def on_custom_cursor_changed(self, treeview):
        pass
