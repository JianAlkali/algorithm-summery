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

def extract_text_recursive(elem, depth=0):
    indent = "  " * depth
    result = []
    for child in elem:
        tag_local = child.tag.split('}')[1] if '}' in child.tag else child.tag
        
        if tag_local == 't' and child.text:
            result.append(child.text)
            print(f"{indent}{tag_local}: '{child.text}'")
        else:
            print(f"{indent}{tag_local}")
            result.append(extract_text_recursive(child, depth+1))
    return ''.join(result)

def find_incomplete_formula(docx_path):
    with zipfile.ZipFile(docx_path, 'r') as z:
        with z.open('word/document.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            
            for elem in root.iter():
                tag_local = elem.tag.split('}')[1] if '}' in elem.tag else elem.tag
                
                if tag_local == 't' and elem.text and '1344' in elem.text:
                    print(f"Found '1344' in text: {elem.text}")
                    
                    for p in root.iter():
                        if elem in p:
                            parent = p
                            break
                    
                    for p in root.iter():
                        if parent in p:
                            grandparent = p
                            break
                    
                    if grandparent is not None:
                        print("\nGrandparent element structure:")
                        for child in grandparent:
                            child_tag = child.tag.split('}')[1] if '}' in child.tag else child.tag
                            print(f"\n{child_tag}:")
                            extract_text_recursive(child, 1)
                    break

if __name__ == '__main__':
    find_incomplete_formula(DOCX_PATH)
