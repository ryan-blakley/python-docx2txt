import argparse
import os
import re
import sys
import xml.etree.ElementTree as ET
import zipfile


nsmap = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def process_args():
    parser = argparse.ArgumentParser(description="A pure python-based utility to extract text and images from docx"
                                                 " files.")
    parser.add_argument("docx", help="Path of the docx file to run on.")
    parser.add_argument('-i', '--img_dir', help="Path of directory to extract images to.")

    args = parser.parse_args()

    if not os.path.exists(args.docx):
        print('File {} does not exist.'.format(args.docx))
        sys.exit(1)

    if args.img_dir is not None and not os.path.exists(args.img_dir):
        try:
            os.makedirs(args.img_dir)
        except OSError:
            print("Unable to create img_dir {}".format(args.img_dir))
            sys.exit(1)
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
    zipf = zipfile.ZipFile(args.docx)
    filelist = zipf.namelist()

    # get header text
    # there can be 3 header files in the zip
    header_xmls = 'word/header\d*.xml'
    for fname in filelist:
        if re.match(header_xmls, fname):
            ret_text += xml2text(zipf.read(fname))

    # get main text
    doc_xml = 'word/document.xml'
    ret_text += xml2text(zipf.read(doc_xml))

    # get footer text
    # there can be 3 footer files in the zip
    footer_xmls = 'word/footer\d*.xml'
    for fname in filelist:
        if re.match(footer_xmls, fname):
            ret_text += xml2text(zipf.read(fname))

    if args.img_dir is not None:
        # extract images
        for fname in filelist:
            _, extension = os.path.splitext(fname)
            if extension in [".jpg", ".jpeg", ".png", ".bmp"]:
                dst_fname = os.path.join(args.img_dir, os.path.basename(fname))
                with open(dst_fname, "wb") as dst_f:
                    dst_f.write(zipf.read(fname))

    zipf.close()

    non_blank_lines = [line for line in ret_text.splitlines() if line.strip()]
    cleaned_text = "\n".join(non_blank_lines)
    print(cleaned_text)
