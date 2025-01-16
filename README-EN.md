# Immersive Translate AI Expert Plugin Submission Guide

Customized AI translation strategies can greatly improve translation quality. Immersive Translate refers to these strategies as "AI Experts" — essentially, a series of carefully designed prompts.

## How to Use "AI Experts" in Immersive Translate?

Open the Immersive Translate settings page, find the "AI Experts" Tab, and install the required "AI Expert." Then, you can easily select different AI Experts in the Immersive Translate plugin panel to meet diverse translation needs. The default translation strategy is "General," suitable for most scenarios.

## How to Contribute "AI Experts"?

We welcome more contributions to [Immersive Translate](https://immersivetranslate.com/) [AI Translation Experts](https://ai.immersivetranslate.com/).

If you do not yet have the ability to write Prompts files, you can initiate an Issue discussion [here](https://github.com/immersive-translate/prompts/issues), describing the AI Expert you want.

If you can write Prompts, you can directly initiate a Pull Request to submit or improve an AI Expert.

To ensure your contribution is smoothly adopted, please refer to our existing AI Expert files under the `plugins/` folder.

## Local Debugging

You can find the 【[Developer Settings](https://dash.immersivetranslate.com/#developer)】 on the Immersive Translate settings page, find 【Custom AI Assistant】, and edit in yaml format there. Please refer to the following for the specific format.

## About Context Variables env

- imt_domain: Web domain
- imt_title: Web title

## AI Expert Configuration File Standards

> You should describe the plugin's basic information in English and include at least Simplified Chinese and Traditional Chinese descriptions in the i18n configuration.

```yaml
// Basic information of the plugin
id: custom // A unique identifier to identify the current AI Expert
version: 1.0.0 // Version number
name: Financial Expert // Name. This is also unique
description: The translation of financial articles becomes more professional. // Description
avatar: https://s.immersivetranslate.com/assets/uploads/fina-AXX5s8.png // Avatar, a usable image URL address
details: This expert is designed for professional financial field translation. You can use it to accurately translate financial articles into the target language specified. // Detailed information about the AI Expert, supports markdown and html format
i18n: // Multilingual description of the plugin information (including name, description, details), at least supports zh-CN, zh-TW
  zh-CN:
    name: 金融专家
    description: 特别为金融领域优化，适合用来翻译财经，金融类文章。
    details: 该专家专为专业金融领域翻译而设计，你可以使用它将金融类文章准确翻译为指定的目标语言。
  zh-TW:
    name: 金融專家
    description: 特別為金融領域優化，適合用來翻譯財經，金融類文章。
    details: 該專家專為專業金融領域翻譯而設計，你可以使用它將金融類文章準確翻譯為指定的目標語言。
author: Official // Author name
homepage: https://immersivetranslate.com/ // AI Expert homepage, not required

// Prompt information
env: Placeholders used in prompts, such as source text field, translation text field, source subtitle field, and translation subtitle field, etc. The values of these variables will be replaced by specific text in the prompts
systemPrompt: System-level prompt, describes the role and function of the AI Expert
prompt: Prompt for single sentence translation
multiplePrompt: Prompt for multiple segment translation, to preserve more context, Immersive Translate by default includes 3 segments of text per request, the request will be provided in this format.
subtitlePrompt: Prompt for subtitle translation (subtitles often have multiple sentence segmentation issues, so we set a separate prompt for subtitles)
```

For reference, here is a prompt about two-step paraphrasing (first literal translation, then paraphrasing):

```yaml
id: custom
version: 1.0.1
extensionVersion: 1.4.10
name: Paraphrase Expert
description: Designed for nuanced, interpretive translations, this expert ensures that translations go beyond the literal to capture the essence and tone of the original text.
avatar: https://s.immersivetranslate.com/assets/uploads/fluent-7JVve6.png
author: Official
homepage: https://immersivetranslate.com/
details: |-
  This expert specializes in interpretive translations, aiming to capture not just the words but the meaning and tone behind them. It's perfect for literature, idiomatic expressions, and any text where context matters as much as content. Use this expert to convey the essence of the original text in the target language, ensuring that cultural nuances and implied meanings are not lost in translation.
i18n:
  zh-CN:
    name: 意译大师
    description: 专门设计用于富有细腻差异和意译的翻译，经过先直译，再意译的步骤，确保翻译超越字面，捕捉原文的精髓和语调。
    details: |-
      该专家专注于意译翻译，旨在捕捉不仅仅是文字，而是背后的意义和语调。它非常适合文学、成语表达以及任何上下文和内容同等重要的文本。使用此专家可以确保在目标语言中传达原文的精髓，确保文化细微差别和隐含意义不会在翻译中丢失。
  zh-TW:
    name: 意譯專家
    description: 專門設計用於豐富細膩差異和意譯的翻譯，經過先直譯，再意譯的步驟，確保翻譯超越字面，捕捉原文的精髓和語調。
    details: |-
      該專家專注於意譯翻譯，旨在捕捉不僅僅是文字，而是背後的意義和語調。它非常適合文學、成語表達以及任何上下文和內容同等重要的文本。使用此專家可以確保在目標語言中傳達原文的精髓，確保文化細膩差別和隱含意義不會在翻譯中丟失。
env:
  imt_source_field: source
  imt_trans_field: step2
  imt_sub_source_field: source
  imt_sub_trans_field: step2
  imt_yaml_item: |-
    - id: {{id}}
      {{imt_source_field}}: {{text}}
  imt_subtitle_yaml_item: |-
    - id: {{id}}
      {{imt_sub_source_field}}: {{text}}
  normal_result_yaml_example: |-
    Example request:
      - id: 1
        {{imt_source_field}}: Source
    Example response:
      - id: 1
        step1: Literal translation result
        step2: Paraphrase result
  subtitle_result_yaml_example: |-
    Example request:
      - id: 1
        {{imt_sub_source_field}}: ...
      - id: 2
        {{imt_sub_source_field}}: ...
    Example response:
      - id: 1
        step1: Literal translation result
        step2: Paraphrase result
        {{imt_sub_source_field}}: ...
      - id: 2
        step1: Literal translation result
        step2: Paraphrase result
        {{imt_sub_source_field}}: ...
  normal_result_yaml_example_traditional: |-
    Example request:
      - id: 1
        {{imt_source_field}}: Source
    Example result:
      - id: 1
        step1: Literal translation result
        step2: Paraphrase result
  subtitle_result_yaml_example_traditional: |-
    Example request:
      - id: 1
        {{imt_sub_source_field}}: ...
      - id: 2
        {{imt_sub_source_field}}: ...
    Example response:
      - id: 1
        step1: Literal translation result
        step2: Paraphrase result
        {{imt_sub_source_field}}: ...
      - id: 2
        step1: Literal translation result
        step2: Paraphrase result
        {{imt_sub_source_field}}: ...
systemPrompt: You are a professional translator proficient in {{to}}, responsible for translating it into Chinese without any explanation.
prompt: |-
  Please complete the translation task according to the following requirements: 
  1. Directly translate the {{imt_source_field}} field in the YAML object below into {{to}}, retaining specific terms or media names (if any). Place the result of this translation into the step1 field of the YAML array. 
  2: Based on the result of the first translation, perform a paraphrase, striving for faithfulness, expressiveness, and elegance, but still retaining specific terms or media names (if any), making the text more understandable and in line with Chinese expression habits under the premise of adhering to the original meaning. Place the result of the second translation into the step2 field of the YAML array. 

  Example format:
  {{normal_result_yaml_example}}

  Start translating:

  {{yaml}}

multiplePrompt: |-
  Please complete the translation task according to the following requirements: 
  1. Directly translate the {{imt_source_field}} field in the YAML object below into {{to}}, retaining specific terms or media names (if any). Place the result of this translation into the step1 field of the YAML array. 
  2: Based on the result of the first translation, perform a paraphrase, striving for faithfulness, expressiveness, and elegance, but still retaining specific terms or media names (if any), making the text more understandable and in line with Chinese expression habits under the premise of adhering to the original meaning. Place the result of the second translation into the step2 field of the YAML array. 

  Example format:
  {{normal_result_yaml_example}}

  Start translating:

  {{yaml}}

subtitlePrompt: |-
  Translate all the text in the {{imt_sub_source_field}} fields of the YAML format video subtitles below into {{to}}, and write the translation result in the {{imt_sub_trans_field}} field. You must complete every {{imt_sub_trans_field}} field, retaining every {{imt_sub_source_field}} field. The requirements are as follows:

  1. First, directly translate the content of the {{imt_sub_source_field}} field, placing the result of this translation into the step1 field of the YAML array.
  2. Based on the result of the first translation, perform a paraphrase, striving for faithfulness, expressiveness, and elegance, but still retaining specific terms or media names (if any), making the text more understandable and in line with Chinese expression habits under the premise of adhering to the original meaning. Place the result of the second translation into the step2 field of the YAML array. 

  {{subtitle_result_yaml_example}}

  Start translating:

  {{yaml}}

langOverrides:
  - id: auto2zh-TW
    systemPrompt: You are a professional translator proficient in Traditional Chinese, responsible for translating it into Chinese without any explanation.
    prompt: |-
      Please complete the translation task according to the following requirements: 
      1. Directly translate the {{imt_source_field}} field in the YAML object below into {{to}}, retaining specific terms or media names (if any). Place the result of this translation into the step1 field of the YAML array. 
      2: Based on the result of the first translation, perform a paraphrase, striving for faithfulness, expressiveness, and elegance, but still retaining specific terms or media names (if any), making the text more understandable and in line with Chinese expression habits under the premise of adhering to the original meaning. Place the result of the second translation into the step2 field of the YAML array. 

      Example format:
      {{normal_result_yaml_example_traditional}}

      Start translating:

      {{yaml}}

    multiplePrompt: |-
      Please complete the translation task according to the following requirements: 
      1. Directly translate the {{imt_source_field}} field in the YAML object below into {{to}}, retaining specific terms or media names (if any). Place the result of this translation into the step1 field of the YAML array. 
      2: Based on the result of the first translation, perform a paraphrase, striving for faithfulness, expressiveness, and elegance, but still retaining specific terms or media names (if any), making the text more understandable and in line with Chinese expression habits under the premise of adhering to the original meaning. Place the result of the second translation into the step2 field of the YAML array. 

      Example format:
      {{normal_result_yaml_example_traditional}}

      Start translating:

      {{yaml}}

    subtitlePrompt: |-
      Translate all the text in the {{imt_sub_source_field}} fields of the YAML format video subtitles below into {{to}}, and write the translation result in the {{imt_sub_trans_field}} field. You must complete every {{imt_sub_trans_field}} field, retaining every {{imt_sub_source_field}} field. The requirements are as follows:

      1. First, directly translate the content of the {{imt_sub_source_field}} field, placing the result of this translation into the step1 field of the YAML array.
      2. Based on the result of the first translation, perform a paraphrase, striving for faithfulness, expressiveness, and elegance, but still retaining specific terms or media names (if any), making the text more understandable and in line with Chinese expression habits under the premise of adhering to the original meaning. Place the result of the second translation into the step2 field of the YAML array. 

      Example format:
      {{subtitle_result_yaml_example_traditional}}

      Start translating:

      {{yaml}}
```

## How to Submit

Please follow the steps below to submit your AI Expert plugin:

1. **Fork the Repository**

Before contributing, you need to fork our repository to your own GitHub account.

2. **Create a New Branch**

In your fork, create a new branch to place your contribution. It is recommended to name the branch after the plugin name.

3. **Add Your Plugin Content**

In the new branch, add your AI Expert plugin content according to the "Submission Content Requirements" mentioned above and place it in a **_yml_** file. Please ensure your content is novel and does not duplicate the existing content in the repository.

4. **Write a Commit Message**

When submitting your changes, provide a clear and accurate commit message explaining the changes and new features you have made.

5. **Initiate a Pull Request (PR)**

After ensuring all changes have been submitted, initiate a PR to the original repository. Please describe the functionality and purpose of your plugin in detail in the PR description, and mention any special dependencies or considerations.

6. **Wait for Feedback**

The repository administrators will review your PR. If further information or changes are needed, the administrators will comment in the PR.

7. **Completion of Merging**

Once your PR is accepted and merged, your AI Expert plugin will become part of the repository!

## Considerations

- Ensure your content complies with all applicable copyright laws.

- The content submitted must be original, or you must have the right to contribute it to our repository.

- Contributions containing any malicious code, inappropriate content, or infringing on others' rights are not accepted.

## Conclusion

We look forward to your contributions and thank you for contributing to the development of the AI Expert ecosystem!
