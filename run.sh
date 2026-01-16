#!/bin/bash

echo "================================================"
echo "Real-time Stock Market Sentiment Analyzer"
echo "================================================"
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "================================================"
echo "Choose how to run the application:"
echo "================================================"
echo "1. Streamlit App (Original - Interactive Python)"
echo "2. Modern Web Interface (New - HTML/CSS/JS)"
echo ""
read -p "Enter your choice (1 or 2): " choice

if [ "$choice" = "1" ]; then
    echo ""
    echo "Starting Streamlit application..."
    echo "The app will open in your browser at http://localhost:8501"
    echo ""
    streamlit run app.py
elif [ "$choice" = "2" ]; then
    echo ""
    echo "Opening Modern Web Interface..."
    echo "Opening web_interface.html in your default browser..."
    echo ""
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        open web_interface.html
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        xdg-open web_interface.html
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        # Windows
        start web_interface.html
    else
        echo "Please manually open web_interface.html in your browser"
    fi
else
    echo "Invalid choice. Please run the script again and choose 1 or 2."
fi