# Fuel Route Optimizer API

A Django REST API that calculates the most cost-effective fuel stops along travel routes in the USA using route optimization, fuel price analysis, and geospatial calculations.

---

## 🚀 Features

* Optimizes fuel stops based on fuel prices and vehicle range
* Uses only one routing API call per request
* Fast geospatial calculations with NumPy and Pandas
* Supports 8,000+ fuel stations
* Route-based station filtering using polyline analysis
* In-memory caching for faster repeated responses
* Swagger/OpenAPI documentation with drf-spectacular

---

## 🛠 Tech Stack

* Django 6.0
* Django REST Framework
* Pandas & NumPy
* OpenRouteService API
* Polyline
* drf-spectacular

---

## 📋 Prerequisites

* Python 3.10+
* OpenRouteService API Key

Get API key from:
[OpenRouteService](https://openrouteservice.org/?utm_source=chatgpt.com)

---

## ⚙️ Setup

### 1. Clone Repository

```bash
git clone <repository_url>
cd fuel_route_optimizer
```

### 2. Create Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

In `config/settings.py`:

```python
ORS_API_KEY = "your_api_key_here"
```

### 5. Add Fuel Dataset

Place these files inside `fuel_data/`:

```bash
fuel-prices.csv
us_cities.csv
```

### 6. Run Server

```bash
python manage.py migrate
python manage.py runserver
```

---

## 🔍 API Endpoints

### Health Check

```http
GET /api/
```

### Optimize Route

```http
POST /api/optimize-route/
```

#### Request Body

```json
{
  "start": "New York, NY",
  "destination": "Chicago, IL"
}
```

#### Sample Response

```json
{
  "route_distance_miles": 790,
  "estimated_fuel_stops": 2,
  "fuel_stations": [
    {
      "city": "Cleveland",
      "state": "OH",
      "fuel_price": 3.21
    }
  ]
}
```

---

## 📘 API Documentation

Swagger UI:

```bash
http://127.0.0.1:8000/api/docs/
```

---

## ⚡ Performance Optimizations

* Vectorized Haversine distance calculations
* Single routing API request
* Route polyline filtering
* Local memory caching
* Preprocessed fuel datasets

---

## 📂 Project Structure

```bash
fuel_route_optimizer/
│
├── api/
├── fuel_data/
├── config/
├── requirements.txt
└── manage.py
```
