# MediPredict Frontend

This is the frontend for the MediPredict system, built with React, TailwindCSS, and Recharts.

## Features

- User authentication
- Interactive dashboard with charts
- Device management
- Data upload (CSV/Excel)
- Report generation
- Role-based access control

## Tech Stack

- **Framework**: React with Vite
- **Styling**: TailwindCSS
- **Charts**: Recharts
- **Routing**: React Router

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

## Project Structure

```
frontend/
├── src/
│   ├── components/   # Reusable components
│   ├── pages/        # Page components
│   ├── assets/       # Static assets
│   ├── utils/        # Utility functions
│   ├── services/     # API service functions
│   ├── App.jsx       # Main App component
│   └── main.jsx      # Entry point
├── public/           # Public assets
├── index.html        # HTML template
└── vite.config.js    # Vite configuration
```

## Development

- The app runs on http://localhost:3000
- API requests are proxied to http://localhost:8000