# Vercel Deployment Guide for LayanSociety

## Prerequisites
- GitHub account
- Vercel account (free tier works)
- All Python calculator modules in the project root

## Project Structure
```
web/
├── api/
│   └── index.py          # Vercel serverless function (FastAPI backend)
├── backend/              # Python core modules (copied for deployment)
│   ├── tunisia_inflation_calculator.py
│   ├── tunisia_economic_indicators.py
│   ├── tunisia_future_cost_estimator.py
│   ├── logger_config.py
│   ├── main.py           # Standalone FastAPI backend
│   └── requirements.txt
├── frontend/             # React frontend
│   ├── src/
│   ├── package.json
│   └── ...
├── requirements.txt      # Python dependencies for Vercel
├── vercel.json          # Vercel configuration
└── package.json         # Root package.json
```

## Step 1: Push to GitHub

1. Initialize git repository (if not already done):
```bash
cd "c:\Users\DELL\Desktop\LAYAN SOCIETY FOR COST CALCULATION AND RISK ESTIMATION\LayanSociety\web"
git init
git add .
git commit -m "Initial commit for Vercel deployment"
```

2. Create a new repository on GitHub
3. Add remote and push:
```bash
git remote add origin https://github.com/YOUR_USERNAME/layansociety.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy to Vercel

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "Add New Project"
3. Import your GitHub repository
4. Configure the project:
   - **Framework Preset**: Create (custom)
   - **Root Directory**: `./` (leave as default)
   - **Build Command**: `cd frontend && npm run build`
   - **Output Directory**: `frontend/build`
   - **Install Command**: `cd frontend && npm install`

5. Click "Deploy"

## Step 3: Configure Environment Variables

After deployment, you may need to add environment variables if required.

### What are Environment Variables?

Environment variables are configuration values that are set outside of your code and injected at runtime. They are used to store sensitive information (API keys, database credentials) and configuration settings that may vary between environments (development, staging, production).

### How to Add Environment Variables in Vercel

1. Go to your project dashboard on Vercel
2. Click on **Settings** tab
3. Select **Environment Variables** from the left sidebar
4. Click **Add New** to add each variable:
   - **Key**: The variable name (e.g., `API_KEY`, `DATABASE_URL`)
   - **Value**: The actual value
   - **Environment**: Choose which environments this applies to (Production, Preview, Development)
5. Click **Save**

### Current Environment Variables for This Project

**No environment variables are currently required** for this project. Your code uses hardcoded data and doesn't rely on external APIs or databases that would need configuration.

### Future Environment Variables (If Needed)

If you later add external APIs or databases, you may need:

- **API Keys**: If using external APIs for currency conversion, GDP data, or inflation rates
- **Database URLs**: If connecting to external databases
- **CORS Origins**: To control which domains can access your API
- **Rate Limiting Settings**: To control API usage limits

### Example Environment Variables (For Future Use)

```bash
# Example environment variables (if you add external APIs later)
CURRENCY_API_KEY=your_api_key_here
GDP_DATA_SOURCE=https://api.example.com/gdp
INFLATION_API_ENDPOINT=https://api.example.com/inflation
ALLOWED_ORIGINS=https://layansociety.vercel.app
```

### Accessing Environment Variables in Code

In your Python API (`api/index.py`), access environment variables using:

```python
import os

api_key = os.getenv("CURRENCY_API_KEY")
data_source = os.getenv("GDP_DATA_SOURCE")
```

In your React frontend, you can add environment variables by:
1. Creating a `.env` file in the `frontend/` directory
2. Prefixing variables with `REACT_APP_` (e.g., `REACT_APP_API_URL`)
3. Accessing them via `process.env.REACT_APP_API_URL`

### Important Notes

- Never commit `.env` files to version control
- Environment variables are encrypted in Vercel
- Changes to environment variables require a redeployment to take effect
- Use different values for different environments when needed

## Step 4: Test the Deployment

1. Visit your Vercel URL (e.g., `https://layansociety.vercel.app`)
2. Test the calculators to ensure API calls work
3. Check the Vercel dashboard for any errors

## Important Notes

### API Endpoints
The backend is now deployed as a Vercel serverless function. All API calls use relative paths (`/api`) which will work automatically in production.

### Python Dependencies
The `requirements.txt` file includes:
- fastapi
- uvicorn
- pydantic
- reportlab
- mangum (for ASGI adapter)

### Backend Modules
The `api/index.py` imports from the backend modules. Ensure these Python calculator files are in the project root or adjust the import paths accordingly.

### Troubleshooting

**If API calls fail:**
1. Check Vercel function logs in the dashboard
2. Ensure all Python calculator modules are accessible
3. Verify the import paths in `api/index.py`

**If frontend doesn't build:**
1. Check the build logs in Vercel
2. Ensure all dependencies are in `frontend/package.json`
3. Verify the build command is correct

**If you need to update the backend:**
1. Modify `api/index.py`
2. Push changes to GitHub
3. Vercel will automatically redeploy

## Alternative: Separate Backend Deployment

If the Vercel serverless function approach doesn't work well with your Python modules, consider:

1. **Deploy backend to Render/Railway**:
   - Deploy the FastAPI backend separately
   - Update frontend API_URL to the deployed backend URL
   - Deploy frontend to Vercel

2. **Use Vercel with a different structure**:
   - Convert the backend to individual serverless functions
   - Each endpoint as a separate function in `api/` directory

## Local Testing

To test locally before deployment:

```bash
# Install Vercel CLI
npm i -g vercel

# Run locally
vercel dev
```

This will run both the frontend and API locally using the Vercel development environment.
