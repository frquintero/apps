#!/bin/bash

# Groq Template Tester Setup Script

echo "🚀 Setting up Groq Template Tester..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies in virtual environment..."
pip install groq

# Check if GROQ_API_KEY is set
if [ -z "$GROQ_API_KEY" ]; then
    echo "⚠️  GROQ_API_KEY environment variable is not set."
    echo "📝 Please set your Groq API key:"
    echo "   export GROQ_API_KEY='your_api_key_here'"
    echo "🔑 Get your API key from: https://console.groq.com/keys"
else
    echo "✅ GROQ_API_KEY is set"
fi

# Make the main script executable
chmod +x groq_simple_tester.py

echo "✅ Setup complete!"
echo ""
echo "🎯 To use the app:"
echo "   1. Activate virtual environment: source venv/bin/activate"
echo "   2. Run the app: python groq_simple_tester.py --help"
echo ""
echo "🎯 Quick start:"
echo "   python3 groq_template_tester.py --sample"
echo ""
echo "📖 See README.md for full documentation"
