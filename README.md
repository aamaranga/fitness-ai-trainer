# 🏋️ PrecisionFit

**Your Personal AI Fitness Coach**

PrecisionFit is a Streamlit application that uses AI to generate personalized workout plans based on your fitness goals, experience, equipment, availability, and limitations.

## 🚀 Quick Start

### Prerequisites

* Python 3.8+
* [Groq API Key](https://console.groq.com)
* [uv](https://docs.astral.sh/uv/)

### Installation with uv

```bash
git clone https://github.com/yourusername/fitness-ai-trainer.git
cd fitness-ai-trainer

uv venv
```

Activate the environment:

**Windows**

```bash
.venv\Scripts\activate
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
uv pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

Run the app:

```bash
streamlit run app.py
```

### Alternative: pip

```bash
python -m venv .venv
```

Activate the environment and install:

```bash
pip install -r requirements.txt
```

Then:

```bash
streamlit run app.py
```

## 🛠️ Tech Stack

* **Streamlit** — Web application
* **Groq** — AI API
* **Python-dotenv** — Environment variables
* **uv / pip** — Package management

> ⚠️ Never commit or share your `.env` file or API key.
