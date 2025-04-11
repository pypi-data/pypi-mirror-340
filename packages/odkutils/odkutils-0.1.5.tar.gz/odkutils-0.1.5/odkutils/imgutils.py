import base64
import io
from PIL import Image,ImageGrab
from typing import Tuple,Optional
import os
from .utils import get_clipboard_file_list,get_file_extension
from .odkipfs import crust_upload_file_to_gateway,crust_upload_file
import json
import tempfile
# GIF转为PNG
def gif_to_png(gif_path, output_folder) -> Optional[Exception]:
    # 打开 GIF 文件
    gif = Image.open(gif_path)
    
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)
    
    # 遍历 GIF 的所有帧
    for i in range(gif.n_frames):
        gif.seek(i)  # 切换到第 i 帧
        frame = gif.convert("RGBA")  # 转换为 RGBA 以确保透明度保留
        frame.save(os.path.join(output_folder, f"frame_{i:03d}.png"), format="PNG")

    print("转换完成！")
    return None

# 保存剪切板截图
def save_clipboard_image(save_path) -> Optional[Exception]:
    img = ImageGrab.grabclipboard()
    if isinstance(img, Image.Image):
        img.save(save_path, "PNG")
        return None
    else:
        return ValueError("剪切板中不是图片")

# 获取截图的base64 
def get_clipboard_image_base64() -> Tuple[Optional[str], Optional[Exception]]:
    img = ImageGrab.grabclipboard()
    if isinstance(img, Image.Image):
        # 将图片转换为base64格式
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        return base64.b64encode(img_byte_arr).decode('utf-8'), None
    else:
        return None, ValueError("剪切板中无图片")
        
# 获取图片cid 
def get_image_cid(image_path) -> Tuple[Optional[str], Optional[Exception]]:
    local_gateway = "http://127.0.0.1:5001"
    try:
        cid, err = crust_upload_file_to_gateway(local_gateway, image_path)
        if err is None:
            return cid, err
        cid,err = crust_upload_file(image_path)
        return cid, err
    except Exception as e:
        return None, e

# 获取剪切板中的图片的CID 支持多个
def get_clipboard_image_cids() -> Tuple[Optional[str], Optional[Exception]]:
    cids = []
    img = ImageGrab.grabclipboard()
    if isinstance(img, Image.Image):
        # 获取临时文件路径
        temp_path = tempfile.mktemp(suffix=".png")
        img.save(temp_path, "PNG")
        cid ,err = get_image_cid(temp_path)
        os.remove(temp_path)
        if err is None:
            return [cid], err
        else:
            return None, err
        
    file_list , err = get_clipboard_file_list()
    if err is not None:
        return None, err
    for file_path in file_list:
        file_ext = get_file_extension(file_path)
        if file_ext in [".png",".jpg",".jpeg",".gif"]:
            cid ,err = get_image_cid(file_path)
            if err is None:
                cids.append(cid)
            else:
                return None, err
    return cids, None


# 保存剪切板中图片的CID
def save_clipboard_image_cids(save_path) -> Optional[Exception]:
    cids, err = get_clipboard_image_cids()
    if err is not None:
        return err
    with open(save_path, "w") as f:
        json.dump(cids, f)
    return None