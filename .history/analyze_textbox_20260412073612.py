# -*- coding: utf-8 -*-
import zipfile
import xml.etree.ElementTree as ET
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DOCX_PATH = r"d:\SoftData\Obsidian\JA-algorithm2\A算法模版.docx"

W_NS = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

def analyze_body_structure(docx_path):
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
                print("No body found!")
                return
            
            print(f"Body has {len(body)} direct children")
            
            for idx, child in enumerate(body[:20]):
                tag_local = child.tag.split('}')[1] if '}' in child.tag else child.tag
                print(f"  [{idx}] {tag_local}")
                
                if tag_local == 'p':
                    for sub in child:
                        sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub_tag
                        print(f"       - {sub_tag}")
                        
                        if sub_tag == 'r':
                            for subsub in sub:
                                subsub_tag = subsub.tag.split('}')[1] if '}' in subsub.tag else subsub_tag
                                print(f"         - {subsub_tag}")

if __name__ == '__main__':
    analyze_body_structure(DOCX_PATH)
