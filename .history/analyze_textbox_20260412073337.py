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

def analyze_textboxes(docx_path):
    with zipfile.ZipFile(docx_path, 'r') as z:
        with z.open('word/document.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            
            print("Looking for textbox-related elements...")
            
            for elem in root.iter():
                tag = elem.tag
                if 'txbx' in tag.lower() or 'textbox' in tag.lower() or 'pict' in tag.lower() or 'drawing' in tag.lower() or 'shape' in tag.lower():
                    print(f"\nFound element: {tag}")
                    for attr, val in elem.attrib.items():
                        print(f"  {attr}: {val}")
            
            print("\n\nLooking for w:pict and w:drawing elements...")
            
            for elem in root.iter():
                tag_local = elem.tag.split('}')[1] if '}' in elem.tag else elem.tag
                
                if tag_local == 'pict':
                    print("\n=== Found w:pict ===")
                    for child in elem.iter():
                        child_tag = child.tag.split('}')[1] if '}' in child.tag else child.tag
                        if child_tag == 't' and child.text:
                            print(f"  Text: {child.text[:100]}")
                        elif 'txbx' in child_tag.lower():
                            print(f"  Textbox element: {child_tag}")
                
                elif tag_local == 'drawing':
                    print("\n=== Found w:drawing ===")
                    for child in elem.iter():
                        child_tag = child.tag.split('}')[1] if '}' in child.tag else child_tag
                        if child_tag == 't' and child.text:
                            print(f"  Text: {child.text[:100]}")
                        elif 'txbx' in child_tag.lower():
                            print(f"  Textbox element: {child_tag}")

if __name__ == '__main__':
    analyze_textboxes(DOCX_PATH)
