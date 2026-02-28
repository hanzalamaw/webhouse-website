# Netlify Deployment Commands

## Quick Deployment Options

### Option 1: Netlify CLI (Recommended for Terminal Users)

```bash
# 1. Install Netlify CLI globally
npm install -g netlify-cli

# 2. Navigate to your project directory
cd C:\Users\us\Desktop\WHI_DEV\webhouseinc_website

# 3. Login to Netlify (opens browser)
netlify login

# 4. Initialize site (first time only)
netlify init

# 5. Deploy to draft URL (for testing)
netlify deploy

# 6. Deploy to production
netlify deploy --prod
```

### Option 2: Git Integration (Best for Continuous Deployment)

```bash
# 1. Initialize git (if not already done)
git init

# 2. Add all files
git add .

# 3. Commit files
git commit -m "Initial commit - Coming soon page"

# 4. Create repository on GitHub/GitLab/Bitbucket
# Then connect it:
git remote add origin https://github.com/yourusername/yourrepo.git
git branch -M main
git push -u origin main

# 5. Go to Netlify Dashboard:
# - https://app.netlify.com
# - Add new site → Import from Git
# - Connect your repository
# - Deploy settings: Build command (leave empty), Publish directory: "."
```

### Option 3: Drag & Drop (Fastest for Quick Test)

```bash
# No commands needed! Just:
# 1. Go to https://app.netlify.com
# 2. Drag your project folder onto the page
# 3. Done!
```

## After Deployment

Once deployed, your site will:
- ✅ Redirect ALL URLs to `/coming-soon`
- ✅ Serve static assets (CSS, JS, images) normally
- ✅ Have a clean URL structure

## Useful Commands

```bash
# View deployment status
netlify status

# Open site in browser
netlify open

# View deployment logs
netlify logs

# Open Netlify admin
netlify open:admin

# List all deployments
netlify deploy:list

# Rollback to previous deployment
netlify rollback
```

## Environment Setup (Windows PowerShell)

```powershell
# Check if Node.js is installed
node --version

# If not installed, download from: https://nodejs.org/

# Install Netlify CLI
npm install -g netlify-cli

# Verify installation
netlify --version
```

## Quick Deploy Script

Create a file `deploy.bat` in your project root:

```batch
@echo off
echo Deploying to Netlify...
cd /d "%~dp0"
netlify deploy --prod
pause
```

Then double-click `deploy.bat` to deploy!

## Troubleshooting

```bash
# If deployment fails, check:
netlify status

# Clear Netlify cache and redeploy
netlify deploy --prod --clear-cache

# Test locally with Netlify Dev
netlify dev
```

