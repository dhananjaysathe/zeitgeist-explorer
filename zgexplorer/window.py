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
        self.notebook.append_page(self.explorer_window, Gtk.Label("Explore Events"))

        self.show_all()


class MonitorWindow(Gtk.VBox):

    monitor_builtin = {}
    monitor_custom = {}
    selected_monitor_view = None
    main_window = None

    def __init__(self, window):
        super(MonitorWindow, self).__init__()

        self.main_window = window

        self.monitor_dialog = FilterManagerDialog(self.main_window)
        self.monitor_dialog.set_transient_for(self.main_window)

        self.hbox = Gtk.HBox()
        self.pack_start(self.hbox, True, True, 12)

        list_vbox = Gtk.VBox()
        self.hbox.pack_start(list_vbox, False, False, 0)

        monitor_vbox = Gtk.VBox()
        list_vbox.pack_start(monitor_vbox, True, True, 0)
        self.monitors = Gtk.ListStore(int, str, bool)
        self.monitor_tree = Gtk.TreeView(model=self.monitors)
        self.monitor_tree.connect("cursor-changed", self.on_treeview_selected)
        self.monitor_tree.set_size_request(200, 600)
        self.monitor_tree.set_properties('border_width',1,'visible',True
                            ,'rules_hint',True,'headers_visible',False)

        scroll = Gtk.ScrolledWindow(None, None)
        scroll.add(self.monitor_tree)
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.set_border_width(1)
        monitor_vbox.pack_start(scroll, True, True, 0)

        column_pix_name = Gtk.TreeViewColumn(_('Name'))
        self.monitor_tree.append_column(column_pix_name)
        name_rend = Gtk.CellRendererText(ellipsize=Pango.EllipsizeMode.END)
        column_pix_name.pack_start(name_rend, False)
        column_pix_name.add_attribute(name_rend, "markup", 1)
        column_pix_name.set_resizable(True)

        self.toolbar = Gtk.Toolbar(icon_size=1)
        self.toolbar.set_style(Gtk.ToolbarStyle.ICONS)
        self.toolbar.get_style_context().add_class(Gtk.STYLE_CLASS_INLINE_TOOLBAR)
        self.toolbar.get_style_context().set_junction_sides(Gtk.JunctionSides.TOP)
        list_vbox.pack_start(self.toolbar, False, False, 0)

        filter_add = Gtk.ToolButton.new(None, "Add Filter")
        filter_add.set_icon_name("list-add-symbolic")
        filter_add.connect("clicked", self.on_add_clicked)
        self.toolbar.insert(filter_add, 0)

        filter_remove = Gtk.ToolButton.new(None, "Remove Filter")
        filter_remove.set_icon_name("list-remove-symbolic")
        filter_remove.connect("clicked", self.on_remove_clicked)
        self.toolbar.insert(filter_remove, 1)

    def on_add_clicked(self, button):
        res = self.monitor_dialog.run()
        if res == Gtk.ResponseType.DELETE_EVENT or res == Gtk.ResponseType.CANCEL:
            self.monitor_dialog.hide()
            return

        if res == Gtk.ResponseType.OK:
            index, entry, is_predefined = self.monitor_dialog.get_selected_entry()
            if entry is not None:
                self.monitor_dialog.hide()
                if (is_predefined and index in self.monitor_builtin.keys()) or \
                    (not is_predefined and index in self.monitor_custom.keys()):
                    return

                self.monitors.append([index, entry[0], is_predefined])
                # Add it in the list of ids
                monitor_inst = MonitorViewer()
                monitor_inst.map(index, is_predefined)
                if is_predefined:
                    self.monitor_builtin[index] = monitor_inst
                else:
                    self.monitor_custom[index] = monitor_inst

    def on_remove_clicked(self, button):
        selection = self.monitor_tree.get_selection()
        if selection is not None:
            model, _iter = selection.get_selected()
            if _iter is not None:
                index = model.get(_iter, 0)[0]
                is_predefined = model.get(_iter, 2)[0]

                monitor_inst = self.monitor_builtin[index] if is_predefined \
                    else self.monitor_custom[index]
                if monitor_inst.is_monitor_running():
                    # Ask if the user wants to stop it
                    stop = ConfirmMonitorStop()
                    res = stop.run()
                    stop.hide()
                    if res == Gtk.ResponseType.NO or \
                            res == Gtk.ResponseType.DELETE_EVENT:
                        return

                    monitor_inst.monitor_stop()

                if is_predefined:
                    self.monitor_builtin.pop(index)
                else:
                    self.monitor_custom.pop(index)

                if self.selected_monitor_view is not None:
                    self.hbox.remove(self.selected_monitor_view)
                    self.selected_monitor_view= None

                self.monitors.remove(_iter)

    def on_treeview_selected(self, treeview):
        selection = self.monitor_tree.get_selection()
        if selection is not None:
            model, _iter = selection.get_selected()
            if _iter is not None:
                index = model.get(_iter, 0)[0]
                is_predefined = model.get(_iter, 2)[0]
                monitor_viewer = self.monitor_builtin[index] if is_predefined \
                    else self.monitor_custom[index]

                if self.selected_monitor_view is not None:
                    self.hbox.remove(self.selected_monitor_view)
                self.hbox.pack_start(monitor_viewer, True, True, 12)
                self.selected_monitor_view = monitor_viewer

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
