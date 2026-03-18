# Legacy Java Servlet Application - AI-Generated Dockerfile

This project demonstrates using **Azure OpenAI Agent** to automatically generate Dockerfiles for a legacy Java servlet application and push images to Azure Container Registry.

## Application Details

- **Type**: Legacy Java Servlet (WAR)
- **Server**: Apache Tomcat 9
- **Java Version**: 8
- **Build Tool**: Maven
- **Endpoint**: `/simple-legacy-app/hello`

## How It Works

1. **Azure OpenAI Agent** analyzes your legacy Java servlet code
2. **Generates** a production-ready multi-stage Dockerfile with:
   - Build stage: Maven 3.8 + JDK 8
   - Runtime stage: Tomcat 9 + JRE 8 Alpine
3. **Builds** the Docker image
4. **Pushes** to Azure Container Registry (ACR)

## Local Development

```bash
# Build the WAR file
mvn clean package

# Deploy to local Tomcat
cp target/simple-legacy-app.war /path/to/tomcat/webapps/

# Or run with Docker (after Dockerfile is generated)
docker build -t legacy-app .
docker run -p 8080:8080 legacy-app

# Access the app
curl http://localhost:8080/simple-legacy-app/hello
```

## GitHub Actions Workflow

On every push to `main`:
1. Azure OpenAI Agent generates optimized Dockerfile
2. Builds Docker image with multi-stage build
3. Pushes to ACR as `legacy-servlet-app:latest`

## Repository Structure

```
Java-assignment/
├── src/main/java/com/kyndryl/HelloLegacyServlet.java  # Servlet code
├── src/main/webapp/WEB-INF/web.xml                     # Servlet config
├── pom.xml                                             # Maven config
├── doc.py                                              # AI agent caller
├── requirements.txt                                    # Python deps for doc.py
└── .github/workflows/main.yaml                         # CI/CD workflow
```

## Azure Resources Used

- **Azure OpenAI**: GPT-4.1 model for Dockerfile generation
- **Azure Container Registry**: Stores Docker images
- **GitHub Actions**: Automated CI/CD pipeline

## Secrets Required (Already configured)

- `AZURE_CREDENTIALS` - Service principal for Azure login
- `AZURE_AIF_ENDPOINT` - Azure OpenAI endpoint
- `AZURE_AIF_AGENT_ID` - Assistant ID
- `ACR_NAME` - Container registry name

---

**Generated Dockerfile will include:**
- Multi-stage build (Maven → Tomcat)
- Optimized layer caching
- Minimal runtime image (Alpine-based)
- Health checks
- Security best practices.
