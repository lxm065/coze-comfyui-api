# ComfyUI API 工具集

这是一个用于调用 ComfyUI API 和 Coze AI 服务的 Python 工具集合。

## 项目结构

```
comfyui-api-py/
├── t2i-api.py              # 文字转图片 API 脚本
├── i2v-api.py              # 图片转视频 API 脚本
├── coze_url_pic.py         # Coze AI 图片分析 API 脚本
├── t2i-json/               # 文字转图片 JSON 配置目录
├── i2v-json/               # 图片转视频配置目录
│   ├── json/               # JSON 模板文件
│   └── prompt/             # 提示词文件
└── coze_i2v/               # Coze AI 输入输出目录
    ├── url_pic.txt         # 图片 URL 列表（输入）
    ├── content.txt         # 提取的文本内容（输出）
    └── Positive_Prompt.txt # 生成的提示词（输出）
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

### 3. coze_url_pic.py - Coze AI 图片分析工具（新增）

**功能**：批量调用 Coze AI Workflow API，分析图片并提取文本内容和生成正面提示词。

**使用方法**：

```bash
python coze_url_pic.py
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

### 完整的图片分析 → 视频生成流程

1. **准备图片 URL 列表**
   ```bash
   # 编辑 coze_i2v/url_pic.txt
   http://example.com/image1.jpg
   http://example.com/image2.jpg
   ```

2. **调用 Coze AI 分析图片**
   ```bash
   python coze_url_pic.py
   ```
   输出：
   - `coze_i2v/content.txt` - 识别的文本
   - `coze_i2v/Positive_Prompt.txt` - 生成的提示词

3. **将提示词整理到 prom.txt**
   ```bash
   # 从 Positive_Prompt.txt 复制内容到 i2v-json/prompt/prom.txt
   # 格式化为序号格式
   ```

4. **生成视频**
   ```bash
   python i2v-api.py
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

### v1.1.0 (2025-11-16)
- 新增 `coze_url_pic.py` - Coze AI 图片分析工具
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
