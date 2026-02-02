# Chemical Equipment Parameter Visualizer  
**Hybrid Web + Desktop Application**

## Project Overview

The **Chemical Equipment Parameter Visualizer** is a hybrid application that runs as both a **Web Application (React)** and a **Desktop Application (PyQt5)**, powered by a **shared Django REST backend**.

The system allows users to upload CSV files containing chemical equipment data, performs analytics using Pandas, and visualizes results through tables, charts, history tracking, and downloadable PDF reports.

---

## Tech Stack

| Layer | Technology |
|-----|-----------|
| Backend | Python, Django, Django REST Framework |
| Data Processing | Pandas |
| Database | SQLite |
| Web Frontend | React.js, Chart.js |
| Desktop Frontend | PyQt5, Matplotlib |
| Authentication | DRF Token Authentication |
| Reporting | ReportLab + Matplotlib |

---

## Key Features

### CSV Upload
- Upload CSV files from **both Web and Desktop apps**
- Backend validates file format and required columns

### Data Analytics
- Total equipment count
- Average Flowrate, Pressure, Temperature
- Equipment type distribution

### Visualizations
- **Web**: Charts rendered using Chart.js  
- **Desktop**: Charts rendered using Matplotlib  

### History Management
- Stores **last 5 uploaded datasets**
- History shared across Web & Desktop clients
- Clicking a past dataset reloads its analytics

### PDF Report Generation
- Downloadable PDF report per dataset
- Includes:
  - Summary statistics
  - Equipment type distribution chart
- Generated fully on the backend

### Authentication
- API protected using **Django REST Framework Token Authentication**
- Same token used by both clients (provided via environment variables)

---

## Project Structure
```
.
├── backend/
│ ├── api/
│ ├── backend/
│ ├── manage.py
│ └── requirements.txt
│
├── chemical-visualizer-web/
│ ├── public/
│ ├── src/
│ ├── package.json
│ └── package-lock.json
│
├── desktop-app/
│ ├── main.py
│ ├── api_client.py
│ └── charts.py
│
├── .gitignore
└── README.md
```

---

## Authentication Setup

The backend APIs are protected using **Token Authentication**.

For demo purposes, a **pre-generated token** is used by both the Web and Desktop clients.

### Web (React)
Create a `.env` file in `chemical-visualizer-web/`:

```env
REACT_APP_BASE_URL=http://127.0.0.1:8000/api/
REACT_APP_API_TOKEN=your_token_here
```

#### Desktop (PyQt)
Set environment variables before running the app.
Windows (cmd):
```
set API_BASE=http://127.0.0.1:8000/api/
set API_TOKEN=your_token_here
```

### How to run the project:
1. Backend (Django)
```
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
2. Web application
```
cd chemical-visualizer-web
npm install
npm start
```
Access at:
```
http://localhost:3000
```
3. Destop application
```
cd desktop-app
python main.py
```

### Sample CSV format:
```
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-1,Pump,120,5.2,110
Valve-1,Valve,60,4.1,105
```

---

### Conclusion
This project highlights the design of a scalable, secure data-driven system supporting both web and desktop clients from a single backend.
