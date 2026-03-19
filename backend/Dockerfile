# 1. BASE IMAGE
# Start with a lightweight Linux machine that already has Python 3.12
# "slim" = minimal version (~150MB instead of ~900MB)
FROM python:3.12-slim

# 2. WORKING DIRECTORY
# Create /app folder inside the container and cd into it
# All future commands run inside /app
WORKDIR /app

# 3. COPY REQUIREMENTS FIRST (for caching)
# Docker caches each step. If requirements.txt hasn't changed,
# Docker skips the pip install step on rebuild = much faster rebuilds
COPY requirements.txt .

# 4. INSTALL PYTHON PACKAGES
# --no-cache-dir = don't store pip's download cache (saves image space)
RUN pip install --no-cache-dir -r requirements.txt

# 5. COPY THE REST OF YOUR CODE
# Done AFTER pip install so changing code doesn't re-trigger pip install
COPY . .

# 6. EXPOSE PORT
# Tells Docker/Render this app listens on port 8001
EXPOSE 8001

# 7. START COMMAND
# --host 0.0.0.0 = accept connections from outside the container (required!)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]