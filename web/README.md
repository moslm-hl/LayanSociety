# LayanSociety Web Application

A modern web-based economic analysis platform with a beautiful UI/UX for Tunisia's economic calculations and projections.

## 🚀 Features

- **Dashboard**: Real-time economic indicators overview
- **Inflation Calculator**: Adjust costs for inflation (2010-2026)
- **GDP Projection Calculator**: Economic growth forecasts with scenarios
- **Unemployment Rate Calculator**: Labor market trend analysis
- **Currency Converter**: TND/USD/EUR historical exchange rates
- **Interest Rate Calculator**: Investment/loan impact analysis

## 🎨 UI/UX Highlights

- Modern glassmorphism design
- Gradient backgrounds with purple theme
- Responsive layout for all devices
- Smooth animations and transitions
- Interactive charts and data visualizations
- Real-time API integration
- Professional color-coded results

## 📁 Project Structure

```
web/
├── backend/
│   ├── main.py              # FastAPI backend server
│   └── requirements.txt     # Python dependencies
└── frontend/
    ├── package.json         # Node.js dependencies
    ├── tailwind.config.js   # TailwindCSS configuration
    ├── public/
    │   └── index.html       # HTML template
    └── src/
        ├── App.js           # Main React component
        ├── App.css          # Global styles
        ├── index.js         # React entry point
        └── components/
            ├── Dashboard.js
            ├── InflationCalculator.js
            ├── GDPCalculator.js
            ├── UnemploymentCalculator.js
            ├── CurrencyConverter.js
            └── InterestCalculator.js
```

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd web/backend
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the FastAPI server:**
   ```bash
   python main.py
   ```

   The backend will run on `http://localhost:8000`

4. **Access API documentation:**
   Open `http://localhost:8000/docs` in your browser for interactive API documentation.

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd web/frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start the React development server:**
   ```bash
   npm start
   ```

   The frontend will run on `http://localhost:3000`

## 🌐 Running the Application

### Option 1: Development Mode (Recommended)

Run both backend and frontend in separate terminals:

**Terminal 1 (Backend):**
```bash
cd web/backend
python main.py
```

**Terminal 2 (Frontend):**
```bash
cd web/frontend
npm start
```

### Option 2: Production Build

1. **Build the frontend:**
   ```bash
   cd web/frontend
   npm run build
   ```

2. **Serve with FastAPI:**
   Update the backend to serve the static files from the build directory.

## 📡 API Endpoints

### Economic Data
- `GET /api/inflation-rates` - Get all inflation rates
- `GET /api/economic-summary/{year}` - Get economic summary for a year

### Calculators
- `POST /api/inflation` - Calculate inflation adjustment
- `POST /api/future-cost` - Calculate future cost projection
- `POST /api/gdp` - Calculate GDP projection
- `POST /api/unemployment` - Calculate unemployment projection
- `POST /api/currency` - Convert currency
- `POST /api/interest` - Calculate interest impact

## 🎯 Usage Examples

### Inflation Calculator
1. Enter amount in TND
2. Select base year (2010-2026)
3. Click "Calculate Inflation"
4. View adjusted amount and multiplier

### GDP Projection
1. Enter initial GDP value
2. Select start and target years
3. Choose scenario (optimistic/baseline/pessimistic)
4. View year-by-year projections

### Currency Converter
1. Enter amount
2. Select from/to currencies (TND/USD/EUR)
3. Select year for historical rate
4. View conversion result

## 🎨 Customization

### Colors
Edit `src/App.css` to customize the color scheme:
- Primary color: Purple (`#a855f7`)
- Background: Slate/Purple gradient
- Glass effect: `rgba(255, 255, 255, 0.05)`

### Components
Each calculator is a separate component in `src/components/`. Modify them to add features or change layouts.

## 📊 Data Sources

- **Inflation Rates**: Central Bank of Tunisia
- **GDP Data**: World Bank, IMF
- **Unemployment**: National Statistics Institute (INS)
- **Exchange Rates**: Central Bank of Tunisia
- **Interest Rates**: Central Bank of Tunisia policy rates

## 🔧 Troubleshooting

### Backend Issues
- **Port 8000 already in use**: Change the port in `main.py`
- **Import errors**: Ensure you're running from the `web/backend` directory
- **Module not found**: Install dependencies with `pip install -r requirements.txt`

### Frontend Issues
- **Port 3000 already in use**: React will automatically try the next available port
- **API connection errors**: Ensure backend is running on port 8000
- **Build errors**: Clear cache with `npm cache clean --force`

## 🚀 Deployment

### Backend Deployment
- Deploy to AWS, Google Cloud, or Azure
- Use Gunicorn with Uvicorn workers
- Set up environment variables for production

### Frontend Deployment
- Build with `npm run build`
- Deploy to Netlify, Vercel, or serve from backend
- Configure environment variables for API URL

## 📝 License

This project is part of LayanSociety for Cost Calculation and Risk Estimation.

## 🤝 Support

For issues or questions, please contact the development team.

---

**Built with ❤️ for Tunisia's economic analysis**
