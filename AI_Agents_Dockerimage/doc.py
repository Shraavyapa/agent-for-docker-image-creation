import os, time, json, requests, pathlib

# ---- Env from GitHub Secrets or local .env ----
AIF_ENDPOINT = os.environ["AZURE_AIF_ENDPOINT"].rstrip("/")
# Try to use Entra token first (from workflow), fallback to API key
AIF_TOKEN = os.environ.get("AIF_TOKEN")  # Entra token from Azure login
AIF_KEY = os.environ.get("AZURE_AIF_API_KEY")  # API key fallback
AGENT_ID = os.environ["AZURE_AIF_AGENT_ID"]
API_VERSION = "2024-05-01-preview"  # Azure OpenAI Assistants API version

# Minimal project signal to the agent

project_summary = {
    "files": sorted([str(p) for p in pathlib.Path(".").glob("**/*") if p.is_file()])[:50],
    "language_hint": "java",
    "build_tool": "maven",
    "packaging": "war",
    "app_type": "servlet",
    "app_entry": "Deploy WAR to Tomcat"
}

user_prompt = f"""
You are a DevOps agent. Generate a production-ready Dockerfile for a legacy Java servlet application.
Requirements:
- Use multi-stage build (Maven build stage + Tomcat runtime stage)
- Build stage: Use maven:3.8-jdk-8 to build the WAR file
- Runtime stage: Use tomcat:9-jre8-alpine for smaller image
- Copy pom.xml and source code, run mvn clean package
- Copy the WAR file from target/simple-legacy-app.war to Tomcat webapps/
- EXPOSE 8080
- The app runs on Tomcat, accessible at http://localhost:8080/simple-legacy-app/hello
Provide ONLY the Dockerfile content, no explanations or markdown code fences.
Repo summary: {json.dumps(project_summary, indent=2)}
"""

# Use Bearer token if available (Azure Entra), otherwise use API key
headers = {
    "Content-Type": "application/json"
}
if AIF_TOKEN:
    headers["Authorization"] = f"Bearer {AIF_TOKEN}"
    print("Using Entra token authentication")
elif AIF_KEY:
    headers["api-key"] = AIF_KEY
    print("Using API key authentication")
else:
    raise ValueError("Neither AIF_TOKEN nor AZURE_AIF_API_KEY is set")

def _post(url, payload):
    print(f"POST {url}")
    r = requests.post(url, headers=headers, json=payload)
    if r.status_code >= 400:
        print(f"Error response: {r.status_code}")
        print(f"Response body: {r.text}")
    r.raise_for_status()
    return r.json()

def _get(url):
    print(f"GET {url}")
    r = requests.get(url, headers=headers)
    if r.status_code >= 400:
        print(f"Error response: {r.status_code}")
        print(f"Response body: {r.text}")
    r.raise_for_status()
    return r.json()

def main():
    print(f"Using endpoint: {AIF_ENDPOINT}")
    print(f"Using API version: {API_VERSION}")
    print(f"Using agent ID: {AGENT_ID}")
    
    # 1) Create a thread
    thread = _post(f"{AIF_ENDPOINT}/threads?api-version={API_VERSION}", {})
    thread_id = thread["id"]

    # 2) Post a message
    _post(f"{AIF_ENDPOINT}/threads/{thread_id}/messages?api-version={API_VERSION}", {
        "role": "user",
        "content": user_prompt
    })

    # 3) Create a run with your agent
    run = _post(f"{AIF_ENDPOINT}/threads/{thread_id}/runs?api-version={API_VERSION}", {
        "assistant_id": AGENT_ID,
        "instructions": "Respond with only the Dockerfile content."
    })
    run_id = run["id"]

    # 4) Poll until completed
    status = run.get("status", "")
    for _ in range(120):  # ~2–3 min max polling
        time.sleep(2)
        run = _get(f"{AIF_ENDPOINT}/threads/{thread_id}/runs/{run_id}?api-version={API_VERSION}")
        status = run.get("status", "")
        if status in ("completed", "failed", "cancelled"):
            break

    if status != "completed":
        print(f"\n❌ Run failed with status: {status}")
        print(f"Run details: {json.dumps(run, indent=2)}")
        if "last_error" in run:
            print(f"Error: {run['last_error']}")
        raise RuntimeError(f"Agent run did not complete; status={status}")

    # 5) Retrieve the final assistant message(s)
    msgs = _get(f"{AIF_ENDPOINT}/threads/{thread_id}/messages?api-version={API_VERSION}")
    # Get latest assistant message content
    dockerfile_text = None
    for m in reversed(msgs.get("data", [])):
        if m.get("role") == "assistant":
            parts = m.get("content", [])
            # Expect a single text part
            for p in parts:
                if p.get("type") == "text":
                    dockerfile_text = p["text"]
                    if isinstance(dockerfile_text, dict) and "value" in dockerfile_text:
                        dockerfile_text = dockerfile_text["value"]
                    break
            if dockerfile_text:
                break

    if not dockerfile_text:
        raise RuntimeError("Assistant response missing Dockerfile text")

    # Sanitise any markdown fences if present
    dockerfile_text = dockerfile_text.strip()
    if "```" in dockerfile_text:
        # Extract between backticks
        start = dockerfile_text.find("```")
        lang = dockerfile_text[start: start + 10].lower()
        end = dockerfile_text.rfind("```")
        # Remove fences if present
        dockerfile_text = dockerfile_text[start + 3: end].lstrip()
        # If agent accidentally prefixed 'dockerfile' on first line, keep content below
        if dockerfile_text.lower().startswith("dockerfile"):
            dockerfile_text = "\n".join(dockerfile_text.splitlines()[1:])

    with open("Dockerfile", "w", encoding="utf-8") as f:
        f.write(dockerfile_text)

    print("Dockerfile generated by Azure AI Foundry agent ✅")

if __name__ == "__main__":
    main()
