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
        }
        if ns in nsmap:
            return '{' + nsmap[ns] + '}' + tag
    return ns_tag

def print_element(elem, depth=0):
    indent = "  " * depth
    tag_local = elem.tag.split('}')[1] if '}' in elem.tag else elem.tag
    
    if tag_local == 't' and elem.text:
        print(f"{indent}{tag_local}: '{elem.text}'")
    else:
        print(f"{indent}{tag_local}")
        for child in elem:
            print_element(child, depth+1)

def find_incomplete_formula(docx_path):
    with zipfile.ZipFile(docx_path, 'r') as z:
        with z.open('word/document.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            
            for elem in root.iter():
                tag_local = elem.tag.split('}')[1] if '}' in elem.tag else elem.tag
                
                if tag_local == 't' and elem.text and '1344' in elem.text:
                    for p in root.iter():
                        if elem in p:
                            parent = p
                            break
                    
                    for p in root.iter():
                        if parent in p:
                            grandparent = p
                            break
                    
                    if grandparent is not None:
                        for child in grandparent:
                            child_tag = child.tag.split('}')[1] if '}' in child.tag else child_tag
                            if child_tag == 'oMath':
                                has_lt = False
                                has_f = False
                                for sub in child:
                                    sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub_tag
                                    if sub_tag == 'r':
                                        for t in sub.iter():
                                            t_tag = t.tag.split('}')[1] if '}' in t.tag else t_tag
                                            if t_tag == 't' and t.text and '<' in t.text:
                                                has_lt = True
                                    if sub_tag == 'f':
                                        has_f = True
                                
                                if has_lt and has_f:
                                    print("\nTarget oMath structure:")
                                    print_element(child)
                    break

if __name__ == '__main__':
    find_incomplete_formula(DOCX_PATH)
