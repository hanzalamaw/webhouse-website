# Netlify Deployment Guide

## Quick Deployment Steps

### Option 1: Drag & Drop (Easiest)
1. Go to [app.netlify.com](https://app.netlify.com)
2. Sign up or log in
3. Drag and drop your project folder onto the Netlify dashboard
4. Your site will be live in seconds!

### Option 2: Git Integration (Recommended)
1. Push your code to GitHub, GitLab, or Bitbucket
2. Connect your repository to Netlify:
   - Go to Netlify Dashboard → Sites → Add new site → Import an existing project
   - Select your Git provider and repository
   - Configure build settings:
     - **Build command:** Leave empty (static site)
     - **Publish directory:** `.` (root directory)
   - Click "Deploy site"

### Option 3: Netlify CLI
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Deploy from your project directory
netlify deploy

# For production deployment
netlify deploy --prod
```

## Configuration

The `netlify.toml` file is already configured for your site:
- ✅ No build step required (static HTML files)
- ✅ **Clean URLs** - `.html` extension automatically hidden
- ✅ Security headers enabled
- ✅ Caching configured for optimal performance
- ✅ Redirects configured (301 redirects for SEO)

## Your Pages

Your site includes:
- **index.html** - Main homepage (accessible at `/`)
- **coming-soon.html** - Coming soon page (accessible at `/coming-soon`)
- **about.html** - About page (accessible at `/about`)
- **services.html** - Services page (accessible at `/services`)
- **case-studies.html** - Case studies page (accessible at `/case-studies`)
- **how-we-work.html** - Methodology page (accessible at `/how-we-work`)

### Clean URLs (No .html Extension)

✅ **URLs are automatically cleaned!** The `.html` extension is hidden from all URLs.

- `/about.html` → redirects to `/about` (301 redirect)
- `/about` → serves `about.html` (clean URL in browser)
- `/services.html` → redirects to `/services`
- `/coming-soon.html` → redirects to `/coming-soon`

**Note:** You can still access pages with `.html` extension - they'll automatically redirect to the clean URL.

## Using coming-soon.html

### Option 1: Keep as separate page
Access it at: `https://yoursite.netlify.app/coming-soon.html`

### Option 2: Make it the homepage temporarily
In `netlify.toml`, uncomment these lines:
```toml
[[redirects]]
  from = "/"
  to = "/coming-soon.html"
  status = 200
```

### Option 3: Use as maintenance page
1. Go to Netlify Dashboard → Site settings → Build & deploy
2. Scroll to "Deploy notifications"
3. Enable "Maintenance mode" - you can set `coming-soon.html` as the maintenance page

## Custom Domain

1. Go to Netlify Dashboard → Domain settings
2. Click "Add custom domain"
3. Follow the instructions to configure DNS

## Environment Variables

If you need environment variables (for API keys, etc.):
1. Netlify Dashboard → Site settings → Environment variables
2. Add your variables
3. Access them in your code (if you add JavaScript that needs them)

## Performance Tips

✅ Already configured in `netlify.toml`:
- Cache headers for CSS/JS (1 year)
- Cache headers for HTML (1 hour)
- Security headers

## Troubleshooting

### Issue: CSS/JS not loading
- Check that file paths are relative (they are)
- Ensure `assets/`, `css/`, and `js/` folders are in the root

### Issue: Images not showing
- Verify `assets/images/logo.png` exists
- Check image paths are correct

### Issue: 404 errors
- Verify all HTML files are in the root directory
- Check file names match links (case-sensitive)

## Quick Checklist

Before deploying:
- [x] All HTML files in root directory
- [x] `assets/` folder with logo
- [x] `css/` and `js/` folders with styles and scripts
- [x] `netlify.toml` configured
- [ ] Test all links locally
- [ ] Verify all images load
- [ ] Test on mobile devices

## Support

- Netlify Docs: https://docs.netlify.com
- Netlify Community: https://answers.netlify.com

