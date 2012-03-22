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

from zeitgeist import datamodel
event_interpretations = {
 '':'',
 'ACCEPT_EVENT': datamodel.Interpretation.ACCEPT_EVENT,
 'ACCESS_EVENT': datamodel.Interpretation.ACCESS_EVENT,
 'CREATE_EVENT': datamodel.Interpretation.CREATE_EVENT,
 'DELETE_EVENT': datamodel.Interpretation.DELETE_EVENT,
 'DENY_EVENT': datamodel.Interpretation.DENY_EVENT,
 'EVENT': datamodel.Interpretation.EVENT,
 'EXPIRE_EVENT': datamodel.Interpretation.EXPIRE_EVENT,
 'LEAVE_EVENT': datamodel.Interpretation.LEAVE_EVENT,
 'MODIFY_EVENT': datamodel.Interpretation.MODIFY_EVENT,
 'MOVE_EVENT': datamodel.Interpretation.MOVE_EVENT,
 'RECEIVE_EVENT': datamodel.Interpretation.RECEIVE_EVENT,
 'SEND_EVENT': datamodel.Interpretation.SEND_EVENT
}

event_manifestations = {
 '':'',
 'HEURISTIC_ACTIVITY': datamodel.Manifestation.HEURISTIC_ACTIVITY,
 'SCHEDULED_ACTIVITY': datamodel.Manifestation.SCHEDULED_ACTIVITY,
 'USER_ACTIVITY': datamodel.Manifestation.USER_ACTIVITY,
 'WORLD_ACTIVITY': datamodel.Manifestation.WORLD_ACTIVITY
}

subject_interpretations = {
 '':'',
 'ALARM': datamodel.Interpretation.ALARM,
 'APPLICATION': datamodel.Interpretation.APPLICATION,
 'ARCHIVE': datamodel.Interpretation.ARCHIVE,
 'AUDIO': datamodel.Interpretation.AUDIO,
 'BOOKMARK': datamodel.Interpretation.BOOKMARK,
 'BOOKMARK_FOLDER': datamodel.Interpretation.BOOKMARK_FOLDER,
 'CALENDAR': datamodel.Interpretation.CALENDAR,
 'CONTACT': datamodel.Interpretation.CONTACT,
 'CONTACT_GROUP': datamodel.Interpretation.CONTACT_GROUP,
 'CONTACT_LIST': datamodel.Interpretation.CONTACT_LIST,
 'CURSOR': datamodel.Interpretation.CURSOR,
 'DATA_CONTAINER': datamodel.Interpretation.DATA_CONTAINER,
 'DOCUMENT': datamodel.Interpretation.DOCUMENT,
 'EMAIL': datamodel.Interpretation.EMAIL,
 'EVENT_INTERPRETATION': datamodel.Interpretation.EVENT_INTERPRETATION,
 'EXECUTABLE': datamodel.Interpretation.EXECUTABLE,
 'FILESYSTEM': datamodel.Interpretation.FILESYSTEM,
 'FILESYSTEM_IMAGE': datamodel.Interpretation.FILESYSTEM_IMAGE,
 'FOLDER': datamodel.Interpretation.FOLDER,
 'FONT': datamodel.Interpretation.FONT,
 'FREEBUSY': datamodel.Interpretation.FREEBUSY,
 'HTML_DOCUMENT': datamodel.Interpretation.HTML_DOCUMENT,
 'ICON': datamodel.Interpretation.ICON,
 'IMAGE': datamodel.Interpretation.IMAGE,
 'IMMESSAGE': datamodel.Interpretation.IMMESSAGE,
 'JOURNAL': datamodel.Interpretation.JOURNAL,
 'MAILBOX': datamodel.Interpretation.MAILBOX,
 'MEDIA': datamodel.Interpretation.MEDIA,
 'MEDIA_LIST': datamodel.Interpretation.MEDIA_LIST,
 'MESSAGE': datamodel.Interpretation.MESSAGE,
 'MIME_ENTITY': datamodel.Interpretation.MIME_ENTITY,
 'MIND_MAP': datamodel.Interpretation.MIND_MAP,
 'MOVIE': datamodel.Interpretation.MOVIE,
 'MUSIC_ALBUM': datamodel.Interpretation.MUSIC_ALBUM,
 'MUSIC_PIECE': datamodel.Interpretation.MUSIC_PIECE,
 'OPERATING_SYSTEM': datamodel.Interpretation.OPERATING_SYSTEM,
 'ORGANIZATION_CONTACT': datamodel.Interpretation.ORGANIZATION_CONTACT,
 'PAGINATED_TEXT_DOCUMENT': datamodel.Interpretation.PAGINATED_TEXT_DOCUMENT,
 'PERSON_CONTACT': datamodel.Interpretation.PERSON_CONTACT,
 'PLAIN_TEXT_DOCUMENT': datamodel.Interpretation.PLAIN_TEXT_DOCUMENT,
 'PRESENTATION': datamodel.Interpretation.PRESENTATION,
 'RASTER_IMAGE': datamodel.Interpretation.RASTER_IMAGE,
 'SOFTWARE': datamodel.Interpretation.SOFTWARE,
 'SOURCE_CODE': datamodel.Interpretation.SOURCE_CODE,
 'SPREADSHEET': datamodel.Interpretation.SPREADSHEET,
 'TEXT_DOCUMENT': datamodel.Interpretation.TEXT_DOCUMENT,
 'TIMEZONE': datamodel.Interpretation.TIMEZONE,
 'TODO': datamodel.Interpretation.TODO,
 'TRASH': datamodel.Interpretation.TRASH,
 'TVSERIES': datamodel.Interpretation.TVSERIES,
 'TVSHOW': datamodel.Interpretation.TVSHOW,
 'VECTOR_IMAGE': datamodel.Interpretation.VECTOR_IMAGE,
 'VIDEO': datamodel.Interpretation.VIDEO,
 'VISUAL': datamodel.Interpretation.VISUAL,
 'WEBSITE': datamodel.Interpretation.WEBSITE
}

