# Deployment Guide for mosaicpolicy.com

## Current Issue
The website is serving the wrong content ("MHP Brand Automation" instead of MOSAIC Health Policy website) because:
1. Wrong `index.html` file is on the server
2. `dashboard/` and `dashboard-new/` directories from another project exist on the server
3. GitHub Actions workflows are failing due to missing secrets

## Quick Fix: Manual Deployment

### Option 1: Use Git Pull via Cloudways API (Recommended)
This is the most reliable method and doesn't require file permissions:

1. **Set up GitHub Webhook** (if not already done):
   - Go to: https://github.com/kmulroy1972/mosaicweb/settings/hooks
   - Add webhook:
     - Payload URL: `https://mosaicpolicy.com/gitautodeploy.php`
     - Content type: `application/json`
     - Secret: (use the same secret from your `config.php` or `.env`)
     - Events: "Just the push event"

2. **Push to trigger deployment**:
   ```bash
   git push origin main
   ```
   This will automatically trigger `gitautodeploy.php` which uses Cloudways API to pull the latest code.

3. **Purge cache**:
   ```bash
   ssh cloudways-server "curl -I -X PURGE https://mosaicpolicy.com/"
   ```

### Option 2: Fix File Permissions and Use rsync
If you have SSH access, fix permissions first:

```bash
ssh cloudways-server "chmod -R 755 /home/1478529.cloudwaysapps.com/vhxvtajnbg/public_html/"
ssh cloudways-server "chown -R master_wcqkvzhaqv:master_wcqkvzhaqv /home/1478529.cloudwaysapps.com/vhxvtajnbg/public_html/"
```

Then deploy:
```bash
cd /Users/kylemulroy/mosaicweb
bash scripts/cloudways_push.sh
```

### Option 3: Configure GitHub Actions Secrets
To enable automatic deployments via GitHub Actions:

1. Go to: https://github.com/kmulroy1972/mosaicweb/settings/secrets/actions
2. Add these secrets:
   - `SERVER_HOST`: `138.197.40.154`
   - `SERVER_USER`: `master_wcqkvzhaqv`
   - `SERVER_PASSWORD`: (your Cloudways SSH password)
   - `APP_ROOT`: `/home/1478529.cloudwaysapps.com/vhxvtajnbg/public_html/`

## Remove Wrong Files from Server

After deploying, manually remove the dashboard directories:

```bash
ssh cloudways-server "rm -rf /home/1478529.cloudwaysapps.com/vhxvtajnbg/public_html/dashboard"
ssh cloudways-server "rm -rf /home/1478529.cloudwaysapps.com/vhxvtajnbg/public_html/dashboard-new"
```

## Verify Deployment

1. Check the website: https://mosaicpolicy.com (use incognito mode)
2. Verify `index.html` shows "MOSAIC – Health Policy Intelligence" not "MHP Brand Automation"
3. Check that dashboard directories are gone

## Files That Should Be Deployed

- `index.html` (MOSAIC website)
- `styles.css`
- `favicon.svg`
- `mosaic_logo_transparent.png`
- `mosaic_logo_transparent_new.png`
- `CNAME`
- PDF files (if needed)

## Files That Should NOT Be Deployed

- `app/` directory (WSC analytics - different project)
- `dashboard/` and `dashboard-new/` directories (wrong project)
- `*.py` files
- `requirements.txt`
- `remote/` directory (local mirror only)
- `.git/` and `.github/` directories

