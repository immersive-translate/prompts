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
# additional allowed runtime markers
RUNTIME_MARKERS = {'title_prompt', 'summary_prompt', 'terms_prompt', 'normal_result_yaml_example', 'yaml'}


def extract_placeholders(s: str):
    return re.findall(r"\{\{\s*([^}\s]+)\s*\}\}", s)


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

            # placeholder consistency: warn if prompt contains placeholders not known in env or runtime markers
            phs = extract_placeholders(val)
            for ph in phs:
                # literal placeholders like 'imt_source_field' or runtime markers
                if ph in RUNTIME_MARKERS:
                    continue
                if ph in data.get('env', {}):
                    continue
                # allow common tokens 'to', 'id' etc.
                if ph in ('to', 'id'):
                    continue
                print(f"[WARN] {p}: {field} contains unknown placeholder '{{{{{ph}}}}}' — ensure it's supported or present in env")

    # STRICTER: ensure main prompts include at least one input placeholder (imt_source_field or yaml or to)
    main_prompt = None
    for key in ('systemPrompt', 'multiplePrompt'):
        if key in data and isinstance(data.get(key), str):
            main_prompt = data.get(key)
            break
    if main_prompt:
        if ('{{imt_source_field}}' not in main_prompt) and ('{{yaml}}' not in main_prompt) and ('{{to}}' not in main_prompt):
            print(f"[WARN] {p}: main prompt ({'systemPrompt' if 'systemPrompt' in data else 'multiplePrompt'}) should include at least one input placeholder ({{imt_source_field}} or {{yaml}} or {{to}})")

    # Ensure env templates contain expected tokens
    if isinstance(env, dict):
        yaml_item = env.get('imt_yaml_item')
        sub_yaml_item = env.get('imt_subtitle_yaml_item')
        # require {{id}} and {{imt_source_field}} in imt_yaml_item
        if isinstance(yaml_item, str):
            if '{{id}}' not in yaml_item or '{{imt_source_field}}' not in yaml_item:
                fail(f"[ERROR] {p}: env.imt_yaml_item must contain '{{id}}' and '{{imt_source_field}}'")
                ok = False
        else:
            fail(f"[ERROR] {p}: env.imt_yaml_item missing or not a string")
            ok = False

        # require {{id}} and {{imt_sub_source_field}} in imt_subtitle_yaml_item
        if isinstance(sub_yaml_item, str):
            if '{{id}}' not in sub_yaml_item or '{{imt_sub_source_field}}' not in sub_yaml_item:
                fail(f"[ERROR] {p}: env.imt_subtitle_yaml_item must contain '{{id}}' and '{{imt_sub_source_field}}'")
                ok = False
        else:
            fail(f"[ERROR] {p}: env.imt_subtitle_yaml_item missing or not a string")
            ok = False

    # i18n name/description non-empty
    if isinstance(i18n, dict):
        for loc, mapping in i18n.items():
            if isinstance(mapping, dict):
                if not mapping.get('name'):
                    print(f"[WARN] {p}: i18n.{loc}.name is empty")
                if not mapping.get('description'):
                    print(f"[WARN] {p}: i18n.{loc}.description is empty")

    # enableRichTranslate should be boolean if present
    ert = data.get('enableRichTranslate')
    if ert is not None and not isinstance(ert, bool):
        print(f"[WARN] {p}: enableRichTranslate is not boolean: {ert}")

    # priority if present should be integer
    prio = data.get('priority')
    if prio is not None and not isinstance(prio, int):
        print(f"[WARN] {p}: priority should be integer, got: {prio}")

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
