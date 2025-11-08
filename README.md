Mosaic Web — Cloudways GitHub Auto Deploy

**Need the full infrastructure and design overview?** See `docs/mosaicweb-overview.md` for hosting, deployment, and front-end architecture details curated for design partners.

Quick start
- Add `gitautodeploy.php` to your app (already in repo root).
- If your Cloudways UI shows Environment Variables, set:
  - `CLOUDWAYS_EMAIL`, `CLOUDWAYS_API_KEY`
  - `CLOUDWAYS_SERVER_ID`, `CLOUDWAYS_APP_ID`
  - `CLOUDWAYS_BRANCH` (e.g., `main`)
  - `GITHUB_WEBHOOK_SECRET` (same secret you set in GitHub)
- If not, use local config instead:
  - Copy `config.sample.php` to `config.php` and fill values.
  - Optionally create a `.env` file with `KEY=VALUE` lines.
- In GitHub repo settings → Webhooks, add a webhook:
  - Payload URL: `https://your-app-url.com/gitautodeploy.php`
  - Content type: `application/json`
  - Secret: same as `GITHUB_WEBHOOK_SECRET`
  - Events: “Just the push event”
- Optional URL overrides: `?server_id=...&app_id=...&branch_name=...&git_url=...`

What it does
- Verifies GitHub HMAC signature (X-Hub-Signature-256).
- Ensures event is a push to the configured branch.
- Calls Cloudways API to trigger a Git pull for your app.

Notes
- Keep credentials out of the URL. Prefer environment variables.
- If Cloudways doesn’t offer env vars for your app type, use `config.php` (gitignored) or `.env`.
- If your Cloudways setup requires `git_url` for pulls, add it to env or the URL.
- If deployment doesn’t trigger, check Cloudways Activity Log and webhook deliveries in GitHub.

## PST to EML Converter

This repository now includes a Python utility for exporting Outlook `.pst` archives to
individual `.eml` files.

Quick start:
- Install the dependency: `python3 -m pip install -r requirements.txt`
- Convert a PST: `python3 -m pst_to_eml.cli path/to/archive.pst -o output/dir`
- Use the GUI: `python3 -m pst_to_eml.gui`

See `pst_to_eml/README.md` for detailed usage notes, options, and troubleshooting tips.
