import requests
import json
import os

# API 配置
API_URL = "https://api.coze.cn/v1/workflow/run"
WORKFLOW_ID = "7572759395747250214"
BEARER_TOKEN = "pat_4LxLYyrg7MstHUZ4Lwnz8VE5Tr7w67dkoXFzlofUGHrFIYAUm8kWmT2rcvUi4qNl"

# 文件路径配置
URL_PIC_FILE = "coze_i2v/url_pic.txt"
CONTENT_OUTPUT_FILE = "coze_i2v/content.txt"
PROMPT_OUTPUT_FILE = "coze_i2v/Positive_Prompt.txt"

def call_coze_api(image_url):
    """调用 Coze API"""
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "workflow_id": WORKFLOW_ID,
        "parameters": {
            "input_url": image_url
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API 调用失败: {e}")
        return None

def parse_response(response_data):
    """解析 API 返回数据，提取 content 和 Positive_Prompt"""
    try:
        if not response_data or response_data.get("code") != 0:
            print(f"API 返回错误: {response_data.get('msg', 'Unknown error')}")
            return None, None

        # 第一层解析：获取 data 字段（是一个 JSON 字符串）
        data_str = response_data.get("data", "")
        data_obj = json.loads(data_str)

        # 第二层解析：获取 output 字段（也是一个 JSON 字符串）
        output_str = data_obj.get("output", "")
        output_obj = json.loads(output_str)

        # 第三层解析：获取最终的 content 和 Positive_Prompt
        content = output_obj.get("content", "")
        positive_prompt = output_obj.get("Positive_Prompt", "")

        return content, positive_prompt
    except (json.JSONDecodeError, KeyError) as e:
        print(f"数据解析失败: {e}")
        return None, None

def main():
    """主函数"""
    # 确保输出目录存在
    os.makedirs("coze_i2v", exist_ok=True)

    # 检查输入文件是否存在
    if not os.path.exists(URL_PIC_FILE):
        print(f"错误: 文件 {URL_PIC_FILE} 不存在")
        return

    # 读取图片 URL 列表
    with open(URL_PIC_FILE, 'r', encoding='utf-8') as f:
        image_urls = [line.strip() for line in f if line.strip()]

    if not image_urls:
        print("错误: 没有找到图片 URL")
        return

    print(f"共找到 {len(image_urls)} 个图片 URL")

    # 存储所有结果
    all_contents = []
    all_prompts = []

    # 处理每个图片 URL
    for idx, image_url in enumerate(image_urls, 1):
        print(f"\n[{idx}/{len(image_urls)}] 处理图片: {image_url}")

        # 调用 API
        response_data = call_coze_api(image_url)
        if not response_data:
            print(f"  跳过该图片")
            continue

        # 解析数据
        content, positive_prompt = parse_response(response_data)
        if content is None or positive_prompt is None:
            print(f"  跳过该图片")
            continue

        # 保存结果
        all_contents.append(content)
        all_prompts.append(positive_prompt)

        print(f"  Content: {content[:50]}...")
        print(f"  Prompt: {positive_prompt[:50]}...")

    # 写入文件
    if all_contents:
        with open(CONTENT_OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(all_contents))
        print(f"\n[OK] Content 已保存到: {CONTENT_OUTPUT_FILE}")

    if all_prompts:
        with open(PROMPT_OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(all_prompts))
        print(f"[OK] Positive_Prompt 已保存到: {PROMPT_OUTPUT_FILE}")

    print(f"\n处理完成！成功处理 {len(all_contents)} 个图片")

if __name__ == "__main__":
    main()
