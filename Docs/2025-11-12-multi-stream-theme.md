# Multi-Stream Hugo Theme Design

**Date**: 2025-11-12
**Status**: Approved - Ready for Implementation
**Branch**: `multi-stream-theme`

## Objective

Replace the current hugo-split-theme (designed for single-page sites) with a new custom theme that properly supports a multi-page, multi-stream website serving three distinct content areas:

1. **Jogger** - Personal blog (171 posts, legacy content from 2003+)
2. **Music** - Music releases, productions, and updates
3. **Apps** - Two iOS apps (Time Feel and Task Compass) with their own update streams

The new theme must preserve all existing URLs and redirects while providing a responsive, clean design that uses existing assets (background photo, styling cues).

## Background

### Current Site Structure
- **Homepage**: Split-screen single page with hero image and navigation links
- **Content sections**:
  - `/jogger/` - 171 blog posts with permalink pattern `/jogger/:year/:contentbasename/`
  - `/music/` - Music production portfolio
  - `/time-feel/` - App landing page with support pages
  - `/task-compass/` - App landing page with support/philosophy/FAQ pages
  - EPK pages: `/bio/`, `/photos/`, `/press/`, `/performances/`

### URL Preservation Requirements
- 78 files contain `aliases:` redirects that must be preserved
- Key redirects: `/bio/*` pages redirect to root-level pages
- Jogger posts have various redirect patterns from historical blog migrations
- Permalink patterns defined in config.toml must be maintained

### Current Assets
- Background image: `static/images/background.jpg` (hero photo of owner)
- Logo: `static/images/automaciej-logo.jpg`
- Favicon: `static/images/favicon.png`

## Design Ideas

### Architecture: Three-Stream Content Model

**Core concept**: Dual-column homepage (music/apps split) on desktop, with per-section streams on section pages.

#### Content Types
1. **Jogger posts** (type: `jogger`)
   - Legacy blog posts in Polish
   - Existing permalink structure preserved
   - **NOT shown on homepage** - only accessible via `/jogger/` section
   - Reasoning: Language separation (Polish content separate from English)

2. **Music productions** (data-driven)
   - **Data format**: TOML files in `/data/music/`
   - Each production has: title, artist, optional album/EP, date, role, credits, description, links
   - Links support: Bandcamp (album/track), YouTube, Instagram, SoundCloud
   - Rendered via custom template at `/music/`
   - **NOT post-based** - uses Hugo data files for structured information
   - Will appear in homepage music column (future implementation)

3. **App posts** (type: `apps`)
   - Development updates for Time Feel and Task Compass
   - Front matter includes `app: timefeel` or `app: taskcompass`
   - Will appear in homepage right column (desktop) or bottom (mobile)
   - Per-app streams at `/time-feel/posts/` and `/task-compass/posts/`
   - App landing pages retained at `/time-feel/` and `/task-compass/`

#### Stream Views
- **Homepage**: Two-column layout (desktop) / stacked (mobile)
  - Left/Top: Music posts (reverse-chronological)
  - Right/Bottom: App posts (reverse-chronological)
  - Jogger posts NOT included (language separation)
- **Section pages**:
  - `/jogger/` - List of jogger posts only (Polish content)
  - `/music/` - Stream-first: latest music post, then link to all posts, then portfolio
  - `/time-feel/posts/` - Time Feel posts only
  - `/task-compass/posts/` - Task Compass posts only

### Layout Structure

#### Homepage Layout (Desktop)
```
+------------------------------------------+
|  Site Header/Nav                         |
+------------------------------------------+
|  Condensed Hero                          |
|  (Photo + name + tagline)                |
+------------------------------------------+
|  Music Stream   |   Apps Stream          |
|  (Left column)  |   (Right column)       |
|  - Latest posts |   - Latest posts       |
|  - Reverse chr. |   - Reverse chr.       |
|  - Paginated    |   - Paginated          |
+------------------------------------------+
|  Footer                                  |
+------------------------------------------+
```

