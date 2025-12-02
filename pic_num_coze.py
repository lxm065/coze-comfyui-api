import os
import shutil
from pathlib import Path

def rename_images_by_time(start_num):
    """
    按时间排序重命名 coze_i2v/pic 目录中的图片

    Args:
        start_num: 起始序号
    """
    pic_dir = Path("coze_i2v/pic")

    # 检查目录是否存在
    if not pic_dir.exists():
        print(f"错误: 目录 {pic_dir} 不存在")
        return

    # 获取所有图片文件（支持常见图片格式）
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
    image_files = [
        f for f in pic_dir.iterdir()
        if f.is_file() and f.suffix.lower() in image_extensions
    ]

    if not image_files:
        print("没有找到图片文件")
        return

    # 按修改时间排序
    image_files.sort(key=lambda x: x.stat().st_mtime)

    print(f"\n找到 {len(image_files)} 个图片文件，按时间排序：")
    for i, f in enumerate(image_files, start=1):
        print(f"{i}. {f.name}")

    # 先重命名到临时文件名，避免命名冲突
    temp_files = []
    for i, old_file in enumerate(image_files):
        # 获取文件扩展名
        ext = old_file.suffix
        temp_name = pic_dir / f"temp_{i}_{old_file.name}"

        # 重命名到临时文件
        old_file.rename(temp_name)
        temp_files.append((temp_name, ext))

    # 从临时文件重命名到最终文件名
    print(f"\n开始重命名（从序号 {start_num} 开始）：")
    for i, (temp_file, ext) in enumerate(temp_files):
        new_num = start_num + i
        new_name = pic_dir / f"{new_num}{ext}"

        temp_file.rename(new_name)
        print(f"{temp_file.name} -> {new_name.name}")

    print("\n重命名完成！")

if __name__ == "__main__":
    try:
        start_num = int(input("请输入起始序号: "))

        if start_num < 1:
            print("错误: 起始序号必须大于等于1")
        else:
            rename_images_by_time(start_num)

    except ValueError:
        print("错误: 请输入有效的数字")
    except Exception as e:
        print(f"发生错误: {e}")
