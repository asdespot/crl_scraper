# CRL Scraper and Reader

This project contains two Python scripts for scraping and reading Certificate Revocation Lists (CRL) from various Certificate Authorities in Serbia. The CRL files are downloaded and then parsed to extract serial numbers of revoked certificates.

## Features

- **CRL Scraper**: Downloads CRL files from multiple certificate authority URLs.
- **CRL Reader**: Reads CRL files and extracts the serial numbers of revoked certificates.

## Scripts

### 1. CRL Scraper (`crl_scraper.py`)

This script downloads CRL files from a list of predefined URLs. The URLs include several Serbian certificate authorities.

#### Features:
- Downloads CRL files to a local directory (`crl_scraper/crl`).
- Handles dynamic creation of the download directory.
- Extracts `.crl` links from web pages when required (scraping).
- Includes error handling for network and file-related issues.

#### How to Run:
```bash
python crl_scraper.py