#### Homepage Layout (Mobile/Narrow)
```
+------------------------+
|  Site Header/Nav       |
+------------------------+
|  Condensed Hero        |
+------------------------+
|  Music Stream          |
|  (Top, full width)     |
+------------------------+
|  Apps Stream           |
|  (Bottom, full width)  |
+------------------------+
|  Footer                |
+------------------------+
```

#### Section Page Layout (e.g., `/music/`)
```
+------------------------+
|  Site Header/Nav       |
+------------------------+
|  Section Hero          |
|  (section-specific)    |
+------------------------+
|  Section Stream        |
|  (filtered by section) |
+------------------------+
|  Footer                |
+------------------------+
```

#### Single Post Layout
```
+------------------------+
|  Site Header/Nav       |
+------------------------+
|  Article Content       |
|  (full width, readable)|
+------------------------+
|  Footer                |
+------------------------+
```

### Navigation Structure
```
Maciej Bliziński (home)
├── Jogger (blog)
├── Music
│   └── Updates
├── Apps
│   ├── Time Feel
│   │   └── Updates
│   └── Task Compass
│       └── Updates
└── About/EPK
    ├── Bio
    ├── Photos
    └── Press
```

### Responsive Design
- **Mobile-first approach**
- **Breakpoints**:
  - Mobile: < 768px (single column)
  - Tablet: 768px - 1024px (adaptive layout)
  - Desktop: > 1024px (full layout with optional sidebar)
- **Hero image**: Responsive with appropriate cropping/sizing
- **Typography**: Readable on all devices (min 16px base font size)

### Visual Design
- **Fresh start** - Not inheriting from split theme
- **Typography**: Sans-serif font (system font stack for performance)
- **Color scheme**: Automatic day/night mode based on device preference
  - Light mode (daytime): White/light gray backgrounds, dark text
  - Dark mode (nighttime): Dark backgrounds, light text
  - Uses `prefers-color-scheme` media query
- **Apple-inspired aesthetic**:
  - Rounded corners on cards and UI elements
  - Generous white space
  - Clean, minimal design
  - Subtle shadows/borders
- **Hero**: Condensed section with background.jpg, name, and tagline
- **Cards**: Rounded corners, subtle shadows, content-type visual distinction
- **Responsive**: Mobile-first with graceful desktop enhancement

## Implementation Plan

### Stage 0: Architecture Analysis
- Review Hugo theme structure and templating system
- Identify template hierarchy needs for three content types
- Plan taxonomy structure for content organization
- Define front matter schema for new content types

### Stage 1: Theme Scaffolding
- Create new theme directory: `themes/multi-stream/`
- Set up basic directory structure (layouts, static, assets)
- Create minimal base template with header/footer
- Update config.toml to use new theme
- Verify site builds without errors

### Stage 2: Homepage Dual-Column Stream Implementation
- Create homepage template with two-column layout (desktop)
- Implement stream filtering: music posts in left, app posts in right
- Exclude jogger posts from homepage entirely
- Add responsive stacking for mobile (music top, apps bottom)
- Test with existing content

### Stage 3: Section Layouts
- Create section templates for `/jogger/`, `/music/`, app pages
- Implement section-specific stream filtering
- Preserve existing static page content (app landing pages)
- Test navigation between sections

### Stage 4: Single Post Layout
- Create single.html template for individual posts
- Implement proper typography and reading experience
- Add metadata display (date, tags, etc.)
- Test with sample content from each type

### Stage 5: Navigation & Header
- Implement site navigation menu
- Mobile-responsive hamburger menu
- Active state indication for current section
- Test on all breakpoints

### Stage 6: Visual Design & Styling
- Implement CSS framework or custom styles
- Apply responsive typography
- Style stream cards with content-type differentiation
- Integrate hero image responsively
- Test across devices

