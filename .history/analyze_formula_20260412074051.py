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

def find_incomplete_formula(docx_path):
    with zipfile.ZipFile(docx_path, 'r') as z:
        with z.open('word/document.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            
            for elem in root.iter():
                tag_local = elem.tag.split('}')[1] if '}' in elem.tag else elem.tag
                
                if tag_local == 't' and elem.text and '1344' in elem.text:
                    print(f"Found '1344' in text: {elem.text}")
                    
                    parent = None
                    for p in root.iter():
                        if elem in p:
                            parent = p
                            break
                    
                    if parent is not None:
                        grandparent = None
                        for p in root.iter():
                            if parent in p:
                                grandparent = p
                                break
                        
                        if grandparent is not None:
                            print("\nGrandparent element:")
                            for child in grandparent:
                                child_tag = child.tag.split('}')[1] if '}' in child.tag else child.tag
                                print(f"  {child_tag}")
                                
                                if child_tag == 'oMath':
                                    print("    Found oMath!")
                                    for sub in child:
                                        sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub_tag
                                        print(f"      {sub_tag}")

if __name__ == '__main__':
    find_incomplete_formula(DOCX_PATH)
