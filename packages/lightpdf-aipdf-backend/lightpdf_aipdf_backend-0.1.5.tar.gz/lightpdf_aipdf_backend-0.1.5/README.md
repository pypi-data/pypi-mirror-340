# LightPDF AI-PDF Backend

这是LightPDF AI-PDF的后端API服务。

## 安装

使用uv安装：

```bash
uv pip install -e .
```

或者构建并安装：

```bash
uv build
uv pip install dist/*.whl
```

## 配置

有两种配置方式：

### 1. 使用.env文件（开发环境）

创建一个`.env`文件，包含以下环境变量：

```
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini
OPENAI_BASE_URL=https://api.openai.com/v1
# 其他必要的环境变量
```

注意：`.env`文件不会包含在构建包中，需要在部署环境中手动创建。

### 2. 使用环境变量（生产环境）

直接设置环境变量：

```bash
export OPENAI_API_KEY=your_openai_api_key
export OPENAI_MODEL=gpt-4o-mini
export OPENAI_BASE_URL=https://api.openai.com/v1
# 设置其他必要的环境变量
```

## 使用方法

安装后，可以通过以下命令启动服务器：

```bash
lightpdf-aipdf-server
```

也可以作为模块运行：

```bash
python -m lightpdf_aipdf_backend
```

## 开发

安装开发依赖：

```bash
uv pip install -e ".[dev]"
```