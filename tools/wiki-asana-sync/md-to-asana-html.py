#!/usr/bin/env python3
"""
Convert a markdown wiki article to Asana-compatible HTML.
Strips YAML frontmatter, AGENT_CONTEXT blocks, and converts
markdown formatting to the limited HTML subset Asana supports.

Usage: python3 md-to-asana-html.py <path-to-markdown-file>
Output: Asana HTML to stdout
"""

import sys
import re


def strip_frontmatter(text):
    """Remove YAML frontmatter (--- ... ---)"""
    if text.startswith('---'):
        end = text.find('---', 3)
        if end != -1:
            return text[end + 3:].lstrip('\n')
    return text


def strip_agent_context(text):
    """Remove <!-- AGENT_CONTEXT ... --> blocks"""
    return re.sub(r'<!--\s*AGENT_CONTEXT.*?-->', '', text, flags=re.DOTALL)


def convert_table_to_list(text):
    """Convert markdown tables to Asana-compatible lists"""
    lines = text.split('\n')
    result = []
    in_table = False
    table_headers = []
    
    for line in lines:
        stripped = line.strip()
        if '|' in stripped and stripped.startswith('|') and stripped.endswith('|'):
            cells = [c.strip() for c in stripped.split('|')[1:-1]]
            if all(set(c) <= set('- :') for c in cells):
                # Separator row — skip
                continue
            if not in_table:
                # First row = headers
                table_headers = cells
                in_table = True
                continue
            # Data row — format as list item
            parts = []
            for i, cell in enumerate(cells):
                if cell and i < len(table_headers) and table_headers[i]:
                    parts.append(f"{table_headers[i]}: {cell}")
                elif cell:
                    parts.append(cell)
            if parts:
                result.append(f"- {' | '.join(parts)}")
        else:
            if in_table:
                in_table = False
                table_headers = []
            result.append(line)
    
    return '\n'.join(result)


def md_to_asana_html(md_text):
    """Convert markdown to Asana-compatible HTML"""
    # Strip frontmatter and agent context
    text = strip_frontmatter(md_text)
    text = strip_agent_context(text)
    
    # Convert tables to lists before other processing
    text = convert_table_to_list(text)
    
    lines = text.split('\n')
    html_lines = []
    in_list = False
    list_type = None  # 'ul' or 'ol'
    
    for line in lines:
        stripped = line.strip()
        
        # Skip empty lines (but close lists)
        if not stripped:
            if in_list:
                html_lines.append(f'</{list_type}>')
                in_list = False
                list_type = None
            html_lines.append('')
            continue
        
        # Skip horizontal rules
        if stripped in ('---', '***', '___'):
            continue
        
        # Headers → bold
        if stripped.startswith('# '):
            if in_list:
                html_lines.append(f'</{list_type}>')
                in_list = False
            header = stripped[2:].strip()
            html_lines.append(f'<strong>{header}</strong>')
            continue
        if stripped.startswith('## '):
            if in_list:
                html_lines.append(f'</{list_type}>')
                in_list = False
            header = stripped[3:].strip()
            html_lines.append(f'<strong>{header}</strong>')
            continue
        if stripped.startswith('### '):
            if in_list:
                html_lines.append(f'</{list_type}>')
                in_list = False
            header = stripped[4:].strip()
            html_lines.append(f'<strong>{header}</strong>')
            continue
        
        # Unordered list items
        if stripped.startswith('- ') or stripped.startswith('* '):
            if not in_list or list_type != 'ul':
                if in_list:
                    html_lines.append(f'</{list_type}>')
                html_lines.append('<ul>')
                in_list = True
                list_type = 'ul'
            item = stripped[2:]
            item = convert_inline(item)
            html_lines.append(f'<li>{item}</li>')
            continue
        
        # Ordered list items
        ol_match = re.match(r'^(\d+)\.\s+(.+)', stripped)
        if ol_match:
            if not in_list or list_type != 'ol':
                if in_list:
                    html_lines.append(f'</{list_type}>')
                html_lines.append('<ol>')
                in_list = True
                list_type = 'ol'
            item = ol_match.group(2)
            item = convert_inline(item)
            html_lines.append(f'<li>{item}</li>')
            continue
        
        # Blockquotes → italic
        if stripped.startswith('> '):
            if in_list:
                html_lines.append(f'</{list_type}>')
                in_list = False
            content = stripped[2:]
            content = convert_inline(content)
            html_lines.append(f'<em>{content}</em>')
            continue
        
        # Regular paragraph
        if in_list:
            html_lines.append(f'</{list_type}>')
            in_list = False
        para = convert_inline(stripped)
        html_lines.append(para)
    
    # Close any open list
    if in_list:
        html_lines.append(f'</{list_type}>')
    
    # Wrap in body tags
    content = '\n'.join(html_lines).strip()
    return f'<body>\n{content}\n</body>'


def convert_inline(text):
    """Convert inline markdown to HTML"""
    # Bold: **text** → <strong>text</strong>
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic: *text* → <em>text</em>  (but not inside URLs)
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', text)
    # Code: `text` → <code>text</code>
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # Links: [text](url) → <a href="url">text</a>
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    # Strikethrough: ~~text~~ → <s>text</s>
    text = re.sub(r'~~(.+?)~~', r'<s>\1</s>', text)
    return text


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 md-to-asana-html.py <path-to-markdown-file>")
        sys.exit(1)
    
    with open(sys.argv[1], 'r') as f:
        md_text = f.read()
    
    html = md_to_asana_html(md_text)
    print(html)
