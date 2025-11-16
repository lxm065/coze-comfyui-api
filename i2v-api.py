import json
import os
from urllib import request
import re

# 定义路径
PROMPT_FILE = r"D:\pythoncode\comfyui-api-py\i2v-json\prompt\prom.txt"
TEMPLATE_JSON = r"D:\pythoncode\comfyui-api-py\i2v-json\json\video_wan2_2_14B_i2v-api-example.json"
OUTPUT_DIR = r"D:\pythoncode\comfyui-api-py\i2v-json\json"

# 从 JSON 文件读取配置
def load_template_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"加载模板 JSON 失败: {str(e)}")
        return None

# 发送请求到 ComfyUI
def queue_prompt(prompt):
    p = {"prompt": prompt}
    data = json.dumps(p).encode('utf-8')
    req = request.Request("http://127.0.0.1:8188/prompt", data=data)
    request.urlopen(req)

# 解析 prom.txt 文件
def parse_prompt_file(file_path):
    """
    解析 prom.txt 文件，返回 [(序号, 提示词), ...] 列表
    例如：6.传统中国插画风格...
    返回：[(6, "传统中国插画风格..."), ...]
    """
    prompts = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                # 匹配序号.提示词 格式
                match = re.match(r'^(\d+)\.(.+)$', line)
                if match:
                    seq_num = match.group(1)
                    prompt_text = match.group(2).strip()
                    prompts.append((seq_num, prompt_text))

        return prompts
    except Exception as e:
        print(f"读取 prom.txt 失败: {str(e)}")
        return []

# 修改 JSON 配置
def modify_json_for_prompt(template, seq_num, prompt_text):
    """
    修改 JSON 模板：
    - 节点 "93" 的 text 字段改为 prompt_text
    - 节点 "97" 的 image 字段改为 "序号.png"
    """
    modified = json.loads(json.dumps(template))  # 深拷贝

    # 修改文本提示词（节点93）
    if "93" in modified:
        modified["93"]["inputs"]["text"] = prompt_text

    # 修改图像文件名（节点97）
    if "97" in modified:
        modified["97"]["inputs"]["image"] = f"{seq_num}.png"

    return modified

# 保存修改后的 JSON
def save_json(json_data, output_path):
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存 JSON 失败: {str(e)}")
        return False

# 主流程
if __name__ == "__main__":
    # 检查文件是否存在
    if not os.path.exists(PROMPT_FILE):
        print(f"错误: 找不到文件 {PROMPT_FILE}")
        exit(1)

    if not os.path.exists(TEMPLATE_JSON):
        print(f"错误: 找不到模板文件 {TEMPLATE_JSON}")
        exit(1)

    # 加载模板 JSON
    template = load_template_json(TEMPLATE_JSON)
    if not template:
        exit(1)

    # 解析提示词文件
    prompts = parse_prompt_file(PROMPT_FILE)
    if not prompts:
        print("未找到有效的提示词")
        exit(1)

    print(f"找到 {len(prompts)} 个提示词")

    # 用字典追踪每个序号出现的次数
    seq_count = {}

    # 处理每个提示词
    for seq_num, prompt_text in prompts:
        # 更新序号计数
        if seq_num not in seq_count:
            seq_count[seq_num] = 0
        seq_count[seq_num] += 1

        current_count = seq_count[seq_num]

        print(f"\n正在处理序号 {seq_num} (第 {current_count} 次出现)...")
        print(f"提示词: {prompt_text[:50]}...")  # 只显示前50个字符

        # 修改 JSON
        modified_json = modify_json_for_prompt(template, seq_num, prompt_text)

        # 保存新的 JSON 文件 - 如果序号重复，添加后缀
        output_filename = f"video_wan2_2_14B_i2v-api-{seq_num}-{current_count}.json"
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        if not save_json(modified_json, output_path):
            print(f"序号 {seq_num}-{current_count} 保存失败，跳过")
            continue

        print(f"已保存: {output_filename}")

        # 提交到 ComfyUI API
        try:
            queue_prompt(modified_json)
            print(f"已提交到 API: {seq_num}-{current_count}")
        except Exception as e:
            print(f"提交 API 失败 (序号 {seq_num}-{current_count}): {str(e)}")

    print("\n所有任务处理完成！")
