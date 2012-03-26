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

import codecs
from datetime import datetime
from gi.repository import Gtk, Gio
from zeitgeist.datamodel import Event, Subject, Manifestation, \
    Interpretation, StorageState, Symbol, ResultType
from lookupdata import *

# workaround for Gtk ComboBoxText Widgets
def get_active_text(combobox):
      model = combobox.get_model()
      active = combobox.get_active()
      if active < 0:
          return ''
      return model[active][0]

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

        enteries_box.pack_start(Gtk.Label('From :',xalign=0 ,yalign=0.5),False,False,0)
        enteries_box.pack_start(self.start_time,False,False,1)
        enteries_box.pack_start(Gtk.Label('To :',xalign=0 ,yalign=0.5),False,False,0)
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
        date_holder.pack_start(Gtk.Label('DD|MM|YY :'),False,False,3)
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






class TemplateEditor(Gtk.Dialog): # NOTE: INCOMPLETE
    def __init__(self):
        super(TemplateEditor, self).__init__()

        self.set_title("Template Editor")
        self.start_time = None
        self.end_time = None

        self.create()

    def create(self):
        outer = self.get_content_area()
        frame = Gtk.Frame(shadow_type=Gtk.ShadowType.ETCHED_IN,border_width=5)
        outer.add(frame)
        box= Gtk.VBox()
        frame.add(box)

        self.timerange = TimeRangeViewer(self.start_time,self.end_time)
        box.pack_start(self.timerange,False,False,0)

        table = Gtk.Table(1,2,True)
        box.pack_start(table,False,False,0)

        label = Gtk.Label('Result Type :',xalign=0,yalign=0.5)
        table.attach(label, 0, 1, 0, 1, xpadding=6 ,ypadding=6)
        self.result_type = Gtk.ComboBoxText()
        self.result_type.set_active(28)
        table.attach(self.result_type, 1, 2, 0, 1, xpadding=6 ,ypadding=6)
        for entry in dir(ResultType)[:-1]:
            if not ( entry.startswith('__')):
                self.result_type.append_text(entry)

        self.table = Gtk.Table(10, 2, False,border_width=5)
        box.pack_start(self.table, True, True, 0)

        event_label = Gtk.Label()
        event_label.set_markup("<b>%s</b>" %("Event"))

        # Event Interpretation
        event_inter_label = Gtk.Label("Interpretation :",xalign=0,yalign=0.5)
        self.event_inter_field = Gtk.ComboBoxText()
        for entry in event_interpretations.keys():
            self.event_inter_field.append_text(entry)

        # Event Manifesation
        event_manifes_label = Gtk.Label("Manifestation :",xalign=0,yalign=0.5)
        self.event_manifes_field = Gtk.ComboBoxText()
        for entry in event_manifestations.keys():
           self.event_manifes_field.append_text(entry)

        actor_label = Gtk.Label("Actor :",xalign=0,yalign=0.5)
        self.actor_field = Gtk.Label()
        self.actor_field.set_justify(Gtk.Justification.LEFT)
        self.actor_field.set_line_wrap(True)

        actor_hbox = Gtk.HBox(margin_bottom=6)

        self.actor_dropdown = Gtk.ComboBoxText()
        self.app_dict={'':''}
        for app in Gio.DesktopAppInfo.get_all():
            self.actor_dropdown.append_text(app.get_name())
            self.app_dict[app.get_name()] = app.get_id()

        self.actor_dropdown.connect("changed", self.on_app_changed)

        actor_hbox.pack_start(self.actor_dropdown, False, False, 12)
        self.actor_image = Gtk.Image()
        self.actor_image.set_size_request(32, 32)
        actor_hbox.pack_start(self.actor_image, False, False, 2)
        self.actor_value = Gtk.Label(xalign=0,yalign=0.5)
        actor_hbox.pack_start(self.actor_value, False, False, 12)

        subj_label = Gtk.Label()
        subj_label.set_markup("<b>%s</b>" %("Subject"))

        # URI
        uri_label = Gtk.Label("URI :",xalign=0,yalign=0.5)
        self.uri_field = Gtk.Entry(width_chars= 40)

        # Current URI
        curr_uri_label = Gtk.Label("Current URI :",xalign=0,yalign=0.5)
        self.curr_uri_field = Gtk.Entry(width_chars= 40)


        # Subject Interpretation
        subj_inter_label = Gtk.Label("Interpretation :",xalign=0,yalign=0.5)
        self.subj_inter_field = Gtk.ComboBoxText()
        for entry in subject_interpretations.keys():
            self.subj_inter_field.append_text(entry)

        # Subject Manifesation
        subj_manifes_label = Gtk.Label("Manifestation :",xalign=0,yalign=0.5)
        self.subj_manifes_field = Gtk.ComboBoxText()
        for entry in subject_manifestations.keys():
               self.subj_manifes_field.append_text(entry)

        # Origin
        origin_label = Gtk.Label("Origin :",xalign=0,yalign=0.5)
        self.origin_field = Gtk.Entry(width_chars= 40)

        # Mimetype
        mimetype_label = Gtk.Label("Mimetype :",xalign=0,yalign=0.5)
        self.mimetype_field = Gtk.Entry(width_chars= 40)

        # Storage
        storage_label = Gtk.Label("Storage :",xalign=0,yalign=0.5)
        self.storage_field = Gtk.ComboBoxText()
        for entry in storage_states.keys():
               self.storage_field.append_text(entry)


        attach_list = (
             (event_label,(0, 2, 0, 1)),
             (event_inter_label,(0, 1, 1, 2)),
             (self.event_inter_field,(1, 2, 1, 2)),
             (event_manifes_label,(0, 1, 2, 3)),
             (self.event_manifes_field,(1, 2, 2, 3)),
             (actor_label,(0, 1, 3, 4)),
             (self.actor_field,(1, 2, 3, 4)),
             (actor_hbox,(1, 2, 4, 5)),
             (subj_label,(0, 2, 5, 6)),
             (uri_label,(0, 1, 6, 7)),
             (self.uri_field,(1, 2, 6, 7)),
             (curr_uri_label,(0, 1, 7, 8)),
             (self.curr_uri_field,(1, 2, 7, 8)),
             (subj_inter_label,(0, 1, 8, 9)),
             (self.subj_inter_field,(1, 2, 8, 9)),
             (subj_manifes_label,(0, 1, 9, 10)),
             (self.subj_manifes_field,(1, 2, 9,10)),
             (origin_label,(0, 1, 10, 11)),
             (self.origin_field,(1, 2, 10, 11)),
             (mimetype_label,(0, 1, 11, 12)),
             (self.mimetype_field,(1, 2, 11, 12)),
             (storage_label,(0, 1, 12, 13)),
             (self.storage_field,(1, 2, 12, 13))
         )
        for widget_entry in attach_list :
            widget,pos = widget_entry
            self.table.attach(widget,pos[0],pos[1], pos[2], pos[3], xpadding=3, ypadding=3)

        self.add_buttons('Apply',Gtk.ResponseType.APPLY,'Cancel',Gtk.ResponseType.CANCEL,'OK',Gtk.ResponseType.OK,)

    def set_values(self):
        self.event_inter_field.set_active(event_interpretations. \
                        values().index(self.event.get_interpretation()))
        self.event_manifes_field.set_active(event_manifestations.\
                        values().index(self.event.get_manifestation()))

        actor = self.event.get_actor()
        self.actor_field.set_text(actor)
        self.actor_field.set_justify(Gtk.Justification.LEFT)
        self.actor_field.set_line_wrap(True)
        if actor is not "" and actor.startswith("application://"):
            actor =  actor.replace("application://", "")
            try:
                app_info = Gio.DesktopAppInfo.new(actor)
                self.actor_dropdown.set_active(self.app_dict.keys().index(app_info.get_name()))
                self.actor_value.set_text(app_info.get_display_name())
                self.actor_image.set_from_gicon(app_info.get_icon(), Gtk.IconSize.BUTTON)

            except TypeError:
                print("Wrong actor string: %s" %(actor))
        else:
            self.actor_value.set_text("")

        sub = self.event.get_subjects()[0]

        self.uri_field.set_text(sub.get_uri())
        self.curr_uri_field.set_text(sub.get_current_uri())
        self.subj_inter_field.set_active(subject_interpretations. \
                        values().index(sub.get_interpretation()))
        self.subj_manifes_field.set_active(subject_manifestations.\
                        values().index(sub.get_manifestation()))
        self.origin_field.set_text(sub.get_origin())
        self.mimetype_field.set_text(sub.get_mimetype())
        self.storage_field.set_active(storage_states.\
                        values().index(sub.get_storage()))



    def get_values(self):


        ev_inter=get_active_text(self.event_inter_field)
        self.event.set_interpretation(event_interpretations[ev_inter])

        ev_manifes=get_active_text(self.event_manifes_field)
        self.event.set_manifestation(event_manifestations[ev_manifes])

        app=get_active_text(self.actor_dropdown)
        self.event.set_actor(''.join([r"application://",self.app_dict[app]]))

        #subject
        sub = self.event.get_subjects()[0]

        sub.set_uri(self.uri_field.get_text().strip())
        sub.set_current_uri(self.curr_uri_field.get_text().strip())

        sub_inter= get_active_text(self.subj_inter_field)
        sub.set_interpretation(subject_interpretations[sub_inter])

        sub_manifes = get_active_text(self.subj_manifes_field)
        sub.set_manifestation(subject_manifestations[sub_manifes])

        sub.set_origin(self.origin_field.get_text().strip())
        sub.set_mimetype(self.mimetype_field.get_text().strip())

        sub_stor = get_active_text(self.storage_field)
        sub.set_storage(storage_states[sub_stor])

        self.event.set_subjects(sub)

    def on_app_changed(self,widget):
        app=get_active_text(self.actor_dropdown)
        try:
            actor = self.app_dict[app]
            self.actor_field.set_text(''.join([r'application://',actor]))
            self.actor_field.set_justify(Gtk.Justification.LEFT)
            self.actor_field.set_line_wrap(True)
            app_info = Gio.DesktopAppInfo.new(actor)
            self.actor_value.set_text(app_info.get_display_name())
            self.actor_image.set_from_gicon(app_info.get_icon(), Gtk.IconSize.BUTTON)
        except:
            print('DEBUG : Complete Application Info for %s not available',actor)
            self.actor_field.set_text('')
            self.actor_value.set_text('')
            self.actor_image.clear()

    def get_time_range(self):
        start = self.timerange.get_start_time()
        end = self.timerange.get_end_time()
        #TODO
        #return deltatime range in zeitgeist format??

    def get_template(self):
        self.get_values()
        timerange = self.get_time_range()
        template = ['','',self.event,timerange,]
        template[2] = self.event
         # this ensure latest selections are taken before building the template
        #this function prepares a template from the Time range and
        # comment gui fields and self.event that has been stored
        return template

    def set_template(self,template):
        if template is None:

            self.event = Event()
            self.event.set_subjects([Subject(),])
            self.start_time = None
            self.end_time = None
            self.edit_mode = False
        else:
            self.event = template[2]
            #self.start_time =
            #self.end_time =
            self.edit_mode = True

        self.set_values()





