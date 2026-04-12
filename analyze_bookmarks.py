# -*- coding: utf-8 -*-
import zipfile
import xml.etree.ElementTree as ET
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DOCX_PATH = r"d:\SoftData\Obsidian\JA-algorithm2\A算法模版.docx"

def qn(ns_tag):
    parts = ns_tag.split(':')
    if len(parts) == 2:
        ns, tag = parts
        nsmap = {
            'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
            'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
            'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        }
        if ns in nsmap:
            return '{' + nsmap[ns] + '}' + tag
    return ns_tag

def analyze_bookmarks(docx_path):
    bookmark_names = {}
    
    with zipfile.ZipFile(docx_path, 'r') as z:
        with z.open('word/document.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            
            for elem in root.iter():
                tag_local = elem.tag.split('}')[1] if '}' in elem.tag else elem.tag
                if tag_local == 'bookmarkStart':
                    bookmark_id = elem.get(qn('w:id'))
                    bookmark_name = elem.get(qn('w:name'))
                    if bookmark_id and bookmark_name:
                        bookmark_names[bookmark_id] = bookmark_name
            
            print("Sample bookmark names:")
            for i, (bid, bname) in enumerate(list(bookmark_names.items())[:30]):
                print(f"  {bid}: {bname}")

if __name__ == '__main__':
    analyze_bookmarks(DOCX_PATH)
