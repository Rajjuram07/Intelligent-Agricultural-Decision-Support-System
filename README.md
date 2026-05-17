# KrishiMitra AI

## Intelligent Agricultural Decision Support System

AI-powered agricultural intelligence platform built using Retrieval-Augmented Generation (RAG), hybrid vector databases, machine learning forecasting, climate intelligence, and large language models to support data-driven agricultural decision-making.

The platform combines semantic retrieval, predictive analytics, real-time weather intelligence, multilingual agricultural querying, and interactive visual analytics into a unified intelligent ecosystem designed for agricultural insights and forecasting.

Overview

The Intelligent Agricultural Decision Support System is designed to provide intelligent agricultural analytics and forecasting using large-scale agricultural and climate datasets.

The system integrates:

Retrieval-Augmented Generation (RAG)
Gemini AI
FAISS vector database
Pinecone vector database
Machine learning forecasting
PostgreSQL database integration
Real-time weather intelligence
Climate-aware analytics
Multilingual query intelligence
Interactive Streamlit dashboards

The platform enables users to perform natural language agricultural querying, analyze historical crop and rainfall trends, generate AI-powered agricultural insights, and visualize predictive analytics dynamically.

Key Highlights
Built using more than 730,000+ agricultural and climate intelligence records
Hybrid AI + Machine Learning architecture
Retrieval-Augmented Generation pipeline
FAISS and Pinecone vector retrieval
Gemini-powered agricultural reasoning
Machine learning-based crop forecasting
Real-time weather intelligence integration
PostgreSQL-backed persistence layer
Modular enterprise-grade architecture
Interactive analytical dashboards
Multilingual agricultural query support
Core Features
Agricultural Intelligence Engine
Natural language agricultural querying
AI-generated contextual agricultural insights
Intelligent crop and rainfall analysis
Semantic agricultural retrieval
Retrieval-Augmented Generation (RAG)
Embedding-based retrieval pipeline
FAISS semantic vector search
Pinecone cloud vector database integration
Context-aware agricultural intelligence generation
Machine Learning Forecasting
Agricultural production prediction
Yield forecasting
Predictive agricultural analytics
Model evaluation and comparison
Historical trend intelligence
Climate & Weather Intelligence
Real-time weather API integration
Rainfall analysis and visualization
Climate-aware agricultural recommendations
Weather query understanding engine
Interactive Analytics Dashboard
Dynamic agricultural visualizations
Production trend analysis
Rainfall trend analysis
Farmer analytics dashboard
AI forecasting insights
Multilingual Query Processing
Multi-language agricultural interaction
Query intelligence engine
Intelligent routing and parsing
Language-aware agricultural querying
Database & Persistence Layer
PostgreSQL integration
Query history management
Agricultural logging system
Structured data persistence
Dataset Scale

The platform is built on large-scale agricultural and climate intelligence datasets containing:

Agricultural production records
Crop yield statistics
District-level farming intelligence
Rainfall observations
Historical agricultural trends
Climate analytics data
Dataset Statistics
Dataset Type	Records
Agricultural Records	446,301+
Climate & Agricultural Intelligence Records	284,495+
Total Records Processed	730,000+
System Architecture
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
Technology Stack
Category	Technologies
Frontend	Streamlit
AI/LLM	Gemini AI
Vector Databases	FAISS, Pinecone
Machine Learning	Scikit-learn
Database	PostgreSQL
Data Processing	Pandas, NumPy
Visualization	Plotly, Matplotlib
Embeddings	Sentence Transformers
Backend	Python
Weather Intelligence	Weather API
Analytics	Statistical Analysis Engine
Repository Structure
Intelligent-Agricultural-Decision-Support-System/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
│
├── api/
│   ├── advanced_weather.py
│   └── weather_api.py
│
├── database/
│   ├── agriculture_logs.py
│   ├── db.py
│   ├── history.py
│   └── models.py
│
├── data/
│   └── processed/
│
├── data_pipeline/
│   └── government_data_fetcher.py
│
├── data_processing/
│   └── clean_agriculture_data.py
│
├── ml_models/
│   ├── predictor.py
│   ├── advanced_predictor.py
│   ├── train_model.py
│   ├── train_advanced_model.py
│   └── evaluate_models.py
│
├── rag/
│
├── rag_workspace/
│   ├── embeddings.py
│   ├── retriever.py
│   ├── vector_store.py
│   ├── statistics_engine.py
│   └── rag_engine.py
│
├── utils/
│   ├── config.py
│   ├── language_utils.py
│   ├── query_router.py
│   ├── query_intelligence.py
│   └── weather_query_parser.py
│
└── visualization/
    ├── dashboard.py
    ├── agriculture_insights.py
    ├── farmer_analytics.py
    └── model_analytics.py
