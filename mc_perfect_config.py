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

__verison__ = (0, 0, 2, 1)

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

GIT_MENUITEM = '''
G       Git manager
        lazygit-gm --path %d 
'''

PY_MENUITEM = '''
P       Python3 interpreter
        clear
        python3 
'''

DDGR_MENUITEM = '''
D       Internet searching
        dialog --title "Internet" --clear --inputbox "DuckDuckGo search:" 10 81 2> /tmp/inet_search.tmp
        clear
        cat /tmp/inet_search.tmp | ddgr --num 25 --expand  
        echo -n "Press any key..."
        read ANSWER
'''

LYNX_MENUITEM = '''
L       Internet browser
        dialog --title "Internet browser" --clear --inputbox "URL:" 10 81 2> /tmp/inet_url.tmp
        clear
        cat /tmp/inet_url.tmp | lynx -accept_all_cookies - 
'''

MISC_EXT_SIGNATURE = '### Miscellaneous ###'
DOC_EXT_SIGNATURE = '### Documents ###'
IMG_EXT_SIGNATURE = '### Images ###'

LOG_EXT_VIEWER = '''
# Log
regex/\\.[Ll][Oo][Gg]$
    View=lnav %f
'''

PDF_EXT_VIEWER = '''
# Pdf
regex/\\.[Pp][Dd][Ff]$
    View=pdftotext -layout %f - | batcat
'''

HTML_EXT_VIEWER = '''
# Html
regex/\\.[Hh][Tt][Mm][Ll]$
    View=lynx %f
'''

HTM_EXT_VIEWER = '''
# Htm
regex/\\.[Hh][Tt][Mm]$
    View=lynx %f
'''

JSON_EXT_VIEWER = '''
# JSON
regex/\\.[Jj][Ss][Oo][Nn]$
    View=json-tui %f
'''

DOCX_EXT_VIEWER = '''
# Docx
regex/\\.[Dd][Oo][Cc][Xx]$
    View=pandoc -s %f -o /tmp/docx.txt; batcat /tmp/docx.txt
'''

XLSX_EXT_VIEWER = '''
# Xlsx
regex/\\.[Xx][Ll][Ss][Xx]$
    View=xlsx2csv %f /tmp/xlsx.txt; batcat /tmp/xlsx.txt
'''

XML_EXT_VIEWER = '''
# XML
regex/\\.[Xx][Mm][Ll]$
    View=batcat %f
'''

IMG_EXT_VIEWER = '''
# Images
regex/\\.(png|jpg|jpeg|gif)$
    View=tiv %f; echo -n "Press any key...";read ANSWER
'''

DBF_EXT_VIEWER = '''
# Dbf
regex/\\.[Dd][Bb][Ff]$
    View=dbf_view_dos --dbf-filename=%f
'''

