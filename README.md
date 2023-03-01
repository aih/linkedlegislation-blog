# Blog for LinkedLegislation.com

This is the content for blog.linkedlegislation.com. This was originally a Blogger (Google) blog, and I've migrated it to Jekyll hosted on GitHub Pages. The blog can be edited directly in the `_drafts` folder, and then moved to the `_posts` folder when it's ready to be published. It may also be edited using prose.io, a web-based editor that supports markdown. 

The blog is built using the [Beautiful Jekyll](https://beautifuljekyll.com/) theme. Details of how to add content and customize the theme can be found in the [README](https://github.com/daattali/beautiful-jekyll/blob/master/README.md) for that project.

## Installation and Local Development

As a [Jekyll site](https://jekyllrb.com/docs/usage/), this blog can be run locally for development and testing. Follow [the instructions](https://jekyllrb.com/docs/) for installing requirements and serving locally. In brief:

1. Install Ruby and Ruby gems (I found [this guide](https://www.moncefbelyamani.com/how-to-install-xcode-homebrew-git-rvm-ruby-on-ma) helpful on Mac).
2. Install Jekyll and Bundler: `gem install jekyll bundler`
3. Within this directory, run `bundle install` to install dependencies.
4. Build and serve the site: `bundle exec jekyll serve`
5. Browse on `http://localhost:4000`

## Development and automatic build with GH Actions

This blog is automatically built and deployed to GitHub Pages using GitHub Actions. The workflow is defined in `.github/workflows/jekyll.yml`. The workflow is triggered on any push to the `main` branch. It builds the site and deploys it to the `blog` branch (which is the equivalent of `gh-pages` for this site). The site is then available at `https://aih.github.io/blog` and `blog.linkedlegislation.com`.