# -*- coding: utf-8 -*-
import os
import re
import zipfile
import xml.etree.ElementTree as ET
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DOCX_PATH = r"d:\SoftData\Obsidian\JA-algorithm2\A算法模版.docx"
OUTPUT_DIR = r"d:\SoftData\Obsidian\JA-algorithm2"

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

def omml_to_latex(element, depth=0):
    result = []
    
    for child in element:
        tag_local = child.tag.split('}')[1] if '}' in child.tag else child.tag
        
        if tag_local == 'r':
            for sub in child:
                sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub.tag
                if sub_tag == 't':
                    if sub.text:
                        result.append(sub.text)
        elif tag_local == 't':
            if child.text:
                result.append(child.text)
        elif tag_local == 'oMath':
            latex = omml_to_latex(child, depth+1)
            if latex.strip():
                result.append(latex)
        elif tag_local == 'oMathPara':
            latex = omml_to_latex(child, depth+1)
            if latex.strip():
                result.append(latex)
        elif tag_local == 'f':
            num_parts = []
            den_parts = []
            current = 'num'
            for sub in child:
                sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub.tag
                if sub_tag == 'num':
                    current = 'num'
                elif sub_tag == 'den':
                    current = 'den'
                elif sub_tag == 'e':
                    content = omml_to_latex(sub, depth+1)
                    if current == 'num':
                        num_parts.append(content)
                    else:
                        den_parts.append(content)
            num = ''.join(num_parts)
            den = ''.join(den_parts)
            if num or den:
                result.append('\\frac{' + num + '}{' + den + '}')
        elif tag_local == 'num':
            for sub in child:
                sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub.tag
                if sub_tag == 't':
                    if sub.text:
                        result.append(sub.text)
                elif sub_tag == 'e':
                    result.append(omml_to_latex(sub, depth+1))
        elif tag_local == 'den':
            for sub in child:
                sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub.tag
                if sub_tag == 't':
                    if sub.text:
                        result.append(sub.text)
                elif sub_tag == 'e':
                    result.append(omml_to_latex(sub, depth+1))
        elif tag_local == 'e':
            result.append(omml_to_latex(child, depth+1))
        elif tag_local == 'sSup':
            base = ''
            sup = ''
            for sub in child:
                sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub.tag
                if sub_tag == 'e':
                    base = omml_to_latex(sub, depth+1)
                elif sub_tag == 'sup':
                    sup = omml_to_latex(sub, depth+1)
            if base:
                result.append(base + '^{' + sup + '}')
        elif tag_local == 'sSub':
            base = ''
            sub_val = ''
            for sub in child:
                sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub.tag
                if sub_tag == 'e':
                    base = omml_to_latex(sub, depth+1)
                elif sub_tag == 'sub':
                    sub_val = omml_to_latex(sub, depth+1)
            if base:
                result.append(base + '_{' + sub_val + '}')
        elif tag_local == 'sSubSup':
            base = ''
            sub_val = ''
            sup_val = ''
            for sub in child:
                sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub.tag
                if sub_tag == 'e':
                    base = omml_to_latex(sub, depth+1)
                elif sub_tag == 'sub':
                    sub_val = omml_to_latex(sub, depth+1)
                elif sub_tag == 'sup':
                    sup_val = omml_to_latex(sub, depth+1)
            if base:
                result.append(base + '_{' + sub_val + '}^{' + sup_val + '}')
        elif tag_local == 'd':
            dPr = child.find(qn('m:dPr'))
            begChr = '('
            endChr = ')'
            if dPr is not None:
                for pr in dPr:
                    pr_tag = pr.tag.split('}')[1] if '}' in pr.tag else pr.tag
                    if pr_tag == 'begChr':
                        begChr = pr.get(qn('m:val'), '(')
                    elif pr_tag == 'endChr':
                        endChr = pr.get(qn('m:val'), ')')
            
            e_elem = child.find(qn('m:e'))
            content = omml_to_latex(e_elem, depth+1) if e_elem is not None else ''
            
            if begChr == '(' and endChr == ')':
                result.append('\\left(' + content + '\\right)')
            elif begChr == '[' and endChr == ']':
                result.append('\\left[' + content + '\\right]')
            elif begChr == '{' and endChr == '}':
                result.append('\\left\\{' + content + '\\right\\}')
            elif begChr == '|' and endChr == '|':
                result.append('\\left|' + content + '\\right|')
            else:
                result.append('\\left' + begChr + content + '\\right' + endChr)
        elif tag_local == 'func':
            func_name = ''
            arg = ''
            for sub in child:
                sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub.tag
                if sub_tag == 'fName':
                    for fn in sub:
                        fn_tag = fn.tag.split('}')[1] if '}' in fn.tag else fn.tag
                        if fn_tag == 't':
                            if fn.text:
                                func_name = fn.text
                elif sub_tag == 'e':
                    arg = omml_to_latex(sub, depth+1)
            
            latex_func = func_name
            if func_name in ['sin', 'cos', 'tan', 'cot', 'sec', 'csc']:
                latex_func = '\\' + func_name
            elif func_name in ['log', 'ln', 'lg']:
                latex_func = '\\' + func_name
            elif func_name in ['max', 'min', 'sup', 'inf']:
                latex_func = '\\' + func_name
            
            result.append(latex_func + ' ' + arg if arg else latex_func)
        elif tag_local == 'rad':
            deg = ''
            base = ''
            for sub in child:
                sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub.tag
                if sub_tag == 'deg':
                    deg = omml_to_latex(sub, depth+1)
                elif sub_tag == 'e':
                    base = omml_to_latex(sub, depth+1)
            
            if deg:
                result.append('\\sqrt[' + deg + ']{' + base + '}')
            else:
                result.append('\\sqrt{' + base + '}')
        elif tag_local == 'nary':
            nary_chr = ''
            sub_val = ''
            sup_val = ''
            base = ''
            
            for sub in child:
                sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub.tag
                if sub_tag == 'naryPr':
                    for pr in sub:
                        pr_tag = pr.tag.split('}')[1] if '}' in pr.tag else pr.tag
                        if pr_tag == 'chr':
                            nary_chr = pr.get(qn('m:val'), '')
                elif sub_tag == 'sub':
                    sub_val = omml_to_latex(sub, depth+1)
                elif sub_tag == 'sup':
                    sup_val = omml_to_latex(sub, depth+1)
                elif sub_tag == 'e':
                    base = omml_to_latex(sub, depth+1)
            
            latex_op = '\\sum'
            if nary_chr == '∫':
                latex_op = '\\int'
            elif nary_chr == '∏':
                latex_op = '\\prod'
            
            result.append(latex_op + '_{' + sub_val + '}^{' + sup_val + '} ' + base)
        elif tag_local == 'limLow':
            base = ''
            lim = ''
            for sub in child:
                sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub.tag
                if sub_tag == 'e':
                    base = omml_to_latex(sub, depth+1)
                elif sub_tag == 'lim':
                    lim = omml_to_latex(sub, depth+1)
            result.append(base + '_{' + lim + '}')
        elif tag_local == 'limUpp':
            base = ''
            lim = ''
            for sub in child:
                sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub.tag
                if sub_tag == 'e':
                    base = omml_to_latex(sub, depth+1)
                elif sub_tag == 'lim':
                    lim = omml_to_latex(sub, depth+1)
            result.append(base + '^{' + lim + '}')
        elif tag_local == 'm':
            rows = []
            for mr in child:
                mr_tag = mr.tag.split('}')[1] if '}' in mr.tag else mr.tag
                if mr_tag == 'mr':
                    cells = []
                    for e in mr:
                        e_tag = e.tag.split('}')[1] if '}' in e.tag else e.tag
                        if e_tag == 'e':
                            cells.append(omml_to_latex(e, depth+1))
                    rows.append(' & '.join(cells))
            if rows:
                result.append('\\begin{matrix} ' + ' \\\\ '.join(rows) + ' \\end{matrix}')
        elif tag_local == 'acc':
            content = ''
            for sub in child:
                sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub.tag
                if sub_tag == 'e':
                    content = omml_to_latex(sub, depth+1)
            result.append('\\overline{' + content + '}')
        elif tag_local == 'bar':
            content = ''
            for sub in child:
                sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub.tag
                if sub_tag == 'e':
                    content = omml_to_latex(sub, depth+1)
            result.append('\\overline{' + content + '}')
        elif tag_local == 'borderBox':
            content = ''
            for sub in child:
                sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub.tag
                if sub_tag == 'e':
                    content = omml_to_latex(sub, depth+1)
            result.append('\\boxed{' + content + '}')
        else:
            result.append(omml_to_latex(child, depth+1))
    
    return ''.join(result)

