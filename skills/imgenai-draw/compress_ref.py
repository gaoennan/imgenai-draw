#!/usr/bin/env python3
"""压缩图生图参考图（避免大图直传被服务器掐断 ConnectionResetError(10054)/408）。

用法:
  python compress_ref.py 参考图.png ref.jpg   # 输出压缩后的 JPEG 文件（推荐，配合 curl -F 上传）
  python compress_ref.py 参考图.png           # 输出 data URL（给要在 JSON 里传 image 字段的代码用）

Windows 用 python；Mac/Linux 可能要写 python3
依赖: pip install pillow
"""
import sys, base64, io
from PIL import Image, ImageOps, UnidentifiedImageError

MAX_EDGE = 1536  # 最长边上限；要更精细可调到 2048

if len(sys.argv) not in (2, 3):
    sys.exit("用法: python compress_ref.py <参考图路径> [输出.jpg]")

try:
    im = Image.open(sys.argv[1])
    im = ImageOps.exif_transpose(im)  # 手机照片按 EXIF 方向摆正，否则竖拍会变横
except FileNotFoundError:
    sys.exit(f"找不到文件: {sys.argv[1]}")
except UnidentifiedImageError:
    sys.exit(f"打不开这张图: {sys.argv[1]}（iPhone 的 HEIC 请先转成 JPG 或 PNG）")

# 透明部分铺白底；直接 convert("RGB") 会变成黑底
if im.mode in ("RGBA", "LA", "PA") or "transparency" in im.info:
    rgba = im.convert("RGBA")
    im = Image.new("RGB", rgba.size, "white")
    im.paste(rgba, mask=rgba.getchannel("A"))
else:
    im = im.convert("RGB")

if max(im.size) > MAX_EDGE:
    r = MAX_EDGE / max(im.size)
    im = im.resize((max(1, round(im.size[0] * r)), max(1, round(im.size[1] * r))), Image.LANCZOS)

buf = io.BytesIO()
im.save(buf, "JPEG", quality=88, optimize=True)
data = buf.getvalue()

if len(sys.argv) == 3:
    with open(sys.argv[2], "wb") as f:
        f.write(data)
    print(f"{sys.argv[2]}  {im.size[0]}x{im.size[1]}  {len(data) // 1024} KB")
else:
    print("data:image/jpeg;base64," + base64.b64encode(data).decode())
