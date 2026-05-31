<div align="center">

# imgenai-draw

**让 Claude Code 和 Codex CLI 直接说人话出图。**

[![imgenai.net](https://img.shields.io/badge/powered%20by-imgenai.net-2563EB?style=flat-square)](https://imgenai.net)
[![Agent Skills](https://img.shields.io/badge/agentskills.io-compatible-7C3AED?style=flat-square)](https://agentskills.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)](LICENSE)

</div>

---

## 这是什么

这是 [imgenai.net](https://imgenai.net) 科研图像生成 API 的 **Agent Skill**——一个写好的 `SKILL.md` 文件，装到 `~/.claude/skills/` 或 `~/.codex/skills/` 里，**你的 AI 编程助手就会自己看懂怎么调用 imgenai 出图**。

装完之后你直接说：

> 帮我画一张细胞分裂的科研插图，1K，正方形

Claude / Codex 会自动选模型、组装请求、发起调用、把图片 URL 回给你。整个过程不用你写代码、不用你查文档、不用你记参数。

底层走 OpenAI 兼容协议，支持 **9 个模型**（nano-banana 全系 + GPT-Image-2）、**12 种宽高比**、**1K / 2K / 4K** 分辨率，可文生图也可图生图。

---

## 一键安装

### Claude Code

```bash
mkdir -p ~/.claude/skills/imgenai-draw && \
  curl -fsSL https://raw.githubusercontent.com/gaoennan/imgenai-draw/main/skills/imgenai-draw/SKILL.md \
    -o ~/.claude/skills/imgenai-draw/SKILL.md
```

### Codex CLI

```bash
mkdir -p ~/.codex/skills/imgenai-draw && \
  curl -fsSL https://raw.githubusercontent.com/gaoennan/imgenai-draw/main/skills/imgenai-draw/SKILL.md \
    -o ~/.codex/skills/imgenai-draw/SKILL.md
```

### 同时给 Claude + Codex

```bash
mkdir -p ~/.claude/skills/imgenai-draw ~/.codex/skills/imgenai-draw && \
  curl -fsSL https://raw.githubusercontent.com/gaoennan/imgenai-draw/main/skills/imgenai-draw/SKILL.md \
    | tee ~/.claude/skills/imgenai-draw/SKILL.md > ~/.codex/skills/imgenai-draw/SKILL.md
```

---

## 配密钥

去 [imgenai.net → 控制台 → 绘图密钥](https://imgenai.net) 创建一个 `sk_live_` 开头的密钥，然后写进 shell rc：

```bash
echo 'export IMGENAI_API_KEY="sk_live_你的密钥"' >> ~/.zshrc && source ~/.zshrc
# bash 用户把 ~/.zshrc 换成 ~/.bashrc
# fish 用户：set -Ux IMGENAI_API_KEY "sk_live_你的密钥"
```

新用户注册即送 **20000 积分**（约 16 张 nano-banana-2 / 45 张 nano-banana-fast），不用充钱就能试。

---

## 验证装好了

开一个新的 Claude Code 或 Codex 会话，说：

```
画一张红苹果的图
```

应该能看到 AI 自己跑 curl、等几十秒、把图片 URL 回给你。VS Code 里 Markdown 预览会自动渲染成图片。

如果 AI **没有**调起 skill 而是用别的方式（比如建议你装 DALL·E），检查：
- `ls ~/.claude/skills/imgenai-draw/SKILL.md` 文件在不在
- `echo $IMGENAI_API_KEY` 能不能输出 `sk_live_...`
- 重启 Claude Code / Codex 会话（skill 是启动时扫描的）

---

## 几个能跑的范例 prompt

```text
帮我画一张神经元网络的科研插图，蓝紫色调，1:1，2K
```

```text
用 imgenai 给我做一张 16:9 的横幅，写 "GenAI Research"，简约风
```

```text
画一个分子结构图，nano-banana-pro 模型，4K 清晰度
```

```text
快速出张草稿就行，画只猫坐在窗台上看月亮
```

```text
（先粘贴或拖一张图）把这张图改成水彩风格
```

```text
我要做横幅 Banner，用 1:8 长条比例画一片星空
```
（最后这条会自动选 V2 系列，因为只有它支持 1:8 加长比例）

---

## 支持的模型

| model id | 积分/张 | 分辨率 | 推荐场景 |
|---|---:|---|---|
| `nano-banana-fast` | 440 | 1K | 草稿、快速预览 |
| `nano-banana-2` | 1300 | 1K/2K/4K | **默认推荐**，性价比最高 |
| `nano-banana-2-cl` | 3000 | 1K/2K/4K | V2 + 细节清晰加强 |
| `nano-banana-pro` | 1800 | 1K/2K/4K | 科研插图首选 |
| `nano-banana-pro-vt` | 1800 | 1K/2K/4K | Pro 的另一变体 |
| `nano-banana-pro-vip` | 10000 | 1K/2K | 顶级质量 |
| `nano-banana-pro-4k-vip` | 16000 | **4K only** | 超高清出图 |
| `gpt-image-2` | 600 | auto | OpenAI 风格 |
| `gpt-image-2-vip` | 900 | 1K/2K/4K | OpenAI VIP |

**积分参考**：1 元 = 10000 积分。`nano-banana-2` ≈ 1.3 毛/张，`nano-banana-pro-4k-vip` ≈ 1.6 元/张。

---

## 宽高比

**所有模型通用 8 种**：`auto, 1:1, 3:4, 4:3, 9:16, 16:9, 3:2, 2:3`

**V2 系列加长比例**（仅 `nano-banana-2` / `nano-banana-2-cl`）：`1:4, 4:1, 1:8, 8:1`——适合 Banner、长条、瀑布流。

服务端按模型严格校验，传错组合会 400 拒绝，错误消息会列出该模型允许的全部取值，AI 拿到错误后会自己改参数重试。

---

## 直接用 API（不走 skill）

skill 是把"调 API"这件事打包成"说人话"。如果你想直接调 API，imgenai 是完全 [OpenAI 兼容](https://imgenai.net) 的：

```bash
curl -X POST https://imgenai.net/v1/images/generations \
  -H "Authorization: Bearer $IMGENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"nano-banana-2","prompt":"a tiny red apple","aspect_ratio":"1:1","image_size":"1K"}'
```

完整 Python / Node.js 示例 + 异步模式 + 错误码处理见 [`skills/imgenai-draw/SKILL.md`](skills/imgenai-draw/SKILL.md)。

---

## 工作原理

1. 你在 Claude / Codex 里说人话（比如"画只猫"）
2. AI 看到自己 skill 列表里有 `imgenai-draw`，描述匹配，自动加载 SKILL.md
3. AI 按 SKILL.md 里的"工作流"步骤：选模型 → 选参数 → 构造请求 → 发 curl
4. imgenai 服务端 30 秒到 3 分钟内同步返回图片 URL
5. AI 把 URL 给你，VS Code 等 Markdown 预览会内联渲染

SKILL.md 是个普通的 Markdown 文件，前面带一段 YAML frontmatter，遵循 [agentskills.io](https://agentskills.io) 开放标准，理论上 Claude / Codex / Cursor / Gemini CLI 等 30+ 个 agent 工具都能识别。

---

## 链接

- 🏠 主站：[imgenai.net](https://imgenai.net)
- 📚 API 文档：[imgenai.net → 控制台 → API 文档](https://imgenai.net)
- 🧩 Agent Skills 标准：[agentskills.io](https://agentskills.io)
- 🐛 反馈问题：[issues](https://github.com/gaoennan/imgenai-draw/issues)

---

## License

MIT — 见 [LICENSE](LICENSE)。

随便 fork、改、商用，但保留版权声明就行。

---

<div align="center">

Made by [GenAI Research](https://imgenai.net) · 专业级 AI 科研图像生成

</div>
