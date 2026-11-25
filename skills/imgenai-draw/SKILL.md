---
name: imgenai-draw
description: 调用 imgenai.net 的科研图像生成 API（nano-banana 与 gpt-image 系列）按提示词或参考图生成 1K/2K/4K 高清图。Use when the user asks to draw / generate an image / 出图 / 画一张 / 生成图片 / 做配图 with imgenai (or just asks for an AI-generated image and no other backend is configured).
metadata:
  short-description: imgenai.net AI 绘图（OpenAI 兼容）
  homepage: https://imgenai.net
  endpoint: https://imgenai.net/v1/images/generations
---

# imgenai 绘图

## 何时触发

- 用户说"画一张 / 出一张 / 生成一张 / 做个配图 / 给我一张 X 的图"
- 用户明确点名 imgenai / nano-banana / 中转站 / 香蕉绘图
- 用户要科研插图、4K 高清出图、有参考图想做图生图
- 没有其它图像后端配置时，作为默认绘图后端

## 凭据

- 文生图：`https://imgenai.net/v1/images/generations`，图生图：`https://imgenai.net/v1/images/edits`（都兼容 OpenAI）
- 密钥格式：`sk_live_xxx`（去 imgenai.net 控制台 → 绘图密钥 创建）
- 环境变量：`IMGENAI_API_KEY`（**不要**用 `OPENAI_API_KEY`，会跟用户真 OpenAI 密钥冲突）
- HTTP header：`Authorization: Bearer $IMGENAI_API_KEY`

调用前确认密钥已设置，**只看有没有，不要把密钥打印出来**（打印会留在对话记录里）：

```bash
[ -n "$IMGENAI_API_KEY" ] && echo "已设置" || echo "未设置"
```

```powershell
if ($env:IMGENAI_API_KEY) { "已设置" } else { "未设置" }
```

没设置就请用户去 imgenai.net 创建密钥，**由用户自己在终端里**设置，不要让用户把密钥发到对话里：

- zsh（Mac 默认）：在 `~/.zshenv` 里加一行 `export IMGENAI_API_KEY="sk_live_你的密钥"`
- bash：在 `~/.bashrc` 里加同样一行
- Windows：`setx IMGENAI_API_KEY "sk_live_你的密钥"`

设置后要重开 AI 工具的会话才生效。

## 模型选择

模型和价格会变，**以接口返回为准**，拿不准或报 `invalid_model` 时先查一次（不花积分）：

```bash
curl -sS https://imgenai.net/v1/models -H "Authorization: Bearer $IMGENAI_API_KEY"
```

`credits_per_call` 是每张积分，`supported_sizes` 是可选的 `image_size`（`auto` 表示不用传）。下表是 2026-11-25 的快照：

| model id | 积分/张 | 分辨率 | 推荐场景 |
|---|---:|---|---|
| `nano-banana-2` | 1300 | 1K/2K/4K | **默认推荐** |
| `nano-banana-2.1` | 1300 | 1K/2K/4K | V2 升级版，同价 |
| `nano-banana-pro` | 1800 | 1K/2K/4K | 科研插图首选 |
| `nano-banana-2-cl` | **13000** | 1K/2K/4K | V2 + 细节清晰加强 |
| `nano-banana-pro-vip` | **10000** | 1K/2K | 顶级质量 |
| `nano-banana-pro-4k-vip` | **16000** | 仅 4K | 超高清出图 |
| `gpt-image-2` | 600 | 1K | OpenAI 风格 |
| `gpt-image-2.5` | 600 | 1K | 新一代 |
| `gpt-image-2.6` | 600 | 1K | 最新一代，最便宜的一档 |
| `gpt-image-2-vip` | 1300 | 1K/2K/4K | OpenAI VIP |
| `gpt-image-2.5-flare` / `gpt-image-2.5-sunburst` | 3000 | 1K/2K/4K | 2.5 高清 |
| `gpt-image-2.6-flare` / `gpt-image-2.6-sunburst` | 3000 | 1K/2K/4K | 2.6 高清 |

**选型默认值**：
- 用户没指定 → `nano-banana-2` + `aspect_ratio: 1:1` + `image_size: 1K`
- 用户说"高清/精细/出版用" → `nano-banana-pro` + `2K`
- 用户说"快/便宜/草稿" → `gpt-image-2.6`（只出 1K）
- 用户要"4K" → `nano-banana-pro` + `image_size: 4K`（同一模型各分辨率同价）
- **单价 10000 及以上的模型，用户没点名就不要用**；要用先告诉用户每张多少积分，得到同意再调

