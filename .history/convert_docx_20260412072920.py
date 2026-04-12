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

def qn(ns_tag):
    parts = ns_tag.split(':')
    if len(parts) == 2:
        ns, tag = parts
        nsmap = {
            'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
            'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
            'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
            'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
            'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
            'v': 'urn:schemas-microsoft-com:vml',
            'o': 'urn:schemas-microsoft-com:office:office',
            'w14': 'http://schemas.microsoft.com/office/word/2010/wordml',
        }
        if ns in nsmap:
            return '{' + nsmap[ns] + '}' + tag
    return ns_tag

W_NS = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
M_NS = '{http://schemas.openxmlformats.org/officeDocument/2006/math}'
R_NS = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
V_NS = '{urn:schemas-microsoft-com:vml}'
O_NS = '{urn:schemas-microsoft-com:office:office}'

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
                elif sub_tag == 'fPr':
                    pass
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
            elif begChr == '‖' and endChr == '‖':
                result.append('\\left\\|' + content + '\\right\\|')
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
            elif func_name == 'sqrt':
                latex_func = '\\sqrt'
            elif func_name == 'sum':
                latex_func = '\\sum'
            elif func_name == 'prod':
                latex_func = '\\prod'
            elif func_name == 'lim':
                latex_func = '\\lim'
            
            result.append(latex_func + ' ' + arg if arg else latex_func)
        elif tag_local == 'rad':
            deg = ''
            base = ''
            for sub in child:
                sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub.tag
                if sub_tag == 'radPr':
                    pass
                elif sub_tag == 'deg':
                    deg = omml_to_latex(sub, depth+1)
                elif sub_tag == 'e':
                    base = omml_to_latex(sub, depth+1)
            
            if deg:
                result.append('\\sqrt[' + deg + ']{' + base + '}')
            else:
                result.append('\\sqrt{' + base + '}')
        elif tag_local == 'nary':
            nary_chr = ''
            nary_lim_loc = 'undOvr'
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
                        elif pr_tag == 'limLoc':
                            nary_lim_loc = pr.get(qn('m:val'), 'undOvr')
                elif sub_tag == 'sub':
                    sub_val = omml_to_latex(sub, depth+1)
                elif sub_tag == 'sup':
                    sup_val = omml_to_latex(sub, depth+1)
                elif sub_tag == 'e':
                    base = omml_to_latex(sub, depth+1)
            
            latex_op = '\\sum'
            if nary_chr == '∫':
                latex_op = '\\int'
            elif nary_chr == '∬':
                latex_op = '\\iint'
            elif nary_chr == '∏':
                latex_op = '\\prod'
            elif nary_chr == '⋃':
                latex_op = '\\bigcup'
            elif nary_chr == '⋂':
                latex_op = '\\bigcap'
            elif nary_chr == '⊕':
                latex_op = '\\bigoplus'
            elif nary_chr == '⊗':
                latex_op = '\\bigotimes'
            
            if nary_lim_loc == 'undOvr':
                result.append(latex_op + '_{' + sub_val + '}^{' + sup_val + '} ' + base)
            else:
                result.append(latex_op + '^{' + sup_val + '}_{' + sub_val + '} ' + base)
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
            acc_chr = ''
            for sub in child:
                sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub.tag
                if sub_tag == 'accPr':
                    for pr in sub:
                        pr_tag = pr.tag.split('}')[1] if '}' in pr.tag else pr.tag
                        if pr_tag == 'chr':
                            acc_chr = pr.get(qn('m:val'), '')
                elif sub_tag == 'e':
                    content = omml_to_latex(sub, depth+1)
                    if acc_chr == '̄':
                        result.append('\\overline{' + content + '}')
                    elif acc_chr == '⃗':
                        result.append('\\vec{' + content + '}')
                    elif acc_chr == '̇':
                        result.append('\\dot{' + content + '}')
                    elif acc_chr == '̈':
                        result.append('\\ddot{' + content + '}')
                    elif acc_chr == '̂':
                        result.append('\\hat{' + content + '}')
                    elif acc_chr == '̌':
                        result.append('\\check{' + content + '}')
                    elif acc_chr == '̃':
                        result.append('\\tilde{' + content + '}')
                    else:
                        result.append('\\overline{' + content + '}')
        elif tag_local == 'bar':
            bar_pos = 'bot'
            content = ''
            for sub in child:
                sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub.tag
                if sub_tag == 'barPr':
                    for pr in sub:
                        pr_tag = pr.tag.split('}')[1] if '}' in pr.tag else pr.tag
                        if pr_tag == 'pos':
                            bar_pos = pr.get(qn('m:val'), 'bot')
                elif sub_tag == 'e':
                    content = omml_to_latex(sub, depth+1)
            
            if bar_pos == 'top':
                result.append('\\overline{' + content + '}')
            else:
                result.append('\\underline{' + content + '}')
        elif tag_local == 'borderBox':
            content = ''
            for sub in child:
                sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub.tag
                if sub_tag == 'e':
                    content = omml_to_latex(sub, depth+1)
            result.append('\\boxed{' + content + '}')
        elif tag_local == 'groupChr':
            chr_val = '⏞'
            pos = 'bot'
            content = ''
            for sub in child:
                sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub.tag
                if sub_tag == 'groupChrPr':
                    for pr in sub:
                        pr_tag = pr.tag.split('}')[1] if '}' in pr.tag else pr.tag
                        if pr_tag == 'chr':
                            chr_val = pr.get(qn('m:val'), '⏞')
                        elif pr_tag == 'pos':
                            pos = pr.get(qn('m:val'), 'bot')
                elif sub_tag == 'e':
                    content = omml_to_latex(sub, depth+1)
            
            if chr_val == '⏞':
                if pos == 'top':
                    result.append('\\overbrace{' + content + '}')
                else:
                    result.append('\\underbrace{' + content + '}')
            elif chr_val == '⏴':
                if pos == 'top':
                    result.append('\\overbrace{' + content + '}')
                else:
                    result.append('\\underbrace{' + content + '}')
            else:
                result.append(content)
        elif tag_local == 'eqArr':
            eqs = []
            for sub in child:
                sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub.tag
                if sub_tag == 'e':
                    eqs.append(omml_to_latex(sub, depth+1))
            result.append(' = '.join(eqs))
        elif tag_local == 'phant':
            pass
        elif tag_local == 'sp':
            for sub in child:
                sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub.tag
                if sub_tag == 'spPr':
                    for pr in sub:
                        pr_tag = pr.tag.split('}')[1] if '}' in pr.tag else pr.tag
                        if pr_tag == 'spc':
                            spc_val = pr.get(qn('m:val'), '0')
                            try:
                                spc = int(spc_val)
                                result.append(' ' * spc)
                            except:
                                pass
        elif tag_local == 'ctrl':
            pass
        else:
            result.append(omml_to_latex(child, depth+1))
    
    return ''.join(result)

