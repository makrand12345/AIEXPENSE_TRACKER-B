# AI Expense Tracker - Backend Deployment Guide

## Environment Variables Required

For the backend API to work on Vercel, you must set these environment variables in your Vercel project settings:

### Required Variables:
- **MONGO_URI** - MongoDB connection string (Atlas recommended)
  - Format: `mongodb+srv://username:password@cluster.mongodb.net/ai_expense_tracker?retryWrites=true&w=majority`
  - Get from: [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)

- **SECRET_KEY** - JWT secret for token signing
  - Generate: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
  - Keep this secret and change it in production

## Setting Environment Variables on Vercel

1. Go to your Vercel project dashboard
2. Click "Settings" → "Environment Variables"
3. Add:
   - Key: `MONGO_URI`, Value: `<your-mongodb-connection-string>`
   - Key: `SECRET_KEY`, Value: `<your-generated-secret>`
4. Redeploy the project (manually or via git push)

## API Endpoints

- **GET /** - Root endpoint, returns `{"message": "API running"}`
- **GET /health** - Health check (no auth required)
- **POST /auth/signup** - Create new user account
- **POST /auth/login** - Login and get JWT token
- **GET /profile/me** - Get user profile (requires auth)
- **GET /expenses/** - List user expenses (requires auth)
- **GET /analytics/overview** - Get spending analytics (requires auth)
- **GET /finance/me** - Get finance profile (requires auth)

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create `.env` file in `backend/` directory:
   ```
   MONGO_URI=your_mongodb_uri
   SECRET_KEY=your_secret_key
   ```

3. Run development server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Troubleshooting

### 500 Internal Server Error
- Check Vercel deployment logs for specific error
- Verify all environment variables are set correctly
- Check MongoDB Atlas is accessible and IP whitelist includes Vercel IPs

### Connection Refused
- Verify MONGO_URI is correct
- Whitelist Vercel IP ranges in MongoDB Atlas Network Access
- Check MongoDB cluster status

### Invalid Token / 401 Unauthorized
- Ensure SECRET_KEY is set correctly
- Token format should be: `Authorization: Bearer <token>`

## Python Version

Pinned to Python 3.11 via `runtime.txt` for consistency.
