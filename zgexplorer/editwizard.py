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

from gi.repository import Gtk, Gdk, Pango

class TemplateEditWizard(Gtk.Dialog):

    def __init__(self, window):
        super(TemplateEditWizard, self).__init__()
        self.main_window = window

        self.set_destroy_with_parent(True)
        self.set_properties('margin', 6, 'content-area-spacing', 6)
        self.set_type_hint(Gdk.WindowTypeHint.MENU)
        self.is_predefined = True

        box = self.get_content_area()
        self.time_range = TimeRangeSelector(self.main_window)
        box.pack_start(self.time_range, False, False, 6)
        box.show_all()

class TimeRangeSelector(Gtk.VBox):

    def __init__(self, window):
        super(TimeRangeSelector, self).__init__()
        self.set_size_request(700, 500)
        self.main_window = window
        self.set_border_width(12)

        self.start_calendar = CalendarDialog(self.main_window)
        self.end_calendar = CalendarDialog(self.main_window)

        timerange_label = Gtk.Label("Time Range", xalign = 0.5, yalign = 0)
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

        from_label = Gtk.Label("From:", xalign=1, yalign=0)
        self.range_grid.attach(from_label, 0, 0, 1, 1)
        to_label = Gtk.Label("To:", xalign=1, yalign=0)
        self.range_grid.attach(to_label, 0, 1, 1, 1)

        """
        From Date Section
        """
        self.from_date = Gtk.Entry()
        self.from_date.set_editable(False)
        self.from_date.set_width_chars(20)
        self.range_grid.attach(self.from_date, 1, 0, 1, 1)
        self.from_button = Gtk.Button()
        self.from_button.connect("clicked", self.on_start_button_clicked)
        arrow1 = Gtk.Arrow(Gtk.ArrowType.DOWN, 0)
        self.from_button.add(arrow1)
        self.range_grid.attach(self.from_button, 2, 0, 1, 1)

        """
        From Time Section
        """
        self.to_date = Gtk.Entry()
        self.to_date.set_editable(False)
        self.from_date.set_width_chars(20)
        self.range_grid.attach(self.to_date, 1, 1, 1, 1)
        self.to_button = Gtk.Button()
        self.to_button.connect("clicked", self.on_end_button_clicked)
        arrow2 = Gtk.Arrow(Gtk.ArrowType.DOWN, 0)
        self.to_button.add(arrow2)
        self.range_grid.attach(self.to_button, 2, 1, 1, 1)

        """
        From Time section
        """
        self.from_hr = Gtk.SpinButton(numeric=True)
        self.from_hr.set_range(0, 23)
        self.from_hr.set_increments(1, 1)
        self.range_grid.attach(self.from_hr, 3, 0, 1, 1)

        self.from_min = Gtk.SpinButton(numeric=True)
        self.from_min.set_range(0, 59)
        self.from_min.set_increments(1,1)
        self.range_grid.attach(self.from_min, 4, 0, 1, 1)

        self.from_sec = Gtk.SpinButton(numeric=True)
        self.from_sec.set_range(0, 59)
        self.from_min.set_increments(1,1)
        self.range_grid.attach(self.from_sec, 5, 0, 1, 1)


        """
        To Time section
        """
        self.to_hr = Gtk.SpinButton(numeric=True)
        self.to_hr.set_range(0, 23)
        self.to_hr.set_increments(1, 1)
        self.range_grid.attach(self.to_hr, 3, 1, 1, 1)

        self.to_min = Gtk.SpinButton(numeric=True)
        self.to_min.set_range(0, 59)
        self.to_min.set_increments(1,1)
        self.range_grid.attach(self.to_min, 4, 1, 1, 1)

        self.to_sec = Gtk.SpinButton(numeric=True)
        self.to_sec.set_range(0, 59)
        self.to_min.set_increments(1,1)
        self.range_grid.attach(self.to_sec, 5, 1, 1, 1)


        self.update_sensitivity(False)

    def on_end_button_clicked(self, widget):
        self.end_calendar.show_all()
        parent_window = self.get_parent_window()
        window_x, window_y = parent_window.get_position()

        allocation = self.to_date.get_allocation()
        self.end_calendar.move(window_x + allocation.x, \
                    window_y + allocation.y + allocation.height)
        self.end_calendar.set_size_request(allocation.width, -1)
        self.end_calendar.set_resizable(False)
        widget.set_sensitive(False)
        self.end_calendar.connect("focus-out-event", self.on_end_lose_focus)
    
    def on_end_lose_focus(self, widget, event):
        self.end_calendar.hide()
        self.to_button.set_sensitive(True)

    def on_start_button_clicked(self, widget):
        self.start_calendar.show_all()

    def update_custom_sensitivity(self, widget):
        enable = not self.always_radio.get_active()
        self.update_sensitivity(enable)
        
    def update_sensitivity(self, enable):
        self.from_date.set_sensitive(enable)
        self.from_button.set_sensitive(enable)
        self.to_date.set_sensitive(enable)
        self.to_button.set_sensitive(enable)
        self.from_hr.set_sensitive(enable)
        self.from_min.set_sensitive(enable)
        self.from_sec.set_sensitive(enable)
        self.to_hr.set_sensitive(enable)
        self.to_min.set_sensitive(enable)
        self.to_sec.set_sensitive(enable)


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
