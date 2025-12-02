def add_numbering():
    """
    为 coze_i2v/Positive_Prompt.txt 中的每段内容添加递增序号前缀
    格式：序号.内容
    """
    input_file = "coze_i2v/Positive_Prompt.txt"
    output_file = "coze_i2v/Positive_Prompt_numbered.txt"

    try:
        # 获取起始序号
        while True:
            try:
                start_num = int(input("请输入起始序号（例如 58）: "))
                if start_num > 0:
                    break
                else:
                    print("请输入大于0的数字！")
            except ValueError:
                print("请输入有效的数字！")

        # 读取原文件
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 添加序号
        numbered_lines = []
        current_num = start_num
        for line in lines:
            # 只处理非空行
            if line.strip():
                numbered_line = f"{current_num}.{line}"
                numbered_lines.append(numbered_line)
                current_num += 1
            else:
                # 保留空行
                numbered_lines.append(line)

        # 写入新文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(numbered_lines)

        # 显示处理结果
        total_numbered = current_num - start_num
        print(f"\n[OK] 处理完成!")
        print(f"  原文件: {input_file}")
        print(f"  新文件: {output_file}")
        print(f"  起始序号: {start_num}")
        print(f"  结束序号: {current_num - 1}")
        print(f"  共处理: {total_numbered} 段")

        # 显示前3段对比
        print("\n处理前后对比 (前3段):")
        count = 0
        for i, line in enumerate(lines):
            if line.strip() and count < 3:
                print(f"\n--- 第 {count + 1} 段 ---")
                print(f"原文: {line.strip()[:80]}...")
                print(f"处理后: {numbered_lines[i].strip()[:80]}...")
                count += 1
            if count >= 3:
                break

    except FileNotFoundError:
        print(f"错误: 找不到文件 {input_file}")
    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    import sys

    # 检查是否有命令行参数
    if len(sys.argv) > 1:
        try:
            start_num = int(sys.argv[1])
            if start_num <= 0:
                print("错误: 起始序号必须大于0")
                sys.exit(1)

            # 使用命令行参数的起始序号
            input_file = "coze_i2v/Positive_Prompt.txt"
            output_file = "coze_i2v/Positive_Prompt_numbered.txt"

            with open(input_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            numbered_lines = []
            current_num = start_num
            for line in lines:
                if line.strip():
                    numbered_line = f"{current_num}.{line}"
                    numbered_lines.append(numbered_line)
                    current_num += 1
                else:
                    numbered_lines.append(line)

            with open(output_file, 'w', encoding='utf-8') as f:
                f.writelines(numbered_lines)

            total_numbered = current_num - start_num
            print(f"\n[OK] 处理完成!")
            print(f"  原文件: {input_file}")
            print(f"  新文件: {output_file}")
            print(f"  起始序号: {start_num}")
            print(f"  结束序号: {current_num - 1}")
            print(f"  共处理: {total_numbered} 段")

        except ValueError:
            print("错误: 请提供有效的数字作为起始序号")
            print("用法: python prompt_clear.py 58")
            sys.exit(1)
        except FileNotFoundError:
            print(f"错误: 找不到文件 {input_file}")
            sys.exit(1)
        except Exception as e:
            print(f"错误: {e}")
            sys.exit(1)
    else:
        # 交互模式
        add_numbering()
