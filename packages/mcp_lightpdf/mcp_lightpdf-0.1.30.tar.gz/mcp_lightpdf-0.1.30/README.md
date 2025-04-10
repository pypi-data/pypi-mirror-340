# MCP_LightPDF

MCP_LightPDF 是一个基于 MCP (Model Control Protocol) 的文档格式转换工具，支持多种文档格式之间的相互转换。该工具需要在支持 MCP 功能的软件（如 Cursor）中配置使用。

## 配置说明

在 Cursor 中配置 MCP_LightPDF 工具需要修改 `~/.cursor/mcp.json` 文件。添加以下配置：

```json
{
  "mcpServers": {
    "lightpdf": {
      "command": "uvx",
      "args": [
        "mcp_lightpdf@latest"
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
  - `-n`: 直接运行wheel包
  - wheel包路径：指向下载的 MCP_LightPDF wheel 包
- `env`: 环境变量配置
  - `API_KEY`: 你的API密钥

配置完成后，重启 Cursor 使配置生效。

## 功能特性

- 支持多种文档格式的转换
- 支持本地文件和网络URL
- 支持批量转换
- 并发处理，提高转换效率
- 详细的转换进度和结果报告
- 灵活的输出目录配置
- PDF水印去除功能

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

### PDF水印去除
- 支持去除PDF文档中的水印
- 保持原始文档质量和格式
- 支持批量处理多个PDF文件
- 输出格式为PDF文档

## 使用方法

1. 确保你使用的软件支持 MCP 功能（如 Cursor）
2. 在软件中完成 MCP_LightPDF 工具的配置
3. 调用工具时，指定：
   - 输入文件路径或URL
   - 目标转换格式
   - 输出目录（可选）

### 格式转换
使用 `convert_document` 工具，指定输入文件和目标格式。

### 去除水印
使用 `remove_watermark` 工具，指定需要处理的PDF文件路径。工具会自动使用特殊的`doc-repair`格式处理文件，并输出为无水印的PDF文档。

## 参数说明

### 格式转换工具
- `file_paths`: 要转换的文件路径或URL列表
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

### 去除水印工具
- `file_paths`: 要处理的PDF文件路径或URL列表

## 注意事项

1. 确保有足够的磁盘空间用于文件转换
2. 对于网络URL，确保URL可访问且文件大小在合理范围内
3. 批量转换时会自动控制并发数，避免过度占用系统资源
4. 某些格式转换可能需要较长时间，请耐心等待
5. 水印去除功能仅适用于PDF格式文件
6. 复杂水印可能无法完全去除，效果取决于水印类型

## 错误处理

工具会提供详细的错误信息，常见的错误包括：

- API密钥未配置或无效
- 文件格式不支持
- 文件不存在或无法访问
- 网络连接问题
- 输出目录无写入权限

## 许可证

MIT License
