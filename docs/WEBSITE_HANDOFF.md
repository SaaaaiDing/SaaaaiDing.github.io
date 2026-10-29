# Website maintenance and handoff

Last updated: 29 October 2026.

## Current state

- Live website: https://saaaaiding.github.io/
- Repository: https://github.com/SaaaaiDing/SaaaaiDing.github.io
- Production branch: `master`.
- GitHub Pages source: **Deploy from a branch**, `master`, `/(root)` (reported as `legacy` by the API).
- Stack: Jekyll, Liquid templates, structured YAML data, plain CSS, original SVG illustrations. No frontend framework or client-side JavaScript is required.
- Latest website content change at this handoff: `8d640881ad5fae6534eff1957ad147ddfc98bcba`.
- Homepage heading: **Protein Design & Engineering**.
- Portrait: the owner's supplied `LinkedIn_headshot_small.jpg`, published as `static/saisai-ding.jpg`, 1254 × 1254 pixels. The original local file was left unchanged.
- Exactly three main research areas are retained.
- No downloadable CV is currently published.

The heading and portrait update passed the Jekyll build, internal resource checks, automated browser checks, GitHub Pages deployment, and live asset verification. Relevant runs:

- [Content validation](https://github.com/SaaaaiDing/SaaaaiDing.github.io/actions/runs/40950521244)
- [Pages deployment](https://github.com/SaaaaiDing/SaaaaiDing.github.io/actions/runs/40950520439)
- [Live website verification](https://github.com/SaaaaiDing/SaaaaiDing.github.io/actions/runs/40950521054)

## Start here next time

1. Inspect the working directory, applicable `AGENTS.md` files, Git status, remote URL, and current branch. Preserve unrelated work.
2. Confirm which directory is the website checkout. Reference materials belong outside it. Never initialize or stage the parent reference directory as the public website repository.
3. Fetch the current remote state. Do not assume an old local copy or the temporary `website-refresh` branch is current.
4. Read this file, `README.md`, and `docs/public-sources.md`.
5. Make the smallest necessary changes, review the complete diff, validate, and publish through the existing Pages configuration.

During this session, terminal commands failed before execution because of a sandbox temporary-directory permission error. Repository changes were therefore made through the connected GitHub tools. No local checkout was created or synchronized. The separate image-reading tool successfully read the new portrait. Do not infer from that success that the terminal or document readers are working.

## Where to edit

| Change | File |
| --- | --- |
| Name, current role, affiliation, advisor, introduction, public contact links | `_data/main_info.yaml` |
| Three research areas, status labels, descriptions, figures, paper/code links | `_data/research.yaml` |
| Selected publications and public software links | `_data/publications.yaml` |
| Education, industry background, research capabilities | `_data/experience.yaml` |
| Homepage heading and page sections | `index.html` |
| Shared navigation, metadata, footer, stylesheet reference | `_layouts/default.html` |
| Typography, colors, layout, responsive rules | `static/site.css` |
| Public portrait | `static/saisai-ding.jpg` |
| Conceptual research diagrams | `static/research-models.svg`, `static/research-enzymes.svg`, `static/research-sweet.svg` |
| Site URL, exclusions, Jekyll configuration | `_config.yml` |
| Build and browser validation | `.github/workflows/website.yml` |
| Live URL and asset verification | `.github/workflows/verify-live.yml` |

The data files use JSON syntax, which is valid YAML. Retain valid commas, quotation marks, brackets, and `null` values. Keep text in English and use plain text in data fields.

The owner prefers concise, factual language. Avoid promotional slogans. Keep **Protein Design & Engineering** unless the owner requests another heading.

## Updating the three research areas

### 1. Model Design and Agentic Tool Development

Edit the `models` entry in `_data/research.yaml`.

- Distinguish development of a method/model from application of existing models.
- ProChoreo currently links to a verified public preprint and public code repository.
- Do not infer journal publication from a local proof. Verify any new journal record before changing the status.
- Agentic development remains an ongoing direction described at a broad conceptual level. Do not publish internal architecture or implementation details.

### 2. Enzyme Engineering

Edit the `enzymes` entry.

- Describe molecular simulation and structure–function analysis in relation to enzyme behavior and engineering questions.
- The linked cold-active transglutaminase paper is a verified public collaboration.
- That publication does not establish that other collaborative results or local figures are public.
- Keep completed analyses separate from proposed engineering and experiments.
- Add a figure or code link only after verifying its public-release status.

### 3. Sweet Modulator Discovery

Edit the `sweet-modulators` entry.

- Keep the overview concise and non-confidential.
- The conceptual figure represents computational design → protein production → cellular evaluation → iterative refinement.
- It does not assert completion or experimental validation of every stage.
- Add results and links only when ready for public release; update status, caption, and supporting publication together.

Each research entry supports `status`, `summary`, `paragraphs`, `tags`, optional `figure`, `figure_alt`, `caption`, `paper_url`, `paper_label`, `code_url`, and `code_label`. Use `null` for unavailable links. The template hides them automatically.

## Publications and assets

Add a publication object to `_data/publications.yaml` with `year`, `title`, `authors`, `venue`, explicit `status`, optional `note`, `paper_url`, and optional `code_url`. Prefer DOI, publisher, preprint, and verified repository links.

For a new image, review its content and embedded metadata before placing it in `static/`. Add meaningful alternative text and an accurate caption. Conceptual illustrations must be identified as conceptual. Never fabricate measurements or reuse unpublished scientific figures.

When replacing the portrait, preserve the original reference image outside the checkout, publish only the approved image, and update the HTML width/height and CSS aspect ratio if its shape changes.

If a new published asset is intentionally added, update the allowlist in `scripts/check_site.py`. Do not loosen the allowlist to accommodate unreviewed files.

## Confidentiality and evidence

Permission to read references is not permission to publish them.

Do not commit local proposals, resumes, letters, correspondence, manuscript proofs, unpublished research figures, sequences, candidate identifiers, binding-site details, quantitative unpublished results, experimental conditions, internal agent design, or unpublished code. This applies to comments, SVG metadata, documentation, downloads, artifacts, and Git history.

The original local scientific documents and resumes were not read during this rebuild because the terminal was unavailable. The site is based on the owner's brief, the previous public website, and verified public sources listed in `docs/public-sources.md`. Additional biography and project details still require private source review.

Public information is not necessarily a verified personal contribution. Check authorship and contribution statements, and distinguish team findings from the owner's role.

Keep private review notes outside the public checkout. A future downloadable CV requires a separately reviewed public-safe version.

## Validation and publication

For a working local Ruby/Bundler environment:

```sh
git status --short --branch
bundle config set --local path vendor/bundle
bundle install
bundle exec jekyll build --strict_front_matter
python3 scripts/check_site.py
bundle exec jekyll serve --host 127.0.0.1
```

Preview at http://127.0.0.1:4000/. Inspect desktop and mobile layouts if an interactive browser is available.

Before committing, inspect `git diff`, `git diff --cached`, and each staged file. Stage explicit website paths only. Review generated output as well; an excluded file is still public if committed to Git.

The existing CI performs:

- Jekyll build in the GitHub Pages environment.
- Checks for missing internal links, anchors, images, duplicate IDs, unrendered Liquid, SVG/XML validity, and unexpected published files.
- Headless Chromium checks at 320, 390, 768, and 1440 pixels, including horizontal overflow, image decoding, navigation, keyboard access, automated accessibility, and 404 recovery.
- Screenshot artifacts under the `website-screenshots` artifact.
- Live homepage checks, byte-for-byte verification of all files in `static/`, and custom HTTP 404 verification.

Automated accessibility and layout checks do not replace a manual visual or assistive-technology review.

Push normally to `master` after review and successful validation. Do not force-push. The native **pages build and deployment** workflow publishes from the branch. Confirm that it succeeds and that **Verify live website** passes before reporting deployment complete.

`theme: null` intentionally disables the default Pages theme, which otherwise injects an extra stylesheet. Keep it. The obsolete `__deploy.sh` is disabled and must not be used for deployment.

## Remaining follow-up

- Restore terminal access and locate or create an appropriate isolated local checkout before local editing.
- Review local references privately before adding further biographical or scientific detail.
- Check publication status when adding a new article or replacing a preprint citation.
- Perform manual visual and accessibility review when interactive browser tooling is available.
- Never treat the presence of a file in the local reference directory as approval to publish it.
