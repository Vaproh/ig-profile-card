# 🌐 Instagram Profile Card Service

A high-performance FastAPI service that generates aesthetic Instagram profile cards on-the-fly using Instagram's web API with curl_cffi for reliable fetching.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- **Dynamic Profile Cards** 📸 - Automatically sized based on profile data
- **Anti-Detection** 🛡️ - Uses curl_cffi with Chrome impersonation + rotating Android user agents
- **Proxy Support** 🔄 - Backconnect proxy integration for IP rotation
- **Rate Limiting** ⚡ - Built-in request throttling
- **Error Handling** ✅ - Graceful handling of private accounts, missing profiles, and rate limits

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   Client    │────▶│  FastAPI     │────▶│  Instagram API  │
│  (curl)     │     │  (Port 8080) │     │  (i.instagram)  │
└─────────────┘     └──────────────┘     └─────────────────┘
                          │
                          ▼
                   ┌──────────────┐
                   │   PIL Card   │
                   │  Generator   │
                   └──────────────┘
```

## 🛠️ Tech Stack

- **FastAPI** ⚡ - Async web framework
- **curl_cffi** 🔗 - HTTP client with TLS fingerprinting
- **Pillow** 🖼️ - Image generation
- **pydantic-settings** ⚙️ - Configuration management

## 🚀 Setup

```bash
# Clone and enter directory
cd ig-screenshot

# Install dependencies (requires uv)
./setup.sh

# Or use just
just install

# Configure environment
cp .env.example .env
# Edit .env with your proxy credentials
```

## ⚙️ Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8080` | Server port |
| `HOST` | `0.0.0.0` | Server host |
| `LOG_LEVEL` | `INFO` | Logging level |
| `RATE_LIMIT_PER_MINUTE` | `30` | Max requests per minute per IP |
| `PROXY_ENABLED` | `false` | Enable proxy |
| `PROXY_SERVER` | - | Proxy hostname |
| `PROXY_PORT` | `823` | Proxy port |
| `PROXY_USERNAME` | - | Proxy username |
| `PROXY_PASSWORD` | - | Proxy password |

## 📖 Usage

### 🚦 Start/Stop

```bash
./start.sh   # Start service in tmux session 'ig-profile'
./stop.sh    # Stop service and kill tmux session
```

### 📡 API Endpoints

#### `GET /health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "instagram-profile-card"
}
```

---

#### `GET /profile/{username}`

Generate a profile card image for the given Instagram username.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `username` | string | Yes | Instagram username (1-30 chars, alphanumeric + ._ ) |

**Responses:**

| Status | Description |
|--------|-------------|
| `200` | Profile card image (PNG) |
| `400` | Invalid username format |
| `404` | Profile not found or unavailable |
| `429` | Rate limited by Instagram |
| `500` | Internal error (proxy failure, etc.) |

**Example:**
```bash
curl http://localhost:8080/profile/akiraa.init -o card.png
```

**Card Contents:**
- Profile picture (circular) 📷
- Username (@handle) 👤
- Full name 📝
- Verification badge [V] if verified ✨
- Posts / Followers / Following counts 📊
- Bio (auto-wrapped, max 5 lines) 💬
- External URL (if present) 🔗
- [Private Account] badge if private 🔒

---

## ❗ Error Handling

The service handles various error cases:

| Error Case | API Response | Card Output |
|------------|--------------|-------------|
| Profile not found | `404` | No card generated |
| Private account | `200` | Card with [Private Account] badge |
| Rate limited by Instagram | `429` | No card generated |
| Proxy connection failed | `500` | No card generated |
| Invalid username | `400` | No card generated |

## 🛠️ Development

```bash
# Run without tmux
just run

# Or manually
source .venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8080 --reload

# Format code
just fmt

# Lint code
just lint

# Run all checks
just check

# Run tests
just test
```

## 📁 Project Structure

```
ig-screenshot/
├── main.py              # FastAPI application
├── config.py            # Pydantic settings
├── profile_fetcher.py   # Instagram API client
├── card_generator.py    # PIL image generator
├── pyproject.toml       # Python project metadata
├── justfile             # Command runner
├── requirements.txt     # Python dependencies
├── .env                 # Environment configuration (gitignored)
├── .env.example         # Configuration template
├── setup.sh             # Initial setup script
├── start.sh             # Start service script
├── stop.sh              # Stop service script
└── README.md            # This file
```

## 📜 License

MIT
