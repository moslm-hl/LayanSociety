# Environment Variables Guide for LayanSociety

This guide provides detailed information about environment variables, how to configure them in Vercel, and how to use them in your LayanSociety project.

## Table of Contents
- [What are Environment Variables?](#what-are-environment-variables)
- [Current Status](#current-status)
- [When You Need Environment Variables](#when-you-need-environment-variables)
- [Setting Up Environment Variables in Vercel](#setting-up-environment-variables-in-vercel)
- [Using Environment Variables in Your Code](#using-environment-variables-in-your-code)
- [Common Use Cases for This Project](#common-use-cases-for-this-project)
- [Security Best Practices](#security-best-practices)
- [Troubleshooting](#troubleshooting)

## What are Environment Variables?

Environment variables are dynamic values that can affect the behavior of running processes without changing the code. They are:

- **Key-value pairs** stored outside your source code
- **Injected at runtime** into your application
- **Environment-specific** (different values for development, staging, production)
- **Secure** for storing sensitive information like API keys and passwords

### Why Use Environment Variables?

1. **Security**: Keep sensitive data (API keys, database credentials) out of your code
2. **Flexibility**: Change configuration without redeploying code
3. **Environment Management**: Use different settings for development vs production
4. **Collaboration**: Share code without sharing secrets

## Current Status

**Your LayanSociety project currently does not require any environment variables.**

Your implementation uses:
- **Hardcoded economic data** in Python dictionaries:
  - `INFLATION_RATES` in `tunisia_inflation_calculator.py` (lines 17-35)
  - `GDP_GROWTH_RATES`, `UNEMPLOYMENT_RATES`, `EXCHANGE_RATES`, etc. in `tunisia_economic_indicators.py` (lines 13-137)
- Local Python calculator modules
- No external API calls
- No database connections

**Note:** While your code comments reference data sources like World Bank, IMF, and National Statistics Institute, the actual values are hardcoded in your Python files - not fetched dynamically from external servers.

This means you can deploy to Vercel without configuring any environment variables.

## When You Need Environment Variables

You will need environment variables if you plan to:

### 1. Add External APIs
- Currency conversion APIs (e.g., ExchangeRate-API, Fixer.io)
- Real-time GDP data sources (e.g., World Bank API, IMF API)
- Inflation rate APIs (e.g., government statistics APIs)
- Authentication services (e.g., Auth0, Firebase)

### 2. Add Database Connections
- PostgreSQL, MySQL, MongoDB connections
- Database credentials (username, password, host, port)
- Connection strings

### 3. Add Third-Party Services
- Email services (SendGrid, Mailgun)
- File storage (AWS S3, Cloudinary)
- Analytics (Google Analytics, Mixpanel)
- Payment gateways (Stripe, PayPal)

### 4. Configure Application Behavior
- CORS allowed origins
- Rate limiting settings
- Feature flags
- Debug mode settings

## Setting Up Environment Variables in Vercel

### Step-by-Step Instructions

1. **Log in to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Sign in to your account

2. **Navigate to Your Project**
   - Select your LayanSociety project from the dashboard

3. **Access Settings**
   - Click on the **Settings** tab at the top
   - Select **Environment Variables** from the left sidebar

4. **Add Environment Variables**
   - Click the **Add New** button
   - Fill in the fields:
     - **Key**: The variable name (e.g., `CURRENCY_API_KEY`)
     - **Value**: The actual value (e.g., `abc123xyz`)
     - **Environment**: Choose where to apply:
       - **Production**: For your live deployment
       - **Preview**: For preview deployments from pull requests
       - **Development**: For local development
   - Click **Save**

5. **Redeploy (Required)**
   - Environment variable changes require a redeployment
   - Go to the **Deployments** tab
   - Click the three dots (...) next to your latest deployment
   - Select **Redeploy**

### Environment-Specific Values

You can set different values for different environments:

```bash
# Example: Different API keys for different environments
# Production
CURRENCY_API_KEY=prod_key_abc123

# Preview
CURRENCY_API_KEY=preview_key_xyz789

# Development
CURRENCY_API_KEY=dev_key_def456
```

### Using Vercel CLI

You can also set environment variables using the Vercel CLI:

```bash
# Install Vercel CLI (if not already installed)
npm i -g vercel

# Login to Vercel
vercel login

# Add environment variable
vercel env add CURRENCY_API_KEY

# Pull environment variables locally
vercel env pull .env.local
```

## Using Environment Variables in Your Code

### Python (Backend API)

In your `api/index.py` or any Python module:

```python
import os

# Get environment variable
api_key = os.getenv("CURRENCY_API_KEY")
database_url = os.getenv("DATABASE_URL")

# Provide default value if not set
debug_mode = os.getenv("DEBUG", "false") == "true"

# Check if variable exists
if not api_key:
    raise ValueError("CURRENCY_API_KEY environment variable is not set")

# Use in your code
def fetch_currency_data():
    headers = {"Authorization": f"Bearer {api_key}"}
    # ... make API call
```

### React (Frontend)

In your React components, environment variables must be prefixed with `REACT_APP_`:

1. **Create `.env` file in `frontend/` directory:**
```bash
REACT_APP_API_URL=https://layansociety.vercel.app
REACT_APP_GOOGLE_ANALYTICS_ID=UA-123456789-1
```

2. **Use in your React components:**
```javascript
const apiUrl = process.env.REACT_APP_API_URL;
const analyticsId = process.env.REACT_APP_GOOGLE_ANALYTICS_ID;

// Example in a component
function GDPCalculator() {
  useEffect(() => {
    console.log("API URL:", apiUrl);
    // ... use the variable
  }, [apiUrl]);
  
  return <div>...</div>;
}
```

**Important:** React environment variables are embedded during build time, not runtime. Changes require rebuilding the frontend.

### Accessing Vercel Environment Variables in Python

Vercel automatically makes environment variables available to your serverless functions. No additional configuration is needed - they're accessible via `os.getenv()`.

## Common Use Cases for This Project

### Example 1: Adding Currency Conversion API

If you want to use an external API for currency conversion:

**1. Sign up for an API service** (e.g., ExchangeRate-API)
**2. Get your API key**
**3. Add to Vercel:**
   - Key: `CURRENCY_API_KEY`
   - Value: `your_actual_api_key`
   - Environment: Production, Preview, Development

**4. Update your code:**
```python
# In tunisia_economic_indicators.py or api/index.py
import os
import requests

API_KEY = os.getenv("CURRENCY_API_KEY")

def calculate_currency_conversion(amount, from_currency, to_currency, year):
    if not API_KEY:
        # Fall back to hardcoded data
        return use_hardcoded_rates(amount, from_currency, to_currency, year)
    
    # Use external API
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_currency}/{to_currency}"
    response = requests.get(url)
    data = response.json()
    # ... process data
```

### Example 2: Adding Database Connection

If you want to store calculation results in a database:

**1. Set up a database** (e.g., PostgreSQL on Supabase, Neon, or Railway)
**2. Get connection string**
**3. Add to Vercel:**
   - Key: `DATABASE_URL`
   - Value: `postgresql://user:password@host:port/database`
   - Environment: Production, Preview, Development

**4. Update your code:**
```python
import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def save_calculation_result(data):
    with engine.connect() as conn:
        # ... save to database
```

### Example 3: Configuring CORS Origins

To control which domains can access your API:

**Add to Vercel:**
   - Key: `ALLOWED_ORIGINS`
   - Value: `https://layansociety.vercel.app,https://localhost:3000`
   - Environment: Production, Preview, Development

**Update your code:**
```python
# In api/index.py
import os

allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Security Best Practices

### DO:
- ✅ Use environment variables for all sensitive data
- ✅ Rotate API keys regularly
- ✅ Use different values for different environments
- ✅ Limit environment variable access to necessary team members
- ✅ Use Vercel's encrypted environment variables
- ✅ Document required environment variables in README

### DON'T:
- ❌ Commit `.env` files to version control
- ❌ Hardcode API keys or passwords in source code
- ❌ Share environment variables in public repositories
- ❌ Use the same API keys across all environments
- ❌ Log environment variables in production
- ❌ Include environment variables in client-side JavaScript (unless prefixed with `REACT_APP_`)

### Git Ignore

Add this to your `.gitignore` file:
```gitignore
# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local
```

## Troubleshooting

### Environment Variables Not Working

**Problem:** Your code can't access environment variables

**Solutions:**
1. **Check Vercel Settings:**
   - Verify variables are added in the correct environment
   - Ensure variable names match exactly (case-sensitive)
   - Check for typos in key names

2. **Redeploy:**
   - Environment variable changes require redeployment
   - Go to Deployments → Redeploy

3. **Check Code:**
   - Verify you're using `os.getenv("KEY_NAME")` in Python
   - Verify React variables are prefixed with `REACT_APP_`
   - Check for typos in variable names in code

4. **Debug Locally:**
   ```python
   # Add temporary debugging
   import os
   print("All env vars:", dict(os.environ))
   print("Specific var:", os.getenv("YOUR_VAR"))
   ```

### Build Errors

**Problem:** Frontend build fails due to missing environment variables

**Solution:**
- Add default values in your code:
  ```javascript
  const apiUrl = process.env.REACT_APP_API_URL || "http://localhost:5000";
  ```
- Or add the variable to all environments in Vercel

### Runtime Errors

**Problem:** API calls fail with "missing environment variable" error

**Solution:**
- Ensure the variable is set in the correct environment (Production)
- Check Vercel function logs for specific error messages
- Verify the variable name matches exactly in code and Vercel

## Testing Environment Variables

### Local Testing

Create a `.env` file locally for testing:

```bash
# .env file (DO NOT COMMIT)
CURRENCY_API_KEY=test_key_123
DATABASE_URL=postgresql://localhost:5432/testdb
DEBUG=true
```

Load in Python:
```python
from dotenv import load_dotenv
load_dotenv()  # Loads .env file

import os
api_key = os.getenv("CURRENCY_API_KEY")
```

### Vercel CLI Testing

Test with Vercel CLI locally:

```bash
# Pull environment variables from Vercel
vercel env pull .env.local

# Run locally with Vercel environment
vercel dev
```

## Summary

- **Current Status:** No environment variables needed for your current implementation
- **Future Needs:** Add them when integrating external APIs, databases, or third-party services
- **Setup:** Use Vercel dashboard Settings → Environment Variables
- **Access:** Use `os.getenv()` in Python, `process.env.REACT_APP_*` in React
- **Security:** Never commit `.env` files, always use Vercel's encrypted variables
- **Redeploy:** Required after changing environment variables

## Additional Resources

- [Vercel Environment Variables Documentation](https://vercel.com/docs/projects/environment-variables)
- [React Environment Variables](https://create-react-app.dev/docs/adding-custom-environment-variables/)
- [Python `os` Module Documentation](https://docs.python.org/3/library/os.html)
- [12-Factor App: Configuration](https://12factor.net/config)
