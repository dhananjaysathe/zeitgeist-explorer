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
from zeitgeist.datamodel import *
from lookupdata import *
from datamodel import MonitorData

from datetime import datetime

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
        self.time_range.connect("next", self.on_timerange_next_click)
        box.pack_start(self.time_range, False, False, 6)

        self.event_page = EventWizardPage(self.main_window)
        box.pack_start(self.event_page, False, False, 6)
        self.event_page.connect("back", self.on_event_back_click)
        self.event_page.connect("cancel", self.on_cancel_click)
        self.event_page.connect("next", self.on_event_next_click)

        self.subject_page = SubjectWizardPage(self.main_window)
        box.pack_start(self.subject_page, False, False, 6)

        box.show_all()
        self.event_page.hide()
        self.subject_page.hide()
        
        m_data = MonitorData()
        self.set_monitor_data(m_data)

    def on_cancel_click(self, widget):
        self.set_default_response(Gtk.ResponseType.CLOSE)
        self.emit("response", Gtk.ResponseType.CLOSE)

    def on_timerange_next_click(self, widget):
        self.time_range.hide()
        self.event_page.show()
        
    def on_event_next_click(self, widget):
        self.event_page.hide()
        self.subject_page.show()

    def on_event_back_click(self, widget):
        self.event_page.hide()
        self.time_range.show()

    def set_monitor_data(self, monitor_data):
        self.monitor_data = monitor_data
        self.time_range.set_data(monitor_data)
        self.event_page.set_data(monitor_data)
        self.subject_page.set_data(monitor_data)

class SubjectWizardPage(Gtk.VBox):

    __gsignals__ = {
            'back' : (GObject.SIGNAL_RUN_FIRST, None, ()),
            'finish' : (GObject.SIGNAL_RUN_FIRST, None, ()),
            'cancel' : (GObject.SIGNAL_RUN_FIRST, None, ())
        }
    def __init__(self, window):
        super(SubjectWizardPage, self).__init__()

        self.set_size_request(650, 400)
        self.main_window = window
        self.set_border_width(12)

        event_label = Gtk.Label(xalign=0.5, yalign=0)
        event_label.set_markup("<b>%s</b>" %("Subject Details"))
        self.pack_start(event_label, False, False, 6)

        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(15)
        self.grid.set_column_spacing(15)
        self.pack_start(self.grid, False, False, 6)

        
        list_vbox = Gtk.VBox()
        self.grid.attach(list_vbox, 0, 0, 1, 4)

        monitor_vbox = Gtk.VBox()
        list_vbox.pack_start(monitor_vbox, True, True, 0)

        self.subjects = Gtk.ListStore(int)
        self.subject_tree = Gtk.TreeView(model=self.subjects)
        #self.subject_tree.connect("cursor-changed", self.on_treeview_selected)
        self.subject_tree.set_size_request(200, 600)
        self.subject_tree.set_properties('border_width',1,'visible',True
                            ,'rules_hint',True,'headers_visible',False)

        scroll = Gtk.ScrolledWindow(None, None)
        scroll.add(self.subject_tree)
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.set_border_width(1)
        monitor_vbox.pack_start(scroll, True, True, 0)

        column_pix_name = Gtk.TreeViewColumn(_('Subjects'))
        self.subject_tree.append_column(column_pix_name)
        name_rend = Gtk.CellRendererText(ellipsize=Pango.EllipsizeMode.END)
        column_pix_name.pack_start(name_rend, False)
        column_pix_name.add_attribute(name_rend, "markup", 0)
        column_pix_name.set_resizable(True)

        # The toolbar which sits at the bottom just below
        # the list of templates. This toolbar contains + and - buttons
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
        #filter_remove.connect("clicked", self.on_remove_clicked)
        filter_remove.connect("clicked", self.on_remove_clicked)
        self.toolbar.insert(filter_remove, 1)

        
        event_inter_label = Gtk.Label("Interpretation:",xalign=1,yalign=0.5)
        self.grid.attach(event_inter_label, 1, 0, 1, 1)
        self.event_inter_combo = Gtk.ComboBoxText()
        #self.event_inter_combo.set_hexpand(True)
        self.event_inter_combo.set_wrap_width(600)
        self.grid.attach(self.event_inter_combo, 2, 0, 2, 1)
        self.event_inter_combo.append_text("")
        for entry in event_interpretations.keys():
            if entry is not None and len(entry) > 0:
                self.event_inter_combo.append_text(entry)

        # Event Manifesation
        event_manifes_label = Gtk.Label("Manifestation:",xalign=1,yalign=0.5)
        self.grid.attach(event_manifes_label, 1, 1, 1, 1)
        self.event_manifes_combo = Gtk.ComboBoxText()
        #self.event_manifes_combo.set_hexpand(True)
        self.grid.attach(self.event_manifes_combo, 2, 1, 2, 1)
        self.event_manifes_combo.append_text("")
        for entry in event_manifestations.keys():
            if entry is not None and len(entry) > 0:
                self.event_manifes_combo.append_text(entry)

        mimetype_label = Gtk.Label("Mimetype:", xalign=1, yalign=0.5)
        self.grid.attach(mimetype_label, 1, 2, 1, 1)
        self.mimetype_entry = Gtk.Entry()
        self.mimetype_entry.set_width_chars(40)
        self.grid.attach(self.mimetype_entry, 2, 2, 2, 1)

        storage_label = Gtk.Label("Storage:", xalign=1, yalign=0.5)
        self.grid.attach(storage_label, 1, 3, 1, 1)
        self.storage_entry = Gtk.Entry()
        self.storage_entry.set_width_chars(40)
        self.grid.attach(self.storage_entry, 2, 3, 2, 1)

    def on_add_clicked(self, button):
        pass

    def on_remove_clicked(self, button):
        pass

    def set_data(self, monitor_data):
        self.monitor_data = monitor_data

