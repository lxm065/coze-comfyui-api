import json
import os
from urllib import request

# 定义 JSON 目录路径
JSON_DIR = r"D:\pythoncode\comfyui-api-py\t2i-json\1"

# 从 JSON 文件读取配置（优化版）
def load_prompt_from_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"加载 {os.path.basename(file_path)} 失败: {str(e)}")
        return None

# 发送请求到 ComfyUI（保持不变）
def queue_prompt(prompt):
    p = {"prompt": prompt}
    data = json.dumps(p).encode('utf-8')
    req = request.Request("http://127.0.0.1:8188/prompt", data=data)
    request.urlopen(req)

# 自动设置唯一文件名（防止覆盖）
def set_unique_filename(prompt, json_filename):
    # 查找 SaveImage 节点（通常ID为"9"，按需修改）
    for node_id in prompt:
        if prompt[node_id].get("class_type") == "SaveImage":
            prompt[node_id]["inputs"]["filename_prefix"] = f"Gen_{json_filename}"
            break

# 主流程
if __name__ == "__main__":
    # 获取目录下所有 JSON 文件
    json_files = [
        f for f in os.listdir(JSON_DIR)
        if f.endswith(".json") and os.path.isfile(os.path.join(JSON_DIR, f))
    ]

    if not json_files:
        print(f"目录 {JSON_DIR} 中没有 JSON 文件")
        exit(1)

    # 遍历处理每个文件
    for json_file in json_files:
        file_path = os.path.join(JSON_DIR, json_file)
        print(f"\n正在处理: {json_file}")
        
        # 加载配置
        prompt = load_prompt_from_json(file_path)
        if not prompt:
            continue
        
        # 自动设置唯一输出文件名（可选）
        set_unique_filename(prompt, json_file.replace(".json", ""))
        
        # 可在此添加自定义修改（如动态种子）
        # prompt["3"]["inputs"]["seed"] = 新种子值
        #set the text prompt for our positive CLIPTextEncode
        #prompt["6"]["inputs"]["text"] = "masterpiece best quality man"

        # 提交任务
        try:
            queue_prompt(prompt)
            print(f"已提交: {json_file}")
        except Exception as e:
            print(f"提交失败: {json_file} -> {str(e)}")