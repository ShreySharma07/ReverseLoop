<div align="center">

# ♻️ ReverseLoop

### Autonomous Returns Triage Agent

*Turn trash into treasure using Google ADK & Gemini*

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

[Features](#-features) • [Architecture](#️-architecture) • [Quick Start](#-quick-start) • [Documentation](#-documentation)

</div>

---

## 📖 Overview

ReverseLoop is an **autonomous multi-agent system** designed to solve the **$816 Billion reverse logistics crisis**. It autonomously inspects returned items via computer vision, researches their real-time resale value, and calculates whether to **RESELL** or **RECYCLE** them based on net profit margins.

### The Problem

Retailers lose billions annually on returns due to inefficient triage decisions. ReverseLoop automates this process using AI agents that work together to maximize recovery value.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **Multi-Agent System** | Sequential workflow with specialized AI agents |
| 👁️ **Computer Vision** | Automated item inspection using Gemini 1.5 Flash |
| 💰 **Market Intelligence** | Real-time resale value estimation |
| 📊 **Financial Decision Engine** | Profit-based RESELL/RECYCLE recommendations |
| 🔍 **100% Accuracy** | Validated against golden dataset with $0 financial risk |
| 🐳 **Docker Ready** | One-command deployment |

---

## 🏗️ Architecture

ReverseLoop uses a **sequential multi-agent workflow** powered by the Google Agent Development Kit (ADK):

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│ Vision Inspector│─────▶│  Market Broker  │─────▶│ Finance Engine  │
│   (Edge Node)   │      │  (Cloud Node)   │      │  (Logic Layer)  │
└─────────────────┘      └─────────────────┘      └─────────────────┘
      Gemini AI               Tool-Enabled           Deterministic
   Extract Metadata         Query Markets          Calculate Profit
```

### Agent Pipeline

#### 1️⃣ Vision Inspector (Edge Node)
- **Type:** `LlmAgent` (Gemini 1.5 Flash)
- **Input:** Raw product images
- **Output:** Structured metadata (Brand, Condition, Defects)
- **Purpose:** Automated visual inspection and classification

#### 2️⃣ Market Broker (Cloud Node)
- **Type:** `LlmAgent` with Tools
- **Input:** Product metadata
- **Output:** Fair market value estimates
- **Purpose:** Real-time market research via external APIs (eBay Mock)

#### 3️⃣ Finance Engine (Logic Layer)
- **Type:** Deterministic calculator
- **Formula:** `(Market Price - Shipping - Fees - Labor) = Decision`
- **Output:** RESELL or RECYCLE recommendation with profit margin

### Google ADK Concepts Demonstrated

- ✅ **LlmAgent** - Core cognitive workers using `google.adk.agents`
- ✅ **Tool Use** - Custom `MockEbayClient` integrated via `Tool.from_function`
- ✅ **Session Management** - `InMemorySessionService` for stateful execution with `Runner`
- ✅ **Context Engineering** - Strict JSON-output prompts for reliable parsing
- ✅ **Observability** - Full evaluation harness to measure financial accuracy

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))
- Docker (optional, for containerized deployment)

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ReverseLoop.git
cd ReverseLoop

# Create .env file
cat > .env << EOF
GOOGLE_API_KEY="your_gemini_key_here"
EBAY_FEE_PERCENT=0.13
HANDLING_COST=2.00
EOF

# Launch with Docker Compose
docker compose up --build
```

🌐 Access the app at **http://localhost:8501**

### Option 2: Local Installation

```bash
# Clone and navigate
git clone https://github.com/YOUR_USERNAME/ReverseLoop.git
cd ReverseLoop

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1

# Install dependencies
pip install -e .

# Create .env file (same as above)

# Run the application
streamlit run reverse_loop/app.py
```

---

## 🧪 Evaluation & Testing

ReverseLoop includes a comprehensive evaluation suite with a **Golden Dataset** to validate financial decisions against real-world edge cases:

- ✅ Damaged designer goods vs. fast fashion
- ✅ High-value electronics with minor defects
- ✅ Bulk commodity items
- ✅ Counterfeit detection scenarios

### Run Evaluation

```bash
python evaluations/run_eval_full.py
```

### Current Performance Metrics

| Metric | Score |
|--------|-------|
| **Decision Accuracy** | 100% |
| **Financial Risk** | $0.00 |
| **Processing Time** | <3s per item |

---

## 📂 Project Structure

```
ReverseLoop/
│
├── reverse_loop/              # Core application
│   ├── agents/                # AI agent implementations
│   │   ├── vision_inspector.py
│   │   └── market_broker.py
│   ├── tools/                 # Deterministic logic & APIs
│   │   ├── finance_engine.py
│   │   └── mock_ebay_client.py
│   └── app.py                 # Streamlit frontend
│
├── evaluations/               # Testing & validation
│   ├── run_eval_full.py       # Evaluation script
│   └── golden_dataset.json    # Ground truth data
│
├── infra/                     # Infrastructure
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── .env.example               # Environment template
├── requirements.txt           # Python dependencies
├── setup.py                   # Package configuration
└── README.md                  # This file
```

---

## 🔧 Configuration

Configure ReverseLoop via the `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Gemini API authentication key | *Required* |
| `EBAY_FEE_PERCENT` | Marketplace commission rate | `0.13` |
| `HANDLING_COST` | Per-item processing cost (USD) | `2.00` |

---

## 📚 Documentation

### Usage Example

```python
from reverse_loop.agents import VisionInspector, MarketBroker
from reverse_loop.tools import FinanceEngine

# Initialize agents
vision = VisionInspector()
broker = MarketBroker()
finance = FinanceEngine()

# Process returned item
metadata = vision.inspect(image_path)
market_value = broker.get_value(metadata)
decision = finance.calculate(market_value)

print(f"Recommendation: {decision.action}")  # RESELL or RECYCLE
print(f"Expected Profit: ${decision.profit}")
```

### API Reference

For detailed API documentation, see [docs/API.md](docs/API.md)

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [Google Agent Development Kit (ADK)](https://github.com/google/adk)
- Powered by [Gemini 2.5 Flash](https://deepmind.google/technologies/gemini/)
- Inspired by real-world reverse logistics challenges

---

## 📧 Contact & Support

- **Issues:** [GitHub Issues](https://github.com/ShreySharma07
/ReverseLoop/issues)
- **Discussions:** [GitHub Discussions](https://github.com/ShreySharma07
/ReverseLoop/discussions)
- **Email:** shrey7shrey@gmail.com

---

<div align="center">

**Made with ♻️ by [Shrey Sharma]**

*Solving the reverse logistics crisis, one return at a time.*

</div>