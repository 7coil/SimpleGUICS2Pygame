ChangeLog
=========
* 02.00.00 WORKING VERSION — January 29, 2020

  - Converted from Mercurial version control system to Git.
  - Corrected files included in MANIFEST.in for distribution building. (Thanks to `7coil`.)

  - Added a developer's page in documentation.

  - Replaced links of *Read the Docs*.

  - Added ``--last`` command line option.
  - Added ``test/test_command_line_options.py``.
  - Replaced ``_WEBSITE`` value by documentation link.
  - Splitted media links to image links and sound links.

  - Added ``script/pygame_check.py`` to check Pygame installation alone.

  - Added ``ValueError`` exception if ``draw_text()`` try to draw a text containing unprintable whitespace character.
  - Added ``draw_text_multi()`` in ``simplegui_lib_draw``.
  - Updated ``test/test_text.py``.

  - Added alpha possibility on background color.
  - Added ``transparent`` "color" name.

  - Improved dealing of input box.
  - Added ``test/test_input.py``.

  - Updated ``simpleplot`` module, to "run" same if matplotlib is not installed.
  - Updated ``test/test_objects.py``.

  - Corrected "Read the Docs" subpackage problem.

  - Updated ``test/test_sound.py``.

  - Updated ``script/SimpleGUICS2Pygame_check.py``.

  - **Splitted the big file ``simpleguics2pygame.py``.**
  - Added ``example/presentation.py``.

  - Added ``example/stop_example.py``.

  - Corrected ``test/test_sound.py``.

  - Updated documentation. (Thanks to `John Gray` and `Tom Keller`.)

  - Updated media and CodeSkulptor programs links.

* 01.09.00 — January 1st, 2015

  - **Added ``_load_local_image()`` and ``_load_local_sound()`` functions.**
  - Added ``test/test_sound.py``.
  - Updated ``test/test_dir.py``.
  - Updated ``test/test_image.py``.

  - Added ``--fps n`` option.

  - Added Donate button in ``_draw_about()`` panel.

* 01.08.01 — October 9, 2014

  - Added information when pygame is not installed.

  - Corrected local filename bug in ``_load_media()``. (Thanks to `Sergey Sorokin`_.)
  - Updated documentation.

  .. _`Sergey Sorokin`: https://bitbucket.org/SergeyVlSorokin

* 01.08.00 — October 4, 2014

  - Added alternative grey colors.
  - Added HSL and HSLA colors format.
  - Added ``test/test_colors_html_hsla.py``.
  - Updated CodeSkulptor programs links.
  - Updated ``codeskulptor_lib``.
  - Updated ``test/test_colors_html_rgba.py``.

  - Updated media links.

* 01.07.00 — September 2, 2014

  - Added ``plot_scatter()`` function in ``simpleplot`` module.
  - Added ``test/test_simpleplot_scatter.py``.
  - Updated ``test/test_dir.py``.
  - Updated documentation.
  - Updated CodeSkulptor programs links.

* 01.06.03 — July 24, 2014

  - Implemented ``width`` parameter in ``add_label()``.
  - Added ``test/test_button_label.py``.

* 01.06.02 — July 18, 2014

  - Corrected stupid error in ``add_label()``.

* 01.06.01 — July 17, 2014

  - Added (fake) width parameter in ``add_label()``.
  - Corrected gz archive of HTML offline documentation.

  - Added private members in all documentation.

* 01.06.00 — June 16, 2014

  - Updated ``numeric``.
  - Updated ``example/Spaceship_prototype.py`` and ``example/RiceRocks_Asteroids.py``.
  - Updated ``test/test_dir.py``.

  - Added ``Loader.cache_clear()`` and ``Loader.print_stats_cache()``.

  - Added a cache mechanism to Pygame surfaces used by ``Image`` (**improve speed** of ``draw_image()``).
  - Added ``Image._url`` attribute.
  - Moved ``_RADIAN_TO_DEGREE``.
  - Print now to ``stderr`` instead ``stdout``.
  - Updated ``_draw_about()``.

  - Updated documentation.

  - Updated media and CodeSkulptor programs links.

* 01.05.00 — May 25, 2014

  - Added cache for colors and option ``--print-stats-cache``.
  - First public version of ``.hgignore`` and ``Makefile``.
  - Off the mixer if no sound is loaded.
  - Updated ``example/RiceRocks_Asteroids.py``.
  - Updated documentation.

  - Updated ``example/Spaceship_prototype.py``.

  - Updated ``example/Blackjack.py``.

  - Updated ``example/Memory.py``.

  - Updated ``example/Pong.py``.

  - Cosmetic changes in some example programs.

  - Updated ``test/test_all.py``.

  - Better order Pygame initalization.
  - Updated ``script/cs2both.py`` and ``script/SimpleGUICS2Pygame_check.py``.

  - Updated ``simplegui_lib_keys.py`` and ``example/keys.py``.
  - Updated ``example/Stopwatch.py``.

  - Changed filename used by ``_load_media()`` (use now the query part of URLs).

  - Added precision to Window$ installation.
  - Updated media and CodeSkulptor programs links.

* 01.04.00 — December 16, 2013

  - Customized documentation.
  - Splitted changes in a separated file.

  - Added ``numeric`` (``Matrix`` object) module.

  - Corrected some typos by `Maxim Rybalov`_. (Thank you.)

  - Updated ``simplegui_lib_fps.py``.
  - Updated ``example/RiceRocks_Asteroids.py``.

  .. _`Maxim Rybalov`: https://www.linkedin.com/in/mrybalov