## 宽高比与分辨率

`aspect_ratio` 和 `image_size` **每次都明确传**（只出 1K 的 gpt-image 不用传 `image_size`）。

| 模型 | 可选 `aspect_ratio` |
|---|---|
| nano-banana 全系、gpt-image 的 flare / sunburst | `auto, 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3, 5:4, 4:5, 21:9` |
| `nano-banana-2` / `nano-banana-2-cl` 额外 | `1:4, 4:1, 1:8, 8:1`（横幅、长条、Banner） |
| `gpt-image-2` / `2-vip` / `2.5` / `2.6` | 上面 11 个，另加 `9:21, 1:2, 2:1` |

- nano-banana 和 flare / sunburst 传错会 400，错误消息会列出允许的取值，照着改；另外四个 gpt-image 传表外的比例会出正方形，不报错
- `gpt-image-2-vip`、flare、sunburst 传 `auto` 出正方形，要别的比例就明确写
- 也接受 OpenAI 的 `size`（如 `1536x1024`），按最接近的比例和分辨率换算；同时传了 `aspect_ratio` 或 `image_size` 时以它们为准

## 调用方式

提示词常带引号和换行，**先写进文件再传**，不要拼在命令行里。

### 文生图

1. 用写文件工具生成 `body.json`（UTF-8）：

```json
{
  "model": "nano-banana-2",
  "prompt": "一只蓝色的细胞在显微镜下的科研插图，简洁背景",
  "aspect_ratio": "1:1",
  "image_size": "1K"
}
```

2. 发请求，响应存文件，同时看状态码：

```bash
curl -sS -m 600 -X POST https://imgenai.net/v1/images/generations \
  -H "Authorization: Bearer $IMGENAI_API_KEY" \
  -H "Content-Type: application/json" \
  --data-binary @body.json -o resp.json -w "%{http_code}\n"
```

Windows PowerShell 用 `curl.exe`，把 `$IMGENAI_API_KEY` 换成 `$env:IMGENAI_API_KEY`，`@body.json` 加引号写成 `"@body.json"`，命令写在一行里。

3. 状态码 200 时 `resp.json` 里是图片地址；不是 200 就读里面的 `error.message`，别直接取 `data[0].url`：

```json
{"created": 1780067200, "data": [{"url": "https://.../xxx.png", "revised_prompt": null}]}
```

4. **把图下载到本地**再交给用户：`curl -sS -o result.png "图片地址"`

### 图生图（1 到 8 张参考图）

⚠️ **参考图必须先压缩**：原图直传（手机拍的动辄几 MB）上传慢，国内上行带宽差时会被掐断，报 `408` / `ConnectionResetError(10054)`。

1. 用本 skill 目录里的 `compress_ref.py` 压缩（最长边 ≤1536px、JPEG、自动摆正手机照片、透明底铺白）。缺 Pillow 先 `pip install pillow`；脚本不在就下载：

```bash
curl -fsSL https://raw.githubusercontent.com/gaoennan/imgenai-draw/main/skills/imgenai-draw/compress_ref.py -o compress_ref.py
```

```bash
# Windows 用 python；Mac/Linux 可能要写 python3；多张就逐张压缩
python compress_ref.py input.png ref.jpg
```

2. 把提示词写进 `prompt.txt`（UTF-8），用表单上传：

```bash
curl -sS -m 600 -X POST https://imgenai.net/v1/images/edits \
  -H "Authorization: Bearer $IMGENAI_API_KEY" \
  -F "model=nano-banana-pro" \
  -F "prompt=<prompt.txt" \
  -F "aspect_ratio=1:1" \
  -F "image_size=1K" \
  -F "image=@ref.jpg;type=image/jpeg" \
  -o resp.json -w "%{http_code}\n"
```

- **多张参考图**：`image` 字段重复写几次，例如再加一行 `-F "image=@ref2.jpg;type=image/jpeg"`。**顺序就是提示词里的「图1」「图2」**，在提示词里写清每张图的作用
- 最多 8 张，单张不超过 20 MB；张数不影响价格；`mask` 会被忽略
- 走 JSON 接口时，`image` 传一个字符串（data URL、base64 或图片链接），或这类字符串的数组
- 不要用 `curl -d` 把 base64 拼进命令行：一张照片约几百 KB，Linux 单个参数上限 128 KB，Windows 更小，会报「参数列表过长」。一定要走 JSON 时，把 base64 写进文件再 `--data-binary @文件`

