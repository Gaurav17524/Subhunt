# Subdomain Takeover Hunter

**SubHunt** is a tool designed to automate the detection of subdomain takeover vulnerabilities. It helps identify and analyze subdomains, checks CNAME records, and verifies the status of third-party services to spot potential vulnerabilities.

## Features

- **Subdomain Enumeration**: Detects all subdomains using `subfinder`.
- **CNAME Record Checking**: Retrieves and analyzes CNAME records.
- **Service Status Verification**: Assesses if third-party services are active or expired using `httpx`.
- **Vulnerability Alerts**: Highlights potentially vulnerable subdomains.

## Setup

To get started, you need to install the required Python packages and standalone tools. Follow these steps:

### 1. Install Required Python Packages

Run the following command to install Python packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt


### 2. Execute the install_tools.sh script to install the necessary standalone tools:
chmod +x install_tools.sh
./install_tools.sh

