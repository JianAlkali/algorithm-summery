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

def omml_to_latex_debug(element, depth=0):
    indent = "  " * depth
    result = []
    
    for child in element:
        tag_local = child.tag.split('}')[1] if '}' in child.tag else child.tag
        print(f"{indent}Processing: {tag_local}")
        
        if tag_local == 'r':
            for sub in child:
                sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub.tag
                if sub_tag == 't':
                    if sub.text:
                        print(f"{indent}  Text: '{sub.text}'")
                        result.append(sub.text)
        elif tag_local == 't':
            if child.text:
                print(f"{indent}  Text: '{child.text}'")
                result.append(child.text)
        elif tag_local == 'rPr':
            pass
        elif tag_local == 'f':
            print(f"{indent}  Processing fraction...")
            num_parts = []
            den_parts = []
            current = 'num'
            for sub in child:
                sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub.tag
                print(f"{indent}    Fraction child: {sub_tag}")
                if sub_tag == 'num':
                    current = 'num'
                elif sub_tag == 'den':
                    current = 'den'
                elif sub_tag == 'e':
                    content = omml_to_latex_debug(sub, depth+2)
                    print(f"{indent}    e content: '{content}'")
                    if current == 'num':
                        num_parts.append(content)
                    else:
                        den_parts.append(content)
            num = ''.join(num_parts)
            den = ''.join(den_parts)
            print(f"{indent}  Fraction: num='{num}', den='{den}'")
            if num or den:
                result.append('\\frac{' + num + '}{' + den + '}')
        elif tag_local == 'num':
            for sub in child:
                sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub.tag
                if sub_tag == 't':
                    if sub.text:
                        result.append(sub.text)
                elif sub_tag == 'e':
                    result.append(omml_to_latex_debug(sub, depth+1))
        elif tag_local == 'den':
            for sub in child:
                sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub.tag
                if sub_tag == 't':
                    if sub.text:
                        result.append(sub.text)
                elif sub_tag == 'e':
                    result.append(omml_to_latex_debug(sub, depth+1))
        elif tag_local == 'e':
            content = omml_to_latex_debug(child, depth+1)
            result.append(content)
        elif tag_local == 'sSup':
            base = ''
            sup = ''
            for sub in child:
                sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub.tag
                if sub_tag == 'e':
                    base = omml_to_latex_debug(sub, depth+1)
                elif sub_tag == 'sup':
                    sup = omml_to_latex_debug(sub, depth+1)
            if base:
                result.append(base + '^{' + sup + '}')
        elif tag_local == 'rad':
            deg = ''
            base = ''
            for sub in child:
                sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub.tag
                if sub_tag == 'deg':
                    deg = omml_to_latex_debug(sub, depth+1)
                elif sub_tag == 'e':
                    base = omml_to_latex_debug(sub, depth+1)
            
            if deg:
                result.append('\\sqrt[' + deg + ']{' + base + '}')
            else:
                result.append('\\sqrt{' + base + '}')
        elif tag_local == 'ctrlPr':
            pass
        elif tag_local == 'radPr':
            pass
        elif tag_local == 'fPr':
            pass
        else:
            print(f"{indent}  Unknown tag, recursing...")
            result.append(omml_to_latex_debug(child, depth+1))
    
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
                        print("\nLooking for oMath with '<' and fraction...")
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
                                    print("\nFound target oMath!")
                                    latex = omml_to_latex_debug(child)
                                    print(f"\nFinal LaTeX: {latex}")
                    break

if __name__ == '__main__':
    find_incomplete_formula(DOCX_PATH)
