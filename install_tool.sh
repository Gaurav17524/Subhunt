#!/bin/bash

# Function to check for errors and exit if any occur
check_error() {
    if [ $? -ne 0 ]; then
        echo "Error occurred during installation. Exiting."
        exit 1
    fi
}

echo "Installing Subdomain Takeover Hunter prerequisites..."

# Ensure Go is installed
if ! command -v go &> /dev/null; then
    echo "Go is not installed. Please install Go first."
    exit 1
fi

# Install Subfinder
echo "Installing Subfinder..."
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
check_error

# Install httpx
echo "Installing httpx..."
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
check_error

# Install dig
echo "Installing dig..."
if [ -x "$(command -v apt-get)" ]; then
    sudo apt-get update
    sudo apt-get install -y dnsutils
elif [ -x "$(command -v yum)" ]; then
    sudo yum install -y bind-utils
else
    echo "Unsupported package manager. Please install dnsutils manually."
    exit 1
fi
check_error

echo "All tools installed successfully."
