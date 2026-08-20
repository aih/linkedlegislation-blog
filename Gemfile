# frozen_string_literal: true

source "https://rubygems.org"

# This site is built here and deployed to S3/CloudFront, not by GitHub Pages,
# so it is not bound to the gem versions the github-pages gem pins. That gem
# held Jekyll at 3.9.2 and pulled in a large dependency tree that does not
# build on Ruby 3.4.
gem "jekyll", "~> 4.4"

# _config.yml sets markdown: kramdown with input: GFM. Jekyll 4 does not bundle
# the GFM parser.
gem "kramdown-parser-gfm", "~> 1.1"

group :jekyll_plugins do
  gem "jekyll-archives", "~> 2.3"
  gem "jekyll-paginate", "~> 1.1"
  gem "jekyll-redirect-from", "~> 0.16"
  gem "jekyll-remote-theme", "~> 0.4"
  gem "jekyll-sitemap", "~> 1.4"
end

gem "webrick", "~> 1.9"
