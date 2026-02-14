## Repo snapshot — what matters for code-writing agents

- This repo holds AI "Expert" prompt plugins under `plugins/`. Each plugin is a single YAML file (e.g. `plugins/github.yml`, `plugins/financial.yml`, `plugins/paragraph-summarizer-expert.yml`) that defines metadata, i18n, `env` variables and prompts (`systemPrompt`, `prompt`, `multiplePrompt`, `subtitlePrompt`).
- The canonical contributor docs are `README.md` and `README-EN.md` at the repo root — use them to validate expected fields and localization requirements.

## High‑level architecture and intent

- Purpose: collection of configurable prompt-plugins used by the Immersive Translate extension/service. The extension loads these YAMLs and uses the values to build requests to underlying LLM backends.
- Key responsibilities of a plugin file:
  - metadata (id, version, name, author)
  - `i18n` object with at least `zh-CN` and `zh-TW` entries
  - `env` mapping defining placeholder names (e.g. `imt_source_field`, `imt_trans_field`)
  - prompt templates: `systemPrompt`, `prompt`, `multiplePrompt`, `subtitlePrompt`

## Concrete patterns agents should use or preserve

- Do NOT change YAML top-level keys. Example canonical keys are visible in `plugins/github.yml` and `plugins/financial.yml` — preserve `id`, `version`, `extensionVersion` (if present), `i18n`, `env`, `systemPrompt`, `multiplePrompt` and `matches` when applicable.
- Keep `i18n` in English + `zh-CN` + `zh-TW`. If you add other locales, follow the same nested structure used in existing files.
- `env` contains formatting snippets used by the service. When editing prompt text, prefer substituting variables (e.g. `{{imt_source_field}}`, `{{imt_trans_field}}`) rather than hardcoding field names.
- When creating or editing prompts, preserve any special markers the service expects: `{{title_prompt}}`, `{{summary_prompt}}`, `{{terms_prompt}}`, `{{yaml}}`, and `{{normal_result_yaml_example}}` — these are referenced by the extension runtime.

## Developer workflows (how to test locally / validate changes)

- There is no build in this repo. Validation is primarily structural and manual: ensure YAML parses and required fields exist.
- Quick checks:
  1. YAML linting (install `yamllint`) and run against changed files.
  2. Compare your plugin fields to `plugins/github.yml` (good reference for required keys).
- Local debug path used by product: open Immersive Translate > Developer Settings > Custom AI Assistant and paste the YAML to validate runtime behavior. (See `README.md` / `README-EN.md` "Local Debugging" section.)

## Integration and runtime assumptions

- The extension/service will substitute `env` variables into prompt templates and send them to the configured LLM. Keep prompts focused and avoid adding interactive instructions that assume human review.
- Numeric fields used by runtime: `maxTextLengthPerRequest`, `maxTextGroupLengthPerRequest`, `maxTextGroupLengthPerRequestForSubtitle` — maintain sensible defaults if adding them.

## Examples and file references (for quick copy/paste)

- Use `plugins/github.yml` for a canonical multi-paragraph prompt, `plugins/financial.yml` for domain-specific rules and numeric handling, and `plugins/paragraph-summarizer-expert.yml` for examples with `maxTextLengthPerRequest` and summary rules.

## Conventions agents must follow when editing/adding files

- Files must be valid YAML and UTF-8 encoded. Keep top-level file extension `.yml`.
- English `name`, `description`, and `details` are the primary metadata; `i18n` must include `zh-CN` and `zh-TW` translations.
- Avoid changing `id` once created. `name` should be unique.
- Keep prompt `systemPrompt` concise and start with a role declaration (e.g. "You are a professional {{to}} native translator...").

## What not to do

- Don't remove `env` entries or rename variable placeholders without updating every template that references them.
- Don't add runtime-only instructions that contradict `README` (e.g., avoid asking the model to respond with extra explanation when existing rules say "Output only the translated content").

## If you need to add tests or CI

- There is no existing test harness. If you add structural checks, place a lightweight `yamllint` or `python` script under `.github/workflows/` or `scripts/` and document it in the README.

---

If anything in this guide is unclear or you want the instructions to include more examples (e.g. a minimal YAML template or a small validation script), tell me which examples you'd like and I will iterate.
