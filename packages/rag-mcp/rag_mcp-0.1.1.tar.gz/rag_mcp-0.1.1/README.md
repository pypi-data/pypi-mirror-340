# RAG MCP: Document Processing Server

A Retrieval-Augmented Generation (RAG) server built on the Model Context Protocol (MCP) for intelligent document processing and question answering.

## Overview

RAG MCP is a tool that allows you to index various document formats and perform semantic searches against them. It uses advanced embedding techniques and vector databases to make your documents searchable through natural language queries.

## Features

- **Document Indexing**: Support for various document formats (PDF, DOCX, XLSX, PPTX, Markdown, AsciiDoc, HTML, XHTML, CSV)
- **Semantic Search**: Query your documents using natural language
- **High Performance**: Optimized for various hardware configurations with automatic device selection (CUDA, MPS, CPU)
- **Persistent Storage**: Vector embeddings are stored locally for future use

## Requirements

- Python 3.11+
- Environment with access to your documents

## Installation

### 1. Install UV

First, you need to install UV, a Python package installer and resolver:

#### On macOS/Linux:
```bash
curl -sSf https://astral.sh/uv/install.sh | sh
```

#### On Windows:
```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Run RAG MCP

Once UV is installed, you can run RAG MCP directly using:

```bash
uvx rag-mcp
```

This will start the MCP server and make it available for document processing.

## IDE Integration

### VS Code Integration

To integrate with Visual Studio Code, create a `mcp.json` file with the following content:

```json
{
    "servers": {
        "rag-mcp-server": {
            "type": "stdio",
            "command": "uvx",
            "args": [
                "rag-mcp"
            ],
            "env": {
                "PERSIST_DIRECTORY": "/path/to/your/persist/directory"
            }
        }
    }
}
```

Replace `/path/to/your/persist/directory` with the directory where you want to store your vector database.

### Cursor Integration

To integrate with Cursor, go to Cursor Settings > MCP and paste this configuration:

```json
{
    "mcpServers": {
        "rag-mcp": {
            "command": "cmd",
            "args": [
                "/c",
                "uvx",
                "rag-mcp"
            ],
            "env": {
                "PERSIST_DIRECTORY": "/path/to/your/persist/directory"
            }
        }
    }
}
```


## Usage


## Supported Embedding Models

The system supports two types of embedding models:

1. **HuggingFace BGE Embeddings** (default): High-quality embeddings that work offline
   - Uses BAAI/bge-m3 model


## How It Works

1. **Document Loading**: Uses DoclingLoader to parse various document formats
2. **Text Splitting**: Documents are split into manageable chunks using RecursiveCharacterTextSplitter
3. **Embedding Generation**: Text chunks are converted to vector embeddings
4. **Storage**: Embeddings are stored in a Chroma vector database
5. **Retrieval**: When queried, the system finds semantically similar content to answer questions

## Advanced Configuration

You can customize chunk size, overlap, and other parameters by modifying the code in `document_server.py`.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Specify your license here]

## Acknowledgments

- This project uses [LangChain](https://www.langchain.com/) and [Docling](https://github.com/docling-project/docling) for intelligent document parsing
- Vector storage provided by [Chroma](https://www.trychroma.com/)
- Embedding models from [HuggingFace](https://huggingface.co/)
- Built on the [Model Context Protocol](https://github.com/microsoft/model-context-protocol) (MCP)