DELETE_PREV_DBF_VIEWER = '''# dbf
shell/i/.dbf
	Open=/usr/lib/mc/ext.d/misc.sh open dbf
	View=%view{ascii} /usr/lib/mc/ext.d/misc.sh view dbf
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
            info(u'Set <modarin256> skin in file <%s>' % ini_filename)

        menu_filename = os.path.join(home_path, '.config', 'mc', 'menu')
        if not os.path.exists(menu_filename):
            src_menu_filename = os.path.join('etc', 'mc', 'mc.menu')
            if os.path.exists(src_menu_filename):
                shutil.copyfile(src_menu_filename, menu_filename)
                os.chmod(menu_filename, stat.S_IWUSR | stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

        # neofetch / System information
        if not txtfile_func.isInTextFile(menu_filename, NEOFETCH_MENUITEM):
            txtfile_func.appendTextFile(menu_filename, NEOFETCH_MENUITEM)
            info(u'Add <neofetch> system information in file <%s>' % menu_filename)

        # htop / Task monitor
        if not txtfile_func.isInTextFile(menu_filename, HTOP_MENUITEM):
            txtfile_func.appendTextFile(menu_filename, HTOP_MENUITEM)
            info(u'Add <htop> task monitor in file <%s>' % menu_filename)

        # btop / Task monitor
        if not txtfile_func.isInTextFile(menu_filename, BTOP_MENUITEM):
            txtfile_func.appendTextFile(menu_filename, BTOP_MENUITEM)
            info(u'Add <btop> task monitor in file <%s>' % menu_filename)

        # mtr / Traceroute
        if not txtfile_func.isInTextFile(menu_filename, MTR_MENUITEM):
            txtfile_func.appendTextFile(menu_filename, MTR_MENUITEM)
            info(u'Add <mtr> traceroute tool in file <%s>' % menu_filename)

        # lazygit / Git manager
        if not txtfile_func.isInTextFile(menu_filename, GIT_MENUITEM):
            txtfile_func.appendTextFile(menu_filename, GIT_MENUITEM)
            info(u'Add <git> Git manager in file <%s>' % menu_filename)

        # python / Python interpreter
        if not txtfile_func.isInTextFile(menu_filename, PY_MENUITEM):
            txtfile_func.appendTextFile(menu_filename, PY_MENUITEM)
            info(u'Add <python> Python interpreter in file <%s>' % menu_filename)

        # ddgr / Internet searching
        if not txtfile_func.isInTextFile(menu_filename, DDGR_MENUITEM):
            txtfile_func.appendTextFile(menu_filename, DDGR_MENUITEM)
            info(u'Add <ddgr> Internet searching in file <%s>' % menu_filename)

        # lynx / Internet browser
        if not txtfile_func.isInTextFile(menu_filename, LYNX_MENUITEM):
            txtfile_func.appendTextFile(menu_filename, LYNX_MENUITEM)
            info(u'Add <lynx> Internet browser in file <%s>' % menu_filename)

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
            info(u'Add <log> files viewer in file <%s>' % ext_filename)

        # PDF files
        if not txtfile_func.isInTextFile(ext_filename, PDF_EXT_VIEWER):
            txtfile_func.replaceTextFile(ext_filename,
                                         src_text=DOC_EXT_SIGNATURE,
                                         dst_text=DOC_EXT_SIGNATURE+os.linesep+PDF_EXT_VIEWER)
            info(u'Add <pdf> files viewer in file <%s>' % ext_filename)

        # Html files
        if not txtfile_func.isInTextFile(ext_filename, HTML_EXT_VIEWER):
            txtfile_func.replaceTextFile(ext_filename,
                                         src_text=DOC_EXT_SIGNATURE,
                                         dst_text=DOC_EXT_SIGNATURE+os.linesep+HTML_EXT_VIEWER)
            info(u'Add <html> files viewer in file <%s>' % ext_filename)

        # Htm files
        if not txtfile_func.isInTextFile(ext_filename, HTM_EXT_VIEWER):
            txtfile_func.replaceTextFile(ext_filename,
                                         src_text=DOC_EXT_SIGNATURE,
                                         dst_text=DOC_EXT_SIGNATURE+os.linesep+HTM_EXT_VIEWER)
            info(u'Add <htm> files viewer in file <%s>' % ext_filename)

        # JSON files
        if not txtfile_func.isInTextFile(ext_filename, JSON_EXT_VIEWER):
            txtfile_func.replaceTextFile(ext_filename,
                                         src_text=DOC_EXT_SIGNATURE,
                                         dst_text=DOC_EXT_SIGNATURE+os.linesep+JSON_EXT_VIEWER)
            info(u'Add <json> files viewer in file <%s>' % ext_filename)

        # Docx files
        if not txtfile_func.isInTextFile(ext_filename, DOCX_EXT_VIEWER):
            txtfile_func.replaceTextFile(ext_filename,
                                         src_text=DOC_EXT_SIGNATURE,
                                         dst_text=DOC_EXT_SIGNATURE+os.linesep+DOCX_EXT_VIEWER)
            info(u'Add <docx> files viewer in file <%s>' % ext_filename)

        # Xlsx files
        if not txtfile_func.isInTextFile(ext_filename, XLSX_EXT_VIEWER):
            txtfile_func.replaceTextFile(ext_filename,
                                         src_text=DOC_EXT_SIGNATURE,
                                         dst_text=DOC_EXT_SIGNATURE+os.linesep+XLSX_EXT_VIEWER)
            info(u'Add <xlsx> files viewer in file <%s>' % ext_filename)

        # XML files
        if not txtfile_func.isInTextFile(ext_filename, XML_EXT_VIEWER):
            txtfile_func.replaceTextFile(ext_filename,
                                         src_text=DOC_EXT_SIGNATURE,
                                         dst_text=DOC_EXT_SIGNATURE+os.linesep+XML_EXT_VIEWER)
            info(u'Add <xml> files viewer in file <%s>' % ext_filename)

        # Images files
        if not txtfile_func.isInTextFile(ext_filename, IMG_EXT_VIEWER):
            txtfile_func.replaceTextFile(ext_filename,
                                         src_text=IMG_EXT_SIGNATURE,
                                         dst_text=IMG_EXT_SIGNATURE+os.linesep+IMG_EXT_VIEWER)
            info(u'Add <images> files viewer in file <%s>' % ext_filename)

        # DBF files
        if txtfile_func.isInTextFile(ext_filename, DELETE_PREV_DBF_VIEWER):
            txtfile_func.replaceTextFile(ext_filename,
                                         src_text=DELETE_PREV_DBF_VIEWER,
                                         dst_text=os.linesep)
            warning(u'Delete prev <dbf> files viewer in file <%s>' % ext_filename)
        if not txtfile_func.isInTextFile(ext_filename, DBF_EXT_VIEWER):
            txtfile_func.replaceTextFile(ext_filename,
                                         src_text=MISC_EXT_SIGNATURE,
                                         dst_text=MISC_EXT_SIGNATURE+os.linesep+DBF_EXT_VIEWER)
            info(u'Add <dbf> files viewer in file <%s>' % ext_filename)

	# Увеличить масштаб окна dosbox
        dosbox_conf_filename = os.path.join(home_path, '.dosbox', 'dosbox-0.74-3.conf')
        if not txtfile_func.isInTextFile(dosbox_conf_filename, 'scaler=normal2x forced'):
            txtfile_func.replaceTextFile(dosbox_conf_filename,
                                         src_text='scaler=normal2x',
                                         dst_text='scaler=normal2x forced')
            info(u'Set <scaler> X 2 for DosBox in file <%s>' % dosbox_conf_filename)

        info(u'... STOP Config Midnight Commander')
    except:
        fatal(u'Programm  error:')


if __name__ == '__main__':
    main(*sys.argv[1:])

