#!/usr/bin/env python3
"""Apply safe, minimal fixes to plugin YAML files.

Fixes performed:
- If env.imt_subtitle_yaml_item is missing, add a template using imt_sub_source_field or 'source'.
- Replace '{{text}}' in prompts with '{{imt_source_field}}'.
- If env.imt_yaml_item doesn't contain '{{id}}' or '{{imt_source_field}}', replace with a standard template.

This script writes files in-place and prints a summary. Run with care and review changes.
"""
from pathlib import Path
import yaml
import sys

ROOT = Path(__file__).resolve().parents[1]
PLUGINS = ROOT / 'plugins'

def read_yaml_block(text: str):
    if text.lstrip().startswith('```'):
        parts = text.split('```')
        if len(parts) >= 2:
            return parts[1]
    return text

def write_yaml_block(orig_text: str, new_yaml: str):
    if orig_text.lstrip().startswith('```'):
        parts = orig_text.split('```')
        # keep fences and language marker
        prefix = parts[0]
        fence_lang = parts[1][:parts[1].find('\n')].strip()
        return f"```{fence_lang}\n{new_yaml}\n```"
    return new_yaml

def process_file(p: Path):
    text = p.read_text(encoding='utf-8')
    inner = read_yaml_block(text)
    try:
        data = yaml.safe_load(inner)
    except Exception as e:
        print(f"skip {p}: parse error: {e}")
        return False
    changed = False
    env = data.get('env') or {}
    # ensure imt_subtitle_yaml_item exists
    if 'imt_subtitle_yaml_item' not in env:
        sub_src = env.get('imt_sub_source_field', 'source')
        env['imt_subtitle_yaml_item'] = f"- id: {{id}}\n  {{%s}}: {{text}}" % sub_src
        data['env'] = env
        changed = True

    # ensure imt_yaml_item contains id and source
    yaml_item = env.get('imt_yaml_item')
    if not isinstance(yaml_item, str) or ('{{id}}' not in yaml_item or '{{imt_source_field}}' not in yaml_item):
        env['imt_yaml_item'] = "- id: {{id}}\n  {{imt_source_field}}: {{text}}"
        data['env'] = env
        changed = True

    # replace '{{text}}' in prompt fields with '{{imt_source_field}}'
    for key in ('systemPrompt', 'multiplePrompt', 'prompt', 'subtitlePrompt'):
        val = data.get(key)
        if isinstance(val, str) and '{{text}}' in val:
            data[key] = val.replace('{{text}}', '{{imt_source_field}}')
            changed = True

    if changed:
        new_yaml = yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
        new_text = write_yaml_block(text, new_yaml)
        p.write_text(new_text, encoding='utf-8')
        print(f"fixed: {p}")
        return True
    return False

def main():
    if not PLUGINS.exists():
        print('no plugins dir')
        return 1
    files = sorted(PLUGINS.glob('*.yml'))
    modified = []
    for f in files:
        if process_file(f):
            modified.append(str(f.name))
    if modified:
        print('modified files:')
        for m in modified:
            print('-', m)
    else:
        print('no changes')
    return 0

if __name__ == '__main__':
    sys.exit(main())
