# readmodule

一个用于读取 OpenHarmony 模块代码的 MCP (Model Context Protocol) 服务器。

## 介绍

readmodule 是一个基于 MCP 协议的服务器，主要功能是读取指定 OpenHarmony 模块目录中的所有代码文件，包括子目录中的文件。它支持从各种文件类型中读取代码并以结构化格式返回内容。

## 功能特点

该工具支持读取以下类型的文件：

- .md（Markdown 文件）
- .ets（ETS 文件）
- .ts（TypeScript 文件）
- .json（JSON 文件）
- .json5（JSON5 文件）
- .cpp（C++ 源文件）
- .h（C/C++ 头文件）

## 安装

```bash
pip install readmodule
```
## 使用方法

安装后可以通过以下命令启动服务器：

```bash
readmodule-mcp
```


