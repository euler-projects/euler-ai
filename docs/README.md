# Euler AI Documentation Site

This directory contains the Jekyll-based documentation site for Euler AI, hosted on GitHub Pages.

## Prerequisites

### macOS

```bash
brew install ruby
export PATH="/opt/homebrew/opt/ruby/bin:$PATH"  # Add to ~/.zshrc
```

### Linux (Debian/Ubuntu)

```bash
sudo apt install ruby-full build-essential
```

### Linux (Fedora)

```bash
sudo dnf install ruby ruby-devel
```

### Linux (RHEL/CentOS)

```bash
sudo yum install ruby ruby-devel
```

### Linux (Arch)

```bash
sudo pacman -S ruby base-devel
```

## Local Development

### Install Dependencies

```bash
cd docs
bundle config set --local path 'vendor/bundle'
bundle install
```

This installs gems locally to `vendor/bundle/`, keeping dependencies isolated per project.

### Start Development Server

```bash
bundle exec jekyll serve
```

The site will be available at `http://localhost:4000`. Jekyll supports hot reload, so changes will be reflected automatically.

## Directory Structure

```
docs/
├── _includes/       # Reusable HTML partials (header, footer)
├── _layouts/        # Page layout templates
├── _posts/          # Blog posts (YYYY-MM-DD-title.md)
├── _site/           # Generated site (do not edit)
├── assets/
│   ├── css/         # Stylesheets
│   └── js/          # JavaScript files
├── _config.yml      # Jekyll configuration
├── index.html       # Homepage
└── search.json      # Search index data
```

## Creating Content

### Adding a New Post

Create a new file in `_posts/` with the naming convention:

```
YYYY-MM-DD-your-post-title.md
```

Example front matter:

```yaml
---
layout: post
title: "Your Post Title"
date: 2026-03-30
---

Your content here...
```

### Adding a New Page

Create a new `.html` or `.md` file in the root directory with front matter:

```yaml
---
layout: default
title: "Page Title"
---

Your page content...
```

## Deployment

The site is automatically deployed to GitHub Pages when changes are pushed to the main branch. The generated `_site/` directory is ignored by git.
