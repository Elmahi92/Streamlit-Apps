# LLM-RAG: Retrieval-Augmented Generation with Custom Documents
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)  
[![Streamlit](https://img.shields.io/badge/Streamlit-v1.14-brightgreen)](https://streamlit.io/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  

This repository demonstrates the development and application of **Retrieval-Augmented Generation (RAG)**, a method that enhances Large Language Models (LLMs) by allowing them to generate answers based on external, custom documents. This approach improves the relevance and accuracy of generated responses, especially in domains where up-to-date or domain-specific knowledge is required.

## Project Overview
The primary goal of this project is to implement RAG in a chatbot interface using **Streamlit**. The chatbot is designed to provide real-time answers using information from **situation reports** about the ongoing conflict in Sudan, in coordination with **UNDP**.

Key features:
- Retrieval from **custom documents**.
- Use of up-to-date **situation reports** from trusted sources.
- A user-friendly interface powered by Streamlit.
  
The data source for this project includes comprehensive situation reports from the **UN and humanitarian organizations**, accessible via ReliefWeb.

## Data Source
- ReliefWeb: [ReliefWeb Situation Reports](https://reliefweb.int/?_gl=1*chun0m*_ga*NjcyNzk2MzU0LjE3MjU4NzEzOTU.*_ga_E60ZNX2F68*MTcyNTk3MzA0OC40LjEuMTcyNTk3Mzc1My40Ny4wLjA.)
  
## Reference
- Learn more about RAG and Streamlit chatbots from this reference article: [Chat with Documents using LLM](https://www.analyticsvidhya.com/blog/2024/04/rag-and-streamlit-chatbot-chat-with-documents-using-llm/).

## How to Run the App
To run the chatbot locally:
```bash
streamlit run rag_chatbot.py
```

Make sure you have the necessary dependencies installed before running the app. The chatbot will launch in your browser with the provided document-based knowledge retrieval system.

---
