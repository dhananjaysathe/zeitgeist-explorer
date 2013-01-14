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
        self.set_properties('margin', 12, 'content-area-spacing', 6)
        self.set_size_request(600,600)
        self.set_type_hint(Gdk.WindowTypeHint.MENU)
        self.is_predefined = True

        box = self.get_content_area()
        self.time_range = TimeRangeSelector(self.main_window)
        box.pack_start(self.time_range, False, False, 3)
        box.show_all()

class TimeRangeSelector(Gtk.VBox):

    def __init__(self, window):
        super(TimeRangeSelector, self).__init__()
        self.main_window = window

        timerange_label = Gtk.Label("Time Range", xalign = 0.5, yalign = 0)
        self.pack_start(timerange_label, False, False, 3)

        self.always_radio = Gtk.RadioButton(label="Always", xalign = 0.3)
        self.always_radio.set_hexpand(False)
        self.pack_start(self.always_radio, False, False, 3)
        #self.always_radio.connect("toggled", self.update_sensitivity)

        self.custom_radio = Gtk.RadioButton(label="Custom")
        self.custom_radio.join_group(self.always_radio)
        self.pack_start(self.custom_radio, False, False, 3)
