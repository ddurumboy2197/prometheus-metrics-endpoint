from fastapi import FastAPI
from fastapi.responses import JSONResponse
from prometheus_client import Counter, Gauge, Histogram, start_http_server

app = FastAPI()

# Prometheus metrikalari uchun kengaytirilgan funksiyalar
class PrometheusMetrics:
    def __init__(self):
        self.requests_total = Counter('requests_total', 'Jami so\'rovlar soni')
        self.response_time = Histogram('response_time', 'Majburiy javob vaqti')
        self.successful_requests = Gauge('successful_requests', 'Muvaffaqiyatli so\'rovlar soni')

    def increment_requests_total(self):
        self.requests_total.inc()

    def record_response_time(self, response_time):
        self.response_time.observe(response_time)

    def increment_successful_requests(self):
        self.successful_requests.inc()

# Prometheus metrikalari uchun kengaytirilgan funksiyalar
metrics = PrometheusMetrics()

# FastAPI uchun endpoint
@app.get("/")
async def read_root():
    metrics.increment_requests_total()
    metrics.record_response_time(0.5)  # Majburiy javob vaqti
    return JSONResponse(content={"message": "Salom, dunyo!"}, media_type="application/json")

# Prometheus metrikalari uchun endpoint
@app.get("/metrics")
async def read_metrics():
    metrics.increment_successful_requests()
    return JSONResponse(content={"metrics": metrics.requests_total.value, "response_time": metrics.response_time.value}, media_type="application/json")

# Prometheus serverni boshlash uchun funksiya
def start_prometheus_server():
    start_http_server(8000)

# FastAPI serverni boshlash uchun funksiya
def start_fastapi_server():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

# Main funksiya
def main():
    start_prometheus_server()
    start_fastapi_server()

if __name__ == "__main__":
    main()
```

Bu kodda FastAPI uchun endpoint va Prometheus metrikalari uchun endpoint mavjud. Prometheus metrikalari uchun kengaytirilgan funksiyalar mavjud bo'lib, ular FastAPI endpointlarida ishlatiladi. FastAPI serveri va Prometheus serveri alohida alohida boshlanadi.
