# Complete Form Data Collection Guide

Choose the best method for your needs. All methods work with the form in `coming-soon.html`.

---

## 🚀 Quick Start (Easiest Options)

### ⚡ FormSubmit (30 seconds - Email Only)
**Best for:** Quick setup, email notifications  
**Free Tier:** Unlimited  
**Google Sheets:** Via Zapier email forwarding

**Setup:**
1. In `coming-soon.html`, change:
   ```javascript
   METHOD = 'formsubmit'
   FORM_SUBMIT_EMAIL = 'your-email@example.com'
   ```
2. Done! Submissions go to your email.

---

### 📧 EmailJS (2 minutes - Send Emails)
**Best for:** Custom email templates, professional emails  
**Free Tier:** 200 emails/month  
**Google Sheets:** Via Zapier

**Setup:**
1. Go to https://www.emailjs.com and sign up (free)
2. Create an email service (Gmail, Outlook, etc.)
3. Create an email template
4. Get your Public Key, Service ID, and Template ID
5. In `coming-soon.html`, change:
   ```javascript
   METHOD = 'emailjs'
   EMAILJS_PUBLIC_KEY = 'your-public-key'
   EMAILJS_SERVICE_ID = 'your-service-id'
   EMAILJS_TEMPLATE_ID = 'your-template-id'
   EMAILJS_TO_EMAIL = 'your-email@example.com'
   ```

---

## 📊 Direct Google Sheets Integration

### 📈 SheetDB (3 minutes - Direct to Sheets)
**Best for:** Direct Google Sheets integration, no coding  
**Free Tier:** 1,000 requests/month  
**Google Sheets:** ✅ Direct

**Setup:**
1. Go to https://sheetdb.io and sign up (free)
2. Connect your Google Sheet
3. Copy the API URL
4. In `coming-soon.html`, change:
   ```javascript
   METHOD = 'sheetdb'
   SHEETDB_API_URL = 'your-api-url'
   ```

---

### 🔧 Google Apps Script (10 minutes - Full Control)
**Best for:** Complete control, unlimited submissions  
**Free Tier:** Unlimited  
**Google Sheets:** ✅ Direct

**Setup:**
1. See `google-apps-script.js` for detailed instructions
2. Create Google Apps Script
3. Deploy as web app
4. In `coming-soon.html`, change:
   ```javascript
   METHOD = 'google-script'
   GOOGLE_SCRIPT_URL = 'your-script-url'
   ```

---

## 🎯 Form Backend Services

### ✨ Formspree (2 minutes - Recommended)
**Best for:** Clean dashboard, easy integrations  
**Free Tier:** 50 submissions/month  
**Google Sheets:** Via Zapier

**Setup:**
1. Go to https://formspree.io and sign up (free)
2. Create a new form
3. Copy your form ID
4. In `coming-soon.html`, change:
   ```javascript
   METHOD = 'formspree'
   FORMSPREE_ID = 'your-form-id'
   ```

---

### 🌐 Web3Forms (3 minutes - High Limit)
**Best for:** Higher free tier, simple API  
**Free Tier:** 250 submissions/month  
**Google Sheets:** Via dashboard export

**Setup:**
1. Go to https://web3forms.com and sign up (free)
2. Get your access key from dashboard
3. In `coming-soon.html`, change:
   ```javascript
   METHOD = 'web3forms'
   WEB3FORMS_KEY = 'your-access-key'
   ```

---

### 🎨 Getform (2 minutes - Modern UI)
**Best for:** Modern dashboard, webhooks  
**Free Tier:** 50 submissions/month  
**Google Sheets:** Via Zapier

**Setup:**
1. Go to https://getform.io and sign up (free)
2. Create a form endpoint
3. Copy the endpoint URL
4. In `coming-soon.html`, change:
   ```javascript
   METHOD = 'getform'
   GETFORM_ENDPOINT = 'your-endpoint-url'
   ```

---