def extract_text_from_element(elem, bookmark_names=None):
    if bookmark_names is None:
        bookmark_names = {}
    
    result = []
    
    for child in elem:
        tag_local = child.tag.split('}')[1] if '}' in child.tag else child.tag
        
        if tag_local == 't':
            if child.text:
                result.append(child.text)
        elif tag_local == 'tab':
            result.append('\t')
        elif tag_local == 'br':
            result.append('\n')
        elif tag_local == 'cr':
            result.append('\n')
        elif tag_local == 'noBreakHyphen':
            result.append('-')
        elif tag_local == 'softHyphen':
            result.append('-')
        elif tag_local == 'hyperlink':
            hyperlink_text = extract_text_from_element(child, bookmark_names)
            anchor = child.get(qn('w:anchor'))
            if anchor:
                anchor_name = bookmark_names.get(anchor, anchor)
                result.append(f'[[{anchor_name}|{hyperlink_text}]]')
            else:
                result.append(hyperlink_text)
        elif tag_local == 'r':
            for sub in child:
                sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub.tag
                if sub_tag == 't':
                    if sub.text:
                        result.append(sub.text)
                elif sub_tag == 'tab':
                    result.append('\t')
                elif sub_tag == 'br':
                    result.append('\n')
                elif sub_tag == 'cr':
                    result.append('\n')
                elif sub_tag == 'noBreakHyphen':
                    result.append('-')
                elif sub_tag == 'drawing':
                    pass
                elif sub_tag == 'pict':
                    pass
                elif sub_tag == 'object':
                    pass
        elif tag_local == 'bookmarkStart':
            pass
        elif tag_local == 'bookmarkEnd':
            pass
        elif tag_local == 'oMath':
            latex = omml_to_latex(child)
            if latex.strip():
                result.append(f'${latex}$')
        elif tag_local == 'oMathPara':
            latex = omml_to_latex(child)
            if latex.strip():
                result.append(f'\n$$\n{latex}\n$$\n')
        else:
            result.append(extract_text_from_element(child, bookmark_names))
    
    return ''.join(result)

