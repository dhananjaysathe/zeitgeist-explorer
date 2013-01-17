#! /usr/bin/env python
# -.- coding: utf-8 -.-
#
# Zeitgeist Explorer
#
# Copyright © 2013 Manish Sinha <manishsinha@ubuntu.com>.
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

from gi.repository import Gtk, Gdk, GdkPixbuf, Pango, GObject, Gio
from zeitgeist.datamodel import ResultType
from lookupdata import *

class TemplateEditWizard(Gtk.Dialog):

    def __init__(self, window):
        super(TemplateEditWizard, self).__init__()
        self.main_window = window

        self.set_destroy_with_parent(True)
        self.set_properties('margin', 6, 'content-area-spacing', 6)
        self.set_type_hint(Gdk.WindowTypeHint.MENU)
        self.is_predefined = True

        box = self.get_content_area()
        self.time_range = TimeRangeWizardPage(self.main_window)
        self.time_range.connect("cancel", self.on_cancel_click)
        self.time_range.connect("next", self.on_next_click)
        box.pack_start(self.time_range, False, False, 6)

        self.event_page = EventWizardPage(self.main_window)
        box.pack_start(self.event_page, False, False, 6)

        box.show_all()
        self.event_page.hide()

    def on_cancel_click(self, widget):
        self.set_default_response(Gtk.ResponseType.CLOSE)
        self.emit("response", Gtk.ResponseType.CLOSE)

    def on_next_click(self, widget):
        self.time_range.hide()
        self.event_page.show()
        print("Next clicked")
        
class EventWizardPage(Gtk.VBox):

    def __init__(self, window):
        super(EventWizardPage, self).__init__()

        self.set_size_request(650, 400)
        self.main_window = window
        self.set_border_width(12)

        event_label = Gtk.Label(xalign=0.5, yalign=0)
        event_label.set_markup("<b>%s</b>" %("Event Details"))
        self.pack_start(event_label, False, False, 6)

        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(15)
        self.grid.set_column_spacing(15)
        self.pack_start(self.grid, False, False, 6)

        event_inter_label = Gtk.Label("Interpretation:",xalign=1,yalign=0.5)
        self.grid.attach(event_inter_label, 0, 0, 1, 1)
        self.event_inter_combo = Gtk.ComboBoxText()
        #self.event_inter_combo.set_hexpand(True)
        self.event_inter_combo.set_wrap_width(600)
        self.grid.attach(self.event_inter_combo, 2, 0, 3, 1)
        for entry in event_interpretations.keys():
            if entry is not None and len(entry) > 0:
                self.event_inter_combo.append_text(entry)

        # Event Manifesation
        event_manifes_label = Gtk.Label("Manifestation:",xalign=1,yalign=0.5)
        self.grid.attach(event_manifes_label, 0, 1, 1, 1)
        self.event_manifes_combo = Gtk.ComboBoxText()
        #self.event_manifes_combo.set_hexpand(True)
        self.grid.attach(self.event_manifes_combo, 2, 1, 3, 1)
        for entry in event_manifestations.keys():
            if entry is not None and len(entry) > 0:
                self.event_manifes_combo.append_text(entry)

        actor_label = Gtk.Label("Actor:", xalign=1, yalign=0.5)
        self.grid.attach(actor_label, 0, 2, 1, 1)
        self.actor_entry = Gtk.Entry()
        self.actor_entry.set_width_chars(70)
        self.grid.attach(self.actor_entry, 2, 2, 3, 1)

        self.actor_store = Gtk.ListStore(GdkPixbuf.Pixbuf, str, str)
        self.actor_scroll = Gtk.ScrolledWindow()
        self.actor_scroll.set_border_width(1)
        self.actor_scroll.set_shadow_type(Gtk.ShadowType.IN)    
        self.actor_scroll.set_policy(   Gtk.PolicyType.AUTOMATIC,\
                                        Gtk.PolicyType.AUTOMATIC)

        self.actor_treeview = Gtk.TreeView(self.actor_store)
        self.actor_scroll.add(self.actor_treeview)
        self.actor_scroll.set_min_content_height(200)
        self.actor_scroll.set_min_content_width(300)

        self.grid.attach(self.actor_scroll, 2, 3, 3, 2)

        icon_renderer = Gtk.CellRendererPixbuf()
        icon_column = Gtk.TreeViewColumn("", icon_renderer, pixbuf=0)
        self.actor_treeview.append_column(icon_column)

        actor_renderer = Gtk.CellRendererText()
        actor_column = Gtk.TreeViewColumn("Actor", actor_renderer, text=1)
        actor_column.set_resizable(True)
        actor_column.set_max_width(300)
        self.actor_treeview.append_column(actor_column)

        name_renderer = Gtk.CellRendererText()
        name_column = Gtk.TreeViewColumn("Application Name", name_renderer, text=2)
        name_column.set_resizable(True)
        name_column.set_max_width(300)
        self.actor_treeview.append_column(name_column)

        self.app_info = Gio.DesktopAppInfo.get_all()
        for app in self.app_info:
            self.actor_store.append([self.get_icon_pixbuf(app.get_icon()),\
                    app.get_id(), app.get_name()])

    def get_icon_pixbuf(self, icon, size=32):
        theme = Gtk.IconTheme.get_default()
        icon_info = None
        pix = None

        if icon is None:
            icon_info = theme.lookup_icon("gtk-execute", \
                    size, Gtk.IconLookupFlags.FORCE_SVG)
        else:
            icon_info = theme.lookup_by_gicon(icon, \
                    size, Gtk.IconLookupFlags.FORCE_SVG)
            if icon_info is None:
                icon_info = theme.lookup_icon("gtk-execute", \
                            size, Gtk.IconLookupFlags.FORCE_SVG)

        try:
            pix = icon_info.load_icon()
        except:
            return None

        return pix