class EventWizardPage(Gtk.VBox):

    __gsignals__ = {
            'back' : (GObject.SIGNAL_RUN_FIRST, None, ()),
            'next' : (GObject.SIGNAL_RUN_FIRST, None, ()),
            'cancel' : (GObject.SIGNAL_RUN_FIRST, None, ())
        }
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
        self.grid.attach(self.event_inter_combo, 2, 0, 4, 1)
        self.event_inter_combo.append_text("")
        for entry in event_interpretations.keys():
            if entry is not None and len(entry) > 0:
                self.event_inter_combo.append_text(entry)

        # Event Manifesation
        event_manifes_label = Gtk.Label("Manifestation:",xalign=1,yalign=0.5)
        self.grid.attach(event_manifes_label, 0, 1, 1, 1)
        self.event_manifes_combo = Gtk.ComboBoxText()
        #self.event_manifes_combo.set_hexpand(True)
        self.grid.attach(self.event_manifes_combo, 2, 1, 4, 1)
        self.event_manifes_combo.append_text("")
        for entry in event_manifestations.keys():
            if entry is not None and len(entry) > 0:
                self.event_manifes_combo.append_text(entry)

        actor_label = Gtk.Label("Actor:", xalign=1, yalign=0.5)
        self.grid.attach(actor_label, 0, 2, 1, 1)
        self.actor_entry = Gtk.Entry()
        self.actor_entry.set_width_chars(70)
        self.grid.attach(self.actor_entry, 2, 2, 4, 1)

        self.actor_store = Gtk.ListStore(GdkPixbuf.Pixbuf, str, str)
        self.actor_scroll = Gtk.ScrolledWindow()
        self.actor_scroll.set_border_width(1)
        self.actor_scroll.set_shadow_type(Gtk.ShadowType.IN)    
        self.actor_scroll.set_policy(   Gtk.PolicyType.AUTOMATIC,\
                                        Gtk.PolicyType.AUTOMATIC)

        self.actor_treeview = Gtk.TreeView(self.actor_store)
        self.actor_treeview.connect("cursor-changed", self.on_actor_treeview_changed)
        self.actor_scroll.add(self.actor_treeview)
        self.actor_scroll.set_min_content_height(200)
        self.actor_scroll.set_min_content_width(300)

        self.grid.attach(self.actor_scroll, 2, 3, 4, 2)

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


        label = Gtk.Label()
        self.grid.attach(label, 4, 4, 1, 1)

        self.back_button = Gtk.Button(label="Back")
        self.back_button.connect("clicked", self.on_back_clicked)
        self.grid.attach(self.back_button, 3, 5, 1, 1)

        self.next_button = Gtk.Button(label="Next")
        self.next_button.connect("clicked", self.on_next_clicked)
        self.grid.attach(self.next_button, 4, 5, 1, 1)

        self.cancel_button = Gtk.Button(label="Cancel")
        self.cancel_button.connect("clicked", self.on_cancel_clicked)
        self.grid.attach(self.cancel_button, 5, 5, 1, 1)

    def set_data(self, monitor_data):
        self.monitor_data = monitor_data

    def on_actor_treeview_changed(self, widget):
        selection = self.actor_treeview.get_selection()
        model, iter_ = selection.get_selected()
        actor = model.get(iter_, 1)[0]
        self.actor_entry.set_text(actor)

    def on_back_clicked(self, button):
        self.emit("back")

    def on_cancel_clicked(self, button):
        self.emit("cancel")

    def on_next_clicked(self, button):
        self.emit("next")

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
        self.from_sec.set_increments(1,1)
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
        self.to_sec.set_increments(1,1)
        self.range_grid.attach(self.to_sec, 5, 2, 1, 1)

        
        #label = Gtk.Label('Result Type:',xalign=0,yalign=0.5)
        #self.range_grid.attach(label, 0, 3, 2, 1)
        #self.result_type = Gtk.ComboBoxText()
        #self.result_type.set_active(28)
        #self.range_grid.attach(self.result_type, 2, 3, 2, 1)
        #for entry in dir(ResultType)[:-1]:
            #if not ( entry.startswith('__')):
                #self.result_type.append_text(entry)
        # Set to MostRecentEvents
        #self.result_type.set_active(28)

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


    def set_data(self, monitor_data):
        self.monitor_data = monitor_data
        self.monitor_data.timerange = TimeRange.until_now()

        is_always=TimeRange.is_always(self.monitor_data.timerange)
        self.always_radio.set_active(is_always)
        self.custom_radio.set_active(not is_always)

        if not is_always:
            print("Timerange: %s, %s"\
            %(self.monitor_data.timerange[0], \
            self.monitor_data.timerange[1]))
            start_datetime = datetime.fromtimestamp(self.monitor_data.timerange[0]/1000)
            end_datetime = datetime.fromtimestamp(self.monitor_data.timerange[1]/1000)

            self.start_calendar.select_day(start_datetime.day)
            self.start_calendar.select_month( \
                                start_datetime.month - 1, \
                                start_datetime.year)
            self.from_hr.set_value(start_datetime.hour)
            self.from_min.set_value(start_datetime.minute)
            self.from_sec.set_value(start_datetime.second)

            self.end_calendar.select_day(end_datetime.day)
            self.end_calendar.select_month( \
                                end_datetime.month - 1, \
                                end_datetime.year)
            self.to_hr.set_value(end_datetime.hour)
            self.to_min.set_value(end_datetime.minute)
            self.to_sec.set_value(end_datetime.second)

    def save(self):
        if self.always_radio.get_active():
            self.monitor_data.timerange = TimeRange.always()

        if self.custom_radio.get_active():
            date = self.start_calendar.get_date()
            start_datetime = datetime(date[0], \
                                  date[1] + 1, \
                                  date[2], \
                                  int(self.from_hr.get_value()), \
                                  int(self.from_min.get_value()), \
                                  int(self.from_sec.get_value()))

            date = self.start_calendar.get_date()
            end_datetime = datetime(date[0], \
                                  date[1] + 1, \
                                  date[2], \
                                  int(self.from_hr.get_value()), \
                                  int(self.from_min.get_value()), \
                                  int(self.from_sec.get_value()))
        
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