### 💎 Basin (2 minutes - Beautiful Dashboard)
**Best for:** Beautiful UI, spam protection  
**Free Tier:** 100 submissions/month  
**Google Sheets:** Via Zapier

**Setup:**
1. Go to https://usebasin.com and sign up (free)
2. Create a form endpoint
3. Copy the endpoint URL
4. In `coming-soon.html`, change:
   ```javascript
   METHOD = 'basin'
   BASIN_ENDPOINT = 'your-endpoint-url'
   ```

---

## 🗄️ Database Solutions

### 📋 Airtable (5 minutes - Database/Spreadsheet)
**Best for:** Database features, powerful filtering  
**Free Tier:** 1,200 records/base  
**Google Sheets:** Export available

**Setup:**
1. Go to https://airtable.com and sign up (free)
2. Create a base and table
3. Get your API key and Base ID
4. In `coming-soon.html`, change:
   ```javascript
   METHOD = 'airtable'
   AIRTABLE_API_KEY = 'your-api-key'
   AIRTABLE_BASE_ID = 'your-base-id'
   AIRTABLE_TABLE_NAME = 'Submissions'
   ```

---

## 📊 Comparison Table

| Method | Setup Time | Free Limit | Google Sheets | Difficulty | Best For |
|--------|-----------|------------|---------------|------------|----------|
| **FormSubmit** | 30 sec | Unlimited | Via Zapier | ⭐ Easiest | Quick email setup |
| **EmailJS** | 2 min | 200/month | Via Zapier | ⭐⭐ Easy | Custom emails |
| **Formspree** | 2 min | 50/month | Via Zapier | ⭐⭐ Easy | Clean dashboard |
| **Web3Forms** | 3 min | 250/month | Export | ⭐⭐ Easy | Higher limits |
| **Getform** | 2 min | 50/month | Via Zapier | ⭐⭐ Easy | Modern features |
| **Basin** | 2 min | 100/month | Via Zapier | ⭐⭐ Easy | Beautiful UI |
| **SheetDB** | 3 min | 1,000/month | ✅ Direct | ⭐⭐ Easy | Direct Sheets |
| **Airtable** | 5 min | 1,200 records | Export | ⭐⭐⭐ Medium | Database features |
| **Google Script** | 10 min | Unlimited | ✅ Direct | ⭐⭐⭐ Medium | Full control |

---

## 🎯 Recommendations

### For Quickest Setup:
**FormSubmit** - Just add your email address!

### For Best Features:
**Formspree** or **Getform** - Clean dashboards + Zapier integration

### For Direct Google Sheets:
**SheetDB** - Easiest direct integration

### For High Volume:
**Google Apps Script** - Unlimited and free

### For Database Features:
**Airtable** - Powerful filtering and views

---

## 🔗 Google Sheets Integration Options

If your chosen method doesn't directly support Google Sheets, use:

1. **Zapier** (https://zapier.com) - Free tier: 100 tasks/month
   - Connect your form service → Google Sheets
   - Works with: Formspree, EmailJS, Getform, Basin, FormSubmit

2. **Make.com** (formerly Integromat) - Free tier: 1,000 operations/month
   - Similar to Zapier, more operations

3. **Native Export** - Some services (Web3Forms, Airtable) have built-in export

---

## 💡 Tips

- **Test your form** after setup to ensure it's working
- **Check spam folder** if using email-based methods
- **Set up Zapier** for automatic Google Sheets sync (if needed)
- **Monitor your free tier limits** to avoid hitting caps
- **Use SheetDB or Google Script** if you need direct Sheets integration

---

## 🆘 Troubleshooting

**Form not submitting?**
- Check browser console for errors (F12)
- Verify all configuration values are set correctly
- Ensure API keys/endpoints are valid

**Not receiving emails?**
- Check spam folder
- Verify email service is configured correctly
- Test with a different email address

**Google Sheets not updating?**
- Verify SheetDB/Google Script is configured correctly
- Check API permissions
- Ensure sheet is shared with the service account (if needed)
