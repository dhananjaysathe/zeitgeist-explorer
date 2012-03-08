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

class FilterManagerDialog(Gtk.Dialog):

    def __init__(self):
        super(FilterManagerDialog, self).__init__()
        self.set_destroy_with_parent(True)
        self.set_title("Filter Manager")
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.set_size_request(600, 300)
        self.spacing = 6
        self.margin = 12

        self.store = Gtk.ListStore(int, str)

        box = self.get_content_area() 

        # Top Level Radio Button
        radio_hbox = Gtk.HBox()
        box.pack_start(radio_hbox, False, True, 6)

        predefined_radio = Gtk.RadioButton()
        predefined_radio.set_label("Predefined")
        predefined_radio.connect("toggled", self.on_button_toggled, "1")
        radio_hbox.pack_start(predefined_radio, False, False, 0)

        custom_radio = Gtk.RadioButton.new_from_widget(predefined_radio)
        custom_radio.set_label("User Defined")
        custom_radio.connect("toggled", self.on_button_toggled, "2")
        radio_hbox.pack_start(custom_radio, False, False, 0)

         
        self.filter_view = Gtk.TreeView(self.store)
        self.filter_view.set_headers_visible(False)
        self.filter_view.set_rules_hint(True)
        #box.pack_start(self.filter_view, True, True, 0)
        
        self.scroll = Gtk.ScrolledWindow()
        self.scroll.add(self.filter_view)
        self.scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scroll.set_shadow_type(Gtk.ShadowType.IN)
        self.scroll.set_border_width(1)
        box.pack_start(self.scroll, True, True, 6)
        
        box.show_all()

    def on_button_toggled(self, button, name):
        if button.get_active():
            state = "on"
        else:
            state = "off"
        print "Button", name, "was turned", state
