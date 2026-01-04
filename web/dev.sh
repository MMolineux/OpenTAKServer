#!/usr/bin/env bash

# dev quickstart helper script

if command -v yarn &> /dev/null; then
    echo "Yarn is installed, skipping npm install."
elif command -v npm &> /dev/null; then
    echo "Yarn is not installed, but npm is available."
    npm install yarn -D
else
    echo "Neither yarn nor npm is installed. Please install one of them to manage frontend dependencies."
    exit 1
fi

if [[ -d "./node_modules" ]]; then
    echo "node_modules directory already exists. Skipping npm install."
else
    echo "Installing npm dependencies..."
    if ! yarn install; then
        echo "Failed to install npm dependencies."
        exit 1
    fi
    if ! npm run build; then
        echo "Failed to build frontend assets."
        exit 1
    fi
fi

# start dev environment
yarn run dev