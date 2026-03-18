# AI Discovery Agent

An intelligent code discovery agent that automatically analyzes legacy applications to identify dependencies, API endpoints, and database connections using AI-powered pattern recognition.

## 📋 Overview

This project provides an **AI-Enhanced Discovery Agent** that scans Java applications and uses Azure OpenAI to intelligently detect:
- **Dependencies**: Maven/Gradle libraries, Python packages, npm modules
- **API Endpoints**: Servlets, REST APIs, Spring Boot endpoints
- **Database Connections**: PostgreSQL, MySQL, MongoDB, Redis, SQL Server

## 🎯 Key Features

- **Hybrid Detection**: Combines regex pattern matching with Azure OpenAI intelligence
- **Configurable AI Mode**: Run with or without AI enhancement
- **High Accuracy**: Achieves 100% detection rate on test applications
- **Multiple Languages**: Supports Java, Python, JavaScript/TypeScript, C#
- **Framework Detection**: Recognizes Spring Boot, Servlets, Flask, FastAPI, Express

## 📁 Project Structure

```
DiscoveryAI_agent/
├── ai_agent.py              # Main discovery agent script
├── pom.xml                  # Maven configuration
├── requirements.txt         # Python dependencies
├── src/                     # Java source code
│   └── main/
│       ├── java/
│       │   └── com/kyndryl/
│       │       └── HelloLegacyServlet.java  # Sample servlet
│       └── webapp/
│           └── WEB-INF/
│               └── web.xml  # Servlet configuration
└── target/                  # Compiled classes
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Azure OpenAI Account** (optional, for AI mode)
- **Azure CLI** (optional, for AI mode)

### Installation

1. Install Python dependencies:
```powershell
pip install -r requirements.txt
```

2. (Optional) Login to Azure CLI for AI features:
```powershell
az login
```

### Usage

**Basic Mode (Regex Only):**
```powershell
py ai_agent.py .
```

**AI-Enhanced Mode:**
```powershell
$env:USE_AI = "true"
py ai_agent.py .
```

**Scan Different Directory:**
```powershell
py ai_agent.py C:\path\to\application
```

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `USE_AI` | `true` | Enable/disable AI analysis |
| `AZURE_AIF_ENDPOINT` | `https://xxxxxxxxxxxxx.openai.azure.com/` | Azure OpenAI endpoint |

**Example:**
```powershell
$env:USE_AI = "false"              # Disable AI
$env:AZURE_AIF_ENDPOINT = "https://your-endpoint.openai.azure.com/"
```

## 📊 Sample Output

```
============================================================
AI-Enhanced Discovery Agent
Scanning: .
AI Mode: ✅ ENABLED
============================================================

📦 DEPENDENCIES (3 found):
  - Maven: jakarta.servlet-api
  - Maven: simple-legacy-app-demo3
  - Python: requests==2.32.3

🌐 API ENDPOINTS (4 found):
  - Servlet GET /hello
  - Servlet GET /api/hello
  - Servlet POST /hello
  - Servlet POST /api/hello

💾 DATABASE CONNECTIONS (1 found):
  - PostgreSQL in HelloLegacyServlet.java

============================================================
Total items found: 8
Detection rate: 100.0%
KPI Status: ✅ PASS
============================================================
```

## 🧠 How It Works

### Detection Methods

1. **Regex Pattern Matching** (Always Active)
   - Scans configuration files (pom.xml, build.gradle, requirements.txt, package.json)
   - Uses regex to find API annotations (@WebServlet, @GetMapping, @app.route)
   - Searches for database connection strings (jdbc:postgresql, mongodb://)

2. **AI Enhancement** (Optional)
   - Sends code snippets to Azure OpenAI for intelligent analysis
   - Understands context and identifies complex patterns
   - Finds subtle dependencies and non-standard implementations
   - Provides insights on code architecture

### Supported Patterns

**Dependencies:**
- Maven (pom.xml)
- Gradle (build.gradle)
- Python (requirements.txt)
- npm (package.json)

**API Endpoints:**
- Java Servlets (@WebServlet)
- Spring Boot (@GetMapping, @PostMapping, etc.)
- Flask (@app.route)
- FastAPI (@router.get, @router.post)

**Databases:**
- PostgreSQL
- MySQL
- MongoDB
- Redis
- SQL Server

## 🎓 Sample Application

The included Java servlet demonstrates:
- Jakarta Servlet API usage
- Multiple URL mappings (`/hello`, `/api/hello`)
- GET and POST method handlers
- PostgreSQL database connection configuration

## 📈 KPI Metrics

- **Target Detection Rate**: ≥ 80%
- **Achieved Rate**: 100% (on sample application)
- **Total Items Detected**: 8 (3 dependencies + 4 APIs + 1 database)

## 🔧 Troubleshooting

**Issue**: AI mode shows warnings
```
⚠ Warning: Could not get Azure token
```
**Solution**: Install and login to Azure CLI:
```powershell
az login
```

**Issue**: Agent not finding APIs
**Solution**: Ensure your code uses standard annotations or patterns. Enable AI mode for better detection.

**Issue**: Import errors
**Solution**: Install dependencies:
```powershell
pip install requests
```

## 🤝 Use Cases

- **Legacy Application Migration**: Discover all dependencies before cloud migration
- **Architecture Documentation**: Auto-generate component diagrams
- **Code Review**: Identify all external integrations
- **Security Audit**: Find all API endpoints and database connections
- **Dependency Management**: Track outdated libraries




