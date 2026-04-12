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

def analyze_docx(docx_path):
    with zipfile.ZipFile(docx_path, 'r') as z:
        with z.open('word/document.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            
            styles_found = {}
            heading_count = 0
            
            for elem in root.iter():
                tag_local = elem.tag.split('}')[1] if '}' in elem.tag else elem.tag
                
                if tag_local == 'pStyle':
                    style_val = elem.get(qn('w:val'))
                    if style_val:
                        styles_found[style_val] = styles_found.get(style_val, 0) + 1
                
                if tag_local == 'p':
                    pPr = None
                    for child in elem:
                        child_tag = child.tag.split('}')[1] if '}' in child.tag else child.tag
                        if child_tag == 'pPr':
                            pPr = child
                            break
                    
                    if pPr is not None:
                        for child in pPr:
                            child_tag = child.tag.split('}')[1] if '}' in child.tag else child.tag
                            if child_tag == 'pStyle':
                                style_val = child.get(qn('w:val'))
                                if style_val and ('heading' in style_val.lower() or '标题' in style_val or style_val.startswith('Heading')):
                                    heading_count += 1
            
            print("All styles found in document:")
            for style, count in sorted(styles_found.items(), key=lambda x: -x[1]):
                print(f"  {style}: {count}")
            
            print(f"\nTotal potential headings: {heading_count}")
            
            print("\n\nFirst 50 paragraph styles and text preview:")
            para_count = 0
            for elem in root.iter():
                tag_local = elem.tag.split('}')[1] if '}' in elem.tag else elem.tag
                
                if tag_local == 'p':
                    pPr = None
                    for child in elem:
                        child_tag = child.tag.split('}')[1] if '}' in child.tag else child.tag
                        if child_tag == 'pPr':
                            pPr = child
                            break
                    
                    style_val = "None"
                    outline_lvl = None
                    
                    if pPr is not None:
                        for child in pPr:
                            child_tag = child.tag.split('}')[1] if '}' in child.tag else child_tag
                            if child_tag == 'pStyle':
                                style_val = child.get(qn('w:val'), 'None')
                            elif child_tag == 'outlineLvl':
                                outline_lvl = child.get(qn('w:val'))
                    
                    text_parts = []
                    for t in elem.iter():
                        t_tag = t.tag.split('}')[1] if '}' in t.tag else t.tag
                        if t_tag == 't' and t.text:
                            text_parts.append(t.text)
                    text = ''.join(text_parts)[:50]
                    
                    if text.strip():
                        print(f"  Style: {style_val}, OutlineLvl: {outline_lvl}, Text: {text}")
                        para_count += 1
                        if para_count >= 50:
                            break

if __name__ == '__main__':
    analyze_docx(DOCX_PATH)
