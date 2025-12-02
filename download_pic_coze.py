import os
import requests

def download_images():
    # 读取URL文件
    url_file = "coze_i2v/url_pic.txt"
    save_dir = "coze_i2v/pic"

    # 确保保存目录存在
    os.makedirs(save_dir, exist_ok=True)

    # 读取所有URL
    urls = []
    with open(url_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # 格式: 序号→URL
            if "→" in line:
                url = line.split("→", 1)[1].strip()
            else:
                url = line
            urls.append(url)

    if not urls:
        print("没有找到URL")
        return

    print(f"共找到 {len(urls)} 个图片URL")

    # 获取用户输入的起始序号
    start_num = int(input("请输入起始序号: "))

    # 下载图片
    for i, url in enumerate(urls):
        filename = f"{start_num + i}.jpg"
        filepath = os.path.join(save_dir, filename)

        try:
            print(f"正在下载: {url} -> {filename}")
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            with open(filepath, "wb") as f:
                f.write(response.content)
            print(f"  完成: {filename}")
        except Exception as e:
            print(f"  下载失败: {filename} - {e}")

    print(f"\n下载完成! 图片保存在 {save_dir}/")

if __name__ == "__main__":
    download_images()
