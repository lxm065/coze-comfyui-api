# ComfyUI API 工具集

这是一个用于调用 ComfyUI API 和 Coze AI 服务的 Python 工具集合。

## 项目结构

```
comfyui-api-py/
├── t2i-api.py                    # 文字转图片 API 脚本
├── i2v-api.py                    # 图片转视频 API 脚本
├── i2v-api-coze.py               # Coze 提示词转视频 API 脚本
├── get_prome_url_pic-coze.py     # Coze AI 图片分析 API 脚本
├── find_pic_url_add_coze.py      # 网页图片 URL 提取工具（支持批量）
├── t2i-json/                     # 文字转图片 JSON 配置目录
├── i2v-json/                     # 图片转视频配置目录
│   ├── json/                     # JSON 模板文件
│   └── prompt/                   # 提示词文件
└── coze_i2v/                     # Coze AI 输入输出目录
    ├── url_pic.txt               # 图片 URL 列表（输入）
    ├── content.txt               # 提取的文本内容（输出）
    ├── Positive_Prompt.txt       # 生成的提示词（输出）
    └── json/                     # 视频生成 JSON 配置
```

## 功能说明

### 1. t2i-api.py - 文字转图片批量生成

**功能**：批量读取 JSON 配置文件，调用 ComfyUI API 生成图片。

**使用方法**：

```bash
python t2i-api.py
```

**配置**：
- JSON 目录：`D:\pythoncode\comfyui-api-py\t2i-json\1`
- ComfyUI API：`http://127.0.0.1:8188/prompt`

**特点**：
- 自动遍历目录下所有 JSON 文件
- 自动设置唯一文件名防止覆盖
- 支持 SaveImage 节点自动命名

---

### 2. i2v-api.py - 图片转视频批量生成

**功能**：从提示词文件读取内容，使用模板 JSON 批量生成视频。

**使用方法**：

```bash
python i2v-api.py
```

**配置**：
- 提示词文件：`D:\pythoncode\comfyui-api-py\i2v-json\prompt\prom.txt`
- 模板 JSON：`D:\pythoncode\comfyui-api-py\i2v-json\json\video_wan2_2_14B_i2v-api-example.json`
- ComfyUI API：`http://127.0.0.1:8188/prompt`

**提示词格式**：
```
1.传统中国插画风格...
2.古代市集场景...
3.水墨画风格人物...
```

**特点**：
- 自动解析序号格式的提示词
- 动态替换模板中的 prompt 字段
- 支持批量生成并自动命名

---

### 3. find_pic_url_add_coze.py - 网页图片 URL 提取工具（支持批量）

**功能**：从网页中提取图片 URL 并保存到文件，支持批量处理多个网页。

**使用方法**：

**交互模式**：
```bash
python find_pic_url_add_coze.py
```
然后输入多个 URL（用逗号分隔）：
```
请输入网页 URL: http://example.com/page1, http://example.com/page2, http://example.com/page3
```

**命令行模式**：
```bash
python find_pic_url_add_coze.py "http://example.com/page1, http://example.com/page2" 1
```

**输出文件**：`coze_i2v/url_pic.txt`

**特点**：
- ✅ **批量处理**：支持同时处理多个网页 URL，用逗号分隔
- ✅ **智能提取**：自动识别 `<a href>`、`<img src>`、`data-src` 等多种图片链接格式
- ✅ **URL 拼接**：自动将相对路径转换为完整 URL
- ✅ **自动去重**：避免重复添加已存在的 URL
- ✅ **进度显示**：显示每个网页的处理进度和结果
- ✅ **错误处理**：格式错误或无法访问的 URL 会跳过并继续处理

**支持的图片格式**：
- jpg, jpeg, png, gif, webp

**保存模式**：
- 追加模式（默认）：添加到现有文件末尾
- 覆盖模式：清空文件后写入

**批量处理示例**：
```bash
# 同时处理 3 个网页
python find_pic_url_add_coze.py "http://site.com/page1, http://site.com/page2, http://site.com/page3"

# 输出示例：
# 共找到 3 个网页 URL 待处理
# [1/3] 处理第一个网页 -> 找到 15 张图片
# [2/3] 处理第二个网页 -> 找到 20 张图片
# [3/3] 处理第三个网页 -> 找到 18 张图片
# 总共找到 53 个图片 URL
```

---

### 4. get_prome_url_pic-coze.py - Coze AI 图片分析工具

**功能**：批量调用 Coze AI Workflow API，分析图片并提取文本内容和生成正面提示词。

**使用方法**：

```bash
python get_prome_url_pic-coze.py
```

**输入文件**：`coze_i2v/url_pic.txt`
```
http://www.laohuabao.com/x/3/jzy/12.jpg
http://www.laohuabao.com/x/z/qzhk-1982-2/smallpic/18138clip-20522579325.jpg
```

**输出文件**：
- `coze_i2v/content.txt` - 图片中识别的文本内容
- `coze_i2v/Positive_Prompt.txt` - AI 生成的图片描述提示词

**API 配置**：
- API URL：`https://api.coze.cn/v1/workflow/run`
- Workflow ID：`7572759395747250214`
- Token：配置在脚本中的 `BEARER_TOKEN` 变量

**特点**：
- 自动读取 URL 列表批量处理
- 多层 JSON 解析自动提取数据
- 进度显示和错误处理
- 支持中文内容和提示词导出

