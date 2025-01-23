# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh


trading-bot/
├── api/                    # Backend
│   ├── __init__.py
│   ├── config.py          # Keys & constants
│   ├── trading.py         # Your Solana trading code
│   ├── requirements.txt   # Python dependencies
│   └── main.py           # FastAPI server
│
├── src/                   # Frontend
│   ├── components/
│   │   ├── ui/           # shadcn components
│   │   └── TradingInterface.jsx
│   ├── App.jsx
│   └── main.jsx
│
├── vite.config.js
├── package.json
└── README.md   