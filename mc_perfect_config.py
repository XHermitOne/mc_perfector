#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Config Midnight Commander.
"""
import sys
import os
import os.path
import stat
import platform
import shutil

try:
    import rich.console
except ImportError:
    print(u'Import error. Not found rich library')
    print(u'For install: pip3 install rich')
    sys.exit(2)

import txtfile_func

__verison__ = (0, 0, 0, 1)

DEBUG_MODE = True

CONSOLE = rich.console.Console()


def debug(message=u'', is_force_print=False):
    """
    Display debug information.

    :param message: Text message.
    :param is_force_print: Forcibly display.
    """
    if DEBUG_MODE or is_force_print:
        CONSOLE.print(str(message), style='blue')


def info(message=u'', is_force_print=False):
    """
    Print information.

    :param message: Text message.
    :param is_force_print: Forcibly display.
    """
    if DEBUG_MODE or is_force_print:
        CONSOLE.print(str(message), style='green')


def error(message=u'', is_force_print=False):
    """
    Print error message.

    :param message: Text message.
    :param is_force_print: Forcibly display.
    """
    if DEBUG_MODE or is_force_print:
        CONSOLE.print(str(message), style='bold red')


def warning(message=u'', is_force_print=False):
    """
    Print warning message.

    :param message: Text message.
    :param is_force_print: Forcibly display.
    """
    if DEBUG_MODE or is_force_print:
        CONSOLE.print(str(message), style='bold yellow')


def fatal(message=u'', is_force_print=False):
    """
    Print critical error message.

    :param message: Text message.
    :param is_force_print: Forcibly display.
    """
    if DEBUG_MODE or is_force_print:
        error(message, is_force_print=is_force_print)
        CONSOLE.print_exception(extra_lines=8, show_locals=True)


def getHomePath():
    """
    Home directory path.
    """
    os_platform = platform.uname()[0].lower()
    if os_platform == 'windows':
        home_path = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH']
    elif os_platform == 'linux':
        home_path = os.environ['HOME']
    else:
        warning(u'OS <%s> not support' % os_platform)
        return None
    return os.path.normpath(home_path)

NEOFETCH_MENUITEM = '''
I       System information
        clear
        neofetch
        echo -n "Press any key..."
        read ANSWER
'''

HTOP_MENUITEM = '''
H       Task monitor  HTOP
        htop
'''

BTOP_MENUITEM = '''
B       Task monitor  BTOP
        btop
'''

MTR_MENUITEM = '''
M       Network traceroute host MTR
        dialog --title "Traceroute" --clear --inputbox "Entry host address for traceroute:" 10 51 2> /tmp/mtr.tmp
        clear
        mtr --filename /tmp/mtr.tmp 
'''


def main(*argv):
    """
    Main function.

    :param argv: Command line arguments.
    :return:
    """
    try:
        info(u'Config Midnight Commander START...')

        home_path = getHomePath()
        ini_filename = os.path.join(home_path, '.config', 'mc', 'ini')
        if os.path.exists(ini_filename):
            # txtfile_func.replaceTextFile(ini_filename, 'pause_after_run=1', 'pause_after_run=2', auto_add=False)
            # txtfile_func.replaceTextFile(ini_filename, 'pause_after_run=0', 'pause_after_run=2', auto_add=False)
            # info(u'Set pause after run')
            txtfile_func.replaceTextFile(ini_filename, 'skin=default', 'skin=modarin256', auto_add=False)
            info(u'Set <modarin256> skin')

        menu_filename = os.path.join(home_path, '.config', 'mc', 'menu')
        if not os.path.exists(menu_filename):
            src_menu_filename = os.path.join('etc', 'mc', 'mc.menu')
            if os.path.exists(src_menu_filename):
                shutil.copyfile(src_menu_filename, menu_filename)
                os.chmod(menu_filename, stat.S_IWUSR | stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

        # neofetch / System information
        if not txtfile_func.isInTextFile(menu_filename, NEOFETCH_MENUITEM):
            txtfile_func.appendTextFile(menu_filename, NEOFETCH_MENUITEM)
            info(u'Add <neofetch> system information')

        # htop / Task monitor
        if not txtfile_func.isInTextFile(menu_filename, HTOP_MENUITEM):
            txtfile_func.appendTextFile(menu_filename, HTOP_MENUITEM)
            info(u'Add <htop> task monitor')

        # btop / Task monitor
        if not txtfile_func.isInTextFile(menu_filename, BTOP_MENUITEM):
            txtfile_func.appendTextFile(menu_filename, BTOP_MENUITEM)
            info(u'Add <btop> task monitor')

        # mtr / Traceroute
        if not txtfile_func.isInTextFile(menu_filename, MTR_MENUITEM):
            txtfile_func.appendTextFile(menu_filename, MTR_MENUITEM)
            info(u'Add <mtr> traceroute tool')

        info(u'... STOP Config Midnight Commander')
    except:
        fatal(u'Programm  error:')


if __name__ == '__main__':
    main(*sys.argv[1:])

