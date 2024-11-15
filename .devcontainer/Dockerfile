# Stage 1: Backend Environment (Python with FastAPI)
FROM python:3.12-slim as backend

# Set working directory
WORKDIR /app/backend

# Install dependencies
COPY ./backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./backend/. .

# Stage 2: Frontend Environment (Node.js with React)
FROM node:22-slim as frontend

# Set working directory
WORKDIR /app/frontend

# Install dependencies and build the app
COPY ./frontend/package*.json ./
RUN npm install
COPY ./frontend/. .

# Stage 3: Final Image (Combining both environments)
FROM python:3.12-slim

# Install necessary tools for running FastAPI with Uvicorn
RUN apt-get update && apt-get install -y curl gnupg2 \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Set working directories for both backend and frontend
WORKDIR /app

# Copy backend code and dependencies
COPY --from=backend /app/backend ./backend

# Copy frontend build files
COPY --from=frontend /app/frontend/build ./frontend/build

# Install backend dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Expose ports
EXPOSE 8000
EXPOSE 3000

# Start both services
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port 8000 & npm start --prefix ./frontend"]