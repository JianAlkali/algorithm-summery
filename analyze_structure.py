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

def analyze_structure(docx_path):
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
            
            print("Analyzing document structure (first 100 elements)...")
            print("=" * 80)
            
            elem_count = 0
            for elem in body.iter():
                tag_local = elem.tag.split('}')[1] if '}' in elem.tag else elem.tag
                
                if tag_local == 'p':
                    pPr = None
                    for child in elem:
                        child_tag = child.tag.split('}')[1] if '}' in child.tag else child.tag
                        if child_tag == 'pPr':
                            pPr = child
                            break
                    
                    style_val = "None"
                    if pPr is not None:
                        for child in pPr:
                            child_tag = child.tag.split('}')[1] if '}' in child.tag else child_tag
                            if child_tag == 'pStyle':
                                style_val = child.get(qn('w:val'), 'None')
                    
                    text_parts = []
                    for t in elem.iter():
                        t_tag = t.tag.split('}')[1] if '}' in t.tag else t.tag
                        if t_tag == 't' and t.text:
                            text_parts.append(t.text)
                    text = ''.join(text_parts)[:80]
                    
                    is_toc = style_val in ['TOC1', 'TOC2', 'TOC']
                    marker = " [HEADING]" if is_toc else ""
                    
                    if text.strip() or is_toc:
                        print(f"[P] Style: {style_val}{marker}")
                        print(f"    Text: {text}")
                        print()
                        elem_count += 1
                
                elif tag_local == 'txbxContent':
                    print("[TEXTBOX]")
                    para_texts = []
                    for p in elem:
                        p_tag = p.tag.split('}')[1] if '}' in p.tag else p_tag
                        if p_tag == 'p':
                            text_parts = []
                            for t in p.iter():
                                t_tag = t.tag.split('}')[1] if '}' in t.tag else t_tag
                                if t_tag == 't' and t.text:
                                    text_parts.append(t.text)
                            if text_parts:
                                para_texts.append(''.join(text_parts))
                    
                    for pt in para_texts[:3]:
                        print(f"    {pt[:80]}")
                    if len(para_texts) > 3:
                        print(f"    ... ({len(para_texts)} paragraphs total)")
                    print()
                    elem_count += 1
                
                if elem_count >= 100:
                    break

if __name__ == '__main__':
    analyze_structure(DOCX_PATH)
