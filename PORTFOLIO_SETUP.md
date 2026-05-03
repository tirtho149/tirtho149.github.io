# Portfolio Setup - Updated Content

## What's Been Created

I've created a complete content structure for your Wowchemy Hugo portfolio based on your CV. This includes:

### Author Profile
- **File**: `content/authors/admin/_index.md`
- Your bio, interests, education, social links, and research focus
- Positioned as an AI+X researcher specializing in computer vision, agriculture, healthcare, and finance

### Publications (6 entries)
1. **Federated Dental Imaging** - ODIN 2025 @ MICCAI (Privacy-preserving multi-modal imaging)
2. **Market Orientation & Startup Pitches** - JBIM & REU 2025 (LLM-based investor behavior analysis)
3. **Medical AI Safety** - ACM-BCB 2025 (Multi-agent evaluation framework)
4. **Vision-Language Agriculture** - WACV 2025 (VLMs for agricultural tasks)
5. **LlamaHealth** - ICERIE 2025 (Healthcare prediction with LLMs)
6. **Bioemu-1 Benchmarking** - AIChE 2025 (Protein structure prediction)

### Research Projects (4 entries)
1. **LLMs in Finance** - Market analysis and startup evaluation
2. **Medical AI Safety** - Ethical alignment and regulatory compliance
3. **Vision-Language Agriculture** - Crop monitoring and precision farming
4. **Chatbot Frontend** - UI/UX development for agricultural applications

### Blog/Posts
- **Awards & Recognition** - Dean's awards, George Washington Carver Prize, etc.

## Directory Structure

```
content/
├── authors/
│   └── admin/
│       └── _index.md              # Your main profile
├── publication/
│   ├── bioemu-protein-prediction/
│   ├── federated-dental-imaging/
│   ├── llamahealth-healthcare-prediction/
│   ├── market-orientation-startup-pitches/
│   ├── medical-ai-safety/
│   └── vision-language-agricultural-tasks/
├── project/
│   ├── chatbot-frontend-development/
│   ├── llm-finance-research/
│   ├── medical-ai-safety/
│   └── vision-language-agriculture/
└── post/
    └── awards-recognition/
```

## Next Steps to Deploy

### Option 1: Build with Hugo (Recommended)
If you have Hugo installed locally:

```bash
# Install Hugo (if not already installed)
brew install hugo  # macOS

# Build the site from content
hugo

# This generates the static HTML in the public/ directory
```

### Option 2: Use Netlify CMS
The `admin/config.yml` is configured for Netlify CMS. You can:
1. Connect your GitHub repo to Netlify
2. Enable Netlify CMS at `/admin`
3. Make edits through the web interface

### Option 3: Manual Updates
If you prefer, edit the markdown files directly and build locally or use CI/CD.

## Things to Add

To make your portfolio even more complete, consider:

1. **Featured Images**
   - Add `featured.png` or `featured.jpg` in each publication folder
   - Add `featured.png` in each project folder
   - Add profile photo as `avatar.jpg/png` in `content/authors/admin/`

2. **External Links**
   - Add DOI links to publications
   - Add GitHub repository links to projects
   - Add paper PDFs where available

3. **Additional Content**
   - Conference posters from your presentations
   - Teaching or mentoring experience
   - Skills/technical expertise section
   - Links to code repositories

4. **Update `index.html` or config**
   - Remove old placeholder content
   - Update site title and metadata to reflect your name
   - Update analytics tracking ID if needed

## Current Status

✅ Content structure created  
✅ Author profile with bio and interests  
✅ 6 publications catalogued  
✅ 4 research projects documented  
✅ Awards and honors listed  
⏳ Ready for Hugo build  

## Building and Deploying

Once you're ready to build:

```bash
# Verify content with local build
hugo -D

# Preview on localhost:1313
hugo server -D

# Build production site (clean, optimized output)
hugo

# Push changes to GitHub
git add content/
git commit -m "Update portfolio with latest research and CV information"
git push origin main
```

## Contact

If you need to update the content further:
- Edit markdown files in the `content/` directory
- Rebuild with `hugo` command
- Commit and push changes

All files follow Wowchemy/Hugo markdown format and are ready to be processed by the Hugo static site generator.
