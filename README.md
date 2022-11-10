# dsa3101-2210-14-lta
A **DSA3101** Group Project 

![visitors](https://visitor-badge.laobi.icu/badge?page_id=hewliyang.dsa3101-2210-14-lta)

## Installation

```
.
└── 📁 dsa3101-2210-14-lta/
    ├── 📁 backend/
    │   └── 📄.env
    ├── 📁 frontend/
    └── 📄 docker-compose.yml
```

**Important**: You will need to create an `.env` file under the **backend** folder in the following format:
```
PROJECT_API_KEY = "<YOUR_LTA_API_KEY>"
DB_KEY "<YOUR_DETA_ACCESS_TOKEN>"
```
Generate a new **Deta** token for free at  

[![deta](https://www.deta.sh/dist/images/deta_logo.svg)](https://www.deta.sh/)

(_or contact us for our key with access to pre-populated database_)

Run with **Docker** 🐳
```
docker compose up -d
```
