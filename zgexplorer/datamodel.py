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

from gi.repository import GObject
from zeitgeist.datamodel import *

class MonitorData(GObject.GObject):

    def __init__(self):
        super(MonitorData, self).__init__()
        template = Event.new_for_values(subjects=[Subject()])

        self.data = {\
                "name" : "", \
                "timerange" : TimeRange.always(), \
                "template" : Event.new_for_values(subjects=[Subject()]) }

    @property
    def name(self):
        return self.data['name']

    @name.setter
    def name(self, val):
        self.data["name"] = val

    @property
    def timerange(self):
        return self.data['timerange']

    @timerange.setter
    def timerange(self, val):
        self.data["timerange"] = val

    @property
    def template(self):
        return self.data['template']

    @template.setter
    def template(self, val):
        self.data["template"] = val
