# -*- coding: utf-8 -*-
import zipfile
import xml.etree.ElementTree as ET
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DOCX_PATH = r"d:\SoftData\Obsidian\JA-algorithm2\A算法模版.docx"

W_NS = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
A_NS = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
WPS_NS = '{http://schemas.microsoft.com/office/word/2010/wordprocessingShape}'

def extract_text_recursive(elem, depth=0):
    result = []
    for child in elem:
        tag_local = child.tag.split('}')[1] if '}' in child.tag else child.tag
        if tag_local == 't' and child.text:
            result.append(child.text)
        else:
            result.append(extract_text_recursive(child, depth+1))
    return ''.join(result)

def analyze_textbox_content(docx_path):
    with zipfile.ZipFile(docx_path, 'r') as z:
        with z.open('word/document.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            
            print("Looking for textbox content in drawing elements...")
            
            textbox_count = 0
            for elem in root.iter():
                tag_local = elem.tag.split('}')[1] if '}' in elem.tag else elem.tag
                
                if tag_local == 'drawing':
                    for txbxContent in elem.iter():
                        txbx_tag = txbxContent.tag.split('}')[1] if '}' in txbxContent.tag else txbxContent.tag
                        
                        if txbx_tag == 'txbxContent' or 'txbxContent' in txbxContent.tag:
                            textbox_count += 1
                            print(f"\n=== Textbox #{textbox_count} ===")
                            
                            for p in txbxContent:
                                p_tag = p.tag.split('}')[1] if '}' in p.tag else p_tag
                                if p_tag == 'p':
                                    text = extract_text_recursive(p)
                                    if text.strip():
                                        print(f"  {text[:100]}")
            
            print(f"\n\nTotal textboxes found: {textbox_count}")

if __name__ == '__main__':
    analyze_textbox_content(DOCX_PATH)
