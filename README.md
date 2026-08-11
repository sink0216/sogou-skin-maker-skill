# Sogou Skin Maker Skill

[![Validate skill](https://github.com/sink0216/sogou-skin-maker-skill/actions/workflows/validate.yml/badge.svg)](https://github.com/sink0216/sogou-skin-maker-skill/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

用于设计、构建、检查和运行时校准搜狗输入法皮肤的 Codex Skill。

支持 macOS `.mssf` 和 Windows 经典 `.ssf`。两个格式使用不同的配置、资源和打包规则，Skill 会先确定目标平台，再进入对应流程。

设计输入可以是参考图、指定角色、现有皮肤的设计语言，也可以只有一段文本提示词。前者会先拆分身份、画风、构图和格式约束；后者会从零建立原创主题与静态设计板。

## 功能

- 搜索并按 SHA-256 去重本地母包、解包目录和构建产物
- 区分格式参考、视觉参考、精确素材和动作参考
- 根据给定参考图或角色保留身份与画风，同时重新设计候选窗和状态栏
- 仅根据文本提示词生成原创宠物、Q 版人物、极简图形等主题
- 在生产前分别确认参考契约、静态设计和动画
- 检查候选窗短/长状态、选中态、翻页控件和透明背景
- 生成并检查 1x/2x PNG 与 APNG
- 检查皮肤配置编码、图片引用、包结构和变更成员
- 安装后根据真实候选窗截图校准 padding、锚点和控件占位
- 保留已确认资源；修复局部问题时限制像素变更范围

## 格式支持

| 平台 | 格式 | 配置 | 包结构 | 状态 |
|---|---|---|---|---|
| macOS | `.mssf` | `skin.plist` | 外层 ZIP 仅含 `Skin`，`Skin` 为内层 ZIP | 支持 |
| Windows | 经典 `.ssf` | 通常为 UTF-16LE+BOM `skin.ini` | 以实际母包为准，常见为扁平 ZIP | 支持 |
| Windows | H5 / 现代格式 | 未固定 | 需要官方 schema 或可运行样本 | 不推测 |

## 安装

```bash
git clone https://github.com/sink0216/sogou-skin-maker-skill.git
mkdir -p ~/.codex/skills
cp -R sogou-skin-maker-skill/skill/sogou-macos-skin-maker ~/.codex/skills/
```

重新启动 Codex 以重新加载 Skills。

## 使用

创建新皮肤：

```text
$sogou-macos-skin-maker 参考这张图，制作一款 Windows 搜狗输入法皮肤。
```

基于指定角色和设计参考：

```text
$sogou-macos-skin-maker 保留参考图里的角色身份和手绘画风，重新设计一套紧凑双行候选窗与异型状态栏。
```

只使用文本提示词：

```text
$sogou-macos-skin-maker 从零设计一款奶油柯基主题的 macOS 皮肤，手绘文具风，奶油黄与雾霾蓝配色。
```

修改现有皮肤，但不继承其设计：

```text
$sogou-macos-skin-maker 这个文件只作为格式母包。保留包结构，不要沿用图片、布局和颜色。
```

修复布局：

```text
$sogou-macos-skin-maker 保留当前候选窗样式，只修复人物拉伸和上下 padding。
```

增加动画：

```text
$sogou-macos-skin-maker 保持已确认静态设计不变，为左侧角色增加自然眨眼动画。
```

## 设计示例

下面是同一套 Gate A / Gate B 流程产出的静态设计板，用来确认角色位置、候选状态、拉伸区、控件和明暗背景。它们是设计示例，不是运行时截图或可安装皮肤包。

### 宠物主题：奶油柯基

基于既有宠物皮肤的手绘材质与扒框构图重新生成角色和狗狗主题角饰；候选框、文字与控件由固定尺寸代码排版。

![奶油柯基 macOS 搜狗皮肤设计板](docs/demo/pet-corgi-macos.png)

### Q 版人物：莓果洛丽塔

基于给定角色与候选窗分层参考，生成原创三头身洛丽塔角色；人物、中央 H1 框体和右侧帽盒分别锚定，避免角色参与横向拉伸。

![莓果洛丽塔 Windows 搜狗皮肤设计板](docs/demo/lolita-chibi-windows.png)

### 文本生成：极简轨道

不使用角色参考，仅根据“黑白、钴蓝、轨道与节点、无渐变”的文本约束生成原创极简方案。

![极简轨道 Windows 搜狗皮肤设计板](docs/demo/minimal-orbit-windows.png)

## 工作流

1. **发现母包**：搜索当前工作区、已知路径、Downloads、安装目录和历史构建记录；按哈希登记可复用基线。
2. **Gate A — 参考契约**：记录必须保留、可以调整和禁止引入的内容。
3. **Gate B — 静态设计**：检查短栏、五候选、长栏、首项/非首项选中、控件和明暗背景。
4. **Gate C — 动画**：确认运动部位、锚点、帧数、时序和循环；同时检查实际速度与逐帧放大图。
5. **生产**：从已确认母版生成 1x/2x 资源，修改必要配置，保留未知字段和无关资源。
6. **打包检查**：检查 CRC、配置编码、资源引用、APNG 帧、成员变更和包结构。
7. **Gate D — 运行时**：安装唯一版本，调用真实候选窗并用截图校准。没有运行时证据时保持 Gate D 未完成。

只有用户可以批准 Gate A、B 和 C。上游设计发生变化时，下游批准会失效。

## 工具

Skill 自带三个仅依赖 Python 标准库的脚本：

```text
skill/sogou-macos-skin-maker/scripts/
├── inspect_mssf.py  # 检查双层包、plist、图片尺寸、APNG 和资源引用
├── pack_mssf.py     # 按固定文件顺序和时间戳打包 .mssf
└── apng_tool.py     # 检查或组装全画布 APNG
```

检查 macOS 包：

```bash
python3 skill/sogou-macos-skin-maker/scripts/inspect_mssf.py skin.mssf --json
```

打包 macOS 皮肤：

```bash
python3 skill/sogou-macos-skin-maker/scripts/pack_mssf.py path/to/Skin output.mssf
```

检查 APNG：

```bash
python3 skill/sogou-macos-skin-maker/scripts/apng_tool.py inspect animation.png
```

## 验证

仓库测试会检查：

- Skill 元数据和公开安全规则
- Python 脚本语法
- `.mssf` 打包/检查往返
- APNG 组装/检查往返

本地运行：

```bash
python3 -m unittest discover -s tests -v
```

## 仓库结构

```text
skill/sogou-macos-skin-maker/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── design-approval-playbook.md
│   ├── format-map.md
│   ├── official-gallery-study.md
│   ├── qa-playbook.md
│   └── windows-classic-ssf.md
└── scripts/

docs/demo/                  # README 使用的原创静态设计示例
```

仓库不包含成品 `.ssf`/`.mssf`、用户私有素材或专有参考皮肤；`docs/demo/` 只保存本项目生成的原创静态概念图。格式研究不会跨用户复用私有文件，也不会要求用户重复提供当前环境中已经存在的皮肤。

## License

代码和文档采用 [MIT License](LICENSE)。搜狗输入法及相关商标属于相应权利人；本项目与搜狗官方无关联。参见 [NOTICE.md](NOTICE.md)。
