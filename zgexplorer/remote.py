# -.- coding: utf-8 -.-
#
# Zeitgeist Explorer
#
# Copyright © 2011-2012 Collabora Ltd.
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
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime

from zeitgeist.client import ZeitgeistClient
from zeitgeist.datamodel import *

__all__ = ['get_zeitgeist']

class CustomSubject(Subject):

    @property
    def interp_string(self):
        try:
            return Interpretation[self.interpretation].display_name
        except (KeyError, AttributeError):
            return None
    
    @property
    def manif_string(self):
        try:
            return Manifestation[self.manifestation].display_name
        except (KeyError, AttributeError):
            return None

class CustomEvent(Event):

    _subject_type = CustomSubject
    
    @property
    def date_string(self):
        time = datetime.fromtimestamp(int(self.timestamp) / 1000)
        return time.strftime("%Y-%m-%d %I:%M:%S%p")

    @property
    def interp_string(self):
        try:
            return Interpretation[self.interpretation].display_name
        except (KeyError, AttributeError):
            return "(no value)"
    
    @property
    def manif_string(self):
        try:
            return Manifestation[self.manifestation].display_name
        except (KeyError, AttributeError):
            return "(no value)"

class ZeitgeistInterface:

    _client = None
    
    @classmethod
    def get_interface(cls):
        if cls._client is None:
            cls._client = ZeitgeistClient()
            cls._client.register_event_subclass(CustomEvent)
        return cls._client

def get_zeitgeist():
    return ZeitgeistInterface.get_interface()
