FROM python:3.13.9-slim-bookworm

WORKDIR /app

# Replace debian sources and install basic tools
RUN set -eux; \
    if [ -f /etc/apt/sources.list.d/debian.sources ]; then \
        sed -i "s|deb.debian.org|mirrors.aliyun.com|g; s|security.debian.org|mirrors.aliyun.com/debian-security|g" /etc/apt/sources.list.d/debian.sources; \
    else \
        sed -i "s|deb.debian.org|mirrors.aliyun.com|g; s|security.debian.org|mirrors.aliyun.com/debian-security|g" /etc/apt/sources.list; \
    fi; \
    apt update && \
    apt-get install -y curl vim tini && \
    apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Install uv
ENV LANG=C.UTF-8 \
    UV_INSTALLER_GHE_BASE_URL="https://files.m.daocloud.io/github.com" \
    UV_PYTHON_INSTALL_MIRROR="https://files.m.daocloud.io/github.com/astral-sh/python-build-standalone/releases/download" \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/root/.local/bin:$PATH"
RUN curl -LsSf -o uv_install.sh https://files.m.daocloud.io/astral.sh/uv/install.sh && \
    sh uv_install.sh && \
    rm uv_install.sh

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Copy application source code
COPY src /app
COPY deployment/gunicorn.py /app/
COPY deployment/entrypoint.sh /app/
RUN chmod u+x /app/entrypoint.sh
RUN mkdir /app/logs

# Update PATH to include the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Healthcheck
HEALTHCHECK --interval=60s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

EXPOSE 8000

ENTRYPOINT ["/usr/bin/tini", "--", "/app/entrypoint.sh"]
CMD ["gunicorn", "-c", "gunicorn.py"]