AI & RAG Workflow

The platform uses a Retrieval-Augmented Generation workflow for agricultural intelligence generation.

Workflow Pipeline
User submits agricultural query
Query intelligence engine processes the request
Embeddings are generated using semantic encoding
FAISS and Pinecone retrieve relevant agricultural records
Historical agricultural context is assembled
Gemini AI generates contextual agricultural intelligence
Statistical analytics engine computes insights
Interactive dashboard visualizes results dynamically
Machine Learning Capabilities

The ML forecasting pipeline supports:

Agricultural production prediction
Yield estimation
Forecast analytics
Production trend forecasting
Model comparison and evaluation
Climate-aware predictive analysis

The system integrates machine learning predictions with AI-generated contextual reasoning for enhanced agricultural intelligence.

Weather Intelligence Capabilities

The platform includes:

Real-time weather integration
Climate-aware agricultural analysis
Rainfall forecasting insights
Weather query parsing
Agricultural weather intelligence generation
Database Integration

The system uses PostgreSQL for:

Agricultural query logging
Prediction history
User interaction tracking
Structured persistence
Analytical storage
Installation
Clone Repository
git clone https://github.com/Rajjuram07/Intelligent-Agricultural-Decision-Support-System.git
Navigate to Project
cd Intelligent-Agricultural-Decision-Support-System
Install Dependencies
pip install -r requirements.txt
Environment Variables

Create a .env file in the root directory.

Example Configuration
GEMINI_API_KEY=your_gemini_api_key
PINECONE_API_KEY=your_pinecone_api_key
WEATHER_API_KEY=your_weather_api_key

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=agriculture_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
Run Application
streamlit run app.py
Dashboard Modules

The application provides multiple analytical modules including:

Agricultural Intelligence Dashboard
Production Analytics
Rainfall Analytics
Farmer Insights
Machine Learning Analytics
AI Prediction Intelligence
Climate-Aware Visualizations
Weather Intelligence
Use Cases
Agricultural analytics platforms
Smart farming systems
Climate-aware agricultural forecasting
Agricultural decision-support systems
AI-assisted farming intelligence
Government agricultural analytics
Crop intelligence systems
Agricultural research platforms
Enterprise Design Principles

The platform follows modular and scalable software architecture principles:

Separation of concerns
Modular AI pipelines
Independent ML forecasting layer
Scalable vector retrieval architecture
Database-backed persistence
Extensible analytics engine
Reusable utility modules
Enterprise-style project organization
Future Enhancements

Planned enhancements include:

Satellite imagery integration
IoT-based agricultural monitoring
Voice-enabled farmer assistance
Advanced hybrid retrieval ranking
Distributed scalable deployment
Mobile application integration
Advanced climate simulation models
Project Strengths
Large-scale dataset processing
Hybrid AI + ML architecture
RAG-powered agricultural intelligence
FAISS + Pinecone semantic retrieval
Gemini-based contextual reasoning
Climate-aware forecasting
Interactive analytics ecosystem
Enterprise-grade modular design
Author

Rajjuram Goyal

GitHub Repository:

[Intelligent Agricultural Decision Support System](https://github.com/Rajjuram07/Intelligent-Agricultural-Decision-Support-System.git)