def get_style_val(p_elem):
    for child in p_elem:
        tag_local = child.tag.split('}')[1] if '}' in child.tag else child.tag
        if tag_local == 'pPr':
            for ppr_child in child:
                ppr_tag = ppr_child.tag.split('}')[1] if '}' in ppr_child.tag else ppr_child.tag
                if ppr_tag == 'pStyle':
                    return ppr_child.get(qn('w:val'))
    return None

def get_heading_level(style_val):
    if style_val is None:
        return None
    
    if style_val == 'TOC1' or style_val == '1':
        return 1
    elif style_val == 'TOC2' or style_val == '2':
        return 2
    elif style_val == 'TOC3' or style_val == '3':
        return 3
    elif style_val == 'TOC4' or style_val == '4':
        return 4
    elif style_val == 'TOC':
        return 0
    
    return None

def clean_title_text(text):
    text = re.sub(r'\[\[[^\]]+\|([^\]]+)\]\]', r'\1', text)
    text = re.sub(r'\[\[[^\]]+\]\]', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    text = text.replace('\t', ' ')
    return text.strip()

def extract_textbox_from_drawing(drawing_elem, bookmark_names):
    textbox_paras = []
    
    for elem in drawing_elem.iter():
        tag_local = elem.tag.split('}')[1] if '}' in elem.tag else elem.tag
        
        if tag_local == 'txbxContent':
            for p in elem:
                p_tag = p.tag.split('}')[1] if '}' in p.tag else p.tag
                if p_tag == 'p':
                    para_text = extract_text_from_element(p, bookmark_names)
                    if para_text.strip():
                        textbox_paras.append(para_text)
    
    if textbox_paras:
        return '\n'.join(textbox_paras)
    return None

def parse_docx(docx_path):
    bookmark_names = {}
    
    with zipfile.ZipFile(docx_path, 'r') as z:
        with z.open('word/document.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            
            for elem in root.iter():
                tag_local = elem.tag.split('}')[1] if '}' in elem.tag else elem.tag
                if tag_local == 'bookmarkStart':
                    bookmark_id = elem.get(qn('w:id'))
                    bookmark_name = elem.get(qn('w:name'))
                    if bookmark_id and bookmark_name:
                        bookmark_names[bookmark_id] = bookmark_name
            
            body = None
            for child in root:
                tag_local = child.tag.split('}')[1] if '}' in child.tag else child.tag
                if tag_local == 'body':
                    body = child
                    break
            
            if body is None:
                body = root
            
            elements = []
            processed_drawings = set()
            
            def process_paragraph(p_elem):
                style_val = get_style_val(p_elem)
                heading_level = get_heading_level(style_val)
                text = extract_text_from_element(p_elem, bookmark_names)
                
                if heading_level is not None and heading_level > 0:
                    clean_text = clean_title_text(text)
                    elements.append({
                        'type': 'heading',
                        'level': heading_level,
                        'text': clean_text,
                        'content': text
                    })
                elif text.strip() and style_val != 'TOC':
                    elements.append({
                        'type': 'paragraph',
                        'content': text
                    })
            
            def process_drawing(drawing_elem):
                if id(drawing_elem) in processed_drawings:
                    return
                processed_drawings.add(id(drawing_elem))
                
                textbox_content = extract_textbox_from_drawing(drawing_elem, bookmark_names)
                if textbox_content:
                    elements.append({
                        'type': 'textbox',
                        'content': textbox_content
                    })
            
            for child in body:
                tag_local = child.tag.split('}')[1] if '}' in child.tag else child.tag
                
                if tag_local == 'p':
                    for elem in child.iter():
                        elem_tag = elem.tag.split('}')[1] if '}' in elem.tag else elem.tag
                        if elem_tag == 'drawing':
                            process_drawing(elem)
                    
                    process_paragraph(child)
                
                elif tag_local == 'tbl':
                    pass
            
            return elements, bookmark_names

def build_hierarchy(elements):
    root = {'title': '目录', 'level': 0, 'children': [], 'content': []}
    stack = [root]
    
    for elem in elements:
        if elem['type'] == 'heading':
            level = elem['level']
            title = elem['text']
            
            while len(stack) > level:
                stack.pop()
            
            if len(stack) < level:
                while len(stack) < level:
                    placeholder = {
                        'title': '',
                        'level': len(stack),
                        'children': [],
                        'content': []
                    }
                    stack[-1]['children'].append(placeholder)
                    stack.append(placeholder)
            
            node = {
                'title': title,
                'level': level,
                'children': [],
                'content': []
            }
            stack[-1]['children'].append(node)
            stack.append(node)
        else:
            if stack:
                stack[-1]['content'].append(elem)
    
    return root

def sanitize_filename(name):
    name = re.sub(r'[\[\]]', '', name)
    invalid_chars = r'[<>:"/\\|?*]'
    name = re.sub(invalid_chars, '_', name)
    name = re.sub(r'\s+', ' ', name)
    name = name.strip()
    if not name:
        name = 'untitled'
    if len(name) > 200:
        name = name[:200]
    return name

def generate_obsidian_notes(node, output_dir, parent_link=None, created_files=None):
    if created_files is None:
        created_files = set()
    
    if node['title'] and node['title'] != '目录':
        filename = sanitize_filename(node['title']) + '.md'
        filepath = os.path.join(output_dir, filename)
        
        base_name = sanitize_filename(node['title'])
        counter = 1
        while filepath in created_files or os.path.exists(filepath):
            filename = f"{base_name}_{counter}.md"
            filepath = os.path.join(output_dir, filename)
            counter += 1
        
        created_files.add(filepath)
        
        content_lines = []
        
        if parent_link:
            content_lines.append(f"[[{parent_link}]]")
            content_lines.append("")
        
        for child in node['children']:
            if child['title']:
                content_lines.append(f"[[{child['title']}]]")
        
        if node['children']:
            content_lines.append("")
        
        for item in node['content']:
            if item['type'] == 'textbox':
                content_lines.append("```cpp")
                content_lines.append(item['content'])
                content_lines.append("```")
                content_lines.append("")
            else:
                content_lines.append(item['content'])
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content_lines))
        
        print(f"Created: {filename}")
        
        for child in node['children']:
            generate_obsidian_notes(child, output_dir, node['title'], created_files)
    else:
        for child in node['children']:
            generate_obsidian_notes(child, output_dir, None, created_files)

