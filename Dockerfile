FROM python:3.12-slim AS builder
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /build

RUN apt-get update -qq && \
    apt-get install -y -qq wget curl ca-certificates tar && \
    pip install --no-cache-dir --upgrade pip && \   # <-- added
    pip install --no-cache-dir flask docker requests && \
    curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh \
      | sh -s -- -b /build/trivy-bin && \
    chmod +x /build/trivy-bin/trivy

COPY dockerscan /build/app

FROM python:3.12-slim
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY --from=builder /build/trivy-bin/trivy /usr/local/bin/trivy
COPY --from=builder /build/app /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

EXPOSE 8888
CMD ["python", "server.py"]
