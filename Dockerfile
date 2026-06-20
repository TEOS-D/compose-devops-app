FROM python:3.13-slim AS builder

WORKDIR /build

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt


FROM python:3.13-slim AS runtime

WORKDIR /app

RUN adduser --disabled-password --gecos "" appuser

COPY --from=builder /root/.local /home/appuser/.local
COPY app.py /app/app.py

RUN chown -R appuser:appuser /app /home/appuser/.local

USER appuser

ENV PATH="/home/appuser/.local/bin:${PATH}"
ENV PORT=3000

EXPOSE 3000

CMD ["python", "app.py"]
