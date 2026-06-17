#!/usr/bin/env python3
"""压缩图生图参考图，输出 data URL（避免大图直传被服务器掐断 ConnectionResetError(10054)/408）。
用法: python compress_ref.py 参考图.png    # Windows 用 python；Mac/Linux 可能要写 python3
依赖: pip install pillow
"""
import sys, base64, io
from PIL import Image

if len(sys.argv) < 2:
    sys.exit("用法: python compress_ref.py <参考图路径>")

im = Image.open(sys.argv[1]).convert("RGB")
M = 1536  # 最长边上限；要更精细可调到 2048
if max(im.size) > M:
    r = M / max(im.size)
    im = im.resize((round(im.size[0] * r), round(im.size[1] * r)), Image.LANCZOS)
buf = io.BytesIO()
im.save(buf, "JPEG", quality=88, optimize=True)
print("data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode())
