# BeyondFit - Setup Guide

## Overview

This guide will walk you through setting up the complete BeyondFit platform locally.

## Prerequisites

### Required Software
- **Python 3.11+** with pip
- **Node.js 18+** with npm
- **PostgreSQL 14+** (or Supabase account)
- **Git**

### Optional
- AWS S3 account (or S3-compatible storage)
- SMTP email service (Gmail, SendGrid, etc.)

---

## Part 1: Backend Setup (FastAPI)

### 1. Navigate to backend directory
```powershell
cd backend
```

### 2. Create Python virtual environment
```powershell
python -m venv venv
.\venv\Scripts\activate  # On Windows
```

### 3. Install dependencies
```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables
```powershell
copy .env.example .env
```

Edit `.env` with your settings:

**Required:**
- `DATABASE_URL`: Your PostgreSQL connection string
- `SECRET_KEY`: Generate with `python -c "import secrets; print(secrets.token_hex(32))"`

**Optional (for full functionality):**
- `SUPABASE_URL` and `SUPABASE_KEY`: For Supabase integration
- `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`: For S3 storage
- `SMTP_*`: For email OTP delivery

**Example configuration:**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/beyondfit
SECRET_KEY=your-secret-key-here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

### 5. Set up database

If using local PostgreSQL:
```powershell
createdb beyondfit
```

The backend will auto-create tables on first run using SQLAlchemy.

### 6. Create admin user (optional)

Open Python shell:
```powershell
python
```

Run:
```python
from app.database import SessionLocal
from app.models import AdminUser
from app.auth import get_password_hash

db = SessionLocal()
admin = AdminUser(
    email="admin@beyondfit.com",
    hashed_password=get_password_hash("your-password")
)
db.add(admin)
db.commit()
print("Admin created!")
```

### 7. Run the API server
```powershell
python -m uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### 8. Test the API
Open browser: `http://localhost:8000/docs` for interactive API documentation

---

## Part 2: Web App Setup (Next.js)

### 1. Navigate to web directory
```powershell
cd ../web
```

### 2. Install dependencies
```powershell
npm install
```

You may also need to install the Tailwind forms plugin:
```powershell
npm install @tailwindcss/forms
```

### 3. Configure environment
```powershell
copy .env.local.example .env.local
```

Edit `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/v1
NEXT_PUBLIC_APP_NAME=BeyondFit
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### 4. Run development server
```powershell
npm run dev
```

The web app will be available at `http://localhost:3000`

---

## Part 3: Sample Data Setup

### 1. Create sample brand

Using the admin login or direct database:

**API request (using curl or Postman):**
```bash
POST http://localhost:8000/v1/admin/brands
Authorization: Bearer <your-admin-token>
Content-Type: application/json

{
  "name": "Sample Fashion Co",
  "website_url": "https://example.com",
  "affiliate_network": "ShareASale",
  "affiliate_id": "123456",
  "commission_rate": 10.0
}
```

### 2. Upload sample products (CSV)

Create a file `sample_products.csv`:

```csv
product_id,title,description,category,price,available_sizes,fit_type,silhouette,neckline,colors,image_url,affiliate_url
P001,Flowy A-Line Dress,Beautiful summer dress,dresses,89.99,"XS,S,M,L,XL",relaxed,A-line,V-neck,"blue,pink",https://via.placeholder.com/400,https://example.com/p001
P002,High-Waist Jeans,Classic denim,bottoms,79.99,"26,28,30,32",fitted,straight,,,denim,https://via.placeholder.com/400,https://example.com/p002
P003,Wrap Top,Flattering wrap style,tops,49.99,"S,M,L",fitted,wrap,V-neck,"black,white,red",https://via.placeholder.com/400,https://example.com/p003
```

Upload via admin dashboard or API:
```bash
POST http://localhost:8000/v1/admin/products/upload-csv?brand_id=1
Authorization: Bearer <admin-token>
Content-Type: multipart/form-data
file: sample_products.csv
```

---

## Part 4: Testing the Complete Flow

### 1. Web App - Sign Up
1. Go to `http://localhost:3000`
2. Click "Get Started"
3. Enter your email
4. Check console logs for OTP code (if SMTP not configured)
5. Enter OTP and sign in

### 2. Complete Onboarding
1. Set your style preferences
2. Enter size information
3. Set budget range

### 3. Body Scan
1. Navigate to /scan
2. Upload or take photos (front + optional side)
3. Wait for AI analysis
4. View your body type results

### 4. Browse Recommendations
1. See personalized product recommendations
2. Filter by category, price, occasion
3. Click products to view details
4. Use affiliate links to shop

---

## Troubleshooting

### Backend Issues

**Database connection error:**
- Check DATABASE_URL is correct
- Ensure PostgreSQL is running
- For Supabase, enable connection pooling

**MediaPipe installation error:**
```powershell
pip install mediapipe --upgrade
```

**Module import errors:**
```powershell
pip install -r requirements.txt --force-reinstall
```

### Web App Issues

**Port already in use:**
```powershell
# Kill process on port 3000
npx kill-port 3000
```

**Module not found:**
```powershell
rm -rf node_modules package-lock.json
npm install
```

**Tailwind styles not applying:**
```powershell
npm run dev # Restart dev server
```

---

## Production Deployment

### Backend (Render / Fly.io)

1. Create `Procfile`:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

2. Set environment variables in hosting dashboard

3. Deploy via Git or CLI

### Web App (Vercel)

1. Connect GitHub repository
2. Set environment variables:
   - `NEXT_PUBLIC_API_URL`: Your production API URL
3. Deploy automatically on push

### Database (Supabase)

1. Create project at supabase.com
2. Get connection string from settings
3. Update DATABASE_URL in backend

---

## Next Steps

1. **Milestone 2**: Set up React Native mobile app
2. **Milestone 3**: Implement conversion tracking
3. **Customize**: Add your brand partnerships
4. **Scale**: Add Redis for OTP storage
5. **Monitor**: Set up error tracking (Sentry)

---

## Support

For issues or questions:
- Check API docs: `http://localhost:8000/docs`
- Review logs in console
- Check database connections

Happy building! 🚀