* 01.03.00 — December 13, 2013

  - Removed exception to ``get_canvas_image()``.

  - Updated almost all files to add ``except ImportError``.
  - Updated ``codeskulptor_lib.codeskulptor_is()``.

  - Added ``simplegui_lib_fps.py``.

  - Corrected bug in ``_load_media()`` (issue #1). (Thanks to `Sean Flanigan`_.)
  - Updated documentation to clarify local use of images and sounds. (Thanks to `Ines Simicic`_.)

  - Updated ``script/cs2both.py``.

  - Corrected conversion of ``_fps_average`` to ``int`` in Python 2.
  - Corrected mentions of ``Frame._fps`` in comment.

  - Updated ``example/Blackjack.py``.
  - Updated ``example/Spaceship_prototype.py``.

  - Updated ``example/Memory.py``.
  - Updated media and CodeSkulptor programs links.

  .. _`Sean Flanigan`: https://github.com/seanf
  .. _`Ines Simicic`: http://i--s.weebly.com/

* 01.02.00 — November 8, 2013

  - Splitted ``simplegui_lib.py`` in ``simplegui_lib.py``, ``simplegui_lib_draw.py`` and ``simplegui_lib_loader.py``.
  - Added ``simplegui_lib_keys.py``.
  - Added ``example/keys.py`` and ``example/loader.py``.
  - Updated ``example/RiceRocks_Asteroids.py`` and ``example/Spaceship_prototype.py``.
  - Updated ``script/SimpleGUICS2Pygame_check.py``.
  - Updated ``test/test_image.py`` and ``test/test_text.py``.
  - Updated media and CodeSkulptor programs links.

  - Corrected installation documentation.

* 01.01.00 — November 1st, 2013

  - Added ``_block`` and ``_filename`` parameters in ``simpleplot.plot_lines()`` function.
  - Added ``plot_bars()`` function in ``simpleplot`` module.
  - Added ``test/test_simpleplot_bars.py`` and ``test/test_simpleplot_lines.py``.
  - Updated ``test/test_all.py``.
  - Updated media links.
  - Corrected minor errors in documentation.

  - Added ``set_timeout()`` function in ``codeskulptor`` module.
  - Updated ``example/Mandelbrot_Set.py`` (used ``set_timeout()``).
  - Updated CodeSkulptor programs links.

* 01.00.02 — October 31, 2013

  - Corrected bug in ``TextAreaControl.set_text()``: the label text was also modified.

  - Updated documentation.

  - Updated ``cs2both.py``.

  - Updated ``example/Mandelbrot_Set.py`` (optimized draw).
  - Updated media and CodeSkulptor programs links.

* 01.00.01 — October 9, 2013

  - Adapted documentation and ``cs2both.py`` to changes of CodeSkulptor (``int`` and ``float`` are now separate).

* 01.00.00 — July 13, 2013

  - Moved documentation to Read The Docs.

  - Added ``simpleplot`` module.
  - Updated ``example/Mandelbrot_Set.py`` (used vertical symetry).
  - Updated media and CodeSkulptor programs links.

* 00.92.00 — June 27, 2013

  - Changed ``simplegui_lib.Loader`` class to display progression loading in SimpleGUICS2Pygame
    (moved arguments from ``wait_loaded()`` function to ``__init__()``).

  - Replaced ``Frame._already_frame`` by ``Frame._frame_instance``.

  - Updated ``example/RiceRocks_Asteroids.py`` (collisions of asteroids and little asteroids).

  - Added ``Frame._set_canvas_background_image()`` function.

  - Memoization of downloaded images and sounds.
  - Changed save in local directory to avoid conflict.

  - Added ``test/test_image.py``.

  - Added ``--overwrite-downloaded-medias`` and ``--save-downloaded-medias`` options.

  - Display versions in ``script/SimpleGUICS2Pygame_check.py``.

* 00.91.00 — June 23, 2013

  - Changed installation program to build distributions (now ``setuptools`` is used).
  - Added ``--print-load-medias`` option.
  - Added ``script/SimpleGUICS2Pygame_check.py`` and moved and updated ``cs2both.py``.

  - Now, ``_set_option_from_argv()`` deleted SimpleGUICS2Pygame options after use.

  - Memoization of Pygame fonts.
  - Added ``--default-font`` option.

  - Many cosmetic changes to respect PEP 8.
  - Updated media and CodeSkulptor programs links.

  - Some precisions and English corrections in the documentation.
  - Added some CodeSkulptor programs links.

  - ``example/Memory.py``: moved image locations.
  - ``example/Nostalgic_Basic_Blitz.py`` : added spacebar information.

* 00.90.10 — June 19, 2013

  - Adapted button, label and input to display multine text.
  - Simplified handler functions transmitted to ``add_button()`` in some programs.
  - Added ``example/Nostalgic_Basic_Blitz.py``.

  - Changed ``default_pygame_color`` param of ``_simpleguicolor_to_pygamecolor()`` function (now installation is ok even if Pygame not installed).

  - Moved ``_VERSION`` and ``_WEBSITE`` constants from ``simpleguics2pygame.py`` to ``__init__.py``.
  - Removed ``enumerate()`` function from ``codeskulptor_lib`` (now implemented natively by CodeSkulptor).
  - Added ``--display-fps`` option.
  - Added ``example/RiceRocks_Asteroids.py``.
  - Updated some CodeSkulptor programs links.
  - Added some new media links.
  - Added some details in documentations.
  - Some cosmetic changes.

* 00.90.00 — June 13, 2013

  - First public version.
