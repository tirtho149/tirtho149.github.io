#!/usr/bin/env python3
"""
Google Scholar Scraper for Tirtho Roy's Portfolio
Fetches publications from Google Scholar and generates portfolio pages
"""

import json
import os
from datetime import datetime
from scholarly import scholarly
import time

# Google Scholar ID for Tirtho Roy
SCHOLAR_ID = "v1y3XMUAAAAJ"
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLICATION_DIR = os.path.join(OUTPUT_DIR, "publication")

def fetch_publications():
    """Fetch publications from Google Scholar"""
    print(f"Fetching publications for Scholar ID: {SCHOLAR_ID}")

    try:
        author = scholarly.search_author_id(SCHOLAR_ID)
        scholarly.fill(author, sections=['basics', 'indices', 'counts'])

        publications = []

        # Get all publications
        for pub in author['publications']:
            scholarly.fill(pub)
            pub_data = {
                'title': pub.get('bib', {}).get('title', 'Untitled'),
                'authors': pub.get('bib', {}).get('author', 'Unknown'),
                'pub_year': pub.get('bib', {}).get('pub_year', ''),
                'venue': pub.get('bib', {}).get('venue', ''),
                'abstract': pub.get('bib', {}).get('abstract', ''),
                'url': pub.get('pub_url', ''),
                'scholar_url': pub.get('url_scholarbib', ''),
                'num_citations': pub.get('num_citations', 0),
            }
            publications.append(pub_data)
            print(f"✓ {pub_data['title']}")
            time.sleep(1)  # Be respectful to Google Scholar

        return author, publications

    except Exception as e:
        print(f"Error fetching from Google Scholar: {e}")
        print("Using fallback: Reading from local cache if available")
        return None, None

def generate_publication_html(pub, index):
    """Generate HTML for a publication"""
    title = pub['title']
    authors = pub['authors']
    venue = pub['venue']
    year = pub['pub_year']
    citations = pub['num_citations']
    url = pub['url']

    # Create slug from title
    slug = title.lower().replace(' ', '-')[:50].strip('-')

    html = f"""<!DOCTYPE html>
<html lang="en-us" >

<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />

  <meta name="generator" content="Wowchemy 5.3.0 for Hugo" />
  <meta name="author" content="Tirtho Roy" />
  <meta name="description" content="{pub['abstract'][:160] if pub['abstract'] else title}" />

  <link rel="canonical" href="https://tirtho149.github.io/publication/{slug}/" />

  <title>{title} | Tirtho Roy</title>

</head>

<body id="top">

<article class="pub">

<div class="article-container pt-3">
  <h1 class="pub-title">{title}</h1>

  <div class="pub-authors">
    <div class="author-list">
      {authors}
    </div>
  </div>

  <div class="pub-publication">
    {venue}, {year}
  </div>

  <div class="pub-abstract">
    <h3>Abstract</h3>
    <p>{pub['abstract'] if pub['abstract'] else 'No abstract available'}</p>
  </div>

  <div class="pub-links">
    {'<a class="btn btn-outline-primary my-2 mr-2" href="' + url + '" target="_blank" rel="noopener">Paper Link</a>' if url else ''}
    <a class="btn btn-outline-primary my-2 mr-2" href="https://scholar.google.com/citations?user={SCHOLAR_ID}" target="_blank" rel="noopener">View on Google Scholar</a>
  </div>

  <div class="pub-metrics">
    <span class="badge badge-light">{citations} citations</span>
  </div>

</div>

</article>

</body>
</html>"""

    return html, slug

def save_publications(publications):
    """Save publications to portfolio"""
    if not publications:
        print("No publications to save")
        return

    os.makedirs(PUBLICATION_DIR, exist_ok=True)

    publications_data = []

    for idx, pub in enumerate(publications):
        html, slug = generate_publication_html(pub, idx)

        # Create publication directory
        pub_dir = os.path.join(PUBLICATION_DIR, slug)
        os.makedirs(pub_dir, exist_ok=True)

        # Save HTML
        html_path = os.path.join(pub_dir, "index.html")
        with open(html_path, 'w') as f:
            f.write(html)

        print(f"✓ Saved: {pub_dir}/index.html")

        publications_data.append({
            'title': pub['title'],
            'slug': slug,
            'year': pub['pub_year'],
            'venue': pub['venue'],
            'citations': pub['num_citations']
        })

    # Save metadata
    metadata_path = os.path.join(OUTPUT_DIR, "scholar_publications.json")
    with open(metadata_path, 'w') as f:
        json.dump({
            'total': len(publications_data),
            'last_updated': datetime.now().isoformat(),
            'publications': publications_data
        }, f, indent=2)

    print(f"\n✓ Saved {len(publications_data)} publications")
    print(f"✓ Metadata saved to: {metadata_path}")

def main():
    """Main scraper function"""
    print("=" * 60)
    print("Google Scholar Scraper for Tirtho Roy's Portfolio")
    print("=" * 60)

    author, publications = fetch_publications()

    if author:
        print(f"\nAuthor: {author.get('name')}")
        print(f"Total Publications: {len(author.get('publications', []))}")
        print(f"Google Scholar URL: https://scholar.google.com/citations?user={SCHOLAR_ID}")
        print("\n" + "=" * 60)
        print("Generating Publication Pages...")
        print("=" * 60 + "\n")

        save_publications(publications)

        print("\n" + "=" * 60)
        print("✓ Scraping Complete!")
        print("=" * 60)
    else:
        print("Failed to fetch from Google Scholar")
        print("Please ensure you have internet access and the Scholar ID is correct")

if __name__ == "__main__":
    main()