def main():
    print("Parsing Word document...")
    elements, bookmark_names = parse_docx(DOCX_PATH)
    
    print(f"\nTotal elements: {len(elements)}")
    
    heading_count = sum(1 for e in elements if e['type'] == 'heading')
    textbox_count = sum(1 for e in elements if e['type'] == 'textbox')
    paragraph_count = sum(1 for e in elements if e['type'] == 'paragraph')
    print(f"Headings: {heading_count}, Textboxes: {textbox_count}, Paragraphs: {paragraph_count}")
    
    print("\nFirst 30 elements:")
    for i, elem in enumerate(elements[:30]):
        if elem['type'] == 'heading':
            text_preview = elem['text'][:60] if len(elem['text']) > 60 else elem['text']
            print(f"  [{i}] Heading {elem['level']}: {text_preview}")
        elif elem['type'] == 'textbox':
            text_preview = elem['content'][:60] if len(elem['content']) > 60 else elem['content']
            print(f"  [{i}] Textbox: {text_preview}...")
        else:
            text_preview = elem['content'][:60] if len(elem['content']) > 60 else elem['content']
            print(f"  [{i}] Paragraph: {text_preview}")
    
    print("\nBuilding hierarchy...")
    root = build_hierarchy(elements)
    
    print(f"Root has {len(root['children'])} top-level children")
    
    print("\nGenerating Obsidian notes...")
    generate_obsidian_notes(root, OUTPUT_DIR)
    
    print("\nDone!")

if __name__ == '__main__':
    main()
