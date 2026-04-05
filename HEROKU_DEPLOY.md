# Heroku Deployment Guide (SQLite)

## ⚠️ Important: SQLite Limitations on Heroku
- **Data is ephemeral**: Database resets on every dyno restart (24h or on deploy)
- **Good for**: Testing, demos, prototypes
- **Not good for**: Production with persistent data
- **Upgrade path**: Switch to PostgreSQL when ready for production

## Prerequisites
- Heroku CLI installed: `npm install -g heroku`
- Heroku account created

## Quick Deploy (5 Steps)

### Step 1: Create Heroku App
```bash
heroku login
heroku create your-app-name
```

### Step 2: Set Environment Variables
```bash
# Generate secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Set config vars
heroku config:set SECRET_KEY="paste-generated-key-here"
heroku config:set GROQ_API_KEY="gsk_your_groq_api_key"
heroku config:set GEMINI_API_KEY="your_gemini_api_key"
heroku config:set USE_AI="true"
heroku config:set DATABASE_URL="sqlite:///./hospitality.db"
```

### Step 3: Deploy
```bash
git push heroku upcoming-features:main
```

### Step 4: Check Logs
```bash
heroku logs --tail
```

### Step 5: Open App
```bash
heroku open
# Visit: https://your-app-name.herokuapp.com/docs
```

## Testing Deployment

### Test API Health
```bash
curl https://your-app-name.herokuapp.com/docs
```

### Test Event Search
```bash
curl -X POST https://your-app-name.herokuapp.com/search-events \
  -H "Content-Type: application/json" \
  -d '{"timeframe": "1_month", "categories": ["religious"]}'
```

### Test Campaign Generation
1. Get event ID from search results
2. Go to `/docs` in browser
3. Test `POST /events/{event_id}/campaign`

## Environment Variables

| Variable | Value | Where to Get |
|----------|-------|--------------|
| `SECRET_KEY` | Random string | `python -c "import secrets; print(secrets.token_urlsafe(32))"` |
| `GROQ_API_KEY` | `gsk_...` | https://console.groq.com |
| `GEMINI_API_KEY` | `AIza...` | https://aistudio.google.com/apikey |
| `USE_AI` | `true` or `false` | Set to `false` for mock mode (free testing) |
| `DATABASE_URL` | `sqlite:///./hospitality.db` | Already set |

## Troubleshooting

### App Crashes
```bash
heroku logs --tail
# Look for missing environment variables or import errors
```

### Database Empty After Restart
This is expected with SQLite on Heroku. Data resets every 24 hours or on deploy.

**Solution**: Re-run event search to repopulate database, or upgrade to PostgreSQL.

### Slow Cold Starts
Heroku free tier sleeps after 30 min inactivity.

**Solution**: Upgrade to Eco dyno ($5/mo) or use a ping service.

## Cost Estimate
- **Eco Dyno**: $5/month (always-on, 1000 hours shared)
- **Free Tier**: $0/month (sleeps after 30 min, limited hours)

## Production Upgrade Path

When ready for persistent data:

```bash
# Add PostgreSQL
heroku addons:create heroku-postgresql:essential-0

# Remove SQLite config
heroku config:unset DATABASE_URL

# Heroku auto-sets DATABASE_URL to Postgres
heroku config:get DATABASE_URL

# Redeploy
git push heroku upcoming-features:main

# Create tables
heroku run python -c "from app.db import engine; from app.models import Base; Base.metadata.create_all(bind=engine)"
```

## Deployment Checklist
- [ ] Heroku app created
- [ ] All environment variables set
- [ ] Code pushed to Heroku
- [ ] API accessible at /docs
- [ ] Event search working (USE_AI=true)
- [ ] Campaign generation working
- [ ] Understand data resets on restart
