# BeyondFit - System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACES                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐         ┌──────────────┐                    │
│  │   Web App    │         │  Mobile App  │                    │
│  │  (Next.js)   │         │ (React Native)│                   │
│  │              │         │   (Milestone 2)│                  │
│  └──────┬───────┘         └──────┬────────┘                   │
│         │                         │                            │
│         └─────────┬───────────────┘                            │
│                   │                                            │
└───────────────────┼────────────────────────────────────────────┘
                    │
                    │ HTTPS / REST API
                    │
┌───────────────────▼────────────────────────────────────────────┐
│                       BACKEND API                              │
│                      (FastAPI)                                 │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │                  API Routers                           │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │ /auth    │ /users   │ /body    │ /recommendations    │  │
│  │ /products│ /brands  │ /admin   │ /analytics          │  │
│  └────────────────────────────────────────────────────────┘  │
│                          │                                    │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              Business Logic Services                    │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │                                                        │  │
│  │  ┌─────────────────┐    ┌────────────────────────┐  │  │
│  │  │  Body Analyzer  │    │ Recommendation Engine  │  │  │
│  │  │   (MediaPipe)   │    │   (Rule-Based V1)      │  │  │
│  │  │                 │    │                        │  │  │
│  │  │ • Pose Detection│    │ • Body Type Scoring    │  │  │
│  │  │ • Ratio Calc    │    │ • Style Matching       │  │  │
│  │  │ • Classification│    │ • Budget Filtering     │  │  │
│  │  └─────────────────┘    └────────────────────────┘  │  │
│  │                                                      │  │
│  │  ┌──────────────────┐   ┌────────────────────────┐ │  │
│  │  │ Storage Service  │   │  Auth Service          │ │  │
│  │  │                  │   │                        │ │  │
│  │  │ • S3 Upload      │   │ • OTP Generation       │ │  │
│  │  │ • EXIF Stripping │   │ • JWT Tokens           │ │  │
│  │  │ • Auto-Delete    │   │ • Email Sending        │ │  │
│  │  └──────────────────┘   └────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                            │
└────────────────────────────────────────────────────────────┘
                    │                    │
       ────────────┬┴──────────    ─────┴──────────
       │           │           │    │              │
┌──────▼──────┐ ┌──▼────────┐  │  ┌─▼────────────┐│
│  PostgreSQL │ │ S3 Storage│  │  │ Email (SMTP) ││
│  (Supabase) │ │  (Photos) │  │  │  (OTP Codes) ││
│             │ │           │  │  │              ││
│ • Users     │ │ • Photos  │  │  └──────────────┘│
│ • Products  │ │ (temp)    │  │                  │
│ • Analytics │ └───────────┘  │                  │
└─────────────┘                │                  │
                               │                  │
                       ┌───────▼──────────────────▼───┐
                       │   External Services          │
                       ├──────────────────────────────┤
                       │ • Affiliate Networks         │
                       │ • Payment Processors         │
                       │ • Conversion Tracking        │
                       └──────────────────────────────┘
```

## Data Flow

### 1. User Authentication Flow
```
User → Web/Mobile → [POST /auth/request-otp]
                  → Email Service → User receives OTP
User → Enters OTP → [POST /auth/verify-otp]
                  → JWT Token → Stored in client
```

### 2. Body Analysis Flow
```
User → Upload Photos → [POST /body/analyze]
                     → Storage Service → S3 (temp)
                     → Body Analyzer (MediaPipe)
                        ├─ Extract Landmarks
                        ├─ Calculate Ratios
                        ├─ Classify Body Type
                        └─ Generate Recommendations
                     → Save to Database
                     → Delete Photos (if user didn't opt-in)
                     → Return Results
```

### 3. Product Recommendation Flow
```
User → [GET /recommendations/?filters]
    → Recommendation Engine
       ├─ Fetch User's Body Type
       ├─ Get User Preferences
       ├─ Query Products (with filters)
       ├─ Score Each Product (0-100)
       │  ├─ Body type match: +30
       │  ├─ Silhouette match: +15
       │  ├─ Style preference: +5
       │  └─ Budget/color: +8
       ├─ Sort by Score
       └─ Return Top N Products
    → Display to User
```

### 4. Affiliate Click Tracking
```
User → Click Product → [GET /products/{id}/affiliate-link]
                     → Create Click Record
                        ├─ user_id
                        ├─ product_id
                        ├─ timestamp
                        └─ metadata
                     → Return Affiliate URL
                     → Redirect to Brand Site
                     → (Later) Webhook for Conversion
```

## Technology Stack Summary

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS (Custom Theme)
- **State**: React Context + SWR
- **Icons**: Heroicons

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **ORM**: SQLAlchemy 2.0
- **Validation**: Pydantic v2
- **AI/ML**: MediaPipe + OpenCV
- **Auth**: Python-JOSE (JWT) + Passlib (Bcrypt)
- **Storage**: Boto3 (S3)

### Infrastructure
- **Database**: PostgreSQL 14+ (Supabase recommended)
- **Storage**: S3-compatible (AWS, MinIO, etc.)
- **Email**: SMTP (Gmail, SendGrid, etc.)
- **Hosting** (Recommended):
  - Web: Vercel
  - API: Render / Fly.io
  - DB: Supabase

## Security Layers

```
┌──────────────────────────────────────┐
│  Rate Limiting (60/min, 1000/hour)   │
├──────────────────────────────────────┤
│  CORS (Whitelisted origins)          │
├──────────────────────────────────────┤
│  JWT Authentication (30min expiry)   │
├──────────────────────────────────────┤
│  Input Validation (Pydantic)         │
├──────────────────────────────────────┤
│  SQL Injection Protection (ORM)      │
├──────────────────────────────────────┤
│  HTTPS Only (Production)             │
└──────────────────────────────────────┘
```

## Scalability Considerations

### Current (MVP)
- Handles 1K-10K users
- Single server deployment
- In-memory OTP storage
- Synchronous photo processing

### Future Optimizations
- **Horizontal Scaling**: Load balancer + multiple API instances
- **Caching**: Redis for OTP, sessions, product catalog
- **Background Jobs**: Celery for async photo processing
- **CDN**: Cloudflare for static assets
- **Database**: Read replicas for analytics
- **ML Model**: Separate microservice for body analysis
- **Message Queue**: RabbitMQ for conversion tracking

## Deployment Architecture (Production)

```
                    ┌──────────────┐
                    │   Cloudflare │
                    │   CDN + WAF  │
                    └──────┬───────┘
                           │
            ┌──────────────┴──────────────┐
            │                             │
    ┌───────▼────────┐           ┌────────▼──────┐
    │  Vercel (Web)  │           │ Render (API)  │
    │   Next.js App  │           │  FastAPI App  │
    └────────────────┘           └───────┬───────┘
                                         │
                         ┌───────────────┼───────────────┐
                         │               │               │
                  ┌──────▼─────┐  ┌──────▼──────┐ ┌─────▼─────┐
                  │  Supabase  │  │   AWS S3    │ │   SMTP    │
                  │ PostgreSQL │  │   Storage   │ │  Service  │
                  └────────────┘  └─────────────┘ └───────────┘
```

---

**Built for Scale • Privacy First • Production Ready** 🚀
