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

from datetime import datetime
from gi.repository import Gtk

class TimeRangeViewer(Gtk.VBox):

    def __init__(self,start_time=None,end_time=None):
        super(TimeRangeViewer, self).__init__()

        timerange_label = Gtk.Label("Time Range",xalign=0 ,yalign=0.5)
        self.pack_start(timerange_label,False,False,3)

        self.always_radio = Gtk.RadioButton(label= "Always")
        self.pack_start(self.always_radio,False,False,3)
        self.always_radio.connect('toggled',self.update_sensitivity)

        self.custom_radio = Gtk.RadioButton(label= "Custom")
        self.custom_radio.join_group(self.always_radio)
        self.pack_start(self.custom_radio,False,False,3)

        enteries_box = Gtk.VBox()
        enteries_box.set_margin_left(14)
        self.pack_start(enteries_box,False,False,3)

        self.start_time = DatetimePicker(start_time)
        self.end_time = DatetimePicker(end_time)
        self.start_time.update_sensitivity(False)
        self.end_time.update_sensitivity(False)

        enteries_box.pack_start(Gtk.Label('From:',xalign=0 ,yalign=0.5),False,False,0)
        enteries_box.pack_start(self.start_time,False,False,1)
        enteries_box.pack_start(Gtk.Label('To:',xalign=0 ,yalign=0.5),False,False,0)
        enteries_box.pack_start(self.end_time,False,False,1)

    def get_start_time(self):
        return self.start_time.get_datetime()

    def get_end_time(self):
        return self.end_time.get_datetime()

    def update_sensitivity(self,widget):
        enable = not self.always_radio.get_active()
        self.start_time.update_sensitivity(enable)
        self.end_time.update_sensitivity(enable)

class DatetimePicker(Gtk.HBox):

    def __init__(self,time):

        super(DatetimePicker, self).__init__()

        if time is None:
            time = datetime.now()

        #date
        date_holder = Gtk.HBox()
        self.pack_start(date_holder,False,False,3)
        date_holder.pack_start(Gtk.Label('DD|MM|YY:'),False,False,3)
        self.date_spin_day = Gtk.SpinButton(numeric=True)
        self.date_spin_day.set_adjustment(Gtk.Adjustment(lower=1,
                 upper=32,page_size=1,step_increment=1,value=time.day))
        date_holder.pack_start(self.date_spin_day,False,False,0)
        self.date_spin_month = Gtk.SpinButton(numeric=True)
        self.date_spin_month.set_adjustment(Gtk.Adjustment(lower=1,
                upper=13,page_size=1,step_increment=1,value=time.month))
        date_holder.pack_start(self.date_spin_month,False,False,0)
        self.date_spin_year = Gtk.SpinButton(numeric=True)
        self.date_spin_year.set_adjustment(Gtk.Adjustment(lower=2010,
               upper=2100,page_size=1,step_increment=1,value=time.year))
        date_holder.pack_start(self.date_spin_year,False,False,0)

        #time
        time_holder = Gtk.HBox()
        self.pack_end(time_holder,False,False,3)
        time_holder.pack_start(Gtk.Label('HH:MM:SS '),False,False,3)
        self.time_spin_hour = Gtk.SpinButton(numeric=True)
        self.time_spin_hour.set_adjustment(Gtk.Adjustment(lower=0,
                 upper=24,page_size=1,step_increment=1,value=time.hour))
        time_holder.pack_start(self.time_spin_hour,False,False,0)
        self.time_spin_min = Gtk.SpinButton(numeric=True)
        self.time_spin_min.set_adjustment(Gtk.Adjustment(lower=0,
               upper=60,page_size=1,step_increment=1,value=time.minute))
        time_holder.pack_start(self.time_spin_min,False,False,0)
        self.time_spin_sec = Gtk.SpinButton(numeric=True)
        self.time_spin_sec.set_adjustment(Gtk.Adjustment(lower=0,
               upper=60,page_size=1,step_increment=1,value=time.second))
        time_holder.pack_start(self.time_spin_sec,False,False,0)

        self.show_all()

    def get_datetime(self):
        return datetime(self.date_spin_year.get_value_as_int(),
                        self.date_spin_month.get_value_as_int(),
                        self.date_spin_day.get_value_as_int(),
                        self.time_spin_hour.get_value_as_int(),
                        self.time_spin_min.get_value_as_int(),
                        self.time_spin_sec.get_value_as_int())

    def update_sensitivity(self,enable):
        self.date_spin_year.set_sensitive(enable)
        self.date_spin_month.set_sensitive(enable)
        self.date_spin_day.set_sensitive(enable)
        self.time_spin_hour.set_sensitive(enable)
        self.time_spin_min.set_sensitive(enable)
        self.time_spin_sec.set_sensitive(enable)
