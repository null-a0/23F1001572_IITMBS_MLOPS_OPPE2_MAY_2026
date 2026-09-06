FROM python:3.12-slim

WORKDIR /app

COPY heart_disease_model.pkl .
COPY app.py .

RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    pandas \
    scikit-learn \
    joblib

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
