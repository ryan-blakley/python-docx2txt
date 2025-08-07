import xml.etree.ElementTree as ET

from argparse import ArgumentParser
from os import makedirs
from os.path import basename, exists, join, splitext
from re import match
from sys import exit
from zipfile import ZipFile


nsmap = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def process_args():
    parser = ArgumentParser(description="A pure python-based utility to extract text and images from docx files.")
    parser.add_argument("docx", help="Path of the docx file to run on.")
    parser.add_argument('-e', '--extract_imgs', action='store_true',
                        help="Extract all images into a sub directory named after the docx filename.")

    args = parser.parse_args()

    if not exists(args.docx):
        print('File {} does not exist.'.format(args.docx))
        exit(1)
    return args


def qn(tag):
    """
    Stands for 'qualified name', a utility function to turn a namespace-prefixed
    tag name into a Clark-notation qualified tag name for lxml. For example,
    ``qn('p:cSld')`` returns ``'{http://schemas.../main}cSld'``. Source:
    https://github.com/python-openxml/python-docx/
    """
    prefix, tagroot = tag.split(':')
    uri = nsmap[prefix]
    return '{{{}}}{}'.format(uri, tagroot)


def xml2text(xml):
    """
    A string representing the textual content of this run, with content
    child elements like ``<w:tab/>`` translated to their Python
    equivalent.
    Adapted from: https://github.com/python-openxml/python-docx/
    """
    ret_text = u''
    root = ET.fromstring(xml)
    for child in root.iter():
        if child.tag == qn('w:t'):
            t_text = child.text
            ret_text += t_text if t_text is not None else ''
        elif child.tag == qn('w:tab'):
            ret_text += '\t'
        elif child.tag in (qn('w:br'), qn('w:cr')):
            ret_text += '\n'
        elif child.tag == qn("w:p"):
            ret_text += '\n\n'
    return ret_text


def run():
    args = process_args()
    ret_text = u''

    # unzip the docx in memory
    zipf = ZipFile(args.docx)
    filelist = zipf.namelist()

    # get header text
    # there can be 3 header files in the zip
    header_xmls = 'word/header\d*.xml'
    for fname in filelist:
        if match(header_xmls, fname):
            ret_text += xml2text(zipf.read(fname))

    # get main text
    doc_xml = 'word/document.xml'
    ret_text += xml2text(zipf.read(doc_xml))

    # get footer text
    # there can be 3 footer files in the zip
    footer_xmls = 'word/footer\d*.xml'
    for fname in filelist:
        if match(footer_xmls, fname):
            ret_text += xml2text(zipf.read(fname))

    if args.extract_imgs:
        # extract images
        out_dir = f"{args.docx}-images"
        makedirs(out_dir, exist_ok=True)
        for fname in filelist:
            _, extension = splitext(fname)
            if extension in [".jpg", ".jpeg", ".png", ".bmp"]:
                dst_fname = join(out_dir, basename(fname))
                with open(dst_fname, "wb") as dst_f:
                    dst_f.write(zipf.read(fname))

    zipf.close()

    non_blank_lines = [line for line in ret_text.splitlines() if line.strip()]
    cleaned_text = "\n".join(non_blank_lines)
    print(cleaned_text)
