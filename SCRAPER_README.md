# Google Scholar Scraper

Automatically fetch and generate portfolio pages from your Google Scholar profile.

## Quick Start

```bash
# Activate virtual environment
source venv/bin/activate

# Run scraper to update publications
python3 scraper_gs_direct.py
```

## Features

✅ Fetches all publications from Google Scholar  
✅ Generates individual publication pages  
✅ Includes citation counts and metadata  
✅ Creates searchable publication index  
✅ Updates scholar_publications.json with latest data  

## Profile Configuration

**Scholar ID:** `v1y3XMUAAAAJ`  
**Profile URL:** https://scholar.google.com/citations?user=v1y3XMUAAAAJ

## How It Works

1. **Fetches** your Google Scholar profile page
2. **Parses** publication data (title, authors, citations, year)
3. **Generates** individual HTML pages for each publication
4. **Saves** metadata to `scholar_publications.json`
5. **Creates** publication directories in `/publication/`

## Output

- **Publication pages:** `/publication/{slug}/index.html`
- **Metadata:** `scholar_publications.json`
- **Total publications:** 11 (as of last run)

## Updating Publications

To refresh your publications from Google Scholar:

```bash
python3 scraper_gs_direct.py
git add publication/ scholar_publications.json
git commit -m "Update publications from Google Scholar"
git push origin main
```

## Requirements

- Python 3.x
- requests
- beautifulsoup4

Install with:
```bash
source venv/bin/activate
pip install requests beautifulsoup4
```

## Files

- `scraper_gs_direct.py` - Main scraper script
- `scraper_scholar.py` - Alternative scraper using scholarly library
- `scholar_publications.json` - Metadata of all publications
- `publication/` - Generated publication pages

## Notes

- The scraper respects Google Scholar's terms of service
- Each scrape request includes proper User-Agent headers
- Citation counts are updated automatically
- Run regularly to keep publications current

---

Last updated: 2026-05-03
