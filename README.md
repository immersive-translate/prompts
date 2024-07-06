# 沉浸式翻译 AI 专家插件提交指南

通过定制化 AI 翻译策略可以极大地提高翻译质量。沉浸式翻译将这些策略称为 “AI专家” ——本质上是一系列精心设计的提示词。

## 如何在沉浸式翻译中使用【AI专家】？

打开沉浸式翻译设置页面，找到【AI专家】Tab，安装需要的“AI专家”后，即可在沉浸式翻译插件的面板中轻松选择不同的AI专家，满足多样化的翻译需求，默认的翻译策略是【通用】, 适合大多数场景。

## 如何贡献【AI专家】？

欢迎为 [沉浸式翻译](https://immersivetranslate.com/) 贡献更多 [AI 翻译专家](https://ai.immersivetranslate.com/)。

如果您还不具备编写 Prompts 文件的能力，您可以 [在此](https://github.com/immersive-translate/prompts/issues) 发起一个 Issue 讨论，描述您想要的 AI 专家。

如果您可以编写 Prompts，您可以直接发起一个 Pull Request 来提交或者改进其中某个 AI 专家。

为了确保您的贡献能够顺利被采纳，请参照我们已有的 AI 专家文件`plugins/`文件夹下。


## 本地调试

您可以在沉浸式翻译设置页面找到【[开发者设置](https://dash.immersivetranslate.com/#developer)】，找到【Custom AI Assistant】，在里面编辑 yaml 格式即可，具体格式请参考下文。

## 关于上下文变量 env
- imt_domain: 网页域名
- imt_title: 网页标题

## AI 专家配置文件规范


> 您应该用英文描述插件的基础信息，并在 i18n 配置中至少添加简体中文和繁体中文的描述。

```yaml
// 插件的基础信息
id: custom // 一个唯一的标识符，用于标识当前 AI 专家
version: 1.0.0 // 版本号
name: Financial Expert // 名称。这也是唯一的
description: The translation of financial articles becomes more professional. // 描述信息
avatar: https://s.immersivetranslate.com/assets/uploads/fina-AXX5s8.png // 头像，一个可用的图片 URL 地址
details: This expert is designed for professional financial field translation. You can use it to accurately translate financial articles into the target language specified. // AI 专家的详细信息，支持 markdown 和 html 格式
i18n: // 插件信息的多语言描述（包括 name、description、details），至少支持 zh-CN、zh-TW
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
prompt: 单句翻译的提示词
multiplePrompt: 多段翻译的提示词，为了保存更多的上下文，沉浸式翻译默认每次请求会包含 3 段文本，请求会按照这个格式提供。
subtitlePrompt: 字幕翻译的提示词(字幕经常会有多句断句的问题，所以我们单独为字幕设置了提示词)
```

提示词相关信息可参考如下内容，这是一个关于两步意译(先直译，再意译)的提示词：

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
    示例请求:
      - id: 1
        {{imt_source_field}}: Source
    示例结果:
      - id: 1
        step1: 直译结果
        step2: 意译结果
  subtitle_result_yaml_example: |-
    Example request:
      - id: 1
        {{imt_sub_source_field}}: ...
      - id: 2
        {{imt_sub_source_field}}: ...
    Example response:
      - id: 1
        step1: 直译结果
        step2: 意译结果
        {{imt_sub_source_field}}: ...
      - id: 2
        step1: 直译结果
        step2: 意译结果
        {{imt_sub_source_field}}: ...
  normal_result_yaml_example_tranditional: |-
    示例請求:
      - id: 1
        {{imt_source_field}}: Source
    示例結果:
      - id: 1
        step1: 直譯結果
        step2: 意譯結果
  subtitle_result_yaml_example_tranditional: |-
    範例請求:
      - id: 1
        {{imt_sub_source_field}}: ...
      - id: 2
        {{imt_sub_source_field}}: ...
    範例回應:
      - id: 1
        step1: 直譯結果
        step2: 意譯結果
        {{imt_sub_source_field}}: ...
      - id: 2
        step1: 直譯結果
        step2: 意譯結果
        {{imt_sub_source_field}}: ...
systemPrompt: 你是一位精通 {{to}} 的专业翻译，你负责将它翻译成中文，不要有任何解释。
prompt: |-
  请根据以下要求完成翻译任务： 
  1. 将下面 YAML 对象里的 {{imt_source_field}} 字段直接翻译为 {{to}}，保留原文特定的术语或媒体名称（如有）。将本次翻译的结果放入 YAML 数组中的 step1 字段。 
  2：根据第一次翻译的结果进行意译，力求信达雅，但还是要保留特定的术语或媒体名改成（如有），在遵守原意的前提下让文本更通俗易懂，符合中文的表达习惯，将第二次翻译的结果放入 YAML 数组中的 step2 字段。 

  示例格式：
  {{normal_result_yaml_example}}

  开始翻译：

  {{yaml}}

multiplePrompt: |-
  请根据以下要求完成翻译任务： 
  1. 将下面 YAML 对象里的 {{imt_source_field}} 字段直接翻译为 {{to}}，保留原文特定的术语或媒体名称（如有）。将本次翻译的结果放入 YAML 数组中的 step1 字段。 
  2：根据第一次翻译的结果进行意译，力求信达雅，但还是要保留特定的术语或媒体名改成（如有），在遵守原意的前提下让文本更通俗易懂，符合中文的表达习惯，将第二次翻译的结果放入 YAML 数组中的 step2 字段。 

  示例格式：
  {{normal_result_yaml_example}}

  开始翻译：

  {{yaml}}

subtitlePrompt: |-
  将下面 YAML 格式的视频字幕文本中所有的 {{imt_sub_source_field}} 字段中的文本翻译为 {{to}}，并将翻译结果写在 {{imt_sub_trans_field}} 字段中，必须补全每一个 {{imt_sub_trans_field}} 字段，保留每一个 {{imt_sub_source_field}} 字段。要求如下：

  1. 第一次先直接翻译 {{imt_sub_source_field}} 字段的内容，将本次翻译的结果放入 YAML 数组中的 step1 字段。
  2. 根据第一次翻译的结果进行意译，力求信达雅，但还是要保留特定的术语或媒体名改成（如有），在遵守原意的前提下让文本更通俗易懂，符合中文的表达习惯，将第二次翻译的结果放入 YAML 数组中的 step2 字段。 

  {{subtitle_result_yaml_example}}

  开始翻译：

  {{yaml}}

langOverrides:
  - id: auto2zh-TW
    systemPrompt: 您是一位精通繁體中文的專業翻譯，您負責將它翻譯成中文，不要有任何解釋。
    prompt: |-
      請根據以下要求完成翻譯任務： 
      1. 將下面 YAML 對象裡的 {{imt_source_field}} 字段直接翻譯為 {{to}}，保留原文特定的術語或媒體名稱（如有）。將本次翻譯的結果放入 YAML 陣列中的 step1 字段。 
      2：根據第一次翻譯的結果進行意譯，力求信達雅，但還是要保留特定的術語或媒體名稱（如有），在遵守原意的前提下讓文本更通俗易懂，符合中文的表達習慣，將第二次翻譯的結果放入 YAML 陣列中的 step2 字段。 

      示例格式：
      {{normal_result_yaml_example_tranditional}}

      開始翻譯：

      {{yaml}}

    multiplePrompt: |-
      請根據以下要求完成翻譯任務： 
      1. 將下面 YAML 對象裡的 {{imt_source_field}} 字段直接翻譯為 {{to}}，保留原文特定的術語或媒體名稱（如有）。將本次翻譯的結果放入 YAML 陣列中的 step1 字段。 
      2：根據第一次翻譯的結果進行意譯，力求信達雅，但還是要保留特定的術語或媒體名稱（如有），在遵守原意的前提下讓文本更通俗易懂，符合中文的表達習慣，將第二次翻譯的結果放入 YAML 陣列中的 step2 字段。 

      示例格式：
      {{normal_result_yaml_example_tranditional}}

      開始翻譯：

      {{yaml}}

    subtitlePrompt: |-
      將下面 YAML 格式的影片字幕文本中所有的 {{imt_sub_source_field}} 字段中的文本翻譯為 {{to}}，並將翻譯結果寫在 {{imt_sub_trans_field}} 字段中，必須補全每一個 {{imt_sub_trans_field}} 字段，保留每一個 {{imt_sub_source_field}} 字段。要求如下：

      1. 第一次先直接翻譯 {{imt_sub_source_field}} 字段的內容，將本次翻譯的結果放入 YAML 陣列中的 step1 字段。
      2. 根據第一次翻譯的結果進行意譯，力求信達雅，但還是要保留特定的術語或媒體名稱（如有），在遵守原意的前提下讓文本更通俗易懂，符合中文的表達習慣，將第二次翻譯的結果放入 YAML 陣列中的 step2 字段。 

      示例格式：
      {{subtitle_result_yaml_example_tranditional}}

      開始翻譯：

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

