# Finsight-Ai
FinSight AI is a Streamlit application that functions as a Corporate Finance Chat Assistant, allowing users to upload an Excel file and then use a Groq-powered Large Language Model (LLM) to analyze the data and answer finance-related questions.

## ✨ Key Features

* **Excel Data Upload**: Securely upload and load corporate financial data from `.xlsx` or `.xls` files.
* **Groq-Powered LLM**: Leverages the high-speed inference capabilities of the Groq API (specifically `llama3-70b-8192` as seen in `llm.py`) for rapid financial queries.
* **Corporate Finance Expertise**: The AI is prompted to act as a financial expert with 30 years of experience and prestigious business school attendance.
* **Contextual Analysis**: Sends a preview of your uploaded financial data to the LLM for data-aware answers.
* **Interactive Chat Interface**: A multi-turn chat interface built with Streamlit for a seamless user experience.
* **Modular Codebase**: Organized into clear modules for app structure (`app.py`), chat logic (`chat.py`), LLM interaction (`llm.py`), and file handling (`file_handler.py`).

## 💻 Installation and Setup

Follow these steps to get your local development environment set up and running.

### Prerequisites

* Python 3.10 or higher
* A Groq API Key

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd finsight-ai
