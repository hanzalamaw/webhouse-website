/**
 * Google Apps Script — WebHouse Inc. Website Forms
 *
 * SETUP:
 * 1. Set SHEET_ID below to your Google Sheet ID
 * 2. Run setupSpreadsheet() once from the script editor
 * 3. Deploy → Manage deployments → Edit → New version → Deploy
 *    (You MUST create a new version after every code change!)
 *    - Execute as: Me
 *    - Who has access: Anyone
 * 4. Paste the Web App URL into js/form-config.js
 *
 * TEST: Open your Web App URL in a browser — you should see JSON with your sheetId.
 * TEST WRITE: Add ?formType=newsletter&email=test@example.com to the URL — check Newsletter tab.
 */

const SHEET_ID = '1Y0c-J8mAp7m7jFUGKolIzLUQjUO0_gOolKqwpsxTQs4';

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
  return processFormSubmission_(parseRequestData_(e));
}

function doGet(e) {
  var params = e && e.parameter ? e.parameter : {};
  if (params.formType) {
    return processFormSubmission_(params);
  }
  return jsonResponse_({
    status: 'ok',
    message: 'WebHouse Inc. forms backend is running',
    sheetId: SHEET_ID,
    tabs: ['Contact', 'Newsletter', 'Consultation']
  });
}

function processFormSubmission_(data) {
  try {
    var formType = String(data.formType || '').toLowerCase();
    var config = FORM_SHEETS[formType];

    if (!config) {
      return jsonResponse_({ success: false, error: 'Invalid form type: ' + formType });
    }

    for (var i = 0; i < config.required.length; i++) {
      var field = config.required[i];
      if (!String(data[field] || '').trim()) {
        return jsonResponse_({ success: false, error: capitalize_(field) + ' is required' });
      }
    }

    var ss = SpreadsheetApp.openById(SHEET_ID);
    var sheet = getOrCreateSheet_(ss, config);
    var timestamp = data.timestamp || new Date().toISOString();
    var sourcePage = data.sourcePage || '';
    var row;

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

    return jsonResponse_({
      success: true,
      message: 'Submission saved',
      sheet: config.name,
      sheetId: SHEET_ID
    });
  } catch (error) {
    return jsonResponse_({ success: false, error: error.toString() });
  }
}

function setupSpreadsheet() {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  Object.keys(FORM_SHEETS).forEach(function (key) {
    getOrCreateSheet_(ss, FORM_SHEETS[key]);
  });
}

function parseRequestData_(e) {
  var data = {};
  if (e && e.parameter) {
    data = Object.assign({}, e.parameter);
  }
  if (e && e.postData && e.postData.contents) {
    var contentType = String(e.postData.type || '').toLowerCase();
    var parsed = contentType.indexOf('application/json') !== -1
      ? JSON.parse(e.postData.contents)
      : parseFormEncoded_(e.postData.contents);
    data = Object.assign(data, parsed);
  }
  return data;
}

function parseFormEncoded_(body) {
  var data = {};
  body.split('&').forEach(function (pair) {
    var eq = pair.indexOf('=');
    if (eq === -1) return;
    var key = decodeURIComponent(pair.slice(0, eq).replace(/\+/g, ' '));
    var value = decodeURIComponent(pair.slice(eq + 1).replace(/\+/g, ' '));
    data[key] = value;
  });
  return data;
}

function getOrCreateSheet_(ss, config) {
  var sheet = ss.getSheetByName(config.name);
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
