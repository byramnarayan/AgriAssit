# Agricultural Assistant Platform (AgriAssist)

An intelligent, AI-powered agricultural ecosystem built with **FastAPI**, **Google Gemini AI**, **PostgreSQL (Supabase)**, **Neo4j Graph Database**, and **Twilio Voice IVR**.

The platform empowers rural farmers and urban growers alike through automated plant disease and invasive weed detection, interactive multilingual voice assistance (IVR), geodesic farm mapping, carbon credit certification, neighbor-aware crop intelligence, and an autonomous multi-agent business intelligence command center.

---

## 🌟 Key Features

### 📞 Interactive Voice Response (IVR) & Krishi Sahayata Voice AI
- **Dual-Channel Accessibility**: Accessible both via regular cellular phone calls (Twilio telephony webhooks) and directly within web browsers through WebRTC (`@twilio/voice-sdk`) with an on-screen visual dialpad.
- **Native Hindi Speech (Text-to-Speech & ASR)**: Uses Amazon Polly neural voice (`Polly.Aditi`) and Twilio Speech-to-Text for seamless conversational interaction without requiring smartphone literacy.
- **Interactive DTMF & Voice Menu**:
  - **Key 1 (फसल सलाह)**: Context-aware seasonal crop advisory personalized with farmer's soil type, farm size, and neighboring crop trends from Neo4j.
  - **Key 2 (बाजार भाव)**: Real-time APMC Mandi commodity market prices per quintal with live price trend indicators (📈 Rising, 📉 Falling, ➡️ Stable).
  - **Key 3 (मौसम अपडेट)**: GPS-targeted agricultural weather reports (temperature, sky condition, rain outlook) powered by Open-Meteo and Gemini AI.
  - **Key 4 (AI सहायक से बात करें)**: Open-ended conversational voice assistant where farmers ask questions naturally in Hindi, grounded by their profile and farm metadata.

### 🌱 Dual-Engine Plant Identification
- **Offline / Edge Detection**: Ultralytics **YOLOv8** (`yolov8n.pt`) detects plant anomalies and generates localized bounding box annotations.
- **Botanical Multimodal AI**: **Google Gemini 2.5 Flash (Vision)** identifies plant species, common names, regional vernacular names, invasive status, threat levels, and recommended organic/chemical removal methods.
- **Proximity Alerts**: Identifications flagged as invasive trigger automatic outbreak alerts for neighboring farms within a 5 km radius in Neo4j.

### 🏙️ Urban Farmer Ecosystem (v2.0)
- **Balcony & Rooftop Farming**: Tailored for city dwellers to optimize urban micro-gardens, terraces, and window sills.
- **Interactive Polygon Canvas**: Mark cultivation zones directly on photos; Gemini Vision calculates usable area ($m^2$), sunlight exposure hours, container requirements, and companion planting layouts.
- **Urban Carbon Offsets & Yield Forecasting**: Estimates monthly vegetable/herb yields, expected household savings, and urban micro carbon credits.

### 🗺️ Geospatial Farm Mapping & Proximity Intelligence
- **Polygon Area Calculation**: Map farm boundaries using GPS coordinates and compute precise land size in hectares and acres via **Shapely** and **PyProj**.
- **Neo4j Graph Intelligence**: Maps spatial proximity between farms, clustering neighbor soil types, and analyzing community planting trends.

### 🍃 Carbon Credit Estimation & Document Verification
- **Automated Valuation**: Calculates annual sequestered carbon credits and estimated INR value based on farm size, soil classification, and irrigation methods.
- **Land Title Document Verification**: Farmers upload land ownership deeds (7/12 extract, title records) securely to **Supabase Storage**.
- **Admin Verification Workflow**: Administrators review submitted documents, approve/reject certification, and issue formal verification status.

