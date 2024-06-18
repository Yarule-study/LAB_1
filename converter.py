import re
import sys

def is_valid_markdown(text):
    if re.search(r'\*\*.*`.*_.*`.*\*\*', text) or \
       re.search(r'`.*\*\*.*_.*\*\*.*`', text) or \
       re.search(r'_.*\*\*.*`.*\*\*.*_', text):
        return False

    counts = {
        '**': text.count('**'),
        '_': text.count('_'),
        '`': text.count('`'),
        '```': text.count('```')
    }

    return all(count % 2 == 0 for count in counts.values())

def markdown_to_html(markdown_text):
    if not is_valid_markdown(markdown_text):
        print("Error: invalid markdown", file=sys.stderr)
        sys.exit(1)

    preformatted_blocks = re.findall(r'```(.*?)```', markdown_text, re.DOTALL)
    for block in preformatted_blocks:
        html_block = f'<pre>{block}</pre>'
        markdown_text = markdown_text.replace(f'```{block}```', html_block)

    conversions = {
        r'\*\*(.*?)\*\*': r'<b>\1</b>',
        r'_(.*?)_': r'<i>\1</i>',
        r'`(.*?)`': r'<tt>\1</tt>'
    }

    for pattern, replacement in conversions.items():
        markdown_text = re.sub(pattern, replacement, markdown_text)
    
    paragraphs = markdown_text.split('\n\n')
    html_paragraphs = ['<p>{}</p>'.format(p.replace('\n', ' ')) for p in paragraphs]
    html_text = ''.join(html_paragraphs)

    return html_text
