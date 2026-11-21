# Sunny Crumble Bakery

A responsive, static bakery website with no app dependencies or build step. The small illustrations are local SVGs, so the site does not need a CMS, server, or external image service.

## Run it locally

Open `index.html` in a browser, or start a local server from the project directory:

```powershell
python -m http.server 8000
```

Then visit `http://localhost:8000`.

Run the site checks with:

```powershell
python -m unittest discover -s tests -v
```

## Publish to GitHub Pages

The workflow scans the full Git history for secrets before testing or publishing. It deploys from `main` to GitHub Pages using GitHub's OIDC flow; it does not need a stored deployment token or application secret. GitHub Actions are pinned to full commit SHAs, the Gitleaks scanner is pinned by image digest, and the site has no third-party package dependencies.

One-time repository setup:

1. In **Settings → Pages**, set the build and deployment source to **GitHub Actions**.
2. In **Settings → Environments**, create an environment named `production`. Add a named person as a required reviewer and prevent self-review if the repository plan offers that option.
3. In **Settings → Actions → General**, set the default workflow token permission to **read repository contents**. The deploy job requests only `pages: write` and `id-token: write` in addition to read access.
4. Protect `main` with a ruleset or branch protection rule: require pull requests, require the **Site checks** status check, and block direct pushes and force pushes.
5. Open a pull request and confirm the secret scan and site checks pass. After a human merges it, the production deployment pauses for the required environment reviewer. The deployment run and approval are recorded in GitHub Actions.

These settings are enforced by GitHub, not by files in this repository. Do not treat production as protected until the required reviewer and `main` branch rules have been configured and tested.

## Before launch

The website is a design starter. Add the real address, opening hours, ordering/contact details, and any verified product, ingredient, or dietary information before publishing it for customers. The current menu descriptions are examples; availability and allergen details should be confirmed with the bakery.

## Milestone 1 evidence

The workflows and this site provide a starting point for the static-site track in the supplied project brief. A completed milestone still needs a real backlog ticket, an agent-authored pull request, a fresh-context agent review, a human production approval, and an audit trail. Do not claim those steps happened based on this scaffold alone; capture the actual run, decisions, and timestamps for the video and one-page PDF.
