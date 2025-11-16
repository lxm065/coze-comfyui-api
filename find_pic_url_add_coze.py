import requests
import re
from urllib.parse import urljoin, urlparse
import os
import sys

# 输出文件路径
OUTPUT_FILE = "coze_i2v/url_pic.txt"

def extract_image_urls(html_content, base_url):
    """
    从 HTML 内容中提取图片 URL
    支持多种图片链接格式：
    - <a href="/x/3/jzy/11.jpg">
    - <img src="/x/3/jzy/11.jpg">
    """
    image_urls = []

    # 正则表达式匹配多种图片链接格式
    patterns = [
        r'<a\s+href\s*=\s*["\']([^"\']+\.(?:jpg|jpeg|png|gif|webp))["\']',  # <a href="/path/image.jpg">
        r'<img\s+[^>]*src\s*=\s*["\']([^"\']+\.(?:jpg|jpeg|png|gif|webp))["\']',  # <img src="/path/image.jpg">
        r'data-src\s*=\s*["\']([^"\']+\.(?:jpg|jpeg|png|gif|webp))["\']',  # data-src="/path/image.jpg"
    ]

    # 合并所有匹配结果
    all_matches = []
    for pattern in patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        all_matches.extend(matches)

    # 去重并拼接完整 URL
    seen = set()
    for img_path in all_matches:
        # 拼接完整 URL
        full_url = urljoin(base_url, img_path)

        # 去重
        if full_url not in seen:
            seen.add(full_url)
            image_urls.append(full_url)

    return image_urls

def fetch_webpage(url):
    """获取网页内容"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        # 尝试检测编码
        response.encoding = response.apparent_encoding

        return response.text
    except requests.exceptions.RequestException as e:
        print(f"网页获取失败: {e}")
        return None

def save_urls_to_file(urls, file_path, mode='a'):
    """
    保存 URL 到文件
    mode='a' 表示追加模式，'w' 表示覆盖模式
    """
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # 如果是追加模式，先读取已有的 URL 避免重复
        existing_urls = set()
        if mode == 'a' and os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                existing_urls = set(line.strip() for line in f if line.strip())

        # 过滤掉已存在的 URL
        new_urls = [url for url in urls if url not in existing_urls]

        if not new_urls:
            print(f"没有新的 URL 需要添加（可能已存在）")
            return 0

        # 写入文件
        with open(file_path, mode, encoding='utf-8') as f:
            for url in new_urls:
                f.write(url + '\n')

        return len(new_urls)
    except Exception as e:
        print(f"文件保存失败: {e}")
        return 0

def main():
    """主函数"""
    print("=" * 60)
    print("图片 URL 提取工具（支持批量处理）")
    print("=" * 60)

    # 检查命令行参数
    if len(sys.argv) >= 2:
        # 命令行模式
        page_urls_input = sys.argv[1]
        save_mode = 'w' if (len(sys.argv) >= 3 and sys.argv[2] == '2') else 'a'
        print(f"\n[命令行模式]")
    else:
        # 交互模式
        # 获取用户输入的 URL
        print("\n提示：可以输入多个 URL，用逗号分隔")
        print("示例：http://example.com/page1, http://example.com/page2")
        page_urls_input = input("\n请输入网页 URL: ").strip()

        if not page_urls_input:
            print("错误: URL 不能为空")
            return

        # 询问保存模式
        print("\n保存模式:")
        print("  1. 追加模式（默认）- 添加到现有文件末尾")
        print("  2. 覆盖模式 - 清空文件后写入")
        mode_choice = input("请选择模式 [1/2，默认 1]: ").strip()

        save_mode = 'w' if mode_choice == '2' else 'a'

    # 分割多个 URL（用逗号分隔）
    page_urls = [url.strip() for url in page_urls_input.split(',') if url.strip()]

    if not page_urls:
        print("错误: 没有有效的 URL")
        return

    print(f"\n共找到 {len(page_urls)} 个网页 URL 待处理")

    mode_text = "覆盖" if save_mode == 'w' else "追加"

    # 汇总所有图片 URL
    all_image_urls = []

    # 处理每个 URL
    for idx, page_url in enumerate(page_urls, 1):
        print("\n" + "=" * 60)
        print(f"正在处理 [{idx}/{len(page_urls)}]: {page_url}")
        print("=" * 60)

        # 验证 URL 格式
        parsed = urlparse(page_url)
        if not parsed.scheme or not parsed.netloc:
            print(f"[警告] URL 格式不正确，跳过: {page_url}")
            continue

        # 获取网页内容
        html_content = fetch_webpage(page_url)
        if not html_content:
            print(f"[警告] 无法获取网页内容，跳过: {page_url}")
            continue

        print(f"网页内容获取成功，大小: {len(html_content)} 字符")

        # 提取图片 URL
        print("正在提取图片 URL...")
        image_urls = extract_image_urls(html_content, page_url)

        if not image_urls:
            print("未找到任何图片 URL")
            continue

        print(f"找到 {len(image_urls)} 个图片 URL:")
        print("-" * 60)
        for url_idx, url in enumerate(image_urls, 1):
            print(f"{url_idx}. {url}")
        print("-" * 60)

        # 添加到总列表
        all_image_urls.extend(image_urls)

    # 汇总结果
    print("\n" + "=" * 60)
    print("批量处理完成")
    print("=" * 60)

    if not all_image_urls:
        print("所有网页均未找到图片 URL")
        return

    print(f"\n总共找到 {len(all_image_urls)} 个图片 URL")

    # 保存到文件
    print(f"\n正在保存到文件 ({mode_text}模式): {OUTPUT_FILE}")
    saved_count = save_urls_to_file(all_image_urls, OUTPUT_FILE, mode=save_mode)

    if saved_count > 0:
        print(f"\n[成功] 已保存 {saved_count} 个图片 URL 到 {OUTPUT_FILE}")
    else:
        print(f"\n[完成] 没有新的 URL 被保存")

    # 显示文件总行数
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            total_lines = len([line for line in f if line.strip()])
        print(f"文件当前共有 {total_lines} 个 URL")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户取消操作")
    except Exception as e:
        print(f"\n发生错误: {e}")
