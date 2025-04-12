# varnishlog-to-elasticsearch

A lightweight, stream-processing tool that parses Varnish HTTP logs and sends structured JSON documents directly to Elasticsearch.

This tool is designed for simplicity, resilience, and easy integration into production environments. It supports both development and systemd-based deployments, and includes full support for runtime configuration via environment variables.

[![PyPI version](https://badge.fury.io/py/varnishlog-to-elasticsearch.svg)](https://badge.fury.io/py/varnishlog-to-elasticsearch)
[![Python Versions](https://img.shields.io/pypi/pyversions/varnishlog-to-elasticsearch)](https://pypi.org/project/varnishlog-to-elasticsearch/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Features

- Parses full Varnish request lifecycle (`-g request`)
- Captures client and backend metadata
- Automatically determines production/staging mode via headers
- Sends structured JSON documents to Elasticsearch
- Built-in support for environment-based configuration
- Production-ready systemd service example included
- Efficient bulk indexing with configurable buffering
- Secure credential management via environment variables
- Direct Varnish Shared Memory Log (VSL) integration for better performance

## 📦 Installation

### Production Installation (Recommended)

For production systems, install the package system-wide:

```bash
# Install required system packages
sudo apt-get update
sudo apt-get install -y python3-full python3-venv

# Create a system-wide virtual environment
sudo python3 -m venv /opt/varnishlog-to-elasticsearch

# Install the package in the virtual environment
sudo /opt/varnishlog-to-elasticsearch/bin/pip install varnishlog-to-elasticsearch

# Create a symlink to make the command available system-wide
sudo ln -s /opt/varnishlog-to-elasticsearch/bin/varnishlog-to-es /usr/local/bin/varnishlog-to-es

# Verify installation
which varnishlog-to-es
# Should output: /usr/local/bin/varnishlog-to-es
```

### Development Installation

For development or testing:

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package
pip install varnishlog-to-elasticsearch
```

### From Source

1. Clone this repository:

```bash
git clone https://github.com/NIXRUK/varnishlog-to-elasticsearch.git
cd varnishlog-to-elasticsearch
```

2. Install in development mode:

```bash
pip install -e .
```

## ⚙️ Configuration

All configuration is done through environment variables. The following variables are supported:

### Core Configuration

| Variable          | Description                                 | Default Value      |
|-------------------|---------------------------------------------|-------------------|
| `ES_BASE_URL`     | Elasticsearch base URL                      | `http://localhost:9200` |
| `ES_USERNAME`     | Elasticsearch username                      | `elastic`         |
| `ES_PASSWORD`     | Elasticsearch password                      | (empty)           |
| `ES_VERIFY_SSL`   | Verify SSL certs (`true`, `false`, etc.)    | `true`            |

### Buffering Configuration

| Variable              | Description                                 | Default Value |
|-----------------------|---------------------------------------------|---------------|
| `ES_BUFFER_SIZE`      | Maximum number of documents to buffer       | `100`         |
| `ES_FLUSH_INTERVAL`   | Maximum time (seconds) between flushes      | `5`           |

Set them manually like this:

```bash
export ES_BASE_URL=https://10.99.99.4:9200
export ES_USERNAME=elastic
export ES_PASSWORD=your_secure_password
export ES_VERIFY_SSL=true
export ES_BUFFER_SIZE=200
export ES_FLUSH_INTERVAL=10
```

Or define them in a system-wide config file for systemd (see below).

## 🧪 Usage

### VSL Method (Recommended)

The VSL (Varnish Shared Memory Log) method provides direct access to Varnish's log data, offering better performance and reliability:

```bash
varnishlog-to-es --method vsl
```

### Pipe Method (Fallback)

If VSL is not available, you can use the traditional pipe method:

```bash
/usr/bin/varnishlog -g request | varnishlog-to-es --method pipe
```

### Python API

You can also use the tool programmatically:

```python
from varnishlog_to_elasticsearch.parser import main_loop

# Process logs from a file
with open('varnish.log', 'r') as f:
    main_loop(f)

# Or process from stdin
import sys
main_loop(sys.stdin)
```

## 🛠️ Running as a systemd Service

This project includes a ready-to-use systemd service file that uses the VSL method by default.

### 1. Create the environment file

Create a file at `/etc/varnishlog-to-es.env` with your credentials:

```
ES_BASE_URL=https://10.99.99.4:9200
ES_USERNAME=elastic
ES_PASSWORD=your_secure_password
ES_VERIFY_SSL=true
ES_BUFFER_SIZE=200
ES_FLUSH_INTERVAL=10
```

Protect it:

```bash
sudo chmod 640 /etc/varnishlog-to-es.env
sudo chown root:varnish /etc/varnishlog-to-es.env
```

### 2. Create the systemd unit file

Save this to `/etc/systemd/system/varnishlog-to-es.service`:

```
[Unit]
Description=Varnishlog to Elasticsearch
After=network.target

[Service]
Type=simple
User=varnish
Group=varnish
EnvironmentFile=/etc/varnishlog-to-es.env
ExecStart=/usr/local/bin/varnishlog-to-es --method vsl
Restart=always
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

### 3. Enable and start the service

```bash
sudo systemctl daemon-reload
sudo systemctl enable varnishlog-to-es
sudo systemctl start varnishlog-to-es
```

### 4. View logs

```bash
journalctl -u varnishlog-to-es -f
```

## 🔒 Security Notes

- Always use HTTPS for Elasticsearch, especially in production.
- Never commit passwords to source code — use environment variables or secrets managers.
- Use `.env` or systemd's `EnvironmentFile` to manage runtime secrets securely.
- SSL verification is enabled by default (`ES_VERIFY_SSL=true`). Only disable it in development environments.
- The buffer size and flush interval can be tuned based on your security and performance requirements.
- The VSL method requires the varnish user to have access to the Varnish shared memory segment.
- For production systems, always install the package in a system-wide virtual environment.
- On Debian/Ubuntu systems, use the provided installation method to avoid system Python conflicts.

## 🧹 Future Ideas

- Docker container
- GeoIP enrichment
- Log rotation / buffering
- Index lifecycle policy automation
- Retry mechanism for failed bulk operations
- Metrics and monitoring integration

## 📜 License

MIT © Will Riches — open to contributions and extensions.
