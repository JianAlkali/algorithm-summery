# -*- coding: utf-8 -*-
import os
import re
import zipfile
import xml.etree.ElementTree as ET
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DOCX_PATH = r"d:\SoftData\Obsidian\JA-algorithm2\A算法模版.docx"

W_NS = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
M_NS = '{http://schemas.openxmlformats.org/officeDocument/2006/math}'
R_NS = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'

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

def extract_text_recursive(elem):
    result = []
    for child in elem:
        tag_local = child.tag.split('}')[1] if '}' in child.tag else child.tag
        if tag_local == 't' and child.text:
            result.append(child.text)
        else:
            result.append(extract_text_recursive(child))
    return ''.join(result)

def analyze_textbox_extraction(docx_path):
    with zipfile.ZipFile(docx_path, 'r') as z:
        with z.open('word/document.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            
            body = None
            for child in root:
                tag_local = child.tag.split('}')[1] if '}' in child.tag else child.tag
                if tag_local == 'body':
                    body = child
                    break
            
            if body is None:
                body = root
            
            print("Analyzing body children...")
            
            for idx, child in enumerate(body):
                tag_local = child.tag.split('}')[1] if '}' in child.tag else child.tag
                
                if tag_local == 'p':
                    for r in child:
                        r_tag = r.tag.split('}')[1] if '}' in r.tag else r_tag
                        if r_tag == 'r':
                            for sub in r:
                                sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub_tag
                                if sub_tag == 'drawing':
                                    print(f"\n=== Found drawing in paragraph {idx} ===")
                                    
                                    for elem in sub.iter():
                                        elem_tag = elem.tag.split('}')[1] if '}' in elem.tag else elem.tag
                                        
                                        if elem_tag == 'txbxContent':
                                            print(f"  Found txbxContent!")
                                            for p in elem:
                                                p_tag = p.tag.split('}')[1] if '}' in p.tag else p_tag
                                                if p_tag == 'p':
                                                    text = extract_text_recursive(p)
                                                    if text.strip():
                                                        print(f"    Text: {text[:80]}...")

if __name__ == '__main__':
    analyze_textbox_extraction(DOCX_PATH)
