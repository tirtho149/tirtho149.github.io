#!/usr/bin/env python3
"""
Direct Google Scholar HTML Scraper
Fetches publication data by parsing Google Scholar profile page
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
import time

SCHOLAR_ID = "v1y3XMUAAAAJ"
SCHOLAR_URL = f"https://scholar.google.com/citations?user={SCHOLAR_ID}&hl=en&oi=ao"
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLICATION_DIR = os.path.join(OUTPUT_DIR, "publication")

def fetch_scholar_profile():
    """Fetch Google Scholar profile page"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        print(f"Fetching: {SCHOLAR_URL}")
        response = requests.get(SCHOLAR_URL, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching Google Scholar: {e}")
        return None

def parse_publications(html):
    """Parse publications from HTML"""
    soup = BeautifulSoup(html, 'html.parser')
    publications = []

    # Find all publication rows
    pub_rows = soup.find_all('tr', class_='gsc_a_tr')

    print(f"Found {len(pub_rows)} publications\n")

    for row in pub_rows:
        try:
            # Extract title
            title_elem = row.find('a', class_='gsc_a_at')
            title = title_elem.text if title_elem else "Unknown"

            # Extract authors and year
            authors_elem = row.find('div', class_='gs_gray')
            authors_text = authors_elem.text if authors_elem else ""

            # Extract citation count
            cite_elem = row.find('a', class_='gsc_a_ac')
            citations = cite_elem.text if cite_elem else "0"

            # Extract year (usually at the end)
            year_elem = row.find_all('span', class_='gsc_a_h')
            year = year_elem[-1].text if year_elem else ""

            pub_data = {
                'title': title,
                'authors': authors_text,
                'citations': citations,
                'year': year,
                'url': title_elem.get('href', '') if title_elem else ''
            }

            publications.append(pub_data)
            print(f"✓ {title[:60]}... ({year}, {citations} citations)")

        except Exception as e:
            print(f"Error parsing publication: {e}")
            continue

    return publications

def generate_html_page(pub, slug):
    """Generate HTML page for a publication"""
    html = f"""<!DOCTYPE html>
<html lang="en-us">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />
  <meta name="generator" content="Wowchemy 5.3.0 for Hugo" />
  <meta name="author" content="Tirtho Roy" />
  <meta name="description" content="{pub['title']}" />
  <link rel="canonical" href="https://tirtho149.github.io/publication/{slug}/" />
  <title>{pub['title']} | Tirtho Roy</title>
  <link crossorigin="anonymous" href="/css/academic.min.css" rel="stylesheet">
</head>

<body id="top">
<div class="page-header">
  <nav class="navbar navbar-expand-lg navbar-light compensate-for-scrollbar" id="navbar-main">
    <div class="container-lg">
      <a class="navbar-brand" href="/">Tirtho Roy</a>
    </div>
  </nav>
</div>

<main class="page-content">
<div class="container-lg">

<article class="pub">
  <div class="pub-header">
    <h1 class="pub-title">{pub['title']}</h1>
  </div>

  <div class="article-container pt-3">
    <div class="row">
      <div class="col-md-1"></div>
      <div class="col-md-8">

        <div class="row align-items-center">
          <div class="col-md-8">
            <div class="pub-authors">
              {pub['authors']}
            </div>
            <span class="pub-publication">
              {pub['year']}
            </span>
          </div>
          <div class="col-md-4 text-right">
            <span class="pub-citations">
              <span class="badge badge-light">{pub['citations']} citations</span>
            </span>
          </div>
        </div>

        <div class="btn-links mb-3">
          {'<a class="btn btn-outline-primary my-2 mr-2" href="' + pub['url'] + '" target="_blank" rel="noopener">PDF</a>' if pub['url'] else ''}
          <a class="btn btn-outline-primary my-2 mr-2" href="https://scholar.google.com/citations?user={SCHOLAR_ID}" target="_blank" rel="noopener">
            <i class="ai ai-google-scholar"></i> Google Scholar
          </a>
        </div>

      </div>
    </div>
  </div>

</article>

</div>
</main>

<footer class="site-footer">
  <p class="powered-by">© 2026 Tirtho Roy · Powered by <a href="https://wowchemy.com" target="_blank" rel="noopener">Wowchemy</a></p>
</footer>

</body>
</html>"""
    return html

def save_publications(publications):
    """Save publications to portfolio"""
    if not publications:
        print("\\nNo publications to save")
        return

    os.makedirs(PUBLICATION_DIR, exist_ok=True)
    pub_list = []

    print(f"\\nGenerating publication pages...\\n")

    for pub in publications:
        # Create slug from title
        slug = pub['title'].lower()
        slug = ''.join(c if c.isalnum() or c == '-' else '-' for c in slug)
        slug = slug[:60].strip('-')

        # Generate HTML
        html = generate_html_page(pub, slug)

        # Create directory
        pub_dir = os.path.join(PUBLICATION_DIR, slug)
        os.makedirs(pub_dir, exist_ok=True)

        # Save HTML
        with open(os.path.join(pub_dir, "index.html"), 'w') as f:
            f.write(html)

        print(f"✓ {pub_dir}/index.html")

        pub_list.append({
            'title': pub['title'],
            'slug': slug,
            'year': pub['year'],
            'citations': pub['citations'],
            'authors': pub['authors']
        })

    # Save metadata
    with open(os.path.join(OUTPUT_DIR, "scholar_publications.json"), 'w') as f:
        json.dump({
            'total': len(pub_list),
            'last_updated': datetime.now().isoformat(),
            'scholar_id': SCHOLAR_ID,
            'publications': pub_list
        }, f, indent=2)

    print(f"\\n✓ Saved {len(pub_list)} publications")

def main():
    print("=" * 70)
    print("Google Scholar Profile Scraper - Tirtho Roy")
    print("=" * 70)

    html = fetch_scholar_profile()

    if html:
        publications = parse_publications(html)
        save_publications(publications)

        print("\\n" + "=" * 70)
        print("✓ Scraping Complete!")
        print("=" * 70)
    else:
        print("Failed to fetch Google Scholar profile")

if __name__ == "__main__":
    main()
