description: Read and extract content from Feishu (Lark) documents using the ZhiYan platform API with advanced features like secure token management, logging, image localization, and markdown export.

User Input
$ARGUMENTS

## Overview

The Feishu Reader skill extracts content from Feishu documents (docx and wiki formats) using the ZhiYan platform API. It provides secure token management, comprehensive logging, image localization, and markdown export capabilities.

## Usage

### Basic Usage
- Provide a Feishu document URL to extract and read content
- Supports URLs starting with `https://li.feishu.cn/docx/` or `https://li.feishu.cn/wiki/`

### Advanced Features
- **Secure Token Management**: Tokens encrypted and stored locally with proper permissions
- **Detailed Logging**: Complete task history with processing statistics
- **Image Localization**: Download and convert remote images to local files
- **Markdown Export**: Save extracted content as organized markdown files
- **Task Management**: View history, success rates, and processing statistics

## Parameters

- `url`: Feishu document URL (required for basic usage)
- `save`: Save content as markdown file (boolean, default: false)
- `localize_images`: Download and localize images (boolean, default: false)
- `history`: Show task history (boolean, default: false)
- `stats`: Show processing statistics (boolean, default: false)
- `test_mode`: Use test API environment (boolean, default: true)

## Implementation

The skill follows this execution flow:

1. **Input Validation**: Parse and validate Feishu document URL format
2. **Configuration Setup**: Initialize secure token management system
3. **Task Submission**: Submit document extraction task to ZhiYan API
4. **Status Monitoring**: Poll task status until completion or timeout
5. **Content Retrieval**: Download extracted content when ready
6. **Image Processing**: Optionally download and localize images
7. **File Export**: Optionally save content as markdown file
8. **Logging**: Record complete task lifecycle and statistics

## API Integration

**Service**: ZhiYan Platform Document Extraction API
**Endpoints**:
- Test: `https://cfe-doc-backend-test.inner.chj.cloud/openapi`
- Production: `https://cfe-doc-backend.inner.chj.cloud/openapi`

**Task Lifecycle**:
1. POST `/v1/extract/task/submit` - Submit extraction task
2. GET `/v1/extract/task/status` - Monitor task progress
3. GET `/v1/extract/task/{task_id}` - Retrieve results

## File Structure

When installed, the skill creates:
```
~/.claude/feishu/
├── config.json (encrypted token storage)
└── logs/
    └── feishu_tasks_YYYYMM.json (monthly task logs)

./feishu_docs/
├── document_name_extracted_YYYYMMDD_HHMMSS.md
├── document_name_localized_YYYYMMDD_HHMMSS.md
└── images/
    ├── document_YYYYMMDD_HHMMSS_hash.jpg
    └── document_YYYYMMDD_HHMMSS_hash.png
```

## Security Features

- **Token Encryption**: Tokens stored with SHA256 hash keys
- **File Permissions**: Config files set to 0o600 (user read/write only)
- **Multiple Services**: Support for different service tokens
- **Non-interactive Mode**: Automatic token handling for automation

## Error Handling

- **URL Validation**: Comprehensive Feishu URL format checking
- **API Errors**: Detailed error reporting and retry mechanisms
- **Timeout Handling**: Configurable polling with maximum retry limits
- **File System**: Safe file operations with proper error handling

## Usage Examples

```bash
# Basic document reading
skill: "feishu_reader" with url="https://li.feishu.cn/docx/document_id"

# Save as markdown with image localization
skill: "feishu_reader" with url="https://li.feishu.cn/wiki/page_id" save=true localize_images=true

# View task history and statistics
skill: "feishu_reader" with history=true
skill: "feishu_reader" with stats=true

# Production environment
skill: "feishu_reader" with url="https://li.feishu.cn/docx/document_id" test_mode=false
```

## Dependencies

- Python 3.7+
- requests library
- pathlib, json, os, sys, time, re, hashlib (standard library)
- argparse for command-line interface

## Return Value

Returns a dictionary containing:
```python
{
    'task_id': str,
    'doc_name': str,
    'doc_url': str,
    'content': str,
    'content_length': int,
    'images_count': int,
    'saved_path': str,
    'status': str,
    'processing_time': float,
    'created_at': str
}
```