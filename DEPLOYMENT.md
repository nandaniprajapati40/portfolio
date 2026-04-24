# Deployment Guide - Render

This guide explains how to deploy the Nandani Portfolio application to Render.

## Prerequisites

1. **Render Account** - Sign up at [render.com](https://render.com)
2. **GitHub Repository** - Push your code to GitHub
3. **MongoDB Atlas** - Set up a free cluster at [mongodb.com/cloud/atlas](https://mongodb.com/cloud/atlas)

## Deployment Steps

### 1. Prepare MongoDB

1. Go to MongoDB Atlas and create a cluster
2. Create a database user with a strong password
3. Get your connection URI (should look like: `mongodb+srv://username:password@cluster.mongodb.net/portfolio_db`)
4. Whitelist your Render IP or use `0.0.0.0/0` for development

### 2. Deploy to Render

#### Option A: Using Render Dashboard (Recommended for beginners)

1. Go to [render.com/dashboard](https://render.com/dashboard)
2. Click **New +** → **Web Service**
3. Connect your GitHub repository
4. Fill in the details:
   - **Name**: `nandani-portfolio`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`

5. Add Environment Variables:
   - **MONGO_URI**: Your MongoDB connection string (mark as secret)
   - **FLASK_ENV**: `production`

6. Choose Plan: **Free** (or Starter for better performance)
7. Click **Create Web Service**

#### Option B: Using render.yaml (Advanced)

1. Push the `render.yaml` file to your GitHub repo
2. Go to Render Dashboard → **Infrastructure** → **Infrastructure as Code**
3. Connect your GitHub repo
4. Update the `render.yaml` file with your MongoDB URI
5. Deploy with: `render deploy`

### 3. Post-Deployment Configuration

1. **Test the deployment**:
   ```bash
   curl https://your-app-name.onrender.com/health
   ```

2. **Custom Domain** (Optional):
   - Go to your Render service settings
   - Add a custom domain under **Settings** → **Custom Domain**

### 4. Environment Variables

The following environment variables must be set in Render:

| Variable | Required | Example |
|----------|----------|---------|
| `MONGO_URI` | Yes | `mongodb+srv://...` |
| `FLASK_ENV` | No | `production` |

## Important Notes

### Cold Starts
- Free tier services spin down after 15 minutes of inactivity
- First request will take 30+ seconds
- Upgrade to Starter ($7/month) to avoid this

### Logging
- View logs in Render dashboard under **Logs**
- Enable detailed logging for debugging

### Scaling
- Free tier: Single instance, 0.5 CPU, 512 MB RAM
- Starter tier: Better performance and reliability

## Troubleshooting

### App crashes on deploy
- Check build logs for errors
- Verify `requirements.txt` has all dependencies
- Ensure MongoDB URI is correct

### 502 Bad Gateway
- App may be starting, wait 30-60 seconds
- Check Render logs for errors
- Verify health check endpoint works: `GET /health`

### MongoDB connection fails
- Verify connection URI format
- Check if IP whitelist includes `0.0.0.0/0` or Render's IP
- Test connection locally first

## Local Testing

To test before deployment:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
FLASK_ENV=production gunicorn --bind 0.0.0.0:5000 app:app

# Or use Flask dev server
python app.py
```

## Files Included

- `Dockerfile` - Container configuration
- `render.yaml` - Render deployment config
- `.dockerignore` - Files to exclude from Docker build
- `Procfile` - Process definition for Render
- `.env.example` - Environment variables template

## Support

For issues:
1. Check Render [documentation](https://render.com/docs)
2. Review [MongoDB Atlas troubleshooting](https://docs.atlas.mongodb.com/)
3. Check Flask [error handling](https://flask.palletsprojects.com/en/2.3.x/)