### Stage 7: Content Organization Setup
- Set up Hugo content structure for music/apps sections
- Document front matter schema for new content types
- Verify existing content displays correctly
- No sample content needed - using existing content

### Stage 8: URL Preservation & Testing
- Verify all existing permalinks still work
- Test all 78 aliases/redirects
- Generate sitemap and verify structure
- Test RSS feed generation

### Stage 9: Final Polish
- Optimize images and assets
- Add meta tags for SEO/social sharing
- Test accessibility (WCAG basics)
- Cross-browser testing

### Stage 10: Deployment
- Final testing in production-like environment
- Update deployment scripts if needed
- Deploy to production
- Verify all URLs in production

## Testing Strategy

### Unit-Level Testing
- Each template renders correctly with sample data
- Filtering logic correctly segregates content types
- Pagination works across all stream views

### Integration Testing
- Navigation flows work correctly between all sections
- Existing content displays properly in new layouts
- All redirects work (test sample from each redirect pattern)

### Manual Testing
- Visual testing on multiple devices (mobile, tablet, desktop)
- Cross-browser testing (Chrome, Safari, Firefox)
- Reading experience test (typography, spacing, readability)
- Accessibility check (keyboard navigation, screen reader basics)

### URL Preservation Testing
```bash
# Generate list of all existing URLs from current site
hugo --baseURL="https://blizin.ski" && grep -r "permalink:" public/ > old-urls.txt

# After implementation, generate new URL list
hugo --baseURL="https://blizin.ski" && grep -r "permalink:" public/ > new-urls.txt

# Compare to ensure no URLs lost
diff old-urls.txt new-urls.txt
```

## Implementation Log

**[2025-11-12T13:30+00:00] Design Document Created**
- Analyzed existing site structure (171 jogger posts, 2 app sections, music section)
- Identified 78 files with alias redirects requiring preservation
- Documented three-stream architecture approach
- Created initial 10-stage implementation plan

**[2025-11-12T14:15+00:00] Stakeholder Review - Design Approved with Modifications**
- Homepage: Condensed hero section approved
- Content separation: Jogger (Polish) excluded from homepage, only music/apps shown
- Layout: Two-column desktop (music left, apps right), stacked mobile (music top, apps bottom)
- URL structure: Changed from `/updates/` to `/posts/` for app content
- Visual design: Fresh start with sans-serif, day/night auto mode, Apple-inspired aesthetic
- Content: Use existing content, no sample posts needed
- Music section: Stream-first approach (latest post, then all posts link, then portfolio)
- RSS: Single master feed (Hugo default behavior)

**[2025-11-12T15:30+00:00] Music Data Structure Implemented**
- Shifted music from post-based to data-driven architecture
- Created `/data/music/` directory with TOML files for each production
- Data schema includes: title, artist, album (optional), date, role, credits, description, links
- Supported link types: Bandcamp (album/track), YouTube, Instagram, SoundCloud
- Created 13 TOML files from existing music page content (2000-2025)
- Built custom `/music/list.html` template to render from data
- Renders chronologically with embedded players and styled cards
- Site builds successfully with new data-driven music section

**[2025-11-12T18:00+00:00] Complete Theme Implementation and Polish**
- **Theme scaffolding complete**: Created themes/multi-stream/ with all base templates
- **Homepage implementation**:
  - Three-column desktop layout: Music | Apps | Bio
  - Responsive mobile layout with vertical stacking
  - Condensed hero section with circular photo (120px) and social icons
  - Hamburger menu for mobile navigation with JavaScript toggle
  - Section headers clickable with double chevron (») indicator
- **Music section enhancements**:
  - Data-driven display with individual rounded containers for each release
  - Credits converted to structured format: `[[credits]]` with name and roles array
  - Full band information added for Funksters tracks (Ocean, Burza)
  - New release added: "Talkative" by Gaia Marenghi (Nov 2025) with full credits
  - Homepage shows 3 newest releases on all screen sizes
  - Music page uses two-column masonry layout on desktop (flexbox-based)
  - Created reusable partial: `layouts/partials/music-card.html`
  - Images clickable, linking to specific production on music page via anchor IDs
  - Responsive images with 400px/800px variants for mobile optimization
