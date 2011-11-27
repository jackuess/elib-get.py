# -*- coding: utf-8 -*-
# get-elib.py
#      
# Copyright 2011 Jacques de Lval chucky@wrutschkow.org
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os, sys

if len(sys.argv) != 3:
	sys.exit("Usage:\npython get-elib.py <ISBN> <title>")

RTMPDUMP_CMD = "rtmpdump -r rtmpe://212.112.169.73/vod/ -y mp3:ISBN%(isbn)s/mp3/Avsnitt%(chapter)s -o %(title)s%(chapter)s.mp3"

isbn = sys.argv[1]
isbn = isbn.replace('-', '').strip()

title = sys.argv[2]

for just in range(1, 10):
	chapter = '1'.zfill(just)
	status = os.system(RTMPDUMP_CMD % {'isbn': isbn,
					'title': title,
					'chapter': chapter})
	if status == 0:
		print("\033[32mLaddade ner avsnitt 1\033[0m")
		break
	else:
		os.remove(''.join((title, chapter, ".mp3")))

if status != 0:
	sys.exit("Boken kunde inte laddas ner")

i = 2
while True:
	chapter = str(i).zfill(just)
	status = os.system(RTMPDUMP_CMD % {'isbn': isbn,
					'title': title,
					'chapter': chapter})
	if status != 0:
		os.remove(''.join((title, chapter, ".mp3")))
		break
	print("\033[32mLaddade ner avsnitt %d\033[0m" % i)
	i += 1
