FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# HuggingFace Spaces expects the app on port 7860.
#
# NOTE: the live HF Space does NOT use this Dockerfile — the Docker SDK is paywalled on
# that account, so the Space runs the Gradio SDK against app.py (see CLAUDE.md). This file
# is for local/Render use of the FastAPI variant only.
#
# `app:app` was wrong: app.py is now the Gradio module (it exposes `demo`, not `app`), and
# the FastAPI instance moved to app_fastapi.py. The old entrypoint started, failed to find
# the attribute, and the container died.
EXPOSE 7860
CMD ["uvicorn", "app_fastapi:app", "--host", "0.0.0.0", "--port", "7860"]
