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

MISC_EXT_SIGNATURE = '### Miscellaneous ###'
DOC_EXT_SIGNATURE = '### Documents ###'
IMG_EXT_SIGNATURE = '### Images ###'

LOG_EXT_VIEWER = '''
# Log
shell/.log
    View=lnav %f
'''

PDF_EXT_VIEWER = '''
# Pdf
shell/.pdf
    View=pdftotext -layout %f - | batcat
'''

HTML_EXT_VIEWER = '''
# Html
shell/.html
    View=lynx %f
'''

HTM_EXT_VIEWER = '''
# Htm
shell/.htm
    View=lynx %f
'''

DOCX_EXT_VIEWER = '''
# Docx
shell/.docx
    View=pandoc -s %f -o /tmp/docx.txt; batcat /tmp/docx.txt
'''

XLSX_EXT_VIEWER = '''
# Xlsx
shell/.xlsx
    View=xlsx2csv %f /tmp/xlsx.txt; batcat /tmp/xlsx.txt
'''

XML_EXT_VIEWER = '''
# XML
shell/.xml
    View=batcat %f
'''

IMG_EXT_VIEWER = '''
# Images
regex/\\.(png|jpg|jpeg|gif)$
    View=tiv %f; echo -n "Press any key...";read ANSWER
'''

GIT_EXT_VIEWER = '''
# GIT
directory/\\.(git)$
    Open=lazygit-gm
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

        ext_filename = os.path.join(home_path, '.config', 'mc', 'mc.ext')
        if not os.path.exists(ext_filename):
            src_ext_filename = os.path.join('etc', 'mc', 'mc.ext')
            if os.path.exists(src_ext_filename):
                shutil.copyfile(src_ext_filename, ext_filename)
                os.chmod(ext_filename, stat.S_IWUSR | stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

        # Log files
        if not txtfile_func.isInTextFile(ext_filename, LOG_EXT_VIEWER):
            txtfile_func.replaceTextFile(ext_filename,
                                         src_text=MISC_EXT_SIGNATURE,
                                         dst_text=MISC_EXT_SIGNATURE+os.linesep+LOG_EXT_VIEWER)
            info(u'Add <log> files viewer')

        # Git
        if not txtfile_func.isInTextFile(ext_filename, GIT_EXT_VIEWER):
            txtfile_func.replaceTextFile(ext_filename,
                                         src_text=MISC_EXT_SIGNATURE,
                                         dst_text=MISC_EXT_SIGNATURE+os.linesep+GIT_EXT_VIEWER)
            info(u'Add <git> Git manager')

        # PDF files
        if not txtfile_func.isInTextFile(ext_filename, PDF_EXT_VIEWER):
            txtfile_func.replaceTextFile(ext_filename,
                                         src_text=DOC_EXT_SIGNATURE,
                                         dst_text=DOC_EXT_SIGNATURE+os.linesep+PDF_EXT_VIEWER)
            info(u'Add <pdf> files viewer')

        # Html files
        if not txtfile_func.isInTextFile(ext_filename, HTML_EXT_VIEWER):
            txtfile_func.replaceTextFile(ext_filename,
                                         src_text=DOC_EXT_SIGNATURE,
                                         dst_text=DOC_EXT_SIGNATURE+os.linesep+HTML_EXT_VIEWER)
            info(u'Add <html> files viewer')

        # Htm files
        if not txtfile_func.isInTextFile(ext_filename, HTM_EXT_VIEWER):
            txtfile_func.replaceTextFile(ext_filename,
                                         src_text=DOC_EXT_SIGNATURE,
                                         dst_text=DOC_EXT_SIGNATURE+os.linesep+HTM_EXT_VIEWER)
            info(u'Add <htm> files viewer')

        # Docx files
        if not txtfile_func.isInTextFile(ext_filename, DOCX_EXT_VIEWER):
            txtfile_func.replaceTextFile(ext_filename,
                                         src_text=DOC_EXT_SIGNATURE,
                                         dst_text=DOC_EXT_SIGNATURE+os.linesep+DOCX_EXT_VIEWER)
            info(u'Add <docx> files viewer')

        # Xlsx files
        if not txtfile_func.isInTextFile(ext_filename, XLSX_EXT_VIEWER):
            txtfile_func.replaceTextFile(ext_filename,
                                         src_text=DOC_EXT_SIGNATURE,
                                         dst_text=DOC_EXT_SIGNATURE+os.linesep+XLSX_EXT_VIEWER)
            info(u'Add <xlsx> files viewer')

        # XML files
        if not txtfile_func.isInTextFile(ext_filename, XML_EXT_VIEWER):
            txtfile_func.replaceTextFile(ext_filename,
                                         src_text=DOC_EXT_SIGNATURE,
                                         dst_text=DOC_EXT_SIGNATURE+os.linesep+XML_EXT_VIEWER)
            info(u'Add <xml> files viewer')

        # Images files
        if not txtfile_func.isInTextFile(ext_filename, IMG_EXT_VIEWER):
            txtfile_func.replaceTextFile(ext_filename,
                                         src_text=IMG_EXT_SIGNATURE,
                                         dst_text=IMG_EXT_SIGNATURE+os.linesep+IMG_EXT_VIEWER)
            info(u'Add <images> files viewer')

        info(u'... STOP Config Midnight Commander')
    except:
        fatal(u'Programm  error:')


if __name__ == '__main__':
    main(*sys.argv[1:])

