import os
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import logging
import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import re
from typing import Dict, List, Optional
from urllib.parse import urljoin

# Disable SSL verification warnings
urllib3.disable_warnings(InsecureRequestWarning)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class HMMTProblemDownloader:
    def __init__(self):
        self.base_url = "https://www.hmmt.org"
        self.archive_url = f"{self.base_url}/www/archive/problems"
        self.raw_data_dir = os.path.join(os.path.dirname(__file__), "raw_data")
        os.makedirs(self.raw_data_dir, exist_ok=True)
        self.session = requests.Session()
        # Disable SSL verification
        self.session.verify = False

    def download_page(self, url: str) -> Optional[str]:
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error downloading {url}: {e}")
            return None

    def download_pdf(self, url: str, output_path: str) -> bool:
        """Download a PDF file from a URL and save it to the specified path."""
        try:
            # Add https: prefix if the URL is protocol-relative
            if url.startswith('//'):
                url = 'https:' + url
            
            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Download the PDF with SSL verification disabled
            response = requests.get(url, verify=False)
            response.raise_for_status()
            
            # Save the PDF
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            logging.info(f"Successfully downloaded {url} to {output_path}")
            return True
        except Exception as e:
            logging.error(f"Error downloading {url}: {str(e)}")
            return False

    def parse_tournament_links(self, html_content: str) -> List[Dict]:
        if not html_content:
            return []
        
        soup = BeautifulSoup(html_content, 'html.parser')
        tournaments = []
        
        # Find all rows with tournament links
        rows = soup.find_all('div', class_='row')
        for row in rows:
            links = row.find_all('a')
            for link in links:
                if not link.text.strip():
                    continue
                
                href = link.get('href')
                if not href:
                    continue
                
                year = link.text.strip()
                tournament_type = self._determine_tournament_type(row)
                
                if tournament_type:
                    tournaments.append({
                        'year': year,
                        'type': tournament_type,
                        'url': f"{self.base_url}{href}",
                    })
        
        return tournaments

    def _determine_tournament_type(self, row) -> Optional[str]:
        # Based on the column position (col-2), determine if it's November, February, or Invitational
        cols = row.find_all('div', class_='col-2')
        if not cols:
            return None
        
        for i, col in enumerate(cols):
            if col.find('a'):
                if i == 0:
                    return 'November'
                elif i == 1:
                    return 'February'
                elif i == 2:
                    return 'Invitational'
        return None

    def clean_path(self, path: str) -> str:
        """Clean up a path string by removing HTML, navigation text, and invalid characters."""
        # Remove HTML tags
        path = re.sub(r'<[^>]+>', '', path)
        
        # Remove navigation text and common UI elements
        path = re.sub(r'Toggle navigation|HMMT|Registration|General Information|Financial Aid|Deadlines|Video Guides|Apply Tournament|Problems and Results|Education|Photos|POTW|About|Contact|Privacy Policy|FAQ|Log in|Archive of', '', path, flags=re.IGNORECASE)
        
        # Remove newlines and extra whitespace
        path = re.sub(r'\s+', ' ', path).strip()
        
        # Extract just the category name if possible
        # Look for common category patterns
        category_match = re.search(r'(Advanced Topics|Algebra|Calculus|Geometry|General|Team|Guts|Oral|Power)', path)
        if category_match:
            path = category_match.group(1)
        
        # Remove any remaining special characters
        path = re.sub(r'[^\w\s-]', '', path)
        
        # Replace spaces with underscores and convert to lowercase
        path = path.replace(' ', '_').lower()
        
        # Limit path length
        path = path[:50]  # Limit to 50 characters
        
        return path

    def parse_tournament_problems(self, tournament_html: str) -> List[Dict[str, str]]:
        """Parse problem and solution links from tournament HTML."""
        soup = BeautifulSoup(tournament_html, 'html.parser')
        problems = []
        
        # Find all links that end in .pdf
        for link in soup.find_all('a', href=lambda href: href and href.endswith('.pdf')):
            url = link.get('href')
            if not url:
                continue
            
            # Get the parent elements to determine the category
            parents = [p.get_text().strip() for p in link.parents if p.get_text().strip()]
            category = parents[-1] if parents else 'unknown'
            
            # Clean up the category name
            category = self.clean_path(category)
            
            # Determine if this is a problem or solution file
            is_solution = 'solution' in url.lower()
            
            problems.append({
                'url': url,
                'category': category,
                'type': 'solutions' if is_solution else 'problems'
            })
        
        return problems

    def download_tournament_problems(self, tournament_id: int, tournament_html: str, year: int, tournament_type: str) -> None:
        """Download all problems and solutions for a tournament."""
        problems = self.parse_tournament_problems(tournament_html)
        
        for problem in problems:
            # Create the directory path
            dir_path = os.path.join(
                self.raw_data_dir,
                'pdfs',
                tournament_type,
                str(year),
                problem['category']
            )
            
            # Create the file path
            file_path = os.path.join(dir_path, f"{problem['type']}.pdf")
            
            # Download the PDF
            self.download_pdf(problem['url'], file_path)

    def save_tournaments(self, tournaments: List[Dict]):
        if not tournaments:
            return
        
        output_file = os.path.join(self.raw_data_dir, "tournaments.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'download_date': datetime.now().isoformat(),
                'tournaments': tournaments
            }, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved {len(tournaments)} tournaments to {output_file}")

    def process_tournaments(self, tournaments: List[Dict]):
        """Process and download all tournaments."""
        processed_tournaments = []
        for tournament in tournaments:
            logger.info(f"Downloading {tournament['type']} {tournament['year']} tournament...")
            
            # Download tournament page
            html_content = self.download_page(tournament['url'])
            if not html_content:
                continue
            
            # Save raw tournament HTML for debugging
            tournament_id = re.search(r'/archive/(\d+)', tournament['url'])
            raw_file = None
            if tournament_id:
                raw_file = os.path.join(self.raw_data_dir, f"tournament_{tournament_id.group(1)}.html")
                with open(raw_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                logger.info(f"Saved raw tournament HTML to {raw_file}")
            
            # Download problems and solutions
            self.download_tournament_problems(
                tournament_id=int(tournament_id.group(1)) if tournament_id else 0,
                tournament_html=html_content,
                year=tournament['year'],
                tournament_type=tournament['type'].lower()
            )
            
            processed_tournaments.append({
                'year': tournament['year'],
                'type': tournament['type'],
                'url': tournament['url'],
                'raw_html_file': raw_file
            })
        
        # Save tournament metadata
        output_file = os.path.join(self.raw_data_dir, 'tournaments.json')
        with open(output_file, 'w') as f:
            json.dump(processed_tournaments, f, indent=2)
        logger.info(f"Saved {len(processed_tournaments)} tournaments to {output_file}")
        logger.info("Processing completed")

    def run(self):
        """Run the downloader."""
        # Create output directories
        os.makedirs(self.raw_data_dir, exist_ok=True)
        os.makedirs(os.path.join(self.raw_data_dir, 'pdfs'), exist_ok=True)
        
        # Get list of tournaments
        html_content = self.download_page(self.archive_url)
        if not html_content:
            logger.error("Failed to get tournament list")
            return
        
        # Parse tournament links
        tournaments = self.parse_tournament_links(html_content)
        logger.info(f"Found {len(tournaments)} tournaments")
        
        # Process tournaments
        self.process_tournaments(tournaments)

def main():
    downloader = HMMTProblemDownloader()
    downloader.run()

if __name__ == "__main__":
    main() 