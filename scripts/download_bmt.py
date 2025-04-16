import os
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import urllib3
import socket
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def create_dirs():
    base_dir = 'data_sources/bmt'
    os.makedirs(base_dir, exist_ok=True)
    return base_dir

def get_archive_links():
    url = "https://berkeley.mt/archives/"
    print(f"Attempting to connect to {url}")
    try:
        # Try to resolve the hostname first
        try:
            ip = socket.gethostbyname('berkeley.mt')
            print(f"Successfully resolved berkeley.mt to IP: {ip}")
        except socket.gaierror as e:
            print(f"Failed to resolve hostname berkeley.mt: {e}")
            return []

        response = requests.get(url, verify=False, timeout=10)
        response.raise_for_status()
        print(f"Successfully connected to {url}")
        print(f"Response status code: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f"Page title: {soup.title.string if soup.title else 'No title found'}")
        
        links = []
        for link in soup.find_all('a'):
            href = link.get('href')
            text = link.get_text().strip()
            if href and ('BMT' in text or 'BmMT' in text) and 'Archive' in text:
                year = re.search(r'(\d{4})', text)
                if year and 2020 <= int(year.group(1)) <= 2024:  # Only process 2020-2024
                    links.append({
                        'year': year.group(1),
                        'type': 'BMT' if text.startswith('BMT') else 'BmMT',
                        'url': urljoin(url, href)
                    })
        print(f"Found {len(links)} archive links for years 2020-2024")
        return links
    except requests.exceptions.RequestException as e:
        print(f"Failed to get archive links: {str(e)}")
        if hasattr(e, 'response'):
            print(f"Response status code: {e.response.status_code}")
            print(f"Response headers: {e.response.headers}")
        return []

def download_file(url, filename, downloaded_files):
    if filename in downloaded_files:
        print(f"Skipping already downloaded file: {filename}")
        return True
    
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        
        # Check if it's actually a PDF
        content_type = response.headers.get('content-type', '').lower()
        if 'pdf' not in content_type and not url.lower().endswith('.pdf'):
            print(f"Skipping non-PDF file: {filename}")
            return False
            
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Successfully downloaded {filename}")
        downloaded_files.add(filename)
        return True
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {filename}: {str(e)}")
        return False

def get_pdf_links(archive_url):
    try:
        response = requests.get(archive_url, verify=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        pdf_links = []
        seen_urls = set()  # To prevent duplicate downloads
        
        for link in soup.find_all('a'):
            href = link.get('href', '').strip()
            if not href or not href.endswith('.pdf'):
                continue
                
            url = urljoin(archive_url, href)
            if url in seen_urls:
                continue
                
            seen_urls.add(url)
            
            # Try to identify the round from the filename or link text
            link_text = link.get_text().strip().lower()
            filename = os.path.basename(href).lower()
            
            # Common round identifiers
            rounds = ['individual', 'team', 'power', 'general', 'round1', 'round2', 'round3', 
                     'round_1', 'round_2', 'round_3', 'r1', 'r2', 'r3']
            
            round_name = None
            for r in rounds:
                if r in filename or r in link_text:
                    round_name = r
                    break
            
            if 'problem' in filename or 'problem' in link_text:
                pdf_links.append(('problems' if not round_name else f"problems_{round_name}", url))
            elif 'solution' in filename or 'solution' in link_text:
                pdf_links.append(('solutions' if not round_name else f"solutions_{round_name}", url))
            else:
                # If we can't determine if it's problems or solutions, download it anyway
                pdf_links.append(('other', url))
                
        return pdf_links
    except requests.exceptions.RequestException as e:
        print(f"Failed to get PDF links from {archive_url}: {str(e)}")
        return []

def main():
    base_dir = create_dirs()
    archive_links = get_archive_links()
    
    if not archive_links:
        print("No archive links found!")
        return
    
    downloaded_files = set()
    
    for archive in archive_links:
        year = archive['year']
        comp_type = archive['type']
        
        # Create year directory
        year_dir = os.path.join(base_dir, year)
        os.makedirs(year_dir, exist_ok=True)
        
        print(f"\nProcessing {comp_type} {year}:")
        pdf_links = get_pdf_links(archive['url'])
        
        if not pdf_links:
            print(f"No PDF links found for {comp_type} {year}")
            continue
            
        print(f"Found {len(pdf_links)} PDF files")
        
        for pdf_type, pdf_url in pdf_links:
            base_filename = f"{comp_type}_{year}_{pdf_type}.pdf"
            full_path = os.path.join(year_dir, base_filename)
            download_file(pdf_url, full_path, downloaded_files)

if __name__ == "__main__":
    main() 