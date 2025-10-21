#!/usr/bin/env python3
"""Simple validator for plugin YAML files in plugins/.

Checks (discoverable from repo patterns):
- YAML parses
- Required top-level keys: id, version, name
- i18n contains zh-CN and zh-TW
- env contains imt_source_field and imt_trans_field and imt_yaml_item

Exit codes: 0 = OK, non-zero = failures (printed to stdout).
"""
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
PLUGINS = ROOT / "plugins"

REQUIRED_TOP = {"id", "version", "name"}
REQUIRED_I18N = {"zh-CN", "zh-TW"}
REQUIRED_ENV_KEYS = {"imt_source_field", "imt_trans_field", "imt_yaml_item"}
REQUIRED_ENV_ADDITIONAL = {"imt_yaml_item", "imt_subtitle_yaml_item"}
import re

# simple semver-like pattern for extensionVersion (e.g. 1.4.10)
EXT_VER_RE = re.compile(r"^\d+\.\d+(?:\.\d+)?$")
# simple URL-ish check for matches entries
URL_LIKE_RE = re.compile(r"^https?://")
# placeholder tokens we expect in prompts (warnings if absent)
COMMON_PLACEHOLDERS = ['{{to}}', '{{imt_source_field}}', '{{imt_trans_field}}', '{{yaml}}']


def fail(msg: str):
    print(msg)
    return None


def check_file(p: Path) -> bool:
    text = p.read_text(encoding="utf-8")
    # Skip non-yaml blocks if file is fenced (some files in repo are wrapped in ```yaml)
    if text.lstrip().startswith('```'):
        # extract the first fenced code block content (e.g. ```yaml\n...\n```) and parse that
        parts = text.split('```')
        # parts[0] is before first fence, parts[1] is inside first fence
        if len(parts) >= 2:
            text = parts[1]
    try:
        data = yaml.safe_load(text)
    except Exception as e:
        return fail(f"[ERROR] {p}: YAML parse error: {e}")
    if not isinstance(data, dict):
        return fail(f"[ERROR] {p}: top-level YAML is not a mapping")

    ok = True
    # id should match filename (without extension)
    file_stem = p.stem
    file_id = data.get('id')
    if file_id and str(file_id) != file_stem:
        fail(f"[ERROR] {p}: 'id' ({file_id}) does not match filename '{file_stem}'")
        ok = False
    miss = REQUIRED_TOP - data.keys()
    if miss:
        fail(f"[ERROR] {p}: missing required top-level keys: {', '.join(sorted(miss))}")
        ok = False

    i18n = data.get('i18n')
    if not isinstance(i18n, dict):
        fail(f"[ERROR] {p}: missing or invalid 'i18n' mapping")
        ok = False
    else:
        missing_locales = REQUIRED_I18N - i18n.keys()
        if missing_locales:
            fail(f"[ERROR] {p}: i18n missing locales: {', '.join(sorted(missing_locales))}")
            ok = False
        else:
            # ensure each locale has name and description
            for loc, mapping in i18n.items():
                if not isinstance(mapping, dict):
                    fail(f"[ERROR] {p}: i18n.{loc} is not a mapping")
                    ok = False
                else:
                    if 'name' not in mapping or 'description' not in mapping:
                        fail(f"[ERROR] {p}: i18n.{loc} must include 'name' and 'description'")
                        ok = False

    env = data.get('env')
    if not isinstance(env, dict):
        fail(f"[ERROR] {p}: missing or invalid 'env' mapping")
        ok = False
    else:
        missing_env = REQUIRED_ENV_KEYS - env.keys()
        if missing_env:
            fail(f"[ERROR] {p}: env missing keys: {', '.join(sorted(missing_env))}")
            ok = False
        # check additional env keys (yaml item templates)
        missing_env_add = REQUIRED_ENV_ADDITIONAL - env.keys()
        if missing_env_add:
            fail(f"[ERROR] {p}: env missing keys: {', '.join(sorted(missing_env_add))}")
            ok = False

    # Ensure at least one prompt-like field exists
    prompt_fields = [k for k in ('systemPrompt', 'multiplePrompt', 'prompt', 'subtitlePrompt') if k in data]
    if not prompt_fields:
        fail(f"[ERROR] {p}: missing any prompt fields (systemPrompt/multiplePrompt/prompt/subtitlePrompt)")
        ok = False

    # extensionVersion format (if present) should look like X.Y or X.Y.Z
    extver = data.get('extensionVersion')
    if extver and not EXT_VER_RE.match(str(extver)):
        fail(f"[ERROR] {p}: extensionVersion '{extver}' does not match expected pattern X.Y[.Z]")
        ok = False

    # matches entries: if present, should look like http(s) URL patterns
    matches = data.get('matches')
    if matches:
        if not isinstance(matches, list):
            fail(f"[ERROR] {p}: matches must be a list of URL patterns")
            ok = False
        else:
            for m in matches:
                if not isinstance(m, str) or not URL_LIKE_RE.match(m):
                    fail(f"[ERROR] {p}: matches contains non-URL pattern: {m}")
                    ok = False

    # check prompts for common placeholders — warn if missing (does not fail)
    for field in ('systemPrompt', 'multiplePrompt', 'prompt', 'subtitlePrompt'):
        val = data.get(field)
        if isinstance(val, str):
            missing = [ph for ph in COMMON_PLACEHOLDERS if ph not in val]
            if missing:
                print(f"[WARN] {p}: {field} missing placeholders: {', '.join(missing)}")

    return ok


def main():
    if not PLUGINS.exists():
        print("No plugins/ directory found.")
        return 0
    files = sorted(PLUGINS.glob('*.yml'))
    if not files:
        print("No plugin yml files found in plugins/.")
        return 0

    overall = True
    for f in files:
        ok = check_file(f)
        overall = overall and ok

    if not overall:
        print("One or more plugin checks failed.")
        return 2
    print("All plugin checks passed.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
