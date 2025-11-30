# NexusHub

**Production-Ready Modular Business Management Platform**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Next.js](https://img.shields.io/badge/Next.js-15-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)

A next-generation, highly modular business platform combining CRM, Project Management, Team Collaboration, and AI capabilities with production-grade architecture.

## 🎯 Features

### Core Capabilities
- ✅ **CRM** - Contacts, Companies, Deals with custom fields
- ✅ **Project Management** - Projects, Tasks with dependencies & time tracking
- ✅ **Team Collaboration** - Real-time messaging, notifications
- ✅ **AI Integration** - Pluggable AI providers (Ollama/OpenAI/Claude)
- ✅ **Multi-Tenant** - Native multi-tenant support with row-level security
- ✅ **RBAC** - Role-based access control with granular permissions

### Technical Highlights
- 🏗️ **Domain-Driven Design** - Clean architecture with bounded contexts
- 🔒 **Enterprise Security** - Argon2 hashing, JWT auth, CSRF protection
- 🚀 **Modern Stack** - FastAPI + Next.js 15 + PostgreSQL + Redis
- 🐳 **Docker Ready** - One-command setup with Docker Compose
- ✅ **Type Safe** - Strict TypeScript + Pydantic validation
- 📊 **Production Ready** - Logging, monitoring, CI/CD pipelines

## 🚀 Quick Start

### Prerequisites
- **Docker** & **Docker Compose** (recommended)
- **OR** Python 3.12+, Node.js 18+, PostgreSQL 16+, Redis 7+

### Docker Setup (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd nexus-hub

# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local

# Start all services
docker-compose up -d

# Run migrations
docker-compose exec backend alembic upgrade head

# Create admin user
docker-compose exec backend python scripts/create_admin.py
```

**Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/v1/docs
- Adminer (DB UI): http://localhost:8080

### Manual Setup

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Run migrations
alembic upgrade head

# Create admin user
python scripts/create_admin.py

# Start server
uvicorn main:app --reload --port 8000
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Setup environment
cp .env.example .env.local

# Start development server
npm run dev
```

## 📁 Project Structure

```
nexus-hub/
├── backend/                # FastAPI Backend
│   ├── core/              # Shared kernel
│   │   ├── config/        # Settings & configuration
│   │   ├── database/      # Database connection & repository
│   │   ├── security/      # Auth, RBAC, encryption
│   │   └── exceptions/    # Custom exceptions
│   ├── domains/           # Business domains (DDD)
│   │   ├── identity/      # User, auth, tenants
│   │   ├── crm/          # Contacts, companies, deals
│   │   ├── projects/     # Projects, tasks
│   │   ├── collaboration/ # Teams, messages
│   │   └── ai/           # AI providers, context
│   ├── alembic/          # Database migrations
│   └── tests/            # Test suite
├── frontend/              # Next.js Frontend
│   ├── src/
│   │   ├── app/          # Next.js App Router
│   │   ├── features/     # Feature modules
│   │   ├── components/   # Shared UI components
│   │   ├── lib/          # Utilities & API client
│   │   └── types/        # TypeScript types
├── docker/               # Docker configurations
├── docs/                 # Documentation
└── docker-compose.yml    # Local development setup
```

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI 0.115+
- **Language**: Python 3.12+
- **Database**: PostgreSQL 16+ (with asyncpg)
- **ORM**: SQLAlchemy 2.0+ (async)
- **Validation**: Pydantic 2.10+
- **Auth**: JWT with Argon2 hashing
- **Cache**: Redis 7+
- **Migrations**: Alembic

### Frontend
- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript 5.7+ (strict mode)
- **UI**: shadcn/ui + Radix UI
- **Styling**: Tailwind CSS 4+
- **State**: Zustand + React Query
- **Validation**: Zod
- **Forms**: React Hook Form

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Reverse Proxy**: Nginx (production)
- **CI/CD**: GitHub Actions
- **Monitoring**: Structured logging + Prometheus (planned)

## 🔒 Security Features

- **Argon2** password hashing (more secure than bcrypt)
- **JWT** authentication with refresh token rotation
- **RBAC** with granular permissions
- **CSRF** protection
- **Rate limiting** (Redis-backed)
- **Security headers** (HSTS, CSP, etc.)
- **Input validation** (Pydantic + Zod)
- **Multi-tenant** row-level security
- **Audit logging** for sensitive operations

## 📖 API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ --cov=backend --cov-report=html

# Frontend tests
cd frontend
npm run test
npm run test:e2e
```

## 🚢 Deployment

### Production Build

```bash
# Build Docker images
docker-compose -f docker-compose.prod.yml build

# Run in production
docker-compose -f docker-compose.prod.yml up -d
```

See [deployment guide](docs/deployment.md) for detailed instructions.

## 📝 Environment Variables

### Backend (.env)
```env
SECRET_KEY=<64-char-random-string>
CSRF_SECRET=<64-char-random-string>
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/db
REDIS_URL=redis://localhost:6379/0
ENVIRONMENT=production
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Inspired by DevOS with enhanced modularity and production-ready architecture.

## 📧 Support

For support, email [support@nexushub.com](mailto:support@nexushub.com) or open an issue.

---

**Made with ❤️ using Domain-Driven Design principles**
