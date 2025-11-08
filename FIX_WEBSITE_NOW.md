# URGENT: Fix mosaicpolicy.com Website

## Current Problem
- Website shows "MHP Brand Automation" instead of "MOSAIC Health Policy Intelligence"
- Wrong `index.html` file is on the server
- `dashboard/` and `dashboard-new/` directories from wrong project exist
- Direct file deployment blocked by permissions

## SOLUTION: Use Cloudways Control Panel

### Step 1: Access Cloudways Control Panel
1. Log into your Cloudways account
2. Navigate to your application (server 1478529, app vhxvtajnbg)

### Step 2: Configure Git Repository (if not already done)
1. Go to **Application Management** → **Deployment via Git**
2. Set up Git repository:
   - **Git URL**: `https://github.com/kmulroy1972/mosaicweb.git`
   - **Branch**: `main`
   - **Deployment Path**: `/public_html/`

### Step 3: Trigger Git Pull
1. In Cloudways panel, click **"Pull"** or **"Deploy"** button
2. This will pull the latest code from GitHub
3. Wait for deployment to complete (usually 1-2 minutes)

### Step 4: Remove Wrong Files
After git pull, SSH into server and remove dashboard directories:

```bash
ssh cloudways-server
cd /home/1478529.cloudwaysapps.com/vhxvtajnbg/public_html/
rm -rf dashboard dashboard-new
exit
```

### Step 5: Purge Cache
```bash
ssh cloudways-server "curl -I -X PURGE https://mosaicpolicy.com/"
```

### Step 6: Verify
- Visit https://mosaicpolicy.com in incognito mode
- Should see "MOSAIC – Health Policy Intelligence" 
- Should NOT see "MHP Brand Automation"

## Alternative: Manual File Upload via Cloudways File Manager

If Git pull doesn't work:

1. **Access File Manager** in Cloudways control panel
2. Navigate to `/public_html/`
3. **Upload these files** (replace existing):
   - `index.html` (from repository root)
   - `styles.css`
   - `favicon.svg`
   - `mosaic_logo_transparent.png`
   - `mosaic_logo_transparent_new.png`
4. **Delete** these directories:
   - `dashboard/`
   - `dashboard-new/`
5. Purge cache

## Files That Should Be on Server

✅ **Keep these:**
- `index.html` (MOSAIC website - correct version)
- `styles.css`
- `favicon.svg`
- `mosaic_logo_transparent.png`
- `mosaic_logo_transparent_new.png`
- `CNAME`
- `gitautodeploy.php` (for future deployments)

❌ **Remove these:**
- `dashboard/` directory
- `dashboard-new/` directory  
- `test.html` (if not needed)
- Any `*.py` files
- `requirements.txt`

## Verify Correct index.html

The correct `index.html` should start with:
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="MOSAIC delivers decision-grade health policy intelligence...">
    <title>MOSAIC – Health Policy Intelligence</title>
```

NOT:
```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>MHP Brand Automation</title>
```

