# Bugcrowd Targets Fetcher

A Python tool to fetch in-scope domains from Bugcrowd bug bounty programs.

## Features
- Fetches all active bug bounty programs from Bugcrowd
- Extracts in-scope domains for each program or for a specific program
- Saves results to CSV files
- Progress bar for better visibility
- Rate limiting to avoid overloading servers

## Installation
1. Clone this repository
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
- Fetch all programs:
  ```bash
  python bugcrowd_domains_fetcher.py
  ```

- Fetch specific programs:
  ```bash
  python bugcrowd_domains_fetcher.py program1 program2
  ```

## Examples
1. Fetch all programs:
   ```bash
   python bugcrowd_domains_fetcher.py
   ```
   > This will create all_programs_domains.csv containing all domains

2. Fetch specific program:
   ```bash
   python bugcrowd_domains_fetcher.py justeattakeaway
   ```
   > This will create justeattakeaway_domains.csv

## Output Format
- When fetching all programs:
  ```
  Program,Domain
  program1,domain1.com
  program1,domain2.com
  program2,domain3.com
  ```

- When fetching specific program:
  ```
  Domain
  domain1.com
  domain2.com
  ```

## Notes
- The tool uses rate limiting (0.5s between requests) to be respectful to Bugcrowd servers

## Requirements
- Python 3.6+
- requests
- beautifulsoup4
- tqdm

## Legal Disclaimer
This tool is provided for educational and legitimate security research purposes only. Users must comply with Bugcrowd's Terms of Service and follow responsible disclosure practices.

The author accepts no liability for misuse of this tool or any damages that may result from its use. Users are solely responsible for ensuring their use complies with applicable laws and regulations.

## License
MIT License
