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

    name = GObject.property(type=str)
    template = GObject.property(type=GObject.TYPE_OBJECT)
    timerange = GObject.property(type=GObject.TYPE_OBJECT)

    def __init__(self):
        timerange = TimeRange.always()
        template = Event()
        subj = Subject()
        template.append_subject(subj)