class TimeRangeWizardPage(Gtk.VBox):

    __gsignals__ = {
            'next' : (GObject.SIGNAL_RUN_FIRST, None, ()),
            'cancel' : (GObject.SIGNAL_RUN_FIRST, None, ())
        }

    def __init__(self, window):
        super(TimeRangeWizardPage, self).__init__()
        self.set_size_request(650, 400)
        self.main_window = window
        self.set_border_width(12)

        self.start_calendar = Gtk.Calendar()
        self.end_calendar = Gtk.Calendar()

        timerange_label = Gtk.Label(xalign = 0.5, yalign = 0)
        timerange_label.set_markup("<b>%s</b>" %("Time Range"))
        self.pack_start(timerange_label, False, False, 6)

        self.always_radio = Gtk.RadioButton(label="Always", xalign = 0.3)
        self.always_radio.set_hexpand(False)
        self.pack_start(self.always_radio, False, False, 6) 
        self.always_radio.connect("toggled", self.update_custom_sensitivity)

        self.custom_radio = Gtk.RadioButton(label="Custom (Date and HH:MM:SS)")
        self.custom_radio.join_group(self.always_radio)
        self.pack_start(self.custom_radio, False, False, 6)

        self.range_grid = Gtk.Grid()
        self.range_grid.set_row_spacing(5)
        self.range_grid.set_column_spacing(5)
        self.pack_start(self.range_grid, False, False, 6)

        from_label = Gtk.Label("From:", xalign=0.5, yalign=0)
        self.range_grid.attach(from_label, 0, 0, 3, 1)
        to_label = Gtk.Label("To:", xalign=0.5, yalign=0)
        self.range_grid.attach(to_label, 3, 0, 3, 1)

        """
        From and To Date Selection
        """
        self.start_frame = Gtk.Frame(label="From Date:")
        self.start_frame.add(self.start_calendar)
        self.range_grid.attach(self.start_frame, 0, 1, 3, 1)
        self.end_frame = Gtk.Frame(label="End Date:")
        self.end_frame.add(self.end_calendar)
        self.range_grid.attach(self.end_frame, 3, 1, 3, 1)

        """
        From Time section
        """
        self.from_hr = Gtk.SpinButton(numeric=True)
        self.from_hr.set_range(0, 23)
        self.from_hr.set_increments(1, 1)
        self.range_grid.attach(self.from_hr, 0, 2, 1, 1)

        self.from_min = Gtk.SpinButton(numeric=True)
        self.from_min.set_range(0, 59)
        self.from_min.set_increments(1,1)
        self.range_grid.attach(self.from_min, 1, 2, 1, 1)

        self.from_sec = Gtk.SpinButton(numeric=True)
        self.from_sec.set_range(0, 59)
        self.from_min.set_increments(1,1)
        self.range_grid.attach(self.from_sec, 2, 2, 1, 1)


        """
        To Time section
        """
        self.to_hr = Gtk.SpinButton(numeric=True)
        self.to_hr.set_range(0, 23)
        self.to_hr.set_increments(1, 1)
        self.range_grid.attach(self.to_hr, 3, 2, 1, 1)

        self.to_min = Gtk.SpinButton(numeric=True)
        self.to_min.set_range(0, 59)
        self.to_min.set_increments(1,1)
        self.range_grid.attach(self.to_min, 4, 2, 1, 1)

        self.to_sec = Gtk.SpinButton(numeric=True)
        self.to_sec.set_range(0, 59)
        self.to_min.set_increments(1,1)
        self.range_grid.attach(self.to_sec, 5, 2, 1, 1)

        
        label = Gtk.Label('Result Type:',xalign=0,yalign=0.5)
        self.range_grid.attach(label, 0, 3, 2, 1)
        self.result_type = Gtk.ComboBoxText()
        self.result_type.set_active(28)
        self.range_grid.attach(self.result_type, 2, 3, 2, 1)
        for entry in dir(ResultType)[:-1]:
            if not ( entry.startswith('__')):
                self.result_type.append_text(entry)
        # Set to MostRecentEvents
        self.result_type.set_active(28)

        label = Gtk.Label()
        self.range_grid.attach(label, 4, 4, 1, 1)
        self.next_button = Gtk.Button(label="Next")
        self.next_button.connect("clicked", self.on_next_clicked)
        self.range_grid.attach(self.next_button, 4, 5, 1, 1)
        self.cancel_button = Gtk.Button(label="Cancel")
        self.cancel_button.connect("clicked", self.on_cancel_clicked)
        self.range_grid.attach(self.cancel_button, 5, 5, 1, 1)

        self.update_sensitivity(False)
        self.next_button.grab_focus()


    def update_custom_sensitivity(self, widget):
        enable = not self.always_radio.get_active()
        self.update_sensitivity(enable)
        
    def update_sensitivity(self, enable):
        self.start_frame.set_sensitive(enable)
        self.end_frame.set_sensitive(enable)
        self.from_hr.set_sensitive(enable)
        self.from_min.set_sensitive(enable)
        self.from_sec.set_sensitive(enable)
        self.to_hr.set_sensitive(enable)
        self.to_min.set_sensitive(enable)
        self.to_sec.set_sensitive(enable)

    def on_cancel_clicked(self, button):
        self.emit("cancel")

    def on_next_clicked(self, button):
        self.emit("next")


class CalendarDialog(Gtk.Dialog):

    def __init__(self, window):
        super(CalendarDialog, self).__init__()
        self.main_window = window

        self.calendar =  Gtk.Calendar()

        box = self.get_content_area()
        box.add(self.calendar)
        self.set_decorated(False)
        self.set_position(0)
        self.set_property("skip-taskbar-hint", True)

    def get_calendar_widget():
        return self.calendar