subject_manifestations = {
 '':'',
 'ARCHIVE_ITEM': datamodel.Manifestation.ARCHIVE_ITEM,
 'ATTACHMENT': datamodel.Manifestation.ATTACHMENT,
 'CALENDAR_DATA_OBJECT': datamodel.Manifestation.CALENDAR_DATA_OBJECT,
 'CONTACT_LIST_DATA_OBJECT': datamodel.Manifestation.CONTACT_LIST_DATA_OBJECT,
 'DELETED_RESOURCE': datamodel.Manifestation.DELETED_RESOURCE,
 'EMBEDDED_FILE_DATA_OBJECT': datamodel.Manifestation.EMBEDDED_FILE_DATA_OBJECT,
 'EVENT_MANIFESTATION': datamodel.Manifestation.EVENT_MANIFESTATION,
 'FILE_DATA_OBJECT': datamodel.Manifestation.FILE_DATA_OBJECT,
 'HARD_DISK_PARTITION': datamodel.Manifestation.HARD_DISK_PARTITION,
 'HEURISTIC_ACTIVITY': datamodel.Manifestation.HEURISTIC_ACTIVITY,
 'MAILBOX_DATA_OBJECT': datamodel.Manifestation.MAILBOX_DATA_OBJECT,
 'MEDIA_STREAM': datamodel.Manifestation.MEDIA_STREAM,
 'REMOTE_DATA_OBJECT': datamodel.Manifestation.REMOTE_DATA_OBJECT,
 'REMOTE_PORT_ADDRESS': datamodel.Manifestation.REMOTE_PORT_ADDRESS,
 'SCHEDULED_ACTIVITY': datamodel.Manifestation.SCHEDULED_ACTIVITY,
 'SOFTWARE_ITEM': datamodel.Manifestation.SOFTWARE_ITEM,
 'SOFTWARE_SERVICE': datamodel.Manifestation.SOFTWARE_SERVICE,
 'SYSTEM_NOTIFICATION': datamodel.Manifestation.SYSTEM_NOTIFICATION,
 'USER_ACTIVITY': datamodel.Manifestation.USER_ACTIVITY,
 'WORLD_ACTIVITY': datamodel.Manifestation.WORLD_ACTIVITY
}

storage_states = {
 '':'',
 'Any':datamodel.StorageState.Any,
 'Available':datamodel.StorageState.Available,
 'NotAvailable':datamodel.StorageState.NotAvailable
}
