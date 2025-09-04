# GEMINI.md

This file provides guidance to Gemini CLI when working with
code in this repository.

## Project Overview

This is Maciej Bliziński's personal website and music portfolio, built with Hugo
static site generator. The site showcases music productions, performances, press
materials, and includes a blog with posts dating back to 2003.

## Key Technologies

- **Hugo**: v0.147.2 (extended version) - Static site generator
- **Theme**: hugo-split-theme - Custom split-screen layout
- **Content**: Markdown files with TOML front matter
- **Deployment**: Shell script-based rsync deployment

## Essential Commands

### Development
```bash
# Run local development server with live reload and drafts
./util/deploy.sh dev
```

### Building
```bash
# Build production site
hugo --cleanDestinationDir

# Build with drafts included
hugo --cleanDestinationDir -D
```

### Deployment
```bash
# Deploy to production (blizin.ski)
./util/deploy.sh deploy

# Deploy preview with drafts (requires private_cfg.sh)
./util/deploy.sh preview
```

## Architecture & Structure

### Content Organization
- `/content/` - All site content in Markdown
  - `_index.md` - Homepage content
  - `bio.md`, `performances.md`, `photos.md`, `press.md` - EPK pages
  - `/jogger/` - Blog posts (hundreds of entries)
  - `/music/` - Music-related content and subpages

### Data Files
- `/data/performances/` - Performance data in TOML format
- `/data/months.yaml` - Month name translations

### Custom Components
- `/layouts/shortcodes/` - Custom shortcodes for embedding:
  - `bandcamp.html` - Bandcamp player embeds
  - `soundcloud.html` - SoundCloud embeds
  - `youtube.html` - YouTube video embeds

### Configuration
- `config.toml` - Main Hugo configuration with:
  - Site metadata and social links
  - Navigation structure
  - Image processing settings
  - Permalink patterns for blog posts

### Deployment Notes
- Production deploys to: `atemoia.blizinski.pl:www/blizin.ski`
- Preview deployment requires `private_cfg.sh` with PREVIEW_DEST and PREVIEW_URL
- Files are deployed via rsync with proper permissions (755 for dirs, 644 for files)

## Important Patterns

1. **Blog Post URLs**: Follow pattern `/jogger/YYYY/filename/`
2. **Performance Data**: Stored as TOML files in `/data/performances/`
3. **Image Optimization**: Large images should be compressed using ImageMagick:
   ```bash
   magick <name>-big.jpg -interlace jpeg -quality 35 <name>.jpg
   ```
4. **Draft Content**: Use `-D` flag with Hugo to include draft posts
