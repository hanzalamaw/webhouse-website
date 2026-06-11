/**
 * Google Apps Script — WebHouse Inc. Website Forms
 *
 * Collects contact, newsletter, and consultation submissions into one Google Sheet
 * (separate tabs per form type).
 *
 * SETUP:
 * 1. Create a Google Sheet at https://sheets.google.com
 * 2. Copy the Sheet ID from the URL (between /d/ and /edit)
 * 3. Go to https://script.google.com → New project
 * 4. Paste this entire file into the editor
 * 5. Replace YOUR_SHEET_ID_HERE below with your Sheet ID
 * 6. Deploy → New deployment → Web app
 *    - Execute as: Me
 *    - Who has access: Anyone
 * 7. Copy the Web App URL
 * 8. Paste the URL into js/form-config.js (GOOGLE_APPS_SCRIPT_URL)
 */

const SHEET_ID = 'YOUR_SHEET_ID_HERE';

const FORM_SHEETS = {
  contact: {
    name: 'Contact',
    headers: ['Timestamp', 'Name', 'Email', 'Subject', 'Message', 'Source Page'],
    required: ['email']
  },
  newsletter: {
    name: 'Newsletter',
    headers: ['Timestamp', 'Email', 'Source Page'],
    required: ['email']
  },
  consultation: {
    name: 'Consultation',
    headers: ['Timestamp', 'Name', 'Email', 'Phone', 'Message', 'Source Page'],
    required: ['email']
  }
};

function doPost(e) {
  try {
    const data = parseRequestData_(e);
    const formType = String(data.formType || '').toLowerCase();
    const config = FORM_SHEETS[formType];

    if (!config) {
      return jsonResponse_({ success: false, error: 'Invalid form type' });
    }

    for (var i = 0; i < config.required.length; i++) {
      var field = config.required[i];
      if (!String(data[field] || '').trim()) {
        return jsonResponse_({ success: false, error: capitalize_(field) + ' is required' });
      }
    }

    const ss = SpreadsheetApp.openById(SHEET_ID);
    const sheet = getOrCreateSheet_(ss, config);
    const timestamp = data.timestamp || new Date().toISOString();
    const sourcePage = data.sourcePage || '';

    let row;
    if (formType === 'contact') {
      row = [
        timestamp,
        String(data.name || '').trim(),
        String(data.email || '').trim(),
        String(data.subject || '').trim(),
        String(data.message || '').trim(),
        sourcePage
      ];
    } else if (formType === 'newsletter') {
      row = [timestamp, String(data.email || '').trim(), sourcePage];
    } else if (formType === 'consultation') {
      row = [
        timestamp,
        String(data.name || '').trim(),
        String(data.email || '').trim(),
        String(data.phone || '').trim(),
        String(data.message || '').trim(),
        sourcePage
      ];
    }

    sheet.appendRow(row);

    return jsonResponse_({ success: true, message: 'Submission saved' });
  } catch (error) {
    return jsonResponse_({ success: false, error: error.toString() });
  }
}

function doGet() {
  return ContentService.createTextOutput(
    'WebHouse Inc. forms backend is running. Use POST to submit form data.'
  ).setMimeType(ContentService.MimeType.TEXT);
}

/**
 * Run once from the Apps Script editor to create all tabs and headers.
 * Extensions → Apps Script → select setupSpreadsheet → Run
 */
function setupSpreadsheet() {
  const ss = SpreadsheetApp.openById(SHEET_ID);
  Object.keys(FORM_SHEETS).forEach(function (key) {
    getOrCreateSheet_(ss, FORM_SHEETS[key]);
  });
}

function parseRequestData_(e) {
  if (e && e.postData && e.postData.contents) {
    const contentType = String(e.postData.type || '').toLowerCase();
    if (contentType.indexOf('application/json') !== -1) {
      return JSON.parse(e.postData.contents);
    }
    return parseFormEncoded_(e.postData.contents);
  }
  return e && e.parameter ? e.parameter : {};
}

function parseFormEncoded_(body) {
  const data = {};
  body.split('&').forEach(function (pair) {
    const parts = pair.split('=');
    if (parts.length === 2) {
      data[decodeURIComponent(parts[0].replace(/\+/g, ' '))] =
        decodeURIComponent(parts[1].replace(/\+/g, ' '));
    }
  });
  return data;
}

function getOrCreateSheet_(ss, config) {
  let sheet = ss.getSheetByName(config.name);
  if (!sheet) {
    sheet = ss.insertSheet(config.name);
  }
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(config.headers);
    sheet.getRange(1, 1, 1, config.headers.length).setFontWeight('bold');
    sheet.setFrozenRows(1);
  }
  return sheet;
}

function jsonResponse_(payload) {
  return ContentService.createTextOutput(JSON.stringify(payload)).setMimeType(
    ContentService.MimeType.JSON
  );
}

function capitalize_(value) {
  return value.charAt(0).toUpperCase() + value.slice(1);
}