class TemplateViewer(Gtk.VBox):
    def __init__(self):
       super(TemplateViewer, self).__init__()

       self.table = Gtk.Table(10, 2, False, border_width=10)
       self.pack_start(self.table, True, True, 0)

       event_label = Gtk.Label()
       event_label.set_markup("<b>%s</b>" %("Event"))

       # Event Interpretation
       event_inter_label = Gtk.Label(xalign=1.0,yalign=0.5)
       event_inter_label.set_markup("<b>%s :</b>" %("Interpretation"))
       self.event_inter_field = Gtk.Label("", xalign=0,yalign=0.5)
       self.event_inter_field.set_width_chars(60)

       # Event Manifesation
       event_manifes_label = Gtk.Label(xalign=1.0,yalign=0.5)
       event_manifes_label.set_markup("<b>%s : </b>" %("Manifestation"))
       self.event_manifes_field = Gtk.Label("", xalign=0,yalign=0.5)


       actor_label = Gtk.Label(xalign=1.0,yalign=0.5)
       actor_label.set_markup("<b>%s : </b>" %("Actor : "))
       self.actor_field = Gtk.Label("", xalign=0,yalign=0.5)


       actor_hbox = Gtk.HBox(margin_bottom=6)
       self.actor_image = Gtk.Image()
       self.actor_image.set_size_request(32, 32)
       actor_hbox.pack_start(self.actor_image, False, False, 12)
       self.actor_value = Gtk.Label()
       actor_hbox.pack_start(self.actor_value, False, False, 12)

       subj_label = Gtk.Label()
       subj_label.set_markup("<b>%s</b>" %("Subject"))


       # Subject Interpretation
       subj_inter_label = Gtk.Label(xalign=1.0,yalign=0.5)
       subj_inter_label.set_markup("<b>%s : </b>" %("Interpretation"))
       self.subj_inter_field = Gtk.Label("", xalign=0,yalign=0.5)


       # Subject Manifesation
       subj_manifes_label = Gtk.Label(xalign=1.0,yalign=0.5)
       subj_manifes_label.set_markup("<b>%s : </b>" %("Manifestation"))
       self.subj_manifes_field = Gtk.Label("", xalign=0,yalign=0.5)


       # Mimetype
       mimetype_label = Gtk.Label(xalign=1.0,yalign=0.5)
       mimetype_label.set_markup("<b>%s : </b>" %("Mimetype"))
       self.mimetype_field = Gtk.Label("", xalign=0,yalign=0.5)


       # Storage
       storage_label = Gtk.Label(xalign=1.0,yalign=0.5)
       storage_label.set_markup("<b>%s : </b>" %("Storage"))
       self.storage_field = Gtk.Label("", xalign=0,yalign=0.5)


       attach_list = (
            (event_label,(0, 2, 0, 1)),
            (event_inter_label,(0, 1, 1, 2)),
            (self.event_inter_field,(1, 2, 1, 2)),
            (event_manifes_label,(0, 1, 2, 3)),
            (self.event_manifes_field,(1, 2, 2, 3)),
            (actor_label,(0, 1, 3, 4)),
            (self.actor_field,(1, 2, 3, 4)),
            (actor_hbox,(1, 2, 4, 5)),
            (subj_label,(0, 2, 5, 6)),
            (subj_inter_label,(0, 1, 6, 7)),
            (self.subj_inter_field,(1, 2, 6, 7)),
            (subj_manifes_label,(0, 1, 7, 8)),
            (self.subj_manifes_field,(1, 2, 7, 8)),
            (mimetype_label,(0, 1, 8, 9)),
            (self.mimetype_field,(1, 2, 8, 9)),
            (storage_label,(0, 1, 9, 10)),
            (self.storage_field,(1, 2, 9, 10))
        )
       for widget_entry in attach_list :
           widget,pos = widget_entry
           self.table.attach(widget,pos[0],pos[1], pos[2], pos[3], xpadding=3, ypadding=3)

    def set_values(self, values):
        ev = values[2]

        # Event Interpretation
        ev_inter = ev.get_interpretation()
        self.event_inter_field.set_text(ev_inter.name \
                if type(ev_inter) is Symbol else "")
        self.event_inter_field.set_tooltip_text(ev_inter.doc \
                if type(ev_inter) is Symbol else "")

        # Event Manifestation
        ev_manifes = ev.get_manifestation()
        self.event_manifes_field.set_text(ev_manifes.name \
                if type(ev_manifes) is Symbol else "")
        self.event_manifes_field.set_tooltip_text(ev_manifes.doc \
                if type(ev_manifes) is Symbol else "")

        actor = ev.get_actor()
        self.actor_field.set_text(actor)
        self.actor_field.set_line_wrap(True)

        if actor is not "" and actor.startswith("application://"):
            actor =  actor.replace("application://", "")
            try:
                app_info = Gio.DesktopAppInfo.new(actor)
                self.actor_value.set_text(app_info.get_display_name())
                self.actor_image.set_from_gicon(app_info.get_icon(), Gtk.IconSize.BUTTON)
            except TypeError:
                print("Wrong actor string: %s" %(actor))
        else:
            self.actor_value.set_text("")
            self.actor_image.clear()

        subj = None
        if len(ev.get_subjects()) > 0:
            subj = ev.get_subjects()[0]
        else:
            subj = Subject()
        if type(subj) == str :
            subj = Subject()

        # Subject Interpretation
        subj_inter =  subj.get_interpretation()
        self.subj_inter_field.set_text(subj_inter.name \
                if type(subj_inter) is Symbol else "")
        self.subj_inter_field.set_tooltip_text(subj_inter.doc \
                if type(subj_inter) is Symbol else "")

        # Event Manifestation
        subj_manifes =  subj.get_manifestation()
        self.subj_manifes_field.set_text(subj_manifes.name
                if type(subj_manifes) is Symbol else "")
        self.subj_manifes_field.set_tooltip_text(subj_manifes.doc \
                if type(subj_manifes) is Symbol else "")

        self.mimetype_field.set_text(subj.get_mimetype())
        self.storage_field.set_text(subj.get_storage())

