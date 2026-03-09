# 🏺 El Baúl Viejo — Backend

API REST de **El Baúl Viejo**, una tienda de antigüedades. Gestiona la autenticación de administradores, el catálogo de piezas y las categorías. Las fotos se almacenan en **Supabase Storage** y los datos en **PostgreSQL** (Supabase).

> 🔗 **Repositorio del frontend:** [El-Baul-Viejo-Frontend](https://github.com/UrielCandelasMeza/El-Baul-Viejo-Frontend)

---

## ✨ Funcionalidades

- Registro e inicio de sesión con contraseña hasheada (bcrypt)
- Autenticación mediante JWT almacenado en cookies **httpOnly** (renovación automática con refresh token)
- CRUD completo de piezas (con subida de fotos a Supabase Storage por hash SHA-256)
- CRUD de categorías
- Endpoints públicos (GET de piezas y categorías) y protegidos (crear, editar, eliminar)

---

## 🛠 Tecnologías

| Tecnología | Uso |
|---|---|
| Python 3.12 | Lenguaje |
| Flask | Framework web |
| Flask-SQLAlchemy | ORM |
| Flask-Migrate | Migraciones de BD |
| Flask-JWT-Extended | Autenticación JWT (httpOnly cookies) |
| Flask-Bcrypt | Hash de contraseñas |
| Flask-CORS | Cross-Origin Resource Sharing |
| Supabase | Storage de fotos + PostgreSQL |
| Gunicorn | Servidor de producción |

---

## 📡 Endpoints

### Autenticación — `/api/auth`

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `POST` | `/register` | ❌ | Registrar usuario |
| `POST` | `/login` | ❌ | Iniciar sesión (devuelve cookies JWT) |
| `GET` | `/verify` | ✅ | Verificar token y obtener usuario |
| `POST` | `/logout` | ❌ | Cerrar sesión (limpia cookies) |

### Piezas — `/api/piece`

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `POST` | `/create` | ✅ | Crear pieza (`multipart/form-data`) |
| `GET` | `/get` | ❌ | Todas las piezas |
| `GET` | `/get/available` | ❌ | Solo piezas disponibles |
| `GET` | `/get/:id` | ❌ | Pieza por ID |
| `PUT` | `/update/:id` | ✅ | Actualizar pieza (`multipart/form-data`) |
| `DELETE` | `/delete/:id` | ✅ | Eliminar pieza y sus fotos del bucket |

#### Campos FormData para crear/actualizar

| Campo | Tipo | Descripción |
|---|---|---|
| `name` | string | Nombre |
| `price` | string | Precio en MXN |
| `description` | string | Descripción |
| `status` | string | `available` o `sold` |
| `category_ids` | string[] | IDs de categorías |
| `photos` | File[] | Imágenes nuevas (máx. 5 en total) |
| `existing_photos` | string[] | URLs a conservar (solo update) |

### Categorías — `/api/category`

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/get` | ❌ | Todas las categorías |
| `POST` | `/create` | ✅ | Crear categoría |
| `DELETE` | `/delete/:id` | ✅ | Eliminar categoría |

> **Auth ✅** = requiere cookie `access_token_cookie` válida (httpOnly).

---

## 🔐 Variables de entorno

Crea un archivo `.env` en la raíz del proyecto (`api/`):

```env
FLASK_APP=app.py
HOST=localhost
PORT=5000
FLASK_ENV=development

JWT_SECRET_KEY=tu_clave_secreta_minimo_32_caracteres

DATABASE_URL=postgresql+psycopg2://usuario:password@host:5432/db
DATABASE_POOL_URL=postgresql+psycopg2://usuario:password@host:6543/db

SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co
SUPABASE_KEY=sb_secret_xxxxxxxxxxxx
```

| Variable | Descripción |
|---|---|
| `JWT_SECRET_KEY` | Clave secreta para firmar los JWT (mín. 32 caracteres) |
| `DATABASE_URL` | Conexión directa a PostgreSQL (para migraciones) |
| `DATABASE_POOL_URL` | Connection pooler de Supabase (para producción) |
| `SUPABASE_URL` | URL del proyecto Supabase |
| `SUPABASE_KEY` | API key de Supabase (`anon` o `service_role`) |

---

## 💻 Instalación y desarrollo

```bash
# 1. Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Crear variables de entorno
cp .env.example .env          # editar con tus credenciales

# 4. Aplicar migraciones
flask db upgrade

# 5. Iniciar servidor
python app.py
```

El backend se ejecuta en `http://localhost:5000`.

---

## 🐳 Docker

```bash
# Construir imagen
docker build -t baul-api .

# Correr contenedor pasando el .env
docker run --env-file .env -p 5000:5000 baul-api
```

O desde la raíz del monorepo con Docker Compose:

```bash
docker compose up --build
```

---

## 🚀 Despliegue en Render

Configurar como **Web Service** en Render:

| Campo | Valor |
|---|---|
| Root Directory | `api` |
| Runtime | Docker |
| Port | `5000` |

Agregar las variables de entorno en el dashboard de Render (puedes usar el botón **"Add from .env"** para cargar el archivo completo de una vez).

> **Nota:** En producción, `FLASK_ENV=production` activa `JWT_COOKIE_SECURE=True` (requiere HTTPS) y usa `DATABASE_POOL_URL` con connection pooling optimizado.
