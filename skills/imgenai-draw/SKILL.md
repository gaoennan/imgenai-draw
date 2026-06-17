---
name: imgenai-draw
description: 调用 imgenai.net 的科研图像生成 API（nano-banana 与 gpt-image-2 系列）按提示词或参考图生成 1K/2K/4K 高清图。Use when the user asks to draw / generate an image / 出图 / 画一张 / 生成图片 / 做配图 with imgenai (or just asks for an AI-generated image and no other backend is configured).
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

- API 端点：`https://imgenai.net/v1/images/generations`（OpenAI 兼容）
- 密钥格式：`sk_live_xxx`（去 imgenai.net 控制台 → 绘图密钥 创建）
- 环境变量：`IMGENAI_API_KEY`（**不要**用 `OPENAI_API_KEY`，会跟用户真 OpenAI 密钥冲突）
- HTTP header：`Authorization: Bearer $IMGENAI_API_KEY`

调用前先 `echo "$IMGENAI_API_KEY"` 确认存在。没有就提示用户去 imgenai.net 拿一个，并指导其加到 shell rc：
```bash
echo 'export IMGENAI_API_KEY="sk_live_xxx"' >> ~/.zshrc && source ~/.zshrc
```

## 模型选择

| model id | 积分/张 | 分辨率 | 推荐场景 |
|---|---:|---|---|
| `nano-banana-fast` | 440 | 1K | 草稿/快速预览 |
| `nano-banana-2` | 1300 | 1K/2K/4K | **默认推荐**，性价比最高 |
| `nano-banana-2-cl` | 3000 | 1K/2K/4K | V2 + 细节清晰加强 |
| `nano-banana-pro` | 1800 | 1K/2K/4K | 科研插图首选 |
| `nano-banana-pro-vt` | 1800 | 1K/2K/4K | Pro 的另一变体 |
| `nano-banana-pro-vip` | 10000 | 1K/2K | 顶级质量 |
| `nano-banana-pro-4k-vip` | 16000 | **4K only** | 超高清出图 |
| `gpt-image-2` | 600 | auto | OpenAI 风格 |
| `gpt-image-2-vip` | 900 | 1K/2K/4K | OpenAI VIP |

**选型默认值**：
- 用户没指定 → `nano-banana-2` + `aspect_ratio: 1:1` + `image_size: 1K`
- 用户说"高清/精细/出版用" → `nano-banana-pro` + `2K`（4K 比 2K 贵 9 倍，没明说别上 4K）
- 用户说"快/便宜/草稿" → `nano-banana-fast`（注意只支持 1K）
- 用户要"4K" → 优先 `nano-banana-pro` + `image_size: 4K`，特别强调超清才用 `nano-banana-pro-4k-vip`

## 宽高比

基础 8 种（**所有模型**可选）：`auto, 1:1, 3:4, 4:3, 9:16, 16:9, 3:2, 2:3`

`nano-banana-2` / `nano-banana-2-cl` 额外支持：`1:4, 4:1, 1:8, 8:1`（适合横幅、长条、Banner）

服务端会按模型严格校验——传错组合直接 400 拒绝，错误消息会列出该模型允许的取值。

## 调用方式

### 文生图（最常见）

```bash
curl -X POST https://imgenai.net/v1/images/generations \
  -H "Authorization: Bearer $IMGENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nano-banana-2",
    "prompt": "一只蓝色的细胞在显微镜下的科研插图，简洁背景",
    "aspect_ratio": "1:1",
    "image_size": "1K"
  }'
```

返回（同步模式）：
```json
{
  "created": 1780067200,
  "data": [{"url": "https://file5.aitohumanize.com/file/xxx.png", "revised_prompt": null}]
}
```

### 图生图（带参考图）

⚠️ **参考图必须先压缩再传**：原图直传（手机拍的动辄几 MB）上传慢，国内上行带宽差时会超过服务器上传超时被掐断，客户端报 `408` / `ConnectionResetError(10054) 远程主机强制断开`。**先把最长边缩到 ≤1536px + JPEG 压缩**，体积能小 5-10 倍，根治掉线。**千万别 `base64 -i 大图.png` 直传。**

用 Python（Pillow，跨平台 Windows/Mac/Linux；缺了先 `pip install pillow` 或 `pip3 install pillow`）压缩并输出 data URL：

```python
# compress_ref.py — 用法: python compress_ref.py 参考图.png
import sys, base64, io
from PIL import Image
im = Image.open(sys.argv[1]).convert("RGB")
M = 1536  # 最长边上限；要更精细可调到 2048
if max(im.size) > M:
    r = M / max(im.size)
    im = im.resize((round(im.size[0]*r), round(im.size[1]*r)), Image.LANCZOS)
buf = io.BytesIO(); im.save(buf, "JPEG", quality=88, optimize=True)
print("data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode())
```

