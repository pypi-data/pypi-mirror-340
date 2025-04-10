# LightPDF AI助手 MCP Server

LightPDF AI助手 MCP Server 是一个基于 MCP (Model Control Protocol) 的文档格式转换工具，支持多种文档格式之间的相互转换以及PDF的各种处理功能。该工具需要在支持 MCP 功能的软件（如 Cursor）中配置使用。

## 配置说明

在 Cursor 中配置 LightPDF AI助手 MCP Server 工具需要修改 `~/.cursor/mcp.json` 文件。添加以下配置：

```json
{
  "mcpServers": {
    "lightpdf": {
      "command": "uvx",
      "args": [
        "lightpdf-aipdf-mcp@latest"
      ],
      "env": {
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```

配置说明：
- `command`: 使用 `uvx` 命令运行工具
- `args`: 命令行参数
  - 使用最新版的 `lightpdf-aipdf-mcp` 包
- `env`: 环境变量配置
  - `API_KEY`: 你的API密钥

配置完成后，重启 Cursor 使配置生效。

## 功能特性

- 支持多种文档格式的转换
- 支持本地文件和网络URL
- 支持批量转换
- 支持PDF文件的高级处理功能（水印去除/添加、添加页码、压缩、加密/解密等）
- 并发处理，提高转换效率
- 详细的转换进度和结果报告

## 支持的格式

### PDF转换为其他格式
- Word (DOCX)
- Excel (XLSX)
- PowerPoint (PPTX)
- 图片 (JPG, JPEG, PNG, BMP, GIF)
- HTML
- 文本 (TXT)

### 其他格式转换为PDF
- Word (DOCX)
- Excel (XLSX)
- PowerPoint (PPTX)
- 图片 (JPG, JPEG, PNG, BMP, GIF)
- CAD (DWG)
- CAJ
- OFD

## PDF处理功能

### PDF水印处理
- 支持去除PDF文档中的水印
- 支持添加自定义文本水印
- 可设置水印位置、透明度、角度和应用页面范围

### PDF页码添加
- 支持在PDF文档中添加页码
- 可自定义起始页码
- 可选择页码位置（左上、上中、右上、左下、下中、右下）
- 可设置页码边距

### PDF编辑功能
- **拆分PDF**: 支持按页码范围拆分，或每页生成一个新文件
- **合并PDF**: 将多个PDF文件合并为一个
- **旋转PDF**: 支持90°、180°、270°旋转，可指定页面范围
- **压缩PDF**: 优化PDF文件大小，可调整图像质量

### PDF安全功能
- **加密PDF**: 添加密码保护
- **解密PDF**: 移除密码保护（需提供原密码）

## 使用方法

1. 确保你使用的软件支持 MCP 功能（如 Cursor）
2. 在软件中完成 LightPDF AI助手 MCP Server 工具的配置
3. 调用相应的工具，指定输入文件和所需参数
4. 处理完成后，系统会提供结果文件的在线下载链接

### 格式转换
使用 `convert_document` 工具，指定输入文件和目标格式。

### PDF处理功能
- 去除水印: `remove_watermark`
- 添加水印: `add_watermark`
- 添加页码: `add_page_numbers`
- 拆分PDF: `split_pdf`
- 合并PDF: `merge_pdfs`
- 旋转PDF: `rotate_pdf`
- 压缩PDF: `compress_pdf`
- 加密PDF: `protect_pdf`
- 解密PDF: `unlock_pdf`

## 参数说明

### 格式转换工具 (convert_document)
- `files`: 要转换的文件对象列表
  - `path`: 文件路径或URL
  - `password`: 文档密码（如有）
- `format`: 目标格式，支持：
  - `pdf`: 转换为PDF格式
  - `docx`: 转换为Word格式
  - `xlsx`: 转换为Excel格式
  - `pptx`: 转换为PowerPoint格式
  - `jpg`/`jpeg`: 转换为JPG格式
  - `png`: 转换为PNG格式
  - `bmp`: 转换为BMP格式
  - `gif`: 转换为GIF格式
  - `html`: 转换为HTML格式
  - `txt`: 转换为文本格式

### 去除水印工具 (remove_watermark)
- `files`: 要处理的PDF文件对象列表
  - `path`: 文件路径或URL
  - `password`: 文档密码（如有）

### 添加水印工具 (add_watermark)
- `files`: 要处理的PDF文件对象列表
- `text`: 水印文本内容
- `position`: 水印位置，可选值包括"center"、"topleft"等
- `opacity`: 透明度（0.0-1.0）
- `deg`: 旋转角度
- `range`: 页面范围，如 "1,3,5-7"
- `layout`: 水印显示位置，"on"（在内容上）或"under"（在内容下）
- 可选的字体设置: `font_family`、`font_size`、`font_color`

### 添加页码工具 (add_page_numbers)
- `files`: 要处理的PDF文件对象列表
- `start_num`: 起始页码，默认为1
- `position`: 页码位置（1-6），对应左上/上中/右上/左下/下中/右下
- `margin`: 页码边距，可选值为10/30/60，默认为30

### 拆分PDF工具 (split_pdf)
- `files`: 要处理的PDF文件对象列表
- `split_type`: 拆分类型
  - `every`: 每页拆分为一个文件
  - `page`: 按页面规则拆分（默认）
- `pages`: 拆分页面规则，如 "1,3,5-7"
- `merge_all`: 是否合并拆分后的文件（0=否，1=是）

### 合并PDF工具 (merge_pdfs)
- `files`: 要合并的PDF文件对象列表（至少两个文件）

### 旋转PDF工具 (rotate_pdf)
- `files`: 要处理的PDF文件对象列表
- `angle`: 旋转角度，可选值为90、180、270
- `pages`: 页面范围，如 "1,3,5-7"

### 压缩PDF工具 (compress_pdf)
- `files`: 要处理的PDF文件对象列表
- `image_quantity`: 图像质量（1-100），值越低压缩率越高，默认为60

### 加密PDF工具 (protect_pdf)
- `files`: 要处理的PDF文件对象列表
- `password`: 要设置的新密码

### 解密PDF工具 (unlock_pdf)
- `files`: 要处理的PDF文件对象列表
  - `path`: 文件路径或URL
  - `password`: 文档的当前密码（必需）

## 注意事项

1. 确保有足够的磁盘空间用于文件转换
2. 对于网络URL，确保URL可访问且文件大小在合理范围内
3. 批量转换时会自动控制并发数，避免过度占用系统资源
4. 某些格式转换可能需要较长时间，请耐心等待
5. 水印去除功能仅适用于PDF格式文件
6. 复杂水印可能无法完全去除，效果取决于水印类型
7. 所有PDF编辑功能只支持PDF格式的输入文件

## 错误处理

工具会提供详细的错误信息，常见的错误包括：

- API密钥未配置或无效
- 文件格式不支持
- 文件不存在或无法访问
- 网络连接问题
- PDF密码不正确或文件受保护
