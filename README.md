# Saisai Ding — academic website

Jekyll website for [saaaaiding.github.io](https://saaaaiding.github.io/), maintained in [SaaaaiDing/SaaaaiDing.github.io](https://github.com/SaaaaiDing/SaaaaiDing.github.io).

## Content

- `_data/main_info.yaml`: introduction, affiliation, advisor, public contact links.
- `_data/research.yaml`: the three research areas, statuses, descriptions, optional figures, and optional paper/code links.
- `_data/publications.yaml`: selected publications, publication status, DOI links, and public software.
- `_data/experience.yaml`: background and research capabilities.
- `index.html` and `_layouts/default.html`: page structure.
- `static/site.css`: responsive styling.
- `static/research-*.svg`: original conceptual illustrations.
- `static/saisai-ding.jpg`: the portrait previously used on the public website.

Data files use JSON syntax, which is valid YAML and supported by Jekyll. Keep fields as plain text. Use `null` for unavailable URLs; the template hides those links.

## Local preview and validation

Install Ruby and Bundler, then run from the website checkout:

```sh
bundle config set --local path vendor/bundle
bundle install
bundle exec jekyll build --strict_front_matter
python3 scripts/check_site.py
bundle exec jekyll serve --host 127.0.0.1
```

Open http://127.0.0.1:4000/. The automated browser check additionally uses Node.js, Playwright, and @axe-core/playwright. GitHub Actions installs those tools into the runner's temporary directory.

## Publication

The production branch is `master`. Preserve repository history and push normally; never force-push.

The `Validate website` workflow builds with the GitHub Pages Jekyll environment, checks rendered links and assets, and runs headless desktop/mobile and accessibility checks. It reports the current Pages source.

- For **Deploy from a branch**, use `master` and `/(root)`. GitHub's Pages build publishes the site.
- For **GitHub Actions**, the workflow deploys the validated artifact when a commit reaches `master`.
- If Pages is disabled, select a source in [repository Pages settings](https://github.com/SaaaaiDing/SaaaaiDing.github.io/settings/pages).

Check both the Actions run and the live site after pushing. A pushed commit is not proof of deployment. `__deploy.sh` now exits without uploading anything; the former external-server destination is no longer used.

## Updating each research area

1. **Model Design and Agentic Tool Development:** edit the `models` entry in `_data/research.yaml`. Link verified public articles/preprints and repositories. Distinguish method development from applications of existing software. Keep unpublished agentic work conceptual and marked ongoing.
2. **Enzyme Engineering:** edit the `enzymes` entry. Add results only when their publication or public release has been verified. Separate completed analysis from future engineering hypotheses. Replace the conceptual SVG only with an asset reviewed for public use.
3. **Sweet Modulator Discovery:** edit the `sweet-modulators` entry. Retain the ongoing label until public results support a more specific status. Add `paper_url`, `paper_label`, and `code_url` when available. Update the figure and caption together; do not imply planned experiments are completed.

Add papers to `_data/publications.yaml` with explicit `Published`, `Published online`, or `Preprint` status. Optional figures require a path, meaningful alternative text, and caption. Retain exactly three main research areas.

## Public content review

Only reviewed website assets belong here. Do not copy proposals, resumes, correspondence, proofs, unpublished figures, experimental records, or unpublished research code into this repository. Any downloadable CV must be a separately reviewed public version; none is supplied here.

Before committing, inspect `git diff`, `git diff --cached`, and every staged file, including comments and SVG metadata. Check generated `_site` files too. Build exclusions do not protect files committed to Git.

See [public source notes](docs/public-sources.md) for supporting sources and verification limits.

## Credits

This repository began with Martin Saveski's Jekyll personal website template. The current design retains Jekyll and structured content while replacing the layout and styling. The conceptual SVG diagrams are original illustrations, not experimental figures.
