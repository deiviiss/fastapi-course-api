# FastAPI Course API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.139.2-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![SQLModel](https://img.shields.io/badge/SQLModel-0.0.39-red.svg?style=flat)](https://sqlmodel.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063.svg?style=flat&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![Pytest](https://img.shields.io/badge/Tests-Pytest-0A9EDC.svg?style=flat&logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

API RESTful modular construida con **FastAPI** y **SQLModel**, desarrollada como proyecto integral para la gestión de clientes, planes de suscripción, transacciones financieras y facturación.

---

## 🚀 Características Principales

- **Arquitectura Modular por Capas**: Separación estricta entre modelos relacionales, acceso a datos, dependencias y enrutadores.
- **Relaciones Relacionales (SQLModel)**:
  - `1 a N`: Clientes y Transacciones (`Customer` -> `Transaction`).
  - `N a M`: Clientes y Planes (`Customer` <-> `Plan`) vinculados mediante tabla intermedia `CustomerPlan` con estados (`ACTIVE`, `INACTIVE`).
- **Validación Robusta (Pydantic v2)**: Validadores de campo (`@field_validator`) para unicidad y formato de correos.
- **Seguridad**: Autenticación HTTP Basic integrada con esquemas de seguridad de FastAPI.
- **Middlewares Personalizados**: Middleware HTTP para auditoría y medición de tiempos de procesamiento (`X-Process-Time`).
- **Paginación**: Endpoint de transacciones con soporte de paginación mediante `offset` y `limit`.
- **Testing Automatizado**: Suite de pruebas con **Pytest** y `TestClient`, utilizando base de datos en memoria (`StaticPool`) y sobreescritura de dependencias.
- **Data Seeding**: Script de inicialización de datos para desarrollo con perfiles y transacciones realistas.
- **Documentación Interactiva**: Documentación OpenAPI generada automáticamente (Swagger UI y ReDoc).

---

## 📁 Estructura del Proyecto

```text
fastapi-course-api/
├── app/
│   ├── routers/             # Endpoints modulares de la API
│   │   ├── customers.py     # CRUD de clientes y suscripción a planes
│   │   ├── invoices.py      # Generación y cálculo de facturas
│   │   ├── plans.py         # Gestión de planes
│   │   └── transactions.py  # Registro y consulta paginada de transacciones
│   ├── tests/               # Pruebas automatizadas con Pytest
│   │   └── tests_customers.py
│   ├── db.py                # Conexión SQLite, Engine y SessionDep
│   ├── main.py              # Aplicación FastAPI, middlewares y rutas
│   └── models.py            # Modelos SQLModel y esquemas Pydantic
├── scripts/
│   └── seed.py              # Script para poblar la base de datos
├── conftest.py              # Fixtures globales para pruebas unitarias
├── requirements.txt         # Especificación de dependencias del entorno
├── .gitignore               # Exclusiones de Git
└── README.md                # Documentación del proyecto
```

---

## 🛠️ Requisitos Previos

- **Python 3.10** o superior
- **Git**

---

## 📦 Instalación y Configuración

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/deiviiss/fastapi-course-api.git
   cd fastapi-course-api
   ```

2. **Crear y activar el entorno virtual**:
   - En Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - En Windows (Git Bash):
     ```bash
     python -m venv .venv
     source .venv/Scripts/activate
     ```
   - En macOS / Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🖥️ Ejecución de la Aplicación

Para iniciar el servidor de desarrollo con recarga en caliente (*hot-reload*):

```bash
fastapi dev app/main.py
```

O utilizando `uvicorn` directamente:

```bash
uvicorn app.main:app --reload
```

El servidor estará disponible en: **`http://127.0.0.1:8000`**

---

## 📖 Documentación Interactiva

FastAPI genera automáticamente documentación interactiva basada en OpenAPI:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🌱 Poblado de Base de Datos (Seed)

Para generar datos de prueba realistas (clientes, planes, suscripciones y transacciones):

```bash
python scripts/seed.py
```

---

## 🧪 Ejecución de Pruebas

Para ejecutar la suite de pruebas unitarias automatizadas con Pytest:

```bash
pytest app/tests/tests_customers.py -v
```

O ejecutar toda la suite del proyecto:

```bash
pytest -v
```

---

## 📌 Resumen de Endpoints

### 🔐 Autenticación & Raíz
| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/` | Endpoint raíz protegido con **HTTP Basic Auth** |
| `GET` | `/time/{iso_code}` | Consulta de zona horaria por código de país |

### 👥 Clientes (`/customers`)
| Método | Endpoint | Descripción |
|---|---|---|
| `POST` | `/customers` | Registrar un nuevo cliente |
| `GET` | `/customers` | Listar todos los clientes registrados |
| `GET` | `/customers/{id}` | Obtener el detalle de un cliente |
| `PATCH` | `/customers/{id}` | Actualizar datos parciales de un cliente |
| `DELETE` | `/customers/{id}` | Eliminar un cliente por ID |
| `POST` | `/customers/{id}/plan/{plan_id}` | Suscribir un cliente a un plan |
| `DELETE` | `/customers/{id}/plan/{plan_id}` | Cancelar la suscripción de un cliente |

### 📦 Planes (`/plans`)
| Método | Endpoint | Descripción |
|---|---|---|
| `POST` | `/plans` | Crear un nuevo plan de suscripción |
| `GET` | `/plans` | Listar todos los planes disponibles |

### 💳 Transacciones (`/transactions`)
| Método | Endpoint | Descripción |
|---|---|---|
| `POST` | `/transactions` | Registrar una transacción |
| `GET` | `/transactions?skip=0&limit=10` | Listar transacciones con paginación |

### 🧾 Facturación (`/invoices`)
| Método | Endpoint | Descripción |
|---|---|---|
| `POST` | `/invoices` | Calcular y generar el total de una factura |

---

## 📄 Licencia

Este proyecto se distribuye bajo los términos de la licencia MIT.