```bash
# Windows 用 python；Mac/Linux 可能要写 python3
REF=$(python compress_ref.py input.png)
curl -X POST https://imgenai.net/v1/images/generations \
  -H "Authorization: Bearer $IMGENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"nano-banana-pro\",
    \"prompt\": \"把这张图改成水彩风格\",
    \"aspect_ratio\": \"1:1\",
    \"image_size\": \"1K\",
    \"image\": \"$REF\"
  }" | jq -r '.data[0].url'
```

> `image` 字段必须带与实际格式一致的前缀（压缩后是 `data:image/jpeg;base64,`，脚本已自动加好，别再手动拼 png 前缀）。只有原图本就很小（<500KB）时，才可跳过压缩直接 `base64 -i input.png` 传 PNG。

### Python（OpenAI SDK）

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://imgenai.net/v1",
    api_key=os.environ["IMGENAI_API_KEY"],
)

resp = client.images.generate(
    model="nano-banana-2",
    prompt="科研插图：神经元网络",
    extra_body={"image_size": "2K", "aspect_ratio": "1:1"},
)
print(resp.data[0].url)
```

### Node.js（推荐用 fetch，OpenAI SDK 会丢掉非标字段）

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
console.log(data.data[0].url);
```

## 异步模式（长任务）

默认是同步模式（请求会阻塞 30s-3min 直到生图完成）。如果是批量任务或客户端不能久等，加 `?wait=false` 查询参数走异步：

```bash
# 1. 提交，立刻拿 task_id
curl -X POST "https://imgenai.net/v1/images/generations?wait=false" \
  -H "Authorization: Bearer $IMGENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"nano-banana-pro-4k-vip","prompt":"4K 超清"}' \
  | jq -r '.task_id'
# → "7-xxx-yyy"

# 2. 轮询查结果（建议 5-10s 一次）
curl https://imgenai.net/v1/images/generations/7-xxx-yyy \
  -H "Authorization: Bearer $IMGENAI_API_KEY"
# → status: processing / succeeded / failed
```

## 失败处理与定价

| 状态码 | 含义 | 处理 |
|---|---|---|
| 200 | 成功 | `data[0].url` 是图片 |
| 400 | 参数错（model/ratio/size 不匹配） | 错误体里会列出该模型允许值，按提示修正 |
| 401 | 密钥无效 | 检查 `IMGENAI_API_KEY` 是否 `sk_live_` 开头 |
| 402 | 积分不足 | 充值或换便宜模型（fast=440, 比 pro-vip 便宜 22 倍） |
| 504 | 超时（极少） | 重试或切异步模式 |

**返还策略**：
- 生成失败（非违规） → 自动返还积分
- `nano-banana-2-cl` / `pro-vip` / `pro-4k-vip` 这三个是违规模型——输入或输出审查不通过时**不返还**
- 其它模型遇到内容审查也返还

## 完整工作流

1. **检查环境**：`echo "${IMGENAI_API_KEY:-未设}"`，没有就提示用户
2. **选模型**：按上面"选型默认值"，特殊场景看用户原话
3. **选参数**：aspect_ratio 默认 1:1，image_size 默认 1K
4. **构造请求**：txt2img 不带 `image`；img2img **先用 compress_ref.py 压缩参考图**再放进 `image`（直传大图会掉线）
5. **发请求**：sync 模式直接 curl/SDK，等 30s-3min
6. **回显结果**：把图片 URL 给用户。在 Markdown 支持的 IDE 里用 `![](url)` 内联预览；不支持就给链接
7. **失败兜底**：400 看错误消息修参数；402 提示充值

## 一些细节

- imgenai.net 用 nginx + Cloudflare，curl 偶发 502 是缓存问题，重试一次基本就好
- 同步模式服务端阻塞等结果，所以 axios/fetch 客户端**超时要设到 4 分钟以上**（默认 30s 经常被掐）
- **参考图务必先压缩到最长边 ≤1536px + JPEG 再传**（见上面"图生图"段）。大图直传国内上行慢，会超服务器上传超时被掐断，客户端报 `ConnectionResetError(10054)` / `408`——这是真实踩过的坑。data URL 前缀要和实际格式一致（压缩后用 `data:image/jpeg;base64,`），缺前缀 `nano-banana-2-cl` 识别不到
- 不支持 `n>1`，每次请求出 1 张图。多张图就并发多个请求
- 文档源头：https://imgenai.net → 控制台 → API 文档
