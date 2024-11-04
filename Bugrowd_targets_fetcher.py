import json
import sys
import csv
import requests
import time
from bs4 import BeautifulSoup
from tqdm import tqdm

class BugcrowdDomainFetcher:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:132.0) Gecko/20100101 Firefox/132.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'X-Csrf-Token': '0vqHlh11zDnsNXPH26WnNXDiSg-tCdcMendyS7zv7zshhIIsrmD-WrVgBRJ8iGN2b5UmLc3QePahoXR_W3frRg'
        }
        self.base_url = "https://bugcrowd.com"

    def get_engagements(self, page):
        url = f"{self.base_url}/engagements.json"
        params = {
            'category': 'bug_bounty',
            'sort_by': 'promoted',
            'sort_direction': 'desc',
            'page': page
        }
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_changelog_url(self, brief_url):
        response = requests.get(f"{self.base_url}{brief_url}", headers=self.headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        div = soup.find('div', {'class': 'react-component-researcher-engagement-brief'})
        if not div:
            return None
            
        data_props = div.get('data-api-endpoints')
        if not data_props:
            return None
            
        props = json.loads(data_props)
        return props.get('engagementBriefApi', {}).get('getBriefVersionDocument')

    def get_domains(self, changelog_url):
        url = f"{self.base_url}{changelog_url}.json"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        
        domains = []
        if 'data' in data and 'scope' in data['data']:
            for scope_group in data['data']['scope']:
                if scope_group.get('inScope', False):
                    for target in scope_group.get('targets', []):
                        name = target.get('name', '')
                        if name:
                            domains.append(name)
        return domains

    def save_to_csv(self, program_domains, specific_programs=None):
        if specific_programs:
            for program, domains in program_domains.items():
                program_name = program.split('/')[-1]
                if program_name in specific_programs:
                    filename = f"{program_name}_domains.csv"
                    with open(filename, 'w', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(['Domain'])
                        for domain in domains:
                            writer.writerow([domain])
                    print(f"Saved {len(domains)} domains for {program_name} to {filename}")
        else:
            filename = "all_programs_domains.csv"
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Program', 'Domain'])
                for program, domains in program_domains.items():
                    program_name = program.split('/')[-1]
                    for domain in domains:
                        writer.writerow([program_name, domain])
            total_domains = sum(len(domains) for domains in program_domains.values())
            print(f"Saved {total_domains} domains from {len(program_domains)} programs to {filename}")

    def fetch_all_data(self, specific_programs=None):
        print("Fetching program list...")
        page = 1
        brief_urls = []
        program_domains = {}
        
        while True:
            data = self.get_engagements(page)
            if page == 1:
                total_count = data['paginationMeta']['totalCount']
                limit = data['paginationMeta']['limit']
                total_pages = (total_count + limit - 1) // limit
            
            for engagement in data['engagements']:
                brief_urls.append(engagement['briefUrl'])
            
            if page >= total_pages:
                break
            page += 1
            time.sleep(0.5)

        if specific_programs:
            brief_urls = [url for url in brief_urls if any(prog in url for prog in specific_programs)]
            if not brief_urls:
                print("No matching programs found")
                return

        print("Fetching program details...")
        for brief_url in tqdm(brief_urls, desc="Processing programs"):
            try:
                changelog_url = self.get_changelog_url(brief_url)
                if changelog_url:
                    domains = self.get_domains(changelog_url)
                    program_domains[brief_url] = domains
                time.sleep(0.5)
            except requests.exceptions.RequestException as e:
                print(f"Error processing {brief_url}: {e}")
                continue

        return program_domains

def main():
    fetcher = BugcrowdDomainFetcher()
    specific_programs = sys.argv[1:] if len(sys.argv) > 1 else None
    
    try:
        program_domains = fetcher.fetch_all_data(specific_programs)
        if program_domains:
            fetcher.save_to_csv(program_domains, specific_programs)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main() 