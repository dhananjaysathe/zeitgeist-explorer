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
from zeitgeist.datamodel import ResultType

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
        self.set_size_request(650, 400)
        self.main_window = window
        self.set_border_width(12)

        self.start_calendar = Gtk.Calendar()
        self.end_calendar = Gtk.Calendar()

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
        self.range_grid.attach(self.next_button, 4, 5, 1, 1)
        self.cancel_button = Gtk.Button(label="Cancel")
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
