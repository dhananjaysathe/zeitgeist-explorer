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

from gi.repository import Gtk, Gdk, Pango

from templates import BuiltInFilters
from eventwidgets import TemplateViewer, TimeRangeViewer, TemplateEditor

class FilterManagerDialog(Gtk.Dialog):

    main_window = None

    def __init__(self, window):
        super(FilterManagerDialog, self).__init__()
        self.main_window = window
        self.set_destroy_with_parent(True)
        self.set_title("Filter Manager")
        self.set_properties('margin',12,'content-area-spacing',6) #Check Value
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.set_size_request(600, 700)
        self.active_page_index = 0
        self.set_type_hint(Gdk.WindowTypeHint.MENU)
        self.is_predefined = True

        box = self.get_content_area()

        self.notebook = Gtk.Notebook()
        self.notebook.connect('switch-page',self.on_notebook_switch_page)
        box.pack_start(self.notebook, True, True, 0)

        self.add_predefined_tab()
        self.add_custom_tab()

        self.dialog = TemplateEditor()
        self.dialog.set_transient_for(self.main_window)

        self.custom_event_filters={}

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
        self.predefined_box.pack_start(self.predefined_viewer, False, False, 0)

    def add_custom_tab(self):
        self.custom_box = Gtk.VBox()
        self.notebook.append_page(self.custom_box, Gtk.Label("Custom Filter"))

        self.custom_store = Gtk.ListStore(int, str)

        self.custom_view = Gtk.TreeView(model=self.custom_store)
        self.custom_view.connect("cursor-changed", self.on_cursor_changed)

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
        self.custom_scroll.set_shadow_type(Gtk.ShadowType.IN)
        self.custom_scroll.set_border_width(1)
        self.custom_box.pack_start(self.custom_scroll, True, True, 0)

        self.toolbar = Gtk.Toolbar(icon_size=1)
        self.toolbar.set_style(Gtk.ToolbarStyle.ICONS)
        self.toolbar.get_style_context().add_class(Gtk.STYLE_CLASS_INLINE_TOOLBAR)
        self.toolbar.get_style_context().set_junction_sides(Gtk.JunctionSides.TOP)
        self.custom_box.pack_start(self.toolbar, False, False, 0)

        filter_add = Gtk.ToolButton.new(None, "Add Filter")
        filter_add.set_tooltip_text(filter_add.get_label())
        filter_add.set_icon_name("list-add-symbolic")
        filter_add.connect("clicked", self.on_add_clicked)
        self.toolbar.insert(filter_add, -1)

        filter_edit = Gtk.ToolButton.new(None, "Edit Filter")
        filter_edit.set_tooltip_text(filter_edit.get_label())
        filter_edit.set_icon_name("edit-copy-symbolic")
        filter_edit.connect("clicked", self.on_edit_clicked)
        self.toolbar.insert(filter_edit, -1)

        filter_remove = Gtk.ToolButton.new(None, "Remove Filter")
        filter_remove.set_tooltip_text(filter_remove.get_label())
        filter_remove.set_icon_name("list-remove-symbolic")
        filter_remove.connect("clicked", self.on_remove_clicked)
        self.toolbar.insert(filter_remove, -1)

        # See the Template values
        self.custom_viewer = TemplateViewer()
        self.custom_box.pack_start(self.custom_viewer, False, False, 0)


    def get_selected_index(self):
        if self.is_predefined:
            selection = self.predefined_view.get_selection()
        else :
            selection = self.custom_view.get_selection()

        if selection is not None:
            model, _iter = selection.get_selected()
            if _iter is not None:
                app_index = model.get(_iter, 0)
                return app_index[0]
            else:
                return None

    def get_selected_entry(self):
        index = self.get_selected_index()
        if index is not None:
            if self.is_predefined :
                return index,self.builtin[index], True
            else :
                return index,self.custom_event_filters[index], False

        return None, None, None

    def on_notebook_switch_page(self, widget, page, page_num):
        self.is_predefined = not bool(page_num)

    def on_cursor_changed(self, treeview):
        index = self.get_selected_index()
        if index is not None:
            if self.is_predefined :
                self.predefined_viewer.set_values(self.builtin[index])
            else:
                self.custom_viewer.set_values(self.custom_event_filters[index])


    def on_add_clicked(self,widget):
        template = self.run_template_add_edit_dialog()
        if template is not None:
            curr_size = len(self.custom_store)
            self.custom_store.append([curr_size, template[0]])
            self.custom_event_filters[curr_size] = template

    def on_edit_clicked(self,widget):
        index,template,is_predefined = self.get_selected_entry()
        if index is not None:
            template = self.run_template_add_edit_dialog(template)
            self.custom_store[index] = template[0]
            self.custom_event_filters[index] = template

    def on_remove_clicked(self,widget):
        index,template,is_predefind = self.get_selected_entry()
        for row in self.custom_store:
            if row[0] == index :
                self.custom_store.remove(row.iter)
                del self.custom_event_filters[index]
                break


    def run_template_add_edit_dialog(self,template=None):

        self.dialog.set_template(template)
        self.dialog.show_all()

        while True:
            response_id = self.dialog.run()
            if response_id in [Gtk.ResponseType.OK,Gtk.ResponseType.APPLY] :
                template = self.dialog.get_template()

                if response_id == Gtk.ResponseType.OK:
                    self.dialog.hide()
                    break

            else:
                self.dialog.hide()
                return None

        return template




