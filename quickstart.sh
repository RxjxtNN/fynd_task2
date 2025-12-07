#!/bin/bash
# Quick Start Script for Local Development

echo "🚀 AI Feedback System - Quick Start"
echo "===================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi
echo "✓ Python 3 found"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found"
    exit 1
fi
echo "✓ pip3 found"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "⚠️  .env file not found"
    echo "📝 Creating .env.example for reference..."
    if [ ! -f .env.example ]; then
        cat > .env.example << 'EOF'
# Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# PostgreSQL Database URL (for production)
# DATABASE_URL=postgresql://user:password@host/dbname

# For local development with SQLite (fallback):
# Leave DATABASE_URL empty to use local SQLite
EOF
    fi
    echo "✓ Created .env.example"
    echo ""
    echo "Please create a .env file with your API keys:"
    echo "  - GEMINI_API_KEY=your_key_here"
    echo "  - DATABASE_URL=your_postgres_url (optional)"
fi

# Ask user what to run
echo ""
echo "What would you like to run?"
echo "1) User Dashboard (Primary app)"
echo "2) Admin Dashboard (Secondary app)"
echo "3) Run tests"
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo "Starting User Dashboard..."
        streamlit run User_Dashboard.py
        ;;
    2)
        echo "Starting Admin Dashboard..."
        streamlit run pages/Admin_Dashboard.py
        ;;
    3)
        echo "Running verification..."
        python3 verify_setup.py
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
