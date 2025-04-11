# 🤖 Revenium Middleware for LiteLLM

[![PyPI version](https://img.shields.io/pypi/v/revenium-middleware-litellm.svg)](https://pypi.org/project/revenium-middleware-litellm/)
[![Python Versions](https://img.shields.io/pypi/pyversions/revenium-middleware-litellm.svg)](https://pypi.org/project/revenium-middleware-litellm/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

A middleware library for metering and monitoring LiteLLM proxy usage in Python applications. 🐍✨

## ✨ Features

- **📊 Precise Usage Tracking**: Monitor tokens, costs, and request counts across all LLM API endpoints
- **🔌 Seamless Integration**: Custom callback middleware that works with minimal configuration
- **⚙️ Flexible Configuration**: Customize metering behavior to suit your application needs

## 📥 Installation

```bash
pip install -e revenium-middleware-litellm
```

## 🔧 Usage

### 🔄 Integration with LiteLLM Proxy

To integrate the Revenium middleware with your LiteLLM proxy, you need to:

1. Install the middleware
2. Configure your LiteLLM proxy to use the Revenium middleware callback

#### Configuration

Add the Revenium middleware to your LiteLLM config.yaml:

```yaml
model_list:
  - model_name: o3-mini
    litellm_params:
      model: openai/o3-mini
      api_key: "os.environ/OPENAI_API_KEY"

general_settings:
  store_model_in_db: true
  store_prompts_in_spend_logs: true

litellm_settings:
  master_key: "sk-1234"
  salt_key: "sk-1234"
  database_url: "postgresql://user:password@localhost/litellm"
  callbacks: /absolute/path/to/revenium-middleware-litellm/litellm_proxy/middleware.proxy_handler_instance
```

> **⚠️ Important Note**: LiteLLM proxies require the `callbacks` parameter to be the **absolute path** to the Python file. Relative paths will not work. Make sure to provide the full path to the middleware.py file in your installation.

### 📈 Enhanced Tracking with Custom Headers

For more granular usage tracking and detailed reporting, add custom HTTP headers to your LiteLLM requests:

```python
import litellm

response = litellm.completion(
    model="o3-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the meaning of life?"}
    ],
    metadata={
        "headers": {
            "x-revenium-trace-id": "conv-28a7e9d4-1c3b-4e5f-8a9b-7d1e3f2c1b4a",
            "x-revenium-task-id": "chat-summary-af23c910",
            "x-revenium-task-type": "text-classification",
            "x-revenium-organization-id": "acme-corporation-12345",
            "x-revenium-subscription-id": "startup-plan-quarterly-2025-Q1",
            "x-revenium-product-id": "intelligent-document-processor-v3",
            "x-revenium-agent": "customer-support-assistant-v2"
        }
    }
)
```

#### 🏷️ Custom HTTP Headers

The following custom HTTP headers can be added to your API requests:

| Field | Description | Use Case |
|-------|-------------|----------|
| `x-revenium-trace-id` | Unique identifier for a conversation or session | Track multi-turn conversations |
| `x-revenium-task-id` | Identifier for a specific AI task | Group related API calls for a single task |
| `x-revenium-task-type` | Classification of the AI operation | Categorize usage by purpose (e.g., classification, summarization) |
| `x-revenium-organization-id` | Customer or department identifier | Allocate costs to business units |
| `x-revenium-subscription-id` | Reference to a billing plan | Associate usage with specific subscriptions |
| `x-revenium-product-id` | The product or feature using AI | Track usage across different products |
| `x-revenium-agent` | Identifier for the specific AI agent | Compare performance across different AI agents |

All custom headers are optional. Adding them to your API requests enables more detailed reporting and analytics in Revenium.

## 🔄 Compatibility

- 🐍 Python 3.8+
- 🤖 LiteLLM 
- 🌐 Works with all LLM models and endpoints supported by LiteLLM

## 🔍 Logging

This module uses Python's standard logging system. You can control the log level by setting the `REVENIUM_LOG_LEVEL` environment variable:

```bash
# Enable debug logging
export REVENIUM_LOG_LEVEL=DEBUG

# Or when running your script
REVENIUM_LOG_LEVEL=DEBUG python your_script.py
```

Available log levels:
- `DEBUG`: Detailed debugging information
- `INFO`: General information (default)
- `WARNING`: Warning messages only
- `ERROR`: Error messages only
- `CRITICAL`: Critical error messages only

## 👥 Contributing

Contributions are welcome! Please check out our contributing guidelines for details.

1. 🍴 Fork the repository
2. 🌿 Create your feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 Commit your changes (`git commit -m 'Add some amazing feature'`)
4. 🚀 Push to the branch (`git push origin feature/amazing-feature`)
5. 🔍 Open a Pull Request

## 📄 License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## 🙏 Acknowledgments

- 🔥 Thanks to the LiteLLM team for creating an excellent proxy
- 💖 Built with ❤️ by the Revenium team
