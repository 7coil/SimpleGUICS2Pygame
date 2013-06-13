#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""
Script that change a CodeSkulptor program
to run in CodeSkulptor *and* Python SimpleGUICS2Pygame.
(June 13, 2013)

Changes made :
- Add shebang '#!/usr/bin/env python'.
- Add '# -*- coding: latin-1 -*-'.
- Replace import simplegui
  by
  try:
      import simplegui
  except:
      import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
- Try to check if a timer is started *after* the start frame.

Piece of SimpleGUICS2Pygame.
https://bitbucket.org/OPiMedia/simpleguics2pygame

GPLv3 --- Copyright (C) 2013 Olivier Pirson
http://www.opimedia.be/
"""

from __future__ import print_function


import os
import os.path
import re
import sys



########
# Main #
########
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: cs2both.py filename.py')

        exit(1)

    filename = sys.argv[1]

    if filename[-3:] != '.py':
        print("! '{}' have not '.py' extension.".format(filename))

        exit(1)

    if os.path.isfile(filename + '.bak'):
        print("'! {}.bak' alread exist.".format(filename))

        exit(1)


    # Read
    f = open(filename)

    lines = [line.rstrip() for line in f]

    f.close()


    # Check
    if len(lines) < 2:
        print('"Empty" file.')

        exit()

    add_shebang = lines[0][:2]
    add_coding = not re.match('#\w*-\*- coding: \W+ -\*-$', lines[0]) and not re.match('#\w*-\*- coding: \W+ -\*-$', lines[1])

    change_import = False
    already_change_import = False

    end_blank_line = False

    for line in lines:
        if re.search('^\w*import SimpleGUICS2Pygame', line):
            already_change_import = True

            break

    while lines[-1] == '':
        end_blank_line = True
        lines.pop()

    if len(lines) < 2:
        print('"Empty" file.')

        exit()

    if not already_change_import:
        for i, line in enumerate(lines):
            r = re.match('(\w)*import simplegui$', line)
            if r:
                change_import = True
                indent = (r.group(1) if r.group(1)
                          else '')
                lines[i] = '\n' + indent + ('\n' + indent).join(("# Automatically modified by 'cs2both.py' to run in CodeSkulptor *and* Python SimpleGUICS2Pygame.",
                                                                 'try:',
                                                                 '    import simplegui',
                                                                 'except:',
                                                                 '    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui')) + '\n'


    # Write
    if add_shebang or add_coding or change_import or end_blank_line:
        os.rename(filename, filename + '.bak')

        f = (open(filename, mode = 'w', encoding = 'latin_1', newline = '\n') if sys.version_info[0] >= 3
             else open(filename, mode = 'w'))

        if add_shebang:
            print('Add shebang.')
            print('#!/usr/bin/env python', file = f)

        if add_coding:
            print('Add coding latin-1.')
            print('# -*- coding: latin-1 -*-', file = f)

        if change_import:
            print('Change import simplegui.')

        if end_blank_line:
            print('End blank line deleted.')

        print('\n'.join(lines), file = f)

        f.close()
    else:
        print('Nothing changed.')


    while lines:
        line = lines.pop()
        if re.search('^\w*f(rame)?\.start\(\)', line):  # f.start() ou frame.start()
            break
        elif re.search('^\w*[^#]+\.start\(\)', line):   # other .start()
            print('Warning: Maybe a timer is started *after* the start frame.')

            break
