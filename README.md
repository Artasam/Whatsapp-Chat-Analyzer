# 💬 WhatsApp Chat Analyzer

**A Production-Grade, Modular Analytics Dashboard for WhatsApp Exports.**

[![Live Demo](https://img.shields.io/badge/Live-Demo-blue?style=for-the-badge&logo=streamlit)](https://whatsapp-chat-analyzer-ak.streamlit.app/)

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![Streamlit Version](https://img.shields.io/badge/streamlit-1.56+-FF4B4B.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

WhatsApp Chat Analyzer is a high-performance, modular web application designed to transform raw chat exports into deep, actionable insights. Featuring a modern glassmorphism UI, interactive 3D visualizations, and AI-powered sentiment analysis.

---

## ✨ Key Features

-   **🌐 3D Interactive Visualizations**: Explore your chat history through 3D scatter plots and landscapes for timelines and activity patterns.
-   **🧠 AI Sentiment Analysis**: Leveraging the VADER sentiment engine to track user emotions and conversation trajectories over time.
-   **📊 Modern Glassmorphism UI**: A stunning, high-performance dark mode interface with micro-animations and glowing KPI cards.
-   **🗓 Advanced Activity Mapping**: View busiest days, hours, and months with high-contrast heatmaps and bar charts.
-   **⏱️ Response Time Analytics**: Automatically calculates average response times per user to understand conversation dynamics.
-   **📈 Conversation Health Score**: A composite 0–100 score based on participation, richness, and consistency.
-   **🔤 Content Deep-Dive**: Word clouds, most frequent words (excluding stop words), and emoji distribution analysis.
-   **📥 Data Portability**: Export parsed and cleaned chat data directly to CSV for further external analysis.

---

## 🚀 Getting Started

### Prerequisites

-   Python 3.9 or higher
-   A virtual environment (recommended)

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/your-username/whatsapp-chat-analyzer.git
    cd whatsapp-chat-analyzer
    ```

2.  **Set Up Virtual Environment**
    ```bash
    # Create environment
    python -m venv WCA

    # Activate environment (Windows)
    .\WCA\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Launch the App**
    ```bash
    streamlit run app.py
    ```

---

## 📂 Project Structure

The project follows a modular **src-layout** for maximum maintainability:

```
whatsapp-chat-analyzer/
├── src/
│   ├── preprocess/     # Data cleaning and multi-format parsing
│   ├── analytics/      # Statistical engines and AI logic
│   ├── visualization/  # Plotly chart builders and dark templates
│   ├── ui/             # Page layouts, sidebar, and CSS styles
│   └── config.py       # Global theme tokens and constants
├── app.py              # Slim entry point and router
├── requirements.txt    # Project dependencies
└── stop_hinglish.txt   # Custom stop words list
```

---

## 🛠 Tech Stack

-   **Frontend**: [Streamlit](https://streamlit.io/)
-   **Data Analysis**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
-   **Visualization**: [Plotly](https://plotly.com/python/)
-   **Sentiment**: [VADER Sentiment](https://github.com/cjhutto/vaderSentiment)
-   **NLP**: [NLTK](https://www.nltk.org/), [Emoji](https://github.com/carpedm20/emoji)

---

## 📝 How to Export Your Chat

1.  Open the desired chat in **WhatsApp**.
2.  Tap the three dots (⋮) → **More** → **Export chat**.
3.  Choose **Without Media**.
4.  Save the `.txt` file and upload it to the dashboard.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
