#! /usr/bin/env python
# -.- coding: utf-8 -.-
#
# Zeitgeist Explorer
#
# Copyright © 2012 Manish Sinha <manishsinha@ubuntu.com>
# Copyright © 2012 Dhananjay Sathe <dhananjaysathe@gmail.com>
# Copyright © 2012 Collabora Ltd.
#             By Siegfried-A. Gevatter Pujals <siegfried@gevatter.com>
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
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from zeitgeist.datamodel import Interpretation, Manifestation, StorageState

# FIXME: fix eventwidgets.py to show stuff sorted
#        dictionaries don't have order, so it should just use lists
#        of events (and use .display_name itself)

event_interpretations = dict([(x.display_name, x) for x in
    Interpretation.EVENT_INTERPRETATION.get_all_children()])
event_interpretations[''] = ''

event_manifestations = dict([(x.display_name, x) for x in
    Manifestation.EVENT_MANIFESTATION.get_all_children()])
event_manifestations[''] = ''

subject_interpretations = dict([(x.display_name, x) for x in
    Interpretation.get_all_children()
    if not x.is_child_of(Interpretation.EVENT_INTERPRETATION)])
subject_interpretations[''] = ''

subject_manifestations = dict([(x.display_name, x) for x in
    Manifestation.get_all_children()
    if not x.is_child_of(Manifestation.EVENT_MANIFESTATION)])
subject_manifestations[''] = ''

storage_states = dict(StorageState.iteritems())
storage_states[''] = ''
