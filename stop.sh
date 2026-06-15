#!/bin/bash

echo "Stopping Instagram Profile Card Service..."
pkill -f "uvicorn main:app" || true
echo "Service stopped."