def extract_text_from_element(elem, hyperlink_targets=None, bookmark_names=None):
    if hyperlink_targets is None:
        hyperlink_targets = {}
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
        elif tag_local == 'sym':
            char = child.get(qn('w:char'))
            if char:
                try:
                    result.append(chr(int(char, 16)))
                except:
                    result.append(char)
        elif tag_local == 'hyperlink':
            hyperlink_text = extract_text_from_element(child, hyperlink_targets, bookmark_names)
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
            result.append(extract_text_from_element(child, hyperlink_targets, bookmark_names))
    
    return ''.join(result)

def parse_docx_full(docx_path):
    hyperlink_targets = {}
    bookmark_names = {}
    
    with zipfile.ZipFile(docx_path, 'r') as z:
        try:
            with z.open('word/_rels/document.xml.rels') as f:
                rels_tree = ET.parse(f)
                rels_root = rels_tree.getroot()
                for rel in rels_root.iter():
                    if 'Relationship' in rel.tag:
                        rel_id = rel.get('Id')
                        target = rel.get('Target')
                        if rel_id and target:
                            hyperlink_targets[rel_id] = target
        except Exception as e:
            print(f"Warning: Could not parse relationships: {e}")
        
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
            
            print(f"Found {len(bookmark_names)} bookmarks")
            
            body = None
            for child in root:
                tag_local = child.tag.split('}')[1] if '}' in child.tag else child.tag
                if tag_local == 'body':
                    body = child
                    break
            
            if body is None:
                body = root
            
            elements = []
            
            def get_style_val(pPr):
                if pPr is None:
                    return None
                for child in pPr:
                    tag_local = child.tag.split('}')[1] if '}' in child.tag else child.tag
                    if tag_local == 'pStyle':
                        return child.get(qn('w:val'))
                return None
            
            def is_heading_paragraph(p_elem):
                pPr = None
                for child in p_elem:
                    tag_local = child.tag.split('}')[1] if '}' in child.tag else child.tag
                    if tag_local == 'pPr':
                        pPr = child
                        break
                
                style_val = get_style_val(pPr)
                if style_val:
                    style_lower = style_val.lower()
                    if 'heading' in style_lower or style_lower.startswith('heading'):
                        for i in range(1, 10):
                            if str(i) in style_val:
                                return i
                    if '标题' in style_val:
                        for i in range(1, 10):
                            if str(i) in style_val:
                                return i
                return None
            
            def process_paragraph(p_elem):
                heading_level = is_heading_paragraph(p_elem)
                text = extract_text_from_element(p_elem, hyperlink_targets, bookmark_names)
                
                if heading_level:
                    return {
                        'type': 'heading',
                        'level': heading_level,
                        'text': text,
                        'content': text
                    }
                elif text.strip():
                    return {
                        'type': 'paragraph',
                        'content': text
                    }
                return None
            
            def process_textbox_content(txbxContent):
                textbox_paras = []
                for child in txbxContent:
                    tag_local = child.tag.split('}')[1] if '}' in child.tag else child.tag
                    if tag_local == 'p':
                        para_text = extract_text_from_element(child, hyperlink_targets, bookmark_names)
                        if para_text.strip():
                            textbox_paras.append(para_text)
                
                if textbox_paras:
                    return {
                        'type': 'textbox',
                        'content': '\n'.join(textbox_paras)
                    }
                return None
            
            def find_textboxes_in_element(elem):
                textboxes = []
                for child in elem.iter():
                    tag_local = child.tag.split('}')[1] if '}' in child.tag else child.tag
                    if tag_local == 'txbxContent':
                        textbox = process_textbox_content(child)
                        if textbox:
                            textboxes.append((child, textbox))
                return textboxes
            
            all_textboxes = find_textboxes_in_element(body)
            textbox_elements = set()
            for txbx, _ in all_textboxes:
                textbox_elements.add(txbx)
            
            print(f"Found {len(all_textboxes)} textboxes")
            
            def process_body_element(elem, processed_textboxes):
                tag_local = elem.tag.split('}')[1] if '}' in elem.tag else elem.tag
                
                if tag_local == 'p':
                    result = process_paragraph(elem)
                    if result:
                        elements.append(result)
                elif tag_local == 'tbl':
                    pass
                else:
                    for child in elem:
                        child_tag = child.tag.split('}')[1] if '}' in child.tag else child.tag
                        if child_tag == 'p':
                            result = process_paragraph(child)
                            if result:
                                elements.append(result)
                        elif child_tag == 'tbl':
                            pass
            
            for txbx, textbox_data in all_textboxes:
                elements.append(textbox_data)
            
            for child in body:
                process_body_element(child, textbox_elements)
            
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
    invalid_chars = r'[<>:"/\\|?*]'
    name = re.sub(invalid_chars, '_', name)
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
        while filepath in created_files:
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
    elements, bookmark_names = parse_docx_full(DOCX_PATH)
    
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
