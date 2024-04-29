# AI 专家插件提交指南

欢迎为我们的仓库贡献 AI 专家相关的插件内容。为了确保您的贡献能够顺利被采纳，请参照我们已有的 AI 专家文件，并按照以下指南准备和提交您的贡献。

## 提交内容要求

请参照如下内容，提交一个包含完整的 yml 文件：

**PS**：关于插件的基础信息我们希望您使用英文进行描述，并在 i18n 配置中添加中文简体和中文繁体相关内容。

```yaml
// 插件的基础信息
id: financial // 一个唯一的标识符，用于标识当前 AI 专家
version: 1.0.0 // 版本号
name: Financial Expert // 名称。这也是唯一的
description: The translation of financial articles becomes more professional. // 描述信息
avatar: https://s.immersivetranslate.com/assets/uploads/fina-AXX5s8.png // 头像，一个可用的图片 URL 地址
details: This expert is designed for professional financial field translation. You can use it to accurately translate financial articles into the target language specified. // AI 专家的详细信息，支持 markdown 和 html 格式
i18n: // 插件信息的多语言描述（包括 name、description、details），建议至少支持 zh-CN、zh-TW
  zh-CN:
    name: 金融专家
    description: 特别为金融领域优化，适合用来翻译财经，金融类文章。
    details: 该专家专为专业金融领域翻译而设计，你可以使用它将金融类文章准确翻译为指定的目标语言。
  zh-TW:
    name: 金融專家
    description: 特別為金融領域優化，適合用來翻譯財經，金融類文章。
    details: 該專家專為專業金融領域翻譯而設計，你可以使用它將金融類文章準確翻譯為指定的目標語言。
author: Official // 作者名称
homepage: https://immersivetranslate.com/ // AI 专家主页，非必填

// 提示词信息
env: 在提示词中使用的占位符，如源文本字段、翻译文本字段、源字幕字段和翻译字幕字段等。这些变量的值将在提示词中被具体文本替换
systemPrompt: 系统级别的提示，描述了 AI 专家的角色和功能
prompt: 关于单句翻译的提示词
multiplePrompt: 关于多句翻译的提示词
subtitlePrompt: 关于字幕翻译的提示词
```

提示词相关信息可参考如下内容，这是一个关于金融领域翻译专家相关的提示词：

```yaml
env:
  imt_source_field: text
  imt_trans_field: text
  imt_sub_source_field: source
  imt_sub_trans_field: translation
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
    Example result:
      - id: 1
        {{imt_trans_field}}: Translation
  subtitle_result_yaml_example: |-
    Example request:
      - id: 1
        {{imt_sub_source_field}}: ...
      - id: 2
        {{imt_sub_source_field}}: ...
    Example response:
      - id: 1
        {{imt_sub_trans_field}}: ...
        {{imt_sub_source_field}}: ...
      - id: 2
        {{imt_sub_trans_field}}: ...
        {{imt_sub_source_field}}: ...

systemPrompt: You are a highly skilled translation engine with expertise in the financial sector. Your function is to translate texts accurately into the target language specified, maintaining the original format, financial terms, market data, and currency abbreviations. Do not add any explanations or annotations to the translated text.

prompt: |-
  Please translate the following text into {{to}}. Retain the original paragraph formatting, financial terms (e.g., ETFs, ROI), currency symbols (e.g., $, €), and market data. Ensure all numerical values are accurately represented. Do not add explanations or annotations:

  {{text}}

multiplePrompt: |-
  Translate all instances of text in the financial sector within the YAML-formatted document below into {{to}}. Insert the translation in the corresponding {{imt_trans_field}} for each entry. Ensure financial terms, currency symbols, and market data are accurately translated and retain their original formatting. Do not include explanations or annotations.

  Example format:
  {{normal_result_yaml_example}}

  Start translation:

  {{yaml}}

subtitlePrompt: |-
  Translate all subtitle text fields ({{imt_sub_source_field}}) in the YAML-formatted video subtitles below into {{to}}, and fill in the translated text in the corresponding {{imt_sub_trans_field}}. Ensure you maintain the original formatting, accurately translate financial terms, currency symbols, and market data, and do not add explanations or annotations. The output must be in a valid YAML format that retains both the source and translated fields.

  Example format:
  {{subtitle_result_yaml_example}}

  Begin translation:

  {{yaml}}
```

## 如何提交

请按照以下步骤提交您的AI专家插件：

1. **Fork 仓库**

在进行贡献之前，您需要先 fork 我们的仓库到您自己的 GitHub 账户下。

2. **创建新分支**

在您的 fork 中，创建一个新的分支来放置您的贡献内容。建议以插件名称为分支名称。

3. **添加您的插件内容**

在新的分支中，按照上述“提交内容要求”添加您的AI专家插件内容并放在一个 ***yml*** 文件内。请确保您的内容是新颖的，且不与仓库中现有的内容重复。

4. **撰写提交信息**

提交您的更改时，请提供清晰、准确的提交信息，说明您所做的更改和新增的功能。

5. **发起Pull Request (PR)**

在确保所有的更改都已提交之后，向原仓库发起 PR。请在 PR 的描述中详细说明您的插件的功能和用途，并提及任何特殊的依赖或注意事项。

6. **等待反馈**

仓库管理员会审查您的 PR。如果需要进一步的信息或者更改，管理员会在 PR 中评论。

7. **完成合并**

一旦您的 PR 被接受并合并，您的 AI 专家插件就会成为仓库的一部分了！

## 注意事项

* 确保您的内容遵守所有适用的版权法规。

* 提交的内容必须是原创的，或者您有权利将其贡献给我们的仓库。

* 不接受含有任何恶意代码、不适内容或侵犯他人权益的贡献。

## 结语

我们期待着您的贡献，感谢您为 AI 专家生态系统的发展做出的贡献！
