#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Text file functions.
"""

import os
import os.path
import termcolor
import jinja2

__version__ = (0, 0, 3, 2)


def saveTextFile(txt_filename, txt='', rewrite=True):
    """
    Save text file.

    :param txt_filename: Text file name.
    :param txt: Body text file as unicode.
    :param rewrite: Rewrite file if it exists?
    :return: True/False.
    """
    if not isinstance(txt, str):
        txt = str(txt)

    file_obj = None
    try:
        if rewrite and os.path.exists(txt_filename):
            os.remove(txt_filename)
            print(termcolor.colored(u'Remove file <%s>' % txt_filename, 'green'))
        if not rewrite and os.path.exists(txt_filename):
            print(termcolor.colored(u'File <%s> not saved' % txt_filename, 'yellow'))
            return False

        file_obj = open(txt_filename, 'wt')
        file_obj.write(txt)
        file_obj.close()
        return True
    except:
        if file_obj:
            file_obj.close()
        print(termcolor.colored('Save text file <%s> error' % txt_filename, 'red'))
        raise
    return False


def loadTextFile(txt_filename):
    """
    Load from text file.

    :param txt_filename: Text file name.
    :return: File text or empty text if error.
    """
    if not os.path.exists(txt_filename):
        print(termcolor.colored(u'File <%s> not found' % txt_filename, 'yellow'))
        return ''

    file_obj = None
    try:
        file_obj = open(txt_filename, 'rt')
        txt = file_obj.read()
        file_obj.close()
    except:
        if file_obj:
            file_obj.close()
        print(termcolor.colored(u'Load text file <%s> error' % txt_filename, 'red'))
        return ''

    return txt


def appendTextFile(txt_filename, txt, cr=None):
    """
    Add lines to text file.
    If the file does not exist, then the file is created.

    :param txt_filename: Text filename.
    :param txt: Added text.
    :param cr: Carriage return character.
    :return: True/False.
    """
    if cr is None:
        cr = os.linesep

    if not isinstance(txt, str):
        txt = str(txt)

    txt_filename = os.path.normpath(txt_filename)

    if not os.path.exists(txt_filename):
        cr = ''

    file_obj = None
    try:
        file_obj = open(txt_filename, 'at')
        file_obj.write(cr + txt)
        file_obj.close()
        return True
    except:
        if file_obj:
            file_obj.close()
        print(termcolor.colored(u'Error append to text file <%s>' % txt_filename, 'red'))
        raise
    return False


def replaceTextFile(txt_filename, src_text, dst_text, auto_add=True, cr=None):
    """
    Replacing a text in a text file.

    :param txt_filename: Text filename.
    :param src_text: Source text.
    :param dst_text: Destination text.
    :param auto_add: A flag to automatically add a new line.
    :param cr: Carriage return character.
    :return: True/False.
    """
    if cr is None:
        cr = os.linesep

    txt_filename = os.path.normpath(txt_filename)

    if os.path.exists(txt_filename):
        file_obj = None
        try:
            file_obj = open(txt_filename, 'rt')
            txt = file_obj.read()
            file_obj.close()
            txt = txt.replace(src_text, dst_text)
            if auto_add and (dst_text not in txt):
                txt += cr
                txt += dst_text
                print(termcolor.colored('Text file append <%s> in <%s>' % (dst_text, txt_filename), 'green'))
            file_obj = None
            file_obj = open(txt_filename, 'wt')
            file_obj.write(txt)
            file_obj.close()
            file_obj = None
            return True
        except:
            if file_obj:
                file_obj.close()
            print(termcolor.colored('Error replace in text file <%s>' % txt_filename, 'red'))
            raise
    else:
        print(termcolor.colored('Text file <%s> not exists' % txt_filename, 'yellow'))
    return False


def isInTextFile(txt_filename, find_text):
    """
    Is there text in a text file?

    :param txt_filename: Text filename.
    :param find_text: Find text.
    :return: True/False.
    """
    txt_filename = os.path.normpath(txt_filename)

    if os.path.exists(txt_filename):
        file_obj = None
        try:
            file_obj = open(txt_filename, 'rt')
            txt = file_obj.read()
            result = find_text in txt
            file_obj.close()
            file_obj = None
            return result
        except:
            if file_obj:
                file_obj.close()
            print(termcolor.colored('Error find <%s> in text file <%s>' % (find_text, txt_filename), 'red'))
            raise
    else:
        print(termcolor.colored('Text file <%s> not exists' % txt_filename, 'yellow'))
    return False


def generateTextFile(txt_template_filename, txt_output_filename, context=None, output_encoding=None):
    """
    Generation of a text file from a template file.
    
    :param txt_template_filename: Template is a text file.
    :param txt_output_filename: Name the output text file.
    :param context. Context.
        Any dictionary structure can be used as a context.
    :param output_encoding: The code page of the resulting file.
        If not specified, then the code page remains the same as the template.
    :return: True - generation was successful, False - generation error.
    """
    if context is None:
        context = dict()

    template_file = None
    output_file = None

    template_filename = os.path.abspath(txt_template_filename)
    if not os.path.exists(template_filename):
        print(termcolor.colored(u'Template file <%s> not found' % template_filename, 'yellow'))
        return False

    # Read template file
    try:
        template_file = open(template_filename, 'r')
        template_txt = template_file.read()
        template_file.close()
    except:
        if template_file:
            template_file.close()
        print(termcolor.colored(u'Read error template file <%s>' % template_filename, 'red'))
        return False

    #template_encoding = str_func.getCodepage(template_txt)
    #print(termcolor.colored(u'Template code page <%s>' % template_encoding, 'blue'))

    # template_txt = unicode(template_txt, template_encoding)

    # Generate text
    try:
        template = jinja2.Template(template_txt)
        gen_txt = template.render(**context)
    except:
        print(termcolor.colored(u'Error generate text <%s>' % template_txt, 'red'))
        gen_txt = u''
    # if isinstance(gen_txt, str):
    #     if output_encoding is None:
    #         gen_txt = gen_txt.encode(template_encoding)
    #     else:
    #         gen_txt = gen_txt.encode(output_encoding)

    # Write output file
    output_filename = os.path.abspath(txt_output_filename)
    try:
        output_path = os.path.dirname(output_filename)
        if not os.path.exists(output_path):
            print(termcolor.colored(u'Create directory <%s>' % output_path, 'green'))
            os.makedirs(output_path)

        output_file = open(output_filename, 'w+')
        output_file.write(gen_txt)
        output_file.close()
        return os.path.exists(output_filename)
    except:
        if output_file:
            output_file.close()
        print(termcolor.colored(u'Write error text file <%s>' % output_filename, 'red'))
    return False
