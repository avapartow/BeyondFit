<div align="center">

# 💎 BeyondFit

### AI-Powered Fashion Recommendations for Every Body

*Discover clothing that flatters your unique shape*

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub](https://img.shields.io/badge/github-avapartow%2FBeyondFit-blue)](https://github.com/avapartow/BeyondFit)
[![License](https://img.shields.io/badge/license-Proprietary-red.svg)]()

[Live Demo](https://beyondfit-demo.vercel.app) • [Documentation](./docs) • [Report Bug](https://github.com/avapartow/BeyondFit/issues)

---

</div>

## ✨ What is BeyondFit?

**BeyondFit** is a cutting-edge AI-powered fashion platform that revolutionizes online shopping by providing personalized style recommendations based on your unique body type. Unlike traditional fashion apps, BeyondFit uses advanced computer vision to analyze your body proportions and suggest clothing that truly flatters your shape.

### 🌟 Key Highlights

- 🤖 **AI Body Analysis** - MediaPipe-powered body ratio detection
- 👗 **Smart Recommendations** - Personalized outfit suggestions tailored to your shape
- 🛍️ **Seamless Shopping** - Curated affiliate links from top brands
- 🔒 **Privacy First** - Photos deleted immediately after analysis (unless you opt-in)
- 📱 **Cross-Platform** - Beautiful web and mobile experiences

## 🎯 The Problem We Solve

BeyondFit helps users discover clothing that flatters their unique body type through:
- **Body Analysis**: AI-powered body ratio detection from photos
- **Smart Recommendations**: Personalized outfit suggestions based on body type, style preferences, and budget
- **Affiliate Commerce**: Seamless purchasing through curated affiliate links

## 🏗️ Architecture

### Monorepo Structure
```
BeyondFit/
├── backend/          # FastAPI (Python) - Core API & AI
├── web/              # Next.js + Tailwind - Web Application
├── mobile/           # React Native (Expo) - Mobile App
├── shared/           # Shared types, constants, utilities
├── docs/             # Documentation & setup guides
└── scripts/          # Build & deployment scripts
```

### Tech Stack

#### Web App
- **Framework**: Next.js 14+ (React)
- **Styling**: Tailwind CSS
- **State**: React Context + SWR
- **Auth**: Supabase Auth (Email OTP, Google, Apple)

#### Mobile App
- **Framework**: React Native (Expo)
- **Navigation**: Expo Router
- **State**: React Context + React Query
- **Camera**: Expo Camera + Image Picker

#### Backend API
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL (Supabase)
- **Storage**: S3-compatible (photos deleted by default)
- **AI/ML**: MediaPipe for body landmark detection
- **Validation**: Pydantic

#### Infrastructure
- **Database**: Supabase (Postgres + Auth + Storage)
- **Web Hosting**: Vercel
- **API Hosting**: Render / Fly.io
- **CDN**: Cloudflare (optional)

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ and npm/pnpm
- Python 3.11+
- PostgreSQL 14+ (or Supabase account)
- AWS S3 or compatible storage

### Quick Start

1. **Clone and Install**
   ```bash
   git clone <repo-url>
   cd BeyondFit
   npm install
   ```

2. **Setup Backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env  # Configure your environment
   ```

3. **Setup Web**
   ```bash
   cd web
   npm install
   cp .env.local.example .env.local  # Configure your environment
   ```

4. **Setup Mobile**
   ```bash
   cd mobile
   npm install
   ```

See detailed setup in [docs/SETUP.md](docs/SETUP.md)

## 📋 Development Roadmap

### ✅ Milestone 1: Web + Backend + Admin
- [x] Backend API with FastAPI
- [x] Body analysis module (MediaPipe)
- [x] Product catalog & CSV ingestion
- [x] Admin dashboard
- [x] Web app with onboarding
- [x] Auth flow (Email OTP)

### 🔄 Milestone 2: Mobile + Body Scan
- [ ] React Native app setup
- [ ] Camera-based body scan
- [ ] Photo upload flow
- [ ] Results display
- [ ] Product recommendations

### 📊 Milestone 3: Analytics & Tracking
- [ ] Affiliate link tracking
- [ ] Click/conversion analytics
- [ ] Admin analytics dashboard
- [ ] Performance optimization

## 🔐 Privacy & Security

- **Photos**: Processed and deleted immediately (unless user opts in)
- **Data Storage**: Only derived body ratios stored by default
- **EXIF Scrubbing**: Metadata removed from all images
- **Rate Limiting**: API abuse protection
- **Consent**: Clear privacy screens and data deletion options

## 📱 Core Features

### User Features
- Style preference quiz
- Body scan (camera or upload)
- Body type analysis with explanations
- Personalized outfit recommendations
- Product filtering (occasion, price, brand)
- Favorites & lookbooks
- Privacy controls

### Admin Features
- Brand management
- Product feed CSV upload
- Affiliate link management
- Analytics dashboard
- User metrics

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Web tests
cd web
npm test

# Mobile tests
cd mobile
npm test
```

## 📦 Deployment

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed deployment instructions.

## 📄 License

Proprietary - All rights reserved

## 📸 Screenshots

<div align="center">

### 🌐 Live Demo
Check out our [interactive demo](./demo/index.html) with the animated diamond logo!

*Open `demo/index.html` in your browser to see the homepage*

</div>

## 📊 Project Statistics

- **Total Files**: 47
- **Lines of Code**: 6,455+
- **Languages**: Python, TypeScript, JavaScript, CSS
- **Components**: 8 API routers, 4 web pages, complete admin dashboard
- **Documentation**: Architecture diagrams, setup guides, API docs

## 🛠️ Built With

### Frontend
![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js)
![React](https://img.shields.io/badge/React-18-blue?logo=react)
![TailwindCSS](https://img.shields.io/badge/Tailwind-3-38bdf8?logo=tailwind-css)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?logo=typescript)

### Backend
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-336791?logo=postgresql)
![MediaPipe](https://img.shields.io/badge/MediaPipe-AI-orange)

## 🤝 Contributing

Internal project - see team guidelines

## 📄 License

Proprietary - All rights reserved

## 📬 Contact

**Project Link**: [https://github.com/avapartow/BeyondFit](https://github.com/avapartow/BeyondFit)

---

<div align="center">

Built with 💎 by the BeyondFit team

*Empowering everyone to look and feel their best*

</div>