### 🤖 Multi-Agent Business Intelligence (Admin Command Center)
- **LangChain-Powered Agent Orchestrator**: Coordinates 5 specialized autonomous AI agents with real-time **Server-Sent Events (SSE)** streaming (Perplexity-style live execution steps and thoughts):
  1. **Portfolio Analysis Agent**: High-level platform health, total verified acreage, carbon credit aggregates, and soil distribution.
  2. **Personalized Campaigns Agent**: Cross-sell and upsell intelligence, farmer engagement scoring, and personalized SMS/call outreach recommendations.
  3. **Retention Analysis Agent**: Churn risk prediction, identifying inactive farmers, and regional vulnerability hotspots.
  4. **Crop Advisor Audit Agent**: Audits recommendation quality against historical crop yields and market price profitability.
  5. **Data Visualization Agent**: Dynamically generates live Matplotlib charts, heatmaps, and land-distribution plots on the fly with accompanying AI commentary.

### 🏆 Gamification & Engagement
- **Levels & Badges**: Earn points for plant scans, destroying invasive weeds, mapping farms, and verifying land records.
- **Community Leaderboard**: Fosters friendly competition and community-driven sustainable farming practices.

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| **Backend Framework** | [FastAPI](https://fastapi.tiangolo.com/) (Python 3.11+), Uvicorn, Pydantic v2 |
| **Relational Database** | **PostgreSQL (Supabase)** *(Current active database)*, SQLAlchemy 2.0 ORM, Alembic migrations<br>*(SQLite supported for local testing & development)* |
| **Graph Database** | **Neo4j** (AuraDB / Bolt 5.16) for geospatial graph relationships, farmer proximity, and community trends |
| **Cloud Storage** | **Supabase Storage** for farm land records (PDF/images) and plant scan media |
| **Telephony & IVR** | **Twilio Voice API**, TwiML, Twilio WebRTC Voice JS SDK (`@twilio/voice-sdk`), Amazon Polly (`Polly.Aditi`) |
| **AI & Multimodal LLMs** | **Google Gemini 2.5 Flash** (Vision & Pro) with **API Key Rotation Pool** (`GEMINI_API_KEY_POOL`) |
| **AI Redundancy Fallback** | **Groq API** (LLaMA-3 / LLaMA-3.3) for instant zero-downtime failover if Gemini quotas exhaust |
| **Computer Vision** | **Ultralytics YOLOv8** (`yolov8n.pt`), OpenCV, Pillow (PIL) image compression |
| **Agentic Framework** | **LangChain Core** (`@tool` wrappers, Agent Orchestrator, SSE Streaming) |
| **Geospatial & Analytics** | **Shapely**, **PyProj**, **Open-Meteo API** (live weather), **Matplotlib** (chart generation) |
| **Frontend** | Jinja2 Templates, Vanilla CSS & Tailwind CSS, Twilio Voice Client, Canvas API |

---

## 🏗️ Architecture & Database Evolution

```
                          ┌────────────────────────────────────────┐
                          │         Client Applications            │
                          │   (Web Browser / Telephony Mobile)     │
                          └──────────────────┬─────────────────────┘
                                             │ HTTP / WebRTC / Twilio
                                             ▼
                          ┌────────────────────────────────────────┐
                          │         FastAPI Application            │
                          │        (REST APIs + Jinja2)            │
                          └────┬────────────┬─────────────┬────────┘
                               │            │             │
                 SQLAlchemy    │            │ Cypher      │ REST
                     ORM       ▼            ▼             ▼
  ┌───────────────────────────────┐  ┌─────────────┐  ┌───────────────────┐
  │ PostgreSQL (Supabase)         │  │ Neo4j Graph │  │ Supabase Storage  │
  │ • Farmers & Admins            │  │ • Farmer    │  │ • Land Documents  │
  │ • Farms & Verification Status │  │ • Farm      │  │ • Plant Imagery   │
  │ • Plant Scans & Alerts        │  │ • Proximity │  └───────────────────┘
  │ • Mandi Market Prices         │  │ • Outbreaks │
  │ *(SQLite fallback for dev)*   │  └─────────────┘
  └───────────────────────────────┘         ▲
                                            │ Spatial Context
                                            ▼
                       ┌────────────────────────────────────────┐
                       │        AI & Telephony Services         │
                       │ • Gemini 2.5 Flash (Key Pool Rotation) │
                       │ • Groq LLaMA-3 Failover Fallback       │
                       │ • Twilio Voice IVR + Polly.Aditi       │
                       │ • LangChain Multi-Agent Orchestrator   │
                       │ • Ultralytics YOLOv8 Computer Vision   │
                       │ • Open-Meteo Weather Service           │
                       └────────────────────────────────────────┘
```

> [!NOTE]
> **Database Evolution Note**:
> - **Initial Development**: SQLite (`agritech.db`) was used for lightweight standalone testing and rapid prototyping without external dependencies.
> - **Current Production**: The platform runs on **PostgreSQL hosted via Supabase** for concurrent connection pooling, robust relational constraints, and production stability, paired with **Neo4j** for graph traversals and **Supabase Storage** for cloud asset hosting.

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Sarvesh-Bhartu/agriassist.git
cd agriassist
```

### 2. Create Virtual Environment
```bash
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to create your `.env` file:
```bash
cp .env.example .env
```

Configure your credentials inside `.env`:
```env
# Application
APP_NAME=Agricultural Assistant Platform
APP_ENV=development
SECRET_KEY=your-strong-secret-key-for-jwt
DEBUG=True

# Database (PostgreSQL on Supabase)
# For local SQLite testing: DATABASE_URL=sqlite:///./agritech.db
DATABASE_URL=postgresql://postgres.your-project:password@aws-0-region.pooler.supabase.com:6543/postgres

# Supabase Cloud Storage
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-supabase-service-role-key

# Neo4j Graph Database (AuraDB or Local Desktop)
NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-neo4j-password
NEO4J_DATABASE=neo4j

# Google Gemini AI & Rotation Pool
GEMINI_API_KEY=your-primary-gemini-api-key
GEMINI_API_KEY_POOL=key1,key2,key3,key4

# Groq API (Zero-downtime text fallback)
GROQ_API_KEY=your-groq-api-key

# Twilio Telephony & WebRTC Voice Bot (IVR)
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_API_KEY=your-twilio-api-key
TWILIO_API_SECRET=your-twilio-api-secret
TWILIO_TWIML_APP_SID=your-twiml-app-sid
TWILIO_PHONE_NUMBER=+1xxxxxxxxxx
```

### 5. Seed Initial Data
```bash
# Initialize DB tables and create default admin
python script_create_admin.py

# Create demo farmer credentials
python seed_demo_user.py

# Seed current Mandi commodity prices
python seed_prices.py

# Sync relational SQL data to Neo4j graph nodes
python sync_neo4j.py
```

### 6. Run the Application
```bash
# Development server with hot reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Access the Application
- **Web App**: [http://localhost:8000](http://localhost:8000)
- **Interactive Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Admin Portal**: [http://localhost:8000/admin](http://localhost:8000/admin)
- **Urban Farmer Ecosystem**: [http://localhost:8000/urban/space/dashboard](http://localhost:8000/urban/space/dashboard)

---

## 📁 Project Structure

```
agriassist/
├── app/
│   ├── core/                    # Core configuration, security, database & storage
│   │   ├── config.py            # Pydantic environment settings
│   │   ├── database.py          # SQLAlchemy engine (Postgres/SQLite dynamic switch)
│   │   ├── neo4j_driver.py      # Neo4j graph driver connection manager
│   │   ├── security.py          # Password hashing, JWT auth, role validation
│   │   └── storage.py           # Supabase Storage client with collision prevention
│   ├── graph/                   # Cypher graph schemas & queries
│   │   └── urban_farmer_schema.cypher
│   ├── ml_models/               # Local machine learning & computer vision models
│   │   └── yolov8n.pt           # Ultralytics YOLOv8 model weights
│   ├── models/                  # SQLAlchemy models & Pydantic schemas
│   │   ├── alert.py             # Notifications & outbreak alerts
│   │   ├── crop.py              # Market prices & crop trends
│   │   ├── farm.py              # Farm geometry, carbon credits & verification
│   │   ├── gamification.py      # Points, badges & achievements
│   │   ├── plant.py             # Plant detection history & invasive status
│   │   ├── schemas.py           # Request & response schemas
│   │   ├── urban_farmer_models.py
│   │   └── user.py              # Farmer and Admin models
│   ├── routers/                 # FastAPI REST and Webhook endpoints
│   │   ├── admin.py             # Admin dashboard, land verification & agent chat
│   │   ├── alerts.py            # Alert queries and status updates
│   │   ├── auth.py              # Farmer registration and JWT login
│   │   ├── dashboard.py         # Dashboard statistics aggregation
│   │   ├── farms.py             # Farm creation, area calculation & document uploads
│   │   ├── gamification.py      # Leaderboard, stats, and badge collections
│   │   ├── plants.py            # Dual-engine plant scanner & verification
│   │   ├── recommendations.py   # Crop recommendation endpoints
│   │   ├── urban_farmer/        # Urban Agriculture subsystem
│   │   │   ├── auth.py          # Urban farmer authentication
│   │   │   └── space.py         # Balcony/rooftop polygon submission & analysis
│   │   └── voice_bot.py         # Twilio IVR webhooks, DTMF menu & WebRTC token
│   ├── services/                # Business logic and external service integrations
│   │   ├── agents/              # LangChain Multi-Agent BI system
│   │   │   ├── agent_crop_advisor.py     # Advisory quality auditor agent
│   │   │   ├── agent_orchestrator.py     # LangChain orchestrator + SSE streaming
│   │   │   ├── agent_personalized.py     # Cross-sell/upsell campaign agent
│   │   │   ├── agent_portfolio.py        # Executive portfolio BI agent
│   │   │   ├── agent_retention.py        # Churn prediction & retention agent
│   │   │   └── agent_visualization.py    # Dynamic chart & heatmap generator agent
│   │   ├── alert_service.py     # Notification dispatching
│   │   ├── carbon_service.py    # Carbon credit formula calculation
│   │   ├── farm_calculator.py   # Geospatial polygon area calculations
│   │   ├── gamification_service.py # Points, tiers, and badge evaluation
│   │   ├── gemini_service.py    # Gemini 2.5 Flash + rotation pool + Groq failover
│   │   ├── graph_service.py     # Neo4j queries for proximity & community trends
│   │   ├── market_service.py    # Mandi commodity price updates & trends
│   │   ├── recommendation_service.py # AI crop recommendation logic
│   │   ├── urban_gemini_service.py   # Balcony polygon analysis & planting plans
│   │   ├── vision_service.py    # YOLOv8 inference wrapper
│   │   └── weather_service.py   # Open-Meteo real-time weather integration
│   ├── static/                  # CSS stylesheets, JavaScript files & assets
│   ├── templates/               # Jinja2 HTML templates
│   └── main.py                  # FastAPI application entrypoint & middleware
├── uploads/                     # Local fallback storage directory
├── script_create_admin.py       # Admin initialization utility
├── seed_demo_user.py            # Demo farmer seeder
├── seed_prices.py               # Mandi price seeder
├── sync_neo4j.py                # Postgres/SQLite to Neo4j synchronizer
├── requirements.txt             # Python dependencies
├── Procfile                     # Web server process file
├── railway.toml                 # Railway deployment configuration
├── nixpacks.toml                # Nixpacks system dependencies build config
└── .env.example                 # Example environment variables template
```

---

## 📡 API Endpoints Overview

### 🔐 Authentication & Users
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/register` | Register new farmer account |
| `POST` | `/api/auth/login` | Authenticate farmer and obtain JWT token |
| `GET` | `/api/auth/me` | Retrieve profile and gamification stats of authenticated farmer |

### 📞 IVR & Voice Assistant
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/voice/token` | Generate Twilio Client JWT token for WebRTC in-browser calls |
| `POST` | `/api/voice/webhook` | Incoming Twilio voice call webhook; handles caller lookup and speaks main menu in Hindi |
| `POST` | `/api/voice/menu` | Processes DTMF digit selection (1: Crop Advice, 2: Mandi Prices, 3: Weather, 4: AI Voice Assistant) |
| `POST` | `/api/voice/ai-response` | Transcribes spoken question (ASR) and generates conversational spoken Hindi audio reply |

### 🌱 Plant Identification
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/plants/identify` | Upload image for dual YOLOv8 + Gemini 2.5 Flash botanical & invasive identification |
| `GET` | `/api/plants/history` | Retrieve user's plant detection scan history |
| `POST` | `/api/plants/{id}/mark-destroyed` | Mark confirmed invasive plant as destroyed and receive bonus gamification points |

### 🌾 Farm Management & Land Records
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/farms/` | Create new farm with GPS boundary coordinates (synced to Neo4j) |
| `GET` | `/api/farms/` | List all farms belonging to current farmer |
| `GET` | `/api/farms/{id}` | Get specific farm details, calculated area, and carbon estimates |
| `POST` | `/api/farms/{id}/document` | Upload land record document (7/12 extract) to Supabase Storage for verification |
| `POST` | `/api/farms/{id}/calculate-carbon` | Recalculate annual carbon credit yield |

### 💡 Crop Recommendations
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/recommendations/` | Generate Gemini AI crop recommendations grounded by soil and Neo4j neighbor trends |

### 🏙️ Urban Farmer Ecosystem
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/urban/auth/register` | Register an urban farmer account in Neo4j |
| `GET` | `/urban/space/list` | Retrieve all urban spaces registered to the user |
| `POST` | `/urban/space/submit` | Upload balcony/terrace photos with polygon boundary JSON for Gemini analysis |

### 🛡️ Admin & Multi-Agent BI Command Center
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/admin/login` | Admin login and cookie/JWT authorization |
| `GET` | `/api/admin/dashboard` | List all farms with land verification documents and approval statuses |
| `POST` | `/api/admin/farms/{id}/verify` | Approve or reject farm land document and issue carbon credit verification |
| `GET` | `/api/admin/chat` | **SSE Streaming Endpoint**: Perplexity-style live reasoning and agent tool execution |
| `GET` | `/api/admin/agents/portfolio` | Run Portfolio Analysis Agent for platform KPIs |
| `GET` | `/api/admin/agents/personalized`| Run Targeted Outreach & Cross-Sell Agent |
| `GET` | `/api/admin/agents/retention` | Run Farmer Retention & Churn Risk Agent |
| `GET` | `/api/admin/agents/crop-advisor`| Run Crop Recommendation Audit Agent |
| `GET` | `/api/admin/agents/visualization`| Run Dynamic Data Visualization Agent (generates live charts) |

### 🔔 Alerts & Gamification
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/alerts/` | Fetch notifications and nearby 5 km invasive plant outbreak alerts |
| `POST` | `/api/alerts/{id}/mark-read` | Mark alert as read |
| `GET` | `/api/gamification/leaderboard` | View top farmer leaderboard rankings |
| `GET` | `/api/gamification/badges` | List all available and unlocked badges |
| `GET` | `/api/gamification/my-stats` | Fetch current level, points to next tier, and achievements |

---

## 🔑 Demo Credentials

To explore the application locally without manual registration:

### Farmer Login
- **URL**: [http://localhost:8000/login](http://localhost:8000/login)
- **Phone**: `9876543210` (or `+919876543210`)
- **Password**: `Demo@123`

### Admin Command Center
- **URL**: [http://localhost:8000/admin](http://localhost:8000/admin)
- **Admin ID**: `T12478`
- **Password**: `Offcial@12897`

---

## 🚢 Deployment & Production Readiness

The codebase includes out-of-the-box support for containerized and PaaS deployments:

- **Procfile**: Runs FastAPI with Uvicorn configured for dynamic `$PORT` assignment.
- **Railway / Nixpacks**: Configured via `railway.toml` and `nixpacks.toml` including OpenGL (`libGL`) and GLib system packages for OpenCV and YOLOv8 image processing.
- **Production Checklist**:
  1. Set `DEBUG=False` in `.env`.
  2. Point `DATABASE_URL` to your production Supabase PostgreSQL connection pool.
  3. Ensure `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` point to your Supabase project with a public `farm-documents` storage bucket.
  4. Connect `NEO4J_URI` to a managed Neo4j AuraDB instance.
  5. Provide a comma-separated list of Gemini keys in `GEMINI_API_KEY_POOL` to enable automatic key cycling under heavy traffic.
  6. Configure your Twilio webhook URL to point to `https://your-domain.com/api/voice/webhook`.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

**Built with ❤️ for Indian Farmers & Sustainable Urban Growers**
