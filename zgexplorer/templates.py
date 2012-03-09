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

from zeitgeist.datamodel import Event, Subject, Interpretation, Manifestation

class BuiltInFilters(dict):

    def __init__(self):
        template1 = Event()
        self[0] = ["All", "Get all the events", template1]
        
        template2  = Event.new_for_values(interpretation = \
            Interpretation.ACCESS_EVENT)
        self[1] = ["Access events", "Fetch all the access events", template2]
