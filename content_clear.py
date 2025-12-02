import re

def clean_content(overwrite=False):
    """
    读取 coze_i2v/content.txt 文件，去除行首的数字编号
    格式：行号→数字编号 内容  =>  内容

    参数:
        overwrite: 是否覆盖原文件 (默认False，生成新文件)
    """
    input_file = "coze_i2v/content.txt"
    output_file = input_file if overwrite else "coze_i2v/content_cleaned.txt"

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        cleaned_lines = []
        for line in lines:
            # 使用正则表达式匹配并去除行首的编号部分
            # 匹配模式：开头的任意空白字符 + 数字 + tab + 数字 + 空格
            # Read工具显示的→实际上是tab制表符\t
            cleaned_line = re.sub(r'^\s*\d+\t\d+\s+', '', line)
            # 如果仍有内容且行首是数字+空格，也去除
            cleaned_line = re.sub(r'^\d+\s+', '', cleaned_line)
            cleaned_lines.append(cleaned_line)

        # 写入清理后的内容到新文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(cleaned_lines)

        print(f"[OK] 处理完成!")
        print(f"  原文件: {input_file}")
        print(f"  新文件: {output_file}")
        print(f"  共处理 {len(cleaned_lines)} 行")

        # 显示前3行对比
        print("\n处理前后对比 (前3行):")
        for i in range(min(3, len(lines))):
            print(f"\n原文: {lines[i].strip()}")
            print(f"处理后: {cleaned_lines[i].strip()}")

    except FileNotFoundError:
        print(f"错误: 找不到文件 {input_file}")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    import sys

    # 检查命令行参数
    overwrite = False
    if len(sys.argv) > 1 and sys.argv[1] in ['-o', '--overwrite']:
        overwrite = True
        print("警告: 将覆盖原文件!")

    clean_content(overwrite=overwrite)