**返回数据示例**：
```json
{
  "data": "{\"output\":\"{\\\"Positive_Prompt\\\":\\\"Traditional Chinese...\\\",\\\"content\\\":\\\"图片中的文字内容\\\"}\"}",
  "code": 0,
  "msg": ""
}
```

**使用场景**：
- 批量分析古籍、插画图片
- 提取图片中的文字内容
- 生成 AI 绘画的正面提示词
- 图片转视频的前置处理

---

### 5. i2v-api-coze.py - Coze 提示词转视频批量生成

**功能**：读取 Coze AI 生成的提示词文件，批量生成视频配置并提交到 ComfyUI。

**使用方法**：

```bash
python i2v-api-coze.py
```

**配置**：
- 提示词文件：`coze_i2v/Positive_Prompt.txt`
- 模板 JSON：`coze_i2v/json/video_wan2_2_14B_i2v-api-example.json`
- 输出目录：`coze_i2v/json/`
- ComfyUI API：`http://127.0.0.1:8188/prompt`

**提示词格式**：
```
74.Traditional Chinese black and white line drawing...
75.Traditional Chinese classical illustration style...
76.Traditional Chinese black ink illustration...
```

**特点**：
- 自动解析 "序号.提示词" 格式
- 动态替换模板中的文本提示词和图片文件名
- 生成的 JSON 文件命名：`video_wan2_2_14B_i2v-api-{序号}-{次数}.json`
- 自动提交到 ComfyUI API 进行视频生成

**工作流程**：
1. 读取 `Positive_Prompt.txt` 中的提示词
2. 使用模板 JSON 生成配置文件
3. 修改节点 93（text）为提示词内容
4. 修改节点 97（image）为对应序号的图片
5. 保存 JSON 并提交到 ComfyUI API

---

## 环境要求

### Python 版本
- Python 3.6+

### 依赖安装

```bash
pip install requests
```

### ComfyUI 要求
- ComfyUI 需在本地运行
- 默认端口：`8188`
- API 端点：`http://127.0.0.1:8188/prompt`

---

## 使用流程示例

### 完整的网页图片 → AI 分析 → 视频生成流程

**流程图**：
```
网页 URL → find_pic_url_add_coze.py → url_pic.txt
         → get_prome_url_pic-coze.py → Positive_Prompt.txt + content.txt
         → i2v-api-coze.py → 视频生成
```

**详细步骤**：

1. **从网页提取图片 URL（支持批量）**
   ```bash
   python find_pic_url_add_coze.py
   # 输入多个网页 URL（用逗号分隔）：
   # http://example.com/page1, http://example.com/page2
   ```
   输出：`coze_i2v/url_pic.txt` - 包含所有提取的图片 URL

2. **调用 Coze AI 分析图片**
   ```bash
   python get_prome_url_pic-coze.py
   ```
   输出：
   - `coze_i2v/content.txt` - 识别的文本内容
   - `coze_i2v/Positive_Prompt.txt` - AI 生成的图片描述提示词

3. **生成视频配置并提交 ComfyUI**
   ```bash
   python i2v-api-coze.py
   ```
   自动：
   - 读取 `Positive_Prompt.txt` 中的提示词
   - 生成 JSON 配置文件到 `coze_i2v/json/`
   - 提交到 ComfyUI API 进行视频生成

### 单独使用示例

**仅提取图片 URL**：
```bash
# 批量提取多个网页的图片
python find_pic_url_add_coze.py "http://site.com/p1, http://site.com/p2, http://site.com/p3"
```

**仅分析图片**：
```bash
# 准备好 url_pic.txt 后
python get_prome_url_pic-coze.py
```

**使用现有提示词生成视频**：
```bash
# 编辑好 Positive_Prompt.txt 后
python i2v-api-coze.py
```

---

## 常见问题

### Q1: ComfyUI 连接失败
**A**: 确保 ComfyUI 正在运行，端口为 8188

### Q2: Coze API 调用失败
**A**: 检查网络连接和 Bearer Token 是否有效

### Q3: 输出文件乱码
**A**: 脚本已使用 UTF-8 编码，如果查看时乱码请使用支持 UTF-8 的编辑器

### Q4: 批量处理中断
**A**: 脚本会跳过失败的项继续处理，检查控制台输出查看具体错误信息

---

## 更新日志

### v1.2.0 (2025-11-16)
- ✨ **新增批量处理功能**：`find_pic_url_add_coze.py` 支持批量处理多个网页 URL（用逗号分隔）
- 🔄 **重命名脚本**：
  - `coze_i2v-api.py` → `i2v-api-coze.py`
  - `coze_url_pic.py` → `get_prome_url_pic-coze.py`
  - `url_down_pic_add.py` → `find_pic_url_add_coze.py`
- 📝 更新 Positive_Prompt.txt 提示词（79-88 号）
- 🛠️ 完善错误处理和进度显示

### v1.1.0 (2025-11-16)
- 新增 `get_prome_url_pic-coze.py` - Coze AI 图片分析工具
- 新增 `find_pic_url_add_coze.py` - 网页图片 URL 提取工具
- 新增 `i2v-api-coze.py` - Coze 提示词转视频工具
- 支持批量 URL 处理
- 自动提取图片文本内容和生成提示词
- 完善错误处理和进度显示

### v1.0.0
- 初始版本
- t2i-api.py - 文字转图片
- i2v-api.py - 图片转视频

---

## 许可证

本项目仅供学习和研究使用。

## 联系方式

如有问题或建议，请提交 Issue。