class EventViewer(Gtk.VBox):

    def __init__(self):
        super(EventViewer, self).__init__()

        self.table = Gtk.Table(18, 4, False,border_width=1)
        self.pack_start(self.table, False, False, 6)

        id_label = Gtk.Label(xalign=0,yalign=0.5)
        id_label.set_markup("<b>%s</b>" %("Event ID"))

        self.id_entry = Gtk.Label(xalign=0,yalign=0.5)

        time_label = Gtk.Label(xalign=0,yalign=0.5)
        time_label.set_markup("<b>%s</b>" %("Timestamp"))

        self.time_entry = Gtk.Label(xalign=0,yalign=0.5)

        event_int_label = Gtk.Label(xalign=0,yalign=0.5)
        event_int_label.set_markup("<b>%s</b>" %("Interpretation"))

        self.event_int_entry = Gtk.Label(xalign=0,yalign=0.5)

        event_manifes_label = Gtk.Label(xalign=0,yalign=0.5)
        event_manifes_label.set_markup("<b>%s</b>" %("Manifestation"))

        self.event_manifes_entry = Gtk.Label(xalign=0,yalign=0.5)

        actor_label = Gtk.Label(xalign=0,yalign=0.5)
        actor_label.set_markup("<b>%s</b>" %("Actor"))

        self.actor_entry = Gtk.Label(xalign=0,yalign=0.5)

        actor_box = Gtk.HBox()
        self.image_entry = Gtk.Image(xalign=0,yalign=0.5)
        actor_box.pack_start(self.image_entry, False, False, 6)
        self.actor_name_entry = Gtk.Label(xalign=0,yalign=0.5)
        actor_box.pack_start(self.actor_name_entry, False, False, 6)

        uri_label = Gtk.Label(xalign=0,yalign=0.5)
        uri_label.set_markup("<b>%s</b>" %("URI"))

        self.uri_entry = Gtk.Label(xalign=0,yalign=0.5)

        current_uri_label = Gtk.Label(xalign=0,yalign=0.5)
        current_uri_label.set_markup("<b>%s</b>" %("Current URI"))

        self.current_uri_entry = Gtk.Label(xalign=0,yalign=0.5)

        subj_int_label = Gtk.Label(xalign=0,yalign=0.5)
        subj_int_label.set_markup("<b>%s</b>" %("Interpretation"))

        self.subj_int_entry = Gtk.Label(xalign=0,yalign=0.5)

        subj_manifes_label = Gtk.Label(xalign=0,yalign=0.5)
        subj_manifes_label.set_markup("<b>%s</b>" %("Manifestation"))

        self.subj_manifes_entry = Gtk.Label(xalign=0,yalign=0.5)


        origin_label = Gtk.Label(xalign=0,yalign=0.5)
        origin_label.set_markup("<b>%s</b>" %("Origin"))

        self.origin_entry = Gtk.Label(xalign=0,yalign=0.5)

        mimetype_label = Gtk.Label(xalign=0,yalign=0.5)
        mimetype_label.set_markup("<b>%s</b>" %("Mimetype"))

        self.mime_entry = Gtk.Label(xalign=0,yalign=0.5)

        text_label = Gtk.Label(xalign=0,yalign=0.5)
        text_label.set_markup("<b>%s</b>" %("Text"))

        self.text_entry = Gtk.Label(xalign=0,yalign=0.5)

        storage_label = Gtk.Label(xalign=0,yalign=0.5)
        storage_label.set_markup("<b>%s</b>" %("Storage"))

        self.storage_entry = Gtk.Label(xalign=0,yalign=0.5)

        attach_list = (
            (id_label,(0, 1, 0, 1)),
            (self.id_entry,(1, 2, 0, 1)),
            (time_label,(2, 3, 0, 1)),
            (self.time_entry,(3, 4, 0, 1)),
            (event_int_label,(0, 1, 1, 2)),
            (self.event_int_entry,(1, 4, 1, 2)),
            (event_manifes_label,(0, 1, 2, 3)),
            (self.event_manifes_entry,(1, 4, 2, 3)),
            (actor_label,(0, 1, 3, 4)),
            (self.actor_entry,(1, 2, 3, 4)),
            (actor_box,(2, 4, 3, 4)),
            (uri_label,(0, 1, 4, 5)),
            (self.uri_entry,(1, 4, 4, 5)),
            (current_uri_label,(0, 1, 5, 6)),
            (self.current_uri_entry,(1, 4, 5, 6)),
            (subj_int_label,(0, 1, 6, 7)),
            (self.subj_int_entry,(1, 4, 6, 7)),
            (subj_manifes_label,(0, 1, 7, 8)),
            (self.subj_manifes_entry,(1, 4, 7, 8)),
            (origin_label,(0, 1, 8, 9)),
            (self.origin_entry,(1, 2, 8, 9)),
            (mimetype_label,(2, 3, 8, 9)),
            (self.mime_entry,(3, 4, 8, 9)),
            (text_label,(0, 1, 9, 10)),
            (self.text_entry,(1, 2, 9, 10)),
            (storage_label,(2, 3, 9, 10)),
            (self.storage_entry,(3, 4, 9, 10))
         )
        for widget_entry in attach_list :
           widget,pos = widget_entry
           self.table.attach(widget,pos[0],pos[1], pos[2], pos[3], xpadding=6, ypadding=6)



    def map(self, event):
        try:
            id_val = int(event.get_id())
            self.id_entry.set_text(str(id_val) if id_val > 0 else "")

            timestamp = int(str(event.get_timestamp()))
            time = datetime.fromtimestamp(timestamp/1000).strftime("%Y-%m-%d %I:%M:%S %p")
            self.time_entry.set_text(time if id_val > 0 else "")
        except:
            self.id_entry.set_text("")
            self.time_entry.set_text("")

        self.event_int_entry.set_text(str(event.get_interpretation()))
        self.event_manifes_entry.set_text(str(event.get_manifestation()))

        actor = str(event.get_actor())
        self.actor_entry.set_label(actor)

        if actor.startswith("application://"):
            app_info = Gio.DesktopAppInfo.new(actor.replace("application://", ""))
            self.image_entry.set_from_gicon(app_info.get_icon(), Gtk.IconSize.DIALOG)
            self.actor_name_entry.set_text(app_info.get_display_name())
        else:
            self.image_entry.clear()
            self.actor_name_entry.set_text("")

        if len(event.subjects) > 0:
            subj = event.subjects[0]

            self.uri_entry.set_text(str(subj.get_uri()))
            self.current_uri_entry.set_text(str(subj.get_current_uri()))

            self.subj_int_entry.set_text(str(subj.get_interpretation()))
            self.subj_manifes_entry.set_text(str(subj.get_manifestation()))

            self.origin_entry.set_text(str(subj.get_origin()))
            self.mime_entry.set_text(subj.get_mimetype())
            try:
                txt = str(subj.get_text())
                self.text_entry.set_text(txt)
            except:
                #print unicode(subj.get_text().strip(codecs.BOM_UTF8), 'utf-8')
                self.text_entry.set_text("")
            self.storage_entry.set_text(str(subj.get_storage()))
