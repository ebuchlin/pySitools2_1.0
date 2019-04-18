#! /usr/bin/env python

#    SITools2 client for Python
#    Copyright (C) 2013 - Institut d'astrophysique spatiale
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses

import datetime as dt
import sitools2.clients.sdo_client_medoc as md


server = 'http://idoc-medoc.ias.u-psud.fr'
ls = md.media_search(
    server=server, series='hmi.m_720s', cadence=['12m'],
    dates=[dt.datetime(2018, 1, 1, 0, 0, 0), dt.datetime(2018, 1, 1, 1, 0, 0)])
kw = md.media_metadata_search(media_data_list=ls, keywords=['recnum', 'cdelt1', 'cdelt2'], server=server)
assert(len(ls) == len(kw))
print(kw[0])

server = 'http://medoc-sdo.ias.u-psud.fr'
ls = md.media_search(
    server=server, series='aia.lev1', waves=['193'], cadence=['10m'],
    dates=[dt.datetime(2018, 1, 1, 0, 0, 0), dt.datetime(2018, 1, 1, 1, 0, 0)])
kw = md.media_metadata_search(media_data_list=ls, keywords=['recnum', 'cdelt1', 'cdelt2'], server=server)
assert(len(ls) == len(kw))
print(kw[0])
