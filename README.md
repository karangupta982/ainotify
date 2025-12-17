# AI News Aggregator

A sophisticated, full-stack AI-powered news aggregation platform featuring multi-agent LLM systems, asynchronous data pipelines, personalized content curation, and automated email delivery. This enterprise-grade project demonstrates advanced backend architecture with complex data processing workflows, scalable database design, and robust API integrations.

## Overview

This comprehensive project implements a complete AI news ecosystem with the following advanced capabilities:
- **Multi-Source Data Aggregation**: Concurrent scraping from YouTube channels and RSS feeds with rate limiting and error resilience
- **LLM-Powered Content Processing**: Multi-agent system using Groq API for intelligent summarization, curation, and personalization
- **Asynchronous Pipeline Orchestration**: Complex workflow management with dependency handling and failure recovery
- **Full-Stack Web Application**: FastAPI backend with RESTful APIs, Next.js frontend with modern UI/UX
- **Personalized User Experience**: Profile-based content ranking using advanced NLP techniques
- **Production-Ready Deployment**: Containerized deployment with cron scheduling and environment-aware configuration
- **Scalable Database Architecture**: Hybrid PostgreSQL/MongoDB setup with optimized queries and indexing

---

# Demo

[![Img1](./frontend//app//assets/ainotifyimg1.jpeg)](https://ainotify.vercel.app)

[![Img2](./frontend//app//assets/ainotifyimg2.jpeg)](https://ainotify.vercel.app)

## Architecture

```mermaid
graph TD
    A[Data Sources<br/>YouTube Channels<br/>RSS Feeds] --> B[Scrapers Module<br/>Registry Pattern<br/>BaseScraper]
    B --> C[(Database Layer<br/>PostgreSQL + MongoDB<br/>SQLAlchemy ORM)]
    C --> D[Processing Services<br/>Content Conversion<br/>Transcript Extraction<br/>LLM Summarization]
    D --> C
    C --> E[Multi-Agent LLM System<br/>Curator Agent<br/>Digest Agent<br/>Email Agent]
    E --> F[Email Service<br/>Personalized Digests<br/>SMTP Delivery]
    C --> G[FastAPI Backend<br/>RESTful APIs<br/>Authentication & Security<br/>Billing Integration]
    G --> H[Next.js Frontend<br/>Dashboard UI<br/>User Management<br/>Real-time Updates]
    I[Pipeline Scheduler<br/>Cron Orchestration<br/>Async Task Management] --> B
    I --> D
    I --> E
    I --> F
    
    style A fill:#e1f5ff,color:#000,stroke:#000,stroke-width:1px
    style B fill:#fff4e1,color:#000,stroke:#000,stroke-width:1px
    style C fill:#e8f5e9,stroke:#4caf50,stroke-width:3px,color:#000
    style D fill:#fff4e1,color:#000,stroke:#000,stroke-width:1px
    style E fill:#f3e5f5,color:#000,stroke:#000,stroke-width:1px
    style F fill:#ffe1f5,color:#000,stroke:#000,stroke-width:1px
    style G fill:#d1ecf1,color:#000,stroke:#000,stroke-width:1px
    style H fill:#f8d7da,color:#000,stroke:#000,stroke-width:1px
    style I fill:#d4edda,color:#000,stroke:#000,stroke-width:1px
```

### Backend Architecture Deep Dive

The backend is built on a microservices-inspired architecture within a monolithic structure, featuring:

**Multi-Agent LLM System (`app/agent/`)**:
- **Base Agent Framework**: Abstract base class implementing common LLM interaction patterns, prompt engineering, and response parsing
- **Specialized Agents**: Curator Agent for relevance scoring, Digest Agent for content summarization, Email Agent for personalized content generation
- **Advanced Prompt Engineering**: Context-aware prompts with user profile integration and multi-turn conversations
- **Error Handling & Fallbacks**: Robust error recovery with retry mechanisms and alternative processing paths

**Asynchronous Data Pipeline (`app/pipeline/`)**:
- **Scheduler Module**: Cron-based orchestration with timezone-aware scheduling and manual trigger capabilities
- **Dependency Management**: Complex task dependencies with parallel processing and sequential constraints
- **Monitoring & Logging**: Comprehensive logging with structured data for debugging and performance analysis

**Database Layer (`app/database/`)**:
- **Hybrid Storage**: PostgreSQL for relational data (users, articles, digests), MongoDB for unstructured content and metadata
- **ORM & Repository Pattern**: SQLAlchemy with custom repository layer for data access abstraction
- **Migration & Schema Management**: Automated table creation with environment-specific configurations
- **Connection Pooling**: Optimized database connections with health checks and failover

**API Layer (`app/api/`)**:
- **FastAPI Framework**: High-performance async APIs with automatic OpenAPI documentation
- **Authentication & Authorization**: JWT-based auth with role-based access control
- **Billing Integration**: Razorpay payment gateway integration with webhook handling
- **Security**: Input validation with Pydantic, CORS configuration, and secure headers

**Scrapers Module (`app/scrapers/`)**:
- **Registry Pattern**: Dynamic scraper registration with factory pattern for extensibility
- **Rate Limiting & Proxies**: Webshare proxy integration for YouTube API bypass
- **Content Parsing**: Advanced HTML parsing with BeautifulSoup and feedparser for RSS
- **Error Resilience**: Retry logic with exponential backoff and circuit breaker patterns

**Services Layer (`app/services/`)**:
- **Modular Processing**: Separate services for each content type with shared base classes
- **Content Transformation**: HTML to Markdown conversion, video transcript extraction, LLM-powered summarization
- **Email Generation**: Template-based email creation with personalization and duplicate prevention

## How It Works

### Advanced Pipeline Flow

The system implements a sophisticated asynchronous pipeline with the following complex stages:

1. **Intelligent Scraping** (`app/runner.py`)
   - **Concurrent Execution**: Multi-threaded scraper execution with semaphore-based rate limiting
   - **Dynamic Registry**: Runtime scraper registration supporting plugin-like extensibility
   - **Content Deduplication**: Advanced hashing algorithms to prevent duplicate content ingestion
   - **Error Recovery**: Circuit breaker pattern with exponential backoff for API failures

2. **Multi-Modal Content Processing** (`app/services/process_*.py`)
   - **Anthropic Processing**: HTML parsing with BeautifulSoup, content extraction, and LLM-powered markdown conversion
   - **YouTube Processing**: Video metadata extraction, transcript fetching with proxy rotation, and timestamp alignment
   - **Digest Generation**: Multi-agent LLM collaboration for comprehensive article summarization with key insights extraction

3. **AI-Powered Curation** (`app/services/process_curator.py`)
   - **User Profile Analysis**: NLP-based profile parsing with interest vector generation
   - **Relevance Scoring**: Advanced LLM ranking using cosine similarity and contextual embeddings
   - **Personalization Engine**: Dynamic content filtering based on user preferences and reading history

4. **Intelligent Email Generation** (`app/services/process_email.py`)
   - **Content Selection Algorithm**: Weighted ranking combining relevance scores and recency
   - **LLM-Powered Composition**: Context-aware email drafting with personalized introductions
   - **Template Rendering**: HTML email generation with responsive design and accessibility features
   - **Duplicate Prevention**: Sophisticated tracking system preventing re-delivery of sent content

5. **Reliable Delivery System** (`app/services/email.py`)
   - **SMTP Integration**: Secure Gmail SMTP with OAuth2 authentication and connection pooling
   - **Delivery Tracking**: Comprehensive logging and retry mechanisms for failed deliveries
   - **Bounce Handling**: Automated bounce processing and unsubscribe management

### Daily Pipeline Orchestration

The `run_daily_pipeline()` function implements enterprise-grade workflow orchestration:
- **Environment Detection**: Automatic configuration switching between LOCAL and PRODUCTION
- **Database Health Checks**: Pre-flight validation ensuring data integrity
- **Transactional Processing**: ACID-compliant operations with rollback capabilities
- **Monitoring Integration**: Structured logging with performance metrics collection
- **Graceful Degradation**: Partial failure handling allowing pipeline continuation

## Project Structure

```
├── app/                          # Backend Application
│   ├── agent/                    # Multi-Agent LLM System
│   │   ├── base.py              # Abstract Agent Base Class
│   │   ├── curator_agent.py     # Content Relevance Scoring
│   │   ├── digest_agent.py      # Article Summarization
│   │   └── email_agent.py       # Email Content Generation
│   ├── api/                     # FastAPI RESTful APIs
│   │   ├── auth.py              # Authentication Endpoints
│   │   ├── billing.py           # Payment Integration
│   │   ├── channels.py          # Content Source Management
│   │   ├── deps.py              # Dependency Injection
│   │   ├── profile.py           # User Profile APIs
│   │   ├── schemas.py           # Pydantic Data Models
│   │   ├── security.py          # Security Utilities
│   │   └── server.py            # FastAPI Application
│   ├── database/                # Data Layer Architecture
│   │   ├── models.py            # SQLAlchemy ORM Models
│   │   ├── repository.py        # Repository Pattern Implementation
│   │   ├── connection.py        # Database Connection Management
│   │   ├── mongo.py             # MongoDB Integration
│   │   └── create_tables.py     # Schema Migration Scripts
│   ├── pipeline/                # Workflow Orchestration
│   │   └── scheduler.py         # Cron Job Management
│   ├── profiles/                # User Personalization
│   │   └── user_profile.py      # Profile Configuration
│   ├── scrapers/                # Content Acquisition Layer
│   │   ├── base.py              # Base Scraper Framework
│   │   ├── anthropic.py         # Anthropic RSS Scraper
│   │   ├── openai.py            # OpenAI RSS Scraper
│   │   └── youtube.py           # YouTube Channel Scraper
│   ├── services/                # Business Logic Services
│   │   ├── base.py              # Service Base Classes
│   │   ├── process_anthropic.py # Content Processing
│   │   ├── process_youtube.py   # Video Processing
│   │   ├── process_digest.py    # Summarization Service
│   │   ├── process_curator.py   # Curation Engine
│   │   ├── process_email.py     # Email Generation
│   │   └── email.py             # SMTP Delivery Service
│   ├── config.py                # Configuration Management
│   ├── daily_runner.py          # Pipeline Orchestrator
│   └── runner.py                # Scraper Registry
├── frontend/                     # Next.js Web Application
│   ├── app/                     # App Router Structure
│   │   ├── auth/                # Authentication Pages
│   │   ├── dashboard/           # User Dashboard
│   │   ├── assets/              # Static Assets
│   │   └── components/          # Reusable UI Components
│   ├── components/              # Component Library
│   │   ├── landing/             # Landing Page Components
│   │   └── ui/                  # Design System
│   ├── public/                  # Static Files
│   ├── package.json             # Frontend Dependencies
│   └── next.config.ts           # Next.js Configuration
├── docker/                      # Containerization
│   └── docker-compose.yml       # Multi-Container Setup
├── docs/                        # Documentation
├── pyproject.toml               # Python Project Configuration             
└── requirements.txt             # Python Dependencies
```

## Adding New Scrapers

### RSS Feed Scraper (Easiest)

Create a new file in `app/scrapers/`:

```python
from typing import List
from .base import BaseScraper, Article

class MyArticle(Article):
    pass

class MyScraper(BaseScraper):
    @property
    def rss_urls(self) -> List[str]:
        return ["https://example.com/feed.xml"]

    def get_articles(self, hours: int = 24) -> List[MyArticle]:
        return [MyArticle(**a.model_dump()) for a in super().get_articles(hours)]
```

Then register it in `app/runner.py`:

```python
from .scrapers.my_scraper import MyScraper

def _save_my_articles(scraper, repo, hours):
    return _save_rss_articles(scraper, repo, hours, repo.bulk_create_my_articles)

SCRAPER_REGISTRY = [
    # ... existing scrapers
    ("my_source", MyScraper(), _save_my_articles),
]
```

### Custom Scraper

For non-RSS sources, inherit from the base pattern:

```python
class CustomScraper:
    def get_articles(self, hours: int = 24) -> List[Article]:
        # Your custom scraping logic
        pass
```

## Technical Challenges Overcome

This project addresses several complex engineering challenges that demonstrate advanced software development skills:

### Multi-Agent LLM Coordination
- **Prompt Engineering**: Designing context-aware prompts that maintain conversation state across multiple LLM calls
- **Agent Communication**: Implementing inter-agent data flow with error propagation and fallback mechanisms
- **Cost Optimization**: Balancing LLM API usage with caching strategies and intelligent prompt compression
- **Response Parsing**: Robust parsing of LLM outputs with validation and error recovery

### Asynchronous Data Pipeline Complexity
- **Dependency Management**: Handling complex task dependencies in an async environment with proper error isolation
- **Resource Contention**: Managing database connections, API rate limits, and memory usage across concurrent operations
- **State Management**: Tracking pipeline progress and implementing resumable operations for long-running tasks
- **Monitoring & Debugging**: Implementing comprehensive logging and metrics for distributed async workflows

### Hybrid Database Architecture
- **Data Consistency**: Maintaining referential integrity across PostgreSQL and MongoDB with eventual consistency patterns
- **Query Optimization**: Designing efficient queries that leverage both relational and document database strengths
- **Migration Strategies**: Handling schema evolution and data migration between different database systems
- **Backup & Recovery**: Implementing robust backup strategies for hybrid data stores

### Production Deployment Challenges
- **Environment Configuration**: Managing complex environment variables and secrets across multiple deployment stages
- **Cron Job Reliability**: Ensuring scheduled tasks execute reliably in cloud environments with proper error handling
- **Scalability Considerations**: Designing for horizontal scaling with stateless services and externalized state management
- **Security Hardening**: Implementing comprehensive security measures including input validation, CORS, and secure headers

### Full-Stack Integration Complexity
- **API Design**: Creating RESTful APIs with proper HTTP status codes, pagination, and hypermedia links
- **Frontend-Backend Sync**: Maintaining data consistency between Next.js frontend and FastAPI backend
- **Authentication Flow**: Implementing secure JWT-based authentication with refresh token rotation
- **Real-Time Updates**: Managing state synchronization between client and server for dynamic user interfaces

## Setup

### Prerequisites

- Python 3.12+
- PostgreSQL database
- Groq API key
- Gmail app password (for email sending)
- Webshare proxy credentials (optional, for YouTube transcript fetching)

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   uv sync
   ```

3. Configure environment variables (copy `app/example.env` to `.env`):
   ```bash
   GROQ_API_KEY=your_groq_api_key
   MY_EMAIL=your_email@gmail.com
   APP_PASSWORD=your_gmail_app_password
   DATABASE_URL=postgresql://user:pass@host:port/db
   ENVIRONMENT=LOCAL 
   WEBSHARE_USERNAME=your_username
   WEBSHARE_PASSWORD=your_password
   ```
   
   **Note**: Webshare proxy is optional. If not provided, YouTube transcript fetching will work without a proxy but may be rate-limited.

4. Initialize database:
   ```bash
   uv run python -m app.database.create_tables
   ```
   
   Or check database connection:
   ```bash
   uv run python -m app.database.check_connection
   ```

5. Configure YouTube channels in `app/config.py`

6. Update user profile in `app/profiles/user_profile.py`

### Running

**Full pipeline:**
```bash
uv run main.py
```

**Individual steps:**
```bash
# Scraping
uv run python -m app.runner

# Processing
uv run python -m app.services.process_anthropic
uv run python -m app.services.process_youtube
uv run python -m app.services.process_digest

# Curation
uv run python -m app.services.process_curator

# Email
uv run python -m app.services.process_email
```

### Docker

Build and run:
```bash
docker build -t ai-news-aggregator .
docker run --env-file .env ai-news-aggregator
```

## Key Features

### Advanced Backend Capabilities
- **Multi-Agent LLM Architecture**: Sophisticated agent system with specialized roles for content processing, curation, and personalization
- **Asynchronous Pipeline Orchestration**: Complex workflow management with dependency resolution and parallel execution
- **Hybrid Database Design**: Optimized PostgreSQL for structured data and MongoDB for flexible content storage
- **Enterprise-Grade APIs**: FastAPI-based RESTful services with comprehensive authentication, validation, and documentation
- **Scalable Scraping Framework**: Registry-based scraper system with rate limiting, proxy rotation, and error recovery
- **Intelligent Content Processing**: Multi-modal content handling with LLM-powered summarization and markdown conversion

### Full-Stack Integration
- **Modern Web Frontend**: Next.js application with responsive design and real-time user interactions
- **Secure Authentication**: JWT-based auth system with role-based access control and secure password handling
- **Payment Integration**: Razorpay gateway integration with webhook processing and billing management
- **Real-Time Dashboard**: User interface for managing profiles, channels, and billing information

### Production-Ready Features
- **Environment-Aware Configuration**: Automatic detection and configuration for LOCAL/PRODUCTION environments
- **Containerized Deployment**: Docker-based deployment with optimized images and multi-container orchestration
- **Scheduled Automation**: Cron-based daily pipeline execution with timezone support and manual triggers
- **Comprehensive Monitoring**: Structured logging, error tracking, and performance metrics collection
- **Duplicate Prevention**: Advanced content deduplication algorithms preventing redundant processing
- **Email Delivery Reliability**: SMTP integration with retry mechanisms and bounce handling

## Technology Stack

### Backend Technologies
- **Python 3.12+**: Core language with advanced async/await patterns and type hints
- **FastAPI**: High-performance async web framework with automatic API documentation
- **SQLAlchemy 2.0**: Modern ORM with async support and advanced query optimization
- **Pydantic v2**: Data validation and serialization with JSON Schema generation
- **PostgreSQL**: Relational database with advanced indexing and JSONB support
- **MongoDB**: NoSQL database for unstructured content storage and flexible schemas
- **Groq API**: Ultra-fast LLM inference with Llama-3.3-70b-versatile model

### Frontend Technologies
- **Next.js 14**: React framework with App Router and server-side rendering
- **TypeScript**: Type-safe JavaScript with advanced type inference
- **Tailwind CSS**: Utility-first CSS framework for responsive design
- **ESLint**: Code linting and formatting with custom rules

### Infrastructure & DevOps
- **Docker**: Containerization with multi-stage builds and optimized images
- **Github-actions**: Cloud deployment platform with managed cron jobs
- **Neon-postgreSQL**: Cloud deployment platform with managed PostgreSQL(Neon)
- **Gmail SMTP**: Secure email delivery with OAuth2 authentication
- **Webshare.io**: Proxy rotation for API rate limiting bypass

### Libraries & Tools
- **feedparser**: Robust RSS/Atom feed parsing with error handling
- **youtube-transcript-api**: YouTube video transcript extraction with proxy support
- **BeautifulSoup4**: Advanced HTML parsing and content extraction
- **Jinja2**: Template engine for dynamic email generation
- **python-multipart**: File upload handling for API endpoints
- **passlib**: Password hashing with bcrypt for security
- **python-jose**: JWT token management for authentication

