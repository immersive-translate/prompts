# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个沉浸式翻译（Immersive Translate）插件的 AI 专家提示词仓库。包含各种专业领域的翻译专家配置文件，用于提升翻译质量。

## 核心架构

### 文件结构
- `plugins/` - 所有 AI 专家配置文件目录
- `README.md` - 中文贡献指南
- `README-EN.md` - 英文贡献指南

### AI 专家配置文件格式
每个专家配置文件都是 YAML 格式，包含以下关键部分：

```yaml
# 基础信息
id: 唯一标识符
name: 专家名称
description: 简短描述
details: 详细描述
i18n: 多语言支持（至少包含 zh-CN 和 zh-TW）

# 提示词配置
env: 环境变量占位符
systemPrompt: 系统级提示词
prompt: 单句翻译提示词
multiplePrompt: 多段翻译提示词
subtitlePrompt: 字幕翻译提示词
```

### 关键变量
- `{{to}}` - 目标语言
- `{{imt_source_field}}` - 源文本字段
- `{{imt_trans_field}}` - 翻译文本字段
- `{{yaml}}` - YAML 格式的输入数据

## 开发工作流

### 创建新的 AI 专家
1. 在 `plugins/` 目录下创建新的 `.yml` 文件
2. 遵循现有的配置文件格式
3. 确保包含完整的多语言支持（zh-CN 和 zh-TW）
4. 提供清晰的系统提示词和翻译规则

### 本地调试
- 在沉浸式翻译设置页面的【开发者设置】中编辑 YAML 格式
- 参考 `README.md` 中的详细配置规范

### 提交贡献
1. Fork 仓库并创建新分支
2. 添加新的 `.yml` 配置文件到 `plugins/` 目录
3. 确保内容新颖且不与现有内容重复
4. 提交清晰的提交信息
5. 发起 Pull Request

## 注意事项

- 所有配置文件必须使用 YAML 格式
- 必须包含完整的 i18n 多语言支持
- 专家名称必须是唯一的
- 遵循现有的翻译提示词结构
- 确保不包含恶意代码或侵权内容

## 示例参考

查看 `plugins/github.yml` 作为标准配置文件的参考，包含完整的字段定义和多语言支持。