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

底层走 OpenAI 兼容协议，支持 **14 个模型**（nano-banana 全系 + GPT-Image 2 / 2.5 / 2.6）、**1K / 2K / 4K** 分辨率，可文生图也可图生图（最多 8 张参考图）。

---

## 一键安装

两个文件都要装：`SKILL.md` 是说明，`compress_ref.py` 用来压缩图生图的参考图。

### Claude Code

```bash
mkdir -p ~/.claude/skills/imgenai-draw && cd ~/.claude/skills/imgenai-draw && \
  curl -fsSL --remote-name-all https://raw.githubusercontent.com/gaoennan/imgenai-draw/main/skills/imgenai-draw/{SKILL.md,compress_ref.py}
```

### Codex CLI

```bash
mkdir -p ~/.codex/skills/imgenai-draw && cd ~/.codex/skills/imgenai-draw && \
  curl -fsSL --remote-name-all https://raw.githubusercontent.com/gaoennan/imgenai-draw/main/skills/imgenai-draw/{SKILL.md,compress_ref.py}
```

更新时重新执行一遍同样的命令即可。

---

## 配密钥

去 [imgenai.net → 控制台 → 绘图密钥](https://imgenai.net) 创建一个 `sk_live_` 开头的密钥，然后设成环境变量：

```bash
# zsh（Mac 默认）写 ~/.zshenv，AI 工具开的非交互终端也能读到；bash 改成 ~/.bashrc
echo 'export IMGENAI_API_KEY="sk_live_你的密钥"' >> ~/.zshenv && source ~/.zshenv
# fish 用户：set -Ux IMGENAI_API_KEY "sk_live_你的密钥"
# Windows：setx IMGENAI_API_KEY "sk_live_你的密钥"
```

设置后重开 Claude Code / Codex 会话。密钥不要发到 AI 对话里。

新用户注册即送 **10000 积分**（约 7 张 nano-banana-2，或 16 张 gpt-image-2.6），不用充钱就能试。

---

## 验证装好了

开一个新的 Claude Code 或 Codex 会话，说：

```
画一张红苹果的图
```

应该能看到 AI 自己跑 curl、等一两分钟、把图片存到本地并回给你。VS Code 里 Markdown 预览会自动渲染成图片。

如果 AI **没有**调起 skill 而是用别的方式（比如建议你装 DALL·E），检查：
- `ls ~/.claude/skills/imgenai-draw/SKILL.md` 文件在不在
- 密钥设了没有：`[ -n "$IMGENAI_API_KEY" ] && echo 已设置 || echo 未设置`
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
（先拖两张图）把图1里的仪器放进图2的实验室场景，16:9
```

```text
我要做横幅 Banner，用 1:8 长条比例画一片星空
```
（最后这条会自动选 V2 系列，因为只有它支持 1:8 加长比例）

---

## 支持的模型

| model id | 积分/张 | 分辨率 | 推荐场景 |
|---|---:|---|---|
| `nano-banana-2` | 1300 | 1K/2K/4K | **默认推荐** |
| `nano-banana-2.1` | 1300 | 1K/2K/4K | V2 升级版，同价 |
| `nano-banana-pro` | 1800 | 1K/2K/4K | 科研插图首选 |
| `nano-banana-2-cl` | 13000 | 1K/2K/4K | V2 + 细节清晰加强 |
| `nano-banana-pro-vip` | 10000 | 1K/2K | 顶级质量 |
| `nano-banana-pro-4k-vip` | 16000 | **4K only** | 超高清出图 |
| `gpt-image-2` / `gpt-image-2.5` / `gpt-image-2.6` | 600 | 1K | OpenAI 风格，草稿 |
| `gpt-image-2-vip` | 1300 | 1K/2K/4K | OpenAI VIP |
| `gpt-image-2.5-flare` / `gpt-image-2.5-sunburst` | 3000 | 1K/2K/4K | 2.5 高清 |
| `gpt-image-2.6-flare` / `gpt-image-2.6-sunburst` | 3000 | 1K/2K/4K | 2.6 高清 |

以上是 2026-11-25 的价格，实时的模型和价格以 `GET /v1/models` 为准（不花积分，skill 也会让 AI 先查）。同一模型不同分辨率同价。

**积分参考**：1 元约 10000 积分。`nano-banana-2` ≈ 1.3 毛/张，`nano-banana-pro-4k-vip` ≈ 1.6 元/张。

---

## 宽高比

**nano-banana 全系和 gpt-image 的 flare / sunburst**：`auto, 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3, 5:4, 4:5, 21:9`

**加长比例**（仅 `nano-banana-2` / `nano-banana-2-cl`）：`1:4, 4:1, 1:8, 8:1`——适合 Banner、长条、瀑布流。

**`gpt-image-2` / `2-vip` / `2.5` / `2.6`**：上面 11 个，另加 `9:21, 1:2, 2:1`

nano-banana 和 flare / sunburst 传错组合会 400 拒绝，错误消息会列出该模型允许的取值，AI 拿到错误后会自己改参数重试。

---

## 直接用 API（不走 skill）

skill 是把"调 API"这件事打包成"说人话"。如果你想直接调 API，imgenai 是完全 [OpenAI 兼容](https://imgenai.net) 的：

```bash
curl -X POST https://imgenai.net/v1/images/generations \
  -H "Authorization: Bearer $IMGENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"nano-banana-2","prompt":"a tiny red apple","aspect_ratio":"1:1","image_size":"1K"}'
```

图生图用 `/v1/images/edits` 以文件方式上传参考图，多张就重复 `image` 字段。完整示例 + 异步模式 + 错误码处理见 [`skills/imgenai-draw/SKILL.md`](skills/imgenai-draw/SKILL.md)。

---

## 工作原理

1. 你在 Claude / Codex 里说人话（比如"画只猫"）
2. AI 看到自己 skill 列表里有 `imgenai-draw`，描述匹配，自动加载 SKILL.md
3. AI 按 SKILL.md 里的"工作流"步骤：选模型 → 选参数 → 构造请求 → 发 curl
4. imgenai 服务端同步返回图片 URL，多数在 2 分钟内
5. AI 把图下载到本地给你，VS Code 等 Markdown 预览会内联渲染

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
