# Dockerfile for PATH Framework

# Multi-stage build for optimal image size
FROM python:3.11-slim AS builder

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies in virtual environment
RUN uv sync --frozen --no-dev

# Production stage
FROM python:3.11-slim AS production

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash pathuser

# Set working directory
WORKDIR /app

# Copy UV binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy source code
COPY path_framework ./path_framework
COPY framework ./framework
COPY templates ./templates
COPY pyproject.toml ./

# Change ownership to pathuser
RUN chown -R pathuser:pathuser /app

# Switch to non-root user
USER pathuser

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD uv run path --help || exit 1

# Expose port for web interface (if implemented)
EXPOSE 8000

# Default command
CMD ["uv", "run", "path", "--help"]

# Development stage
FROM builder AS development

# Install development dependencies
RUN uv sync

# Install additional development tools
RUN apt-get update && apt-get install -y \
    git \
    curl \
    vim \
    htop \
    && rm -rf /var/lib/apt/lists/*

# Copy all source code including tests
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash pathdev
RUN chown -R pathdev:pathdev /app

USER pathdev

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Default command for development
CMD ["bash"]
