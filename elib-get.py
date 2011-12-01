# -*- coding: utf-8 -*-
# get-elib.py
#      
# Copyright 2011 Jacques de Laval chucky@wrutschkow.org
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

def download_chapter(n, isbn, title, just):
	RTMPDUMP_CMD = "rtmpdump -r \"rtmpe://212.112.169.73/vod/\" -y \"mp3:ISBN%(isbn)s/mp3/Avsnitt%(chapter)s\" -o \"%(title)s%(chapter)s.flv\""
	CONVERT_CMD = "ffmpeg -v quiet -i \"%(title)s%(chapter)s.flv\" -vn -acodec copy \"%(title)s%(chapter)s.mp3\""
	
	chapter = str(n).zfill(just)
	status = os.system(RTMPDUMP_CMD % {'isbn': isbn,
					'title': title,
					'chapter': chapter})
	if status == 0:
		print("\033[32mLaddade ner avsnitt %d\033[0m" % n)
		status = os.system(CONVERT_CMD % {'title': title, 'chapter': chapter})
		if status == 0:
			print("\033[32mKonverterade avsnitt %d från flv till mp3\033[0m" % n)
			os.remove(''.join((title, chapter, ".flv")))
		else:
			print("\033[31mKunde inte konvertera avsnitt %d från flv till mp3: kontrollera att ffmpeg är installerat\033[0m" % n)
		return 0
	else:
		os.remove(''.join((title, chapter, ".flv")))
		return status

if len(sys.argv) != 3:
	sys.exit("Usage:\npython get-elib.py <ISBN> <title>")

isbn = sys.argv[1]
isbn = isbn.replace('-', '').strip()
title = sys.argv[2]

#Find first chapter and download it
for just in range(1, 10):
	status = download_chapter(1, isbn, title, just)
	if status == 0:
		break

if status != 0:
	sys.exit("Boken kunde inte laddas ner")

#Download the rest of the chapters
i = 2
while status == 0:
	status = download_chapter(i, isbn, title, just)
	i += 1