#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""
Make 'snd_links.html' file
  from snd_links.txt
(January 12, 2016)

Piece of SimpleGUICS2Pygame.
https://bitbucket.org/OPiMedia/simpleguics2pygame

GPLv3 --- Copyright (C) 2013, 2016 Olivier Pirson
http://www.opimedia.be/
"""

from __future__ import print_function


import shutil
import sys

import make_links


DIR_DATA = ''
DIR_DEST = '../'

FILE_DEST = 'snd_links.html'


########
# Main #
########
if __name__ == '__main__':
    print("Make '{}' file...".format(DIR_DEST + FILE_DEST), end='')
    sys.stdout.flush()

    shutil.copy(DIR_DATA + 'snd_links_top.html', DIR_DEST + FILE_DEST)

    f = (open(DIR_DEST + FILE_DEST, mode='a', encoding='utf_8', newline='\n')
         if sys.version_info[0] >= 3
         else open(DIR_DEST + FILE_DEST, mode='a'))

    make_links.print_html_list_snd(
        make_links.read_txt(DIR_DATA + 'snd_links.txt'), f)

    print(file=f)

    f_bottom = open(DIR_DATA + 'links_bottom.html')
    for line in f_bottom:
        print(line[:-1], file=f)
    f_bottom.close()

    f.close()

    print(' Done')