- **Apps section**:
  - Data-driven structure: `/data/apps/` with TOML files
  - Fields: name, type, description, subsection, platforms[], testflight/appstore links
  - Task Compass: iOS/macOS, Time Feel: iOS
  - App posts support with filtering (excludeFromRSS respected)
  - Each app/post in separate rounded container
  - App titles clickable with chevron indicator
- **Bio section**:
  - Added background.jpg photo with responsive srcset
  - Full-width image on mobile (≤767px)
  - Created 400px/800px optimized variants
  - Content in rounded container
  - "More about me →" footer link
- **Visual design**:
  - Day/night color scheme with CSS custom properties
  - `prefers-color-scheme` media query for automatic switching
  - Apple-inspired aesthetic: rounded corners (12px), generous spacing
  - Individual containers for each content item (music, apps, posts)
  - Sans-serif system font stack
  - Fediverse symbol (⁂) for Mastodon in social links
- **Responsive breakpoints**:
  - ≤400px: Very narrow (hero stacks vertically, photo above text)
  - 401-767px: Narrow (single column, 3 music releases, mobile-optimized)
  - 768-1023px: Tablet (single column stacking)
  - ≥1024px: Desktop (three columns with masonry music layout)
- **Mobile optimizations**:
  - Hero photo moved above text on very narrow screens (≤400px)
  - Music preview uses horizontal layout with 80px thumbnails
  - Reduced header/hero padding on mobile
  - Section headers "Music" and "Apps" hidden on mobile, "Bio" shown
  - Bandcamp player properly wraps below content with flex-wrap
  - Image margins optimized (0.75rem spacing)
- **Technical improvements**:
  - Enabled unsafe HTML in config for responsive images
  - Created background-400px.jpg and background-800px.jpg variants
  - Music images use srcset for responsive loading
  - Zero top margin on main element for tighter layout
  - CSS masonry layout using flexbox instead of CSS Grid for better control
  - Proper TOML structure with image field before [[credits]] arrays
- **Content organization**:
  - Music data: 14 productions with full structured credits
  - Apps data: 2 apps with platform information
  - App posts: Support for post/updates under each app section
  - Privacy/support pages excluded from homepage via excludeFromRSS flag
- **Navigation**:
  - Clickable section headers with chevrons
  - "View all music productions →" and "More about me →" links
  - Hamburger menu for mobile with animated icon
- **Site builds**: All 228 pages, 192 aliases preserved, 0 errors

## Key Design Decisions (Resolved)

1. **Homepage Hero**: ✅ Condensed hero section with photo, name, and tagline

2. **Stream Content Mix**: ✅ Jogger (Polish) excluded from homepage. Two-column layout: music left/top, apps right/bottom

3. **App Organization**: ✅ App posts at `/time-feel/posts/` and `/task-compass/posts/`

4. **Navigation**: ✅ (Deferred to implementation - will propose structure based on content)

5. **Visual Styling**: ✅ Fresh start - sans-serif, day/night auto mode, Apple-inspired with rounded corners

6. **Content Creation**: ✅ Use existing content, no sample posts needed

7. **Static vs Stream**: ✅ Stream-first: latest music post highlighted, then link to all posts, then portfolio section

8. **RSS Feeds**: ✅ Single master RSS feed (Hugo default)

## Notes

- Hugo's content organization naturally supports this with section-based organization
- Taxonomies (tags) can work across all content types for cross-cutting themes
- The `excludeFromRSS` front matter already in use can be extended to `excludeFromStream` for fine-grained control
- Existing shortcodes (bandcamp, soundcloud, youtube) will work in new theme with proper CSS
