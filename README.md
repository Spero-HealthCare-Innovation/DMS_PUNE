Project structure

DMS_app/
├── DMS_client/                            # React frontend
│   ├── package.json
│   └── src/
│
├── DMS_goa/                     # Django + DRF backend
│   ├── manage.py
│   ├── DMS_goa/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   └── urls.py
│   │
│   ├── Django app/
│   │   ├── models.py 
│   │   ├── views.py 
│   │   └── serializers.py 
│   │
│   ├── DMS_fastapi_service/           # Embedded FastAPI + web socket Integration
│   │   ├── __init__.py
│   │   ├── main.py                # Entry point: `uvicorn main:app`
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   └── sample.py         # Sample route
│   │   ├── models/               # Optional Pydantic models
│   │   │   └── item.py
│   │   └── dependencies/         # Optional
│   │       └── auth.py
│   │
│   └── requirements.txt
│
├── nginx/
│   └── default.conf
│
├── docker-compose.yml
└── README.md
