# KrishiMitra AI

## Intelligent Agricultural Decision Support System

AI-powered agricultural intelligence platform built using Retrieval-Augmented Generation (RAG), hybrid vector databases, machine learning forecasting, climate intelligence, and large language models to support data-driven agricultural decision-making.

---

## Overview

KrishiMitra AI is a modular agricultural intelligence ecosystem designed to provide intelligent crop analytics, climate-aware forecasting, semantic agricultural retrieval, and AI-powered decision support using large-scale agricultural and climate datasets.

The platform combines:

- Retrieval-Augmented Generation (RAG)
- Gemini AI
- FAISS Vector Database
- Pinecone Vector Database
- Machine Learning Forecasting
- PostgreSQL Integration
- Real-Time Weather Intelligence
- Multilingual Query Processing
- Interactive Analytics Dashboards

---

## Dataset Scale

The system is built using large-scale agricultural and climate intelligence datasets.

| Dataset | Records |
|---|---:|
| Agricultural Production Records | 446,301+ |
| Climate & Agricultural Intelligence Records | 284,495+ |
| Total Records Processed | 730,000+ |

---

## Core Capabilities

### AI Agricultural Intelligence
- Natural language agricultural querying
- AI-generated agricultural insights
- Semantic agricultural retrieval
- Context-aware response generation

### Retrieval-Augmented Generation (RAG)
- Embedding-based retrieval pipeline
- FAISS semantic vector search
- Pinecone cloud vector integration
- Historical agricultural context generation

### Machine Learning Forecasting
- Crop production prediction
- Yield forecasting
- Predictive analytics
- Historical trend analysis
- Model evaluation and comparison

### Weather & Climate Intelligence
- Real-time weather integration
- Rainfall analytics
- Climate-aware agricultural recommendations
- Weather query parsing engine

### Interactive Dashboard System
- Production analytics
- Rainfall visualization
- Farmer analytics
- AI prediction dashboards
- Interactive Plotly visualizations

### Multilingual Query Intelligence
- Multi-language agricultural querying
- Query routing engine
- Intelligent query parsing
- Language-aware response processing

### Database Integration
- PostgreSQL persistence layer
- Query history management
- Agricultural logging system
- Structured analytics storage

---

## System Architecture

```text
User Query
    ↓
Query Intelligence Layer
    ↓
Language Processing Engine
    ↓
Embedding Generation
    ↓
FAISS + Pinecone Retrieval
    ↓
Relevant Agricultural Context
    ↓
Gemini AI Reasoning Engine
    ↓
Machine Learning Forecasting
    ↓
Statistical Analytics Engine
    ↓
Weather Intelligence Layer
    ↓
PostgreSQL Persistence
    ↓
Interactive Dashboard Response
```

---

## Technology Stack

| Category | Technologies |
|---|---|
| Frontend | Streamlit |
| AI / LLM | Gemini AI |
| Vector Databases | FAISS, Pinecone |
| Machine Learning | Scikit-learn |
| Database | PostgreSQL |
| Visualization | Plotly, Matplotlib |
| Embeddings | Sentence Transformers |
| Data Processing | Pandas, NumPy |
| Backend | Python |
| Weather Intelligence | Weather API |

---

## Repository Structure

```text
Intelligent-Agricultural-Decision-Support-System/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
│
├── api/
├── database/
├── data/
├── data_pipeline/
├── data_processing/
├── ml_models/
├── rag/
├── rag_workspace/
├── utils/
└── visualization/
```

---

## RAG Intelligence Workflow

1. User submits agricultural query  
2. Query intelligence engine processes request  
3. Embeddings are generated using semantic encoding  
4. FAISS and Pinecone retrieve relevant agricultural records  
5. Historical agricultural context is assembled  
6. Gemini AI generates contextual agricultural intelligence  
7. Statistical analytics engine computes insights  
8. Dashboard visualizes results dynamically  

---

## Machine Learning Pipeline

The forecasting layer supports:

- Agricultural production prediction
- Yield estimation
- Predictive analytics
- Climate-aware forecasting
- Model evaluation
- Production trend forecasting

The machine learning pipeline works together with the RAG intelligence system to generate AI-assisted agricultural insights.

---

## Weather Intelligence System

KrishiMitra AI includes a climate-aware intelligence layer with:

- Real-time weather API integration
- Rainfall analytics
- Agricultural climate intelligence
- Weather query parsing
- Climate-aware forecasting support

---

## PostgreSQL Integration

The platform uses PostgreSQL for:

- Query history management
- Agricultural interaction logging
- Structured analytics persistence
- Prediction history storage
- Database-backed scalability

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Rajjuram07/Intelligent-Agricultural-Decision-Support-System.git
```

### Navigate to Project

```bash
cd Intelligent-Agricultural-Decision-Support-System
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the root directory.

```env
GEMINI_API_KEY=your_gemini_api_key
PINECONE_API_KEY=your_pinecone_api_key
WEATHER_API_KEY=your_weather_api_key

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=agriculture_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
```

---

## Run Application

```bash
streamlit run app.py
```

---

## Dashboard Modules

The platform includes multiple analytical systems:

- Agricultural Intelligence Dashboard
- Production Analytics
- Rainfall Analytics
- Farmer Insights
- Machine Learning Analytics
- AI Prediction Intelligence
- Climate-Aware Visualizations
- Weather Intelligence

---

## Enterprise Design Principles

KrishiMitra AI follows modular and scalable architecture principles:

- Modular AI pipelines
- Separation of concerns
- Independent ML forecasting layer
- Scalable retrieval architecture
- Database-backed persistence
- Reusable utility modules
- Extensible analytics framework

---

## Future Enhancements

Planned improvements include:

- Satellite imagery integration
- IoT-based agricultural monitoring
- Voice-enabled farmer assistance
- Mobile application integration
- Distributed cloud deployment
- Advanced hybrid retrieval ranking

---

## Use Cases

- Agricultural analytics platforms
- Smart farming systems
- Climate-aware agricultural forecasting
- AI-assisted farming intelligence
- Agricultural decision-support systems
- Government agricultural analytics
- Crop intelligence platforms

---

## Project Strengths

- Large-scale dataset processing
- Hybrid AI + ML architecture
- RAG-powered agricultural intelligence
- FAISS + Pinecone semantic retrieval
- Gemini-based reasoning engine
- Climate-aware forecasting
- Interactive analytics ecosystem
- Enterprise-grade modular architecture

---

## Author

Rajjuram Goyal

GitHub Repository:

https://github.com/Rajjuram07/Intelligent-Agricultural-Decision-Support-System