### Python（OpenAI SDK）

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://imgenai.net/v1",
    api_key=os.environ["IMGENAI_API_KEY"],
    timeout=600,
    max_retries=0,  # SDK 默认会自动重试，超时重试会重复出图、重复扣积分
)

resp = client.images.generate(
    model="nano-banana-2",
    prompt="科研插图：神经元网络",
    extra_body={"image_size": "2K", "aspect_ratio": "1:1"},
)
print(resp.data[0].url)
```

图生图（先用 `compress_ref.py` 压缩；单张就传一个文件，多张传列表）：

```python
resp = client.images.edit(
    model="nano-banana-pro",
    image=[open("ref.jpg", "rb"), open("ref2.jpg", "rb")],
    prompt="把图1里的仪器放进图2的实验室场景",
    extra_body={"image_size": "2K", "aspect_ratio": "16:9"},
)
print(resp.data[0].url)
```

### Node.js

```javascript
const resp = await fetch('https://imgenai.net/v1/images/generations', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.IMGENAI_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    model: 'nano-banana-2',
    prompt: '科研插图：分子结构图',
    aspect_ratio: '1:1',
    image_size: '1K',
  }),
});
const data = await resp.json();
if (!resp.ok) throw new Error(data.error?.message || resp.status);
console.log(data.data[0].url);
```

Node 自带的 fetch 等 5 分钟没响应就会断开，4K 或慢的模型请用异步模式。

## 异步模式（长任务、批量）

同步请求会一直等到出图（多数在 2 分钟内，最长 10 分钟）。批量任务或不能久等时，在地址后加 `?wait=false`：

```bash
# 1. 提交，立刻拿到 task_id
curl -sS -X POST "https://imgenai.net/v1/images/generations?wait=false" \
  -H "Authorization: Bearer $IMGENAI_API_KEY" \
  -H "Content-Type: application/json" \
  --data-binary @body.json

# 2. 轮询结果，5 到 10 秒一次，把 TASK_ID 换成上一步返回的 task_id
curl -sS "https://imgenai.net/v1/images/generations/TASK_ID" \
  -H "Authorization: Bearer $IMGENAI_API_KEY"
```

| 轮询结果 | 含义 |
|---|---|
| HTTP 200，`status: "processing"` | 还在生成，继续轮询 |
| HTTP 200，`status: "succeeded"` | 完成，`data[0].url` 是图片 |
| HTTP 400，`status: "failed"` | 失败，停止轮询；`error.code` 为 `content_violation` 是内容审核没过，`credits_refunded` 说明积分退没退 |

超过 30 分钟没出图会自动判失败并退积分。

## 失败处理与定价

| 状态码 | 含义 | 处理 |
|---|---|---|
| 200 | 成功 | `data[0].url` 是图片 |
| 400 | 参数错（含参考图超过 8 张）、内容审核没过、或生成失败 | 读 `error.message`：参数错按提示改；审核没过就改提示词或参考图，原样重试没用 |
| 401 | 密钥无效 | 检查 `IMGENAI_API_KEY` 是否 `sk_live_` 开头 |
| 402 | 积分不足 | 充值或换便宜模型 |
| 429 | 超过每个密钥每分钟 10 次 | 等一分钟再发，批量时控制节奏 |
| 500 / 502 | 服务端或网络偶发错误 | 重试一次；连续失败就换模型 |
| 504 | 同步等待超过 10 分钟 | 积分已退，改用异步模式 |

**返还策略**：
- 生成失败（非违规）→ 自动返还积分
- `nano-banana-2-cl` / `pro-vip` / `pro-4k-vip` 这三个：输入或输出审查不通过时**不返还**
- 其它模型遇到内容审查也返还

## 完整工作流

1. **检查密钥**：只看有没有，不打印内容
2. **选模型**：按"选型默认值"；贵的模型先征得同意
3. **选参数**：`aspect_ratio` 默认 1:1，`image_size` 默认 1K，都明确写上
4. **写文件**：文生图写 `body.json`；图生图先压缩参考图，再写 `prompt.txt`
5. **发请求**：响应存 `resp.json`，看状态码
6. **交付**：下载图片到本地，告诉用户文件位置、模型和花了多少积分；支持 Markdown 的界面用 `![](url)` 预览
7. **失败兜底**：按上表处理，同一请求最多自动重试一次，避免重复扣积分

## 一些细节

- 不支持 `n>1`，每次请求出 1 张。多张就分开提交，注意每分钟 10 次的限制
- 提示词要写"画什么"。把整份说明文档、多张图的需求一次贴进来，容易被判审核不通过；一次只写一张图的内容
- 文档源头：https://imgenai.net → 控制台 → API 文档
