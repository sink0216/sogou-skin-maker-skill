# Sogou Skin Maker Skill

一个用于设计、制作、修复、验证和运行时校准搜狗输入法皮肤的 Codex Skill，支持：

- macOS `.mssf`
- Windows 经典 `.ssf`
- 静态皮肤与 APNG 动画
- 候选窗、状态栏、翻页控件和中英文切换状态
- 母包发现与哈希去重
- 参考图映射、分阶段确认和运行时验收
- 确定性打包、结构检查与逐帧动画检查

Skill 会优先搜索当前用户环境中已有的母包、解包目录和构建记录，不会为了研究格式而反复索要皮肤文件，也不会跨用户复用私有文件。

## 安装

将 [`skill/sogou-macos-skin-maker`](skill/sogou-macos-skin-maker) 复制到 Codex Skills 目录：

```bash
git clone https://github.com/sink0216/sogou-skin-maker-skill.git
mkdir -p ~/.codex/skills
cp -R sogou-skin-maker-skill/skill/sogou-macos-skin-maker ~/.codex/skills/
```

重新打开 Codex 后，可以这样调用：

```text
$sogou-macos-skin-maker 帮我制作一款 Windows 搜狗输入法皮肤
```

Skill 的历史标识保留为 `sogou-macos-skin-maker`，但当前版本同时支持 macOS 和 Windows 经典皮肤。

## 仓库结构

```text
skill/sogou-macos-skin-maker/
├── SKILL.md
├── agents/openai.yaml
├── references/
└── scripts/
```

仓库不包含任何成品 `.ssf`/`.mssf`、角色图片、用户素材或专有皮肤资源。工具脚本只依赖 Python 标准库。

## 验证

```bash
python3 -m unittest discover -s tests -v
```

## 许可与声明

代码和文档按 [MIT License](LICENSE) 开源。搜狗输入法及其商标属于相应权利人；本项目与搜狗官方无关联。详见 [NOTICE.md](NOTICE.md)。
