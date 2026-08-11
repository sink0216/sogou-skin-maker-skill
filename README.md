# Sogou Skin Maker Skill

[![Validate skill](https://github.com/sink0216/sogou-skin-maker-skill/actions/workflows/validate.yml/badge.svg)](https://github.com/sink0216/sogou-skin-maker-skill/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

想 DIY 一款自己的搜狗输入法皮肤吗？

想让自推、自家宠物，或者脑子里的原创角色，在办公和聊天时陪着你吗？

把参考图交给 Codex，或者只写一句描述。这个 Skill 会把角色、画风和构图拆清楚，先给你看静态设计和动画，再生成、打包并校准真正能用的搜狗皮肤。

支持 macOS `.mssf` 和 Windows 经典 `.ssf`。

## 先看能做什么

这些是同一套设计流程产出的 Gate B 静态设计板。它们用于确认角色位置、候选状态、拉伸区和控件，不是伪造的运行时截图。

### 把自家宠物做成皮肤

给一张宠物照片或喜欢的插画风格，可以继续保留毛色、五官和画风，再重新设计候选窗与配套小物。

![奶油柯基 macOS 搜狗皮肤设计板](docs/demo/pet-corgi-macos.png)

### 让喜欢的角色陪你打字

角色、中央候选框和右侧装饰分别锚定。窗口变长时只拉伸中间区域，人物不会跟着变宽或变糊。

![莓果洛丽塔 Windows 搜狗皮肤设计板](docs/demo/lolita-chibi-windows.png)

### 没有参考图也能开始

只写“黑白、钴蓝、轨道与节点、不要渐变”，也可以从零做出原创方向。

![极简轨道 Windows 搜狗皮肤设计板](docs/demo/minimal-orbit-windows.png)

## 直接开始

安装 Skill：

```bash
git clone https://github.com/sink0216/sogou-skin-maker-skill.git
mkdir -p ~/.codex/skills
cp -R sogou-skin-maker-skill/skill/sogou-macos-skin-maker ~/.codex/skills/
```

重新启动 Codex，然后说你想做什么。

有参考图或指定角色：

```text
$sogou-macos-skin-maker 参考这张图，保留角色身份和手绘画风，为我设计一款 Windows 搜狗输入法皮肤。
```

只有文本提示词：

```text
$sogou-macos-skin-maker 从零设计一款奶油柯基主题的 macOS 皮肤，手绘文具风，奶油黄与雾霾蓝配色。
```

已有皮肤，只想修问题：

```text
$sogou-macos-skin-maker 保留当前候选窗样式，只修复人物拉伸和上下 padding。
```

想加动画：

```text
$sogou-macos-skin-maker 保持已确认的静态设计不变，为左侧角色增加自然眨眼动画。
```

如果现有文件只用于提供格式，也可以明确告诉它不要继承旧设计：

```text
$sogou-macos-skin-maker 这个文件只作为格式母包。保留包结构，不要沿用图片、布局和颜色。
```

## 它不只是生成一张图

搜狗皮肤最容易出问题的地方通常不在“大图好不好看”，而在真实候选窗里：人物被拉长、两行文字间距失控、首候选底色越过拉伸区、透明图层出现锯齿，或者按钮看得见却点不到。

所以这个 Skill 还会处理这些事：

- 搜索并按 SHA-256 去重本地母包、解包目录和构建产物
- 区分格式参考、视觉参考、精确素材和动作参考
- 检查短候选、五候选、长候选、首项和非首项选中
- 拆分角色、候选框、状态栏和拉伸区，避免互相污染
- 生成并检查 1x/2x PNG 与 APNG
- 检查配置编码、图片引用、包结构和变更成员
- 安装后用真实候选窗截图校准 padding、锚点和控件占位
- 修复局部问题时锁定无关资源，避免越改越歪

## 为什么要先确认设计

Skill 不会拿到一张图就直接塞进皮肤包。完整流程分成四个确认节点：

1. **Gate A — 参考契约**：说清楚哪些必须保留、哪些可以调整、哪些不能出现。
2. **Gate B — 静态设计**：检查短栏、长栏、选中态、角色位置、翻页控件和明暗背景。
3. **Gate C — 动画**：确认具体运动部位、锚点、帧数、速度和循环方式。
4. **Gate D — 运行时**：安装唯一版本，调用真实候选窗并用截图校准。

只有用户可以批准 Gate A、B 和 C。角色、构图或动作发生变化时，对应的批准会重新变成待确认。

## 格式支持

| 平台 | 格式 | 配置 | 包结构 | 状态 |
|---|---|---|---|---|
| macOS | `.mssf` | `skin.plist` | 外层 ZIP 仅含 `Skin`，`Skin` 为内层 ZIP | 支持 |
| Windows | 经典 `.ssf` | 通常为 UTF-16LE+BOM `skin.ini` | 以实际母包为准，常见为扁平 ZIP | 支持 |
| Windows | H5 / 现代格式 | 未固定 | 需要官方 schema 或可运行样本 | 不推测 |

macOS 和 Windows 使用不同的配置、资源和打包规则。Skill 会先判断平台，不会拿 macOS 的 plist 规则硬套 Windows。

## 自带工具

三个脚本只依赖 Python 标准库：

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

仓库测试会检查 Skill 元数据、公开安全规则、Python 语法、`.mssf` 打包往返和 APNG 组装往返。

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

仓库不包含成品 `.ssf`/`.mssf`、用户私有素材或专有参考皮肤。`docs/demo/` 只保存本项目生成的原创静态概念图。使用指定角色或参考图时，请确认自己有权使用相关素材。

本 Skill 会先搜索当前环境中已经存在的皮肤和历史构建记录，不会反复要求用户提供同一个文件，也不会跨用户复用私有文件。

## License

代码和文档采用 [MIT License](LICENSE)。搜狗输入法及相关商标属于相应权利人；本项目与搜狗官方无关联。参见 [NOTICE.md](NOTICE.md)。
