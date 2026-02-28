/**
 * Google Apps Script for WebHouse Inc. Coming Soon Form
 * 
 * SETUP INSTRUCTIONS:
 * 1. Go to https://script.google.com
 * 2. Create a new project
 * 3. Paste this code into the editor
 * 4. Create a new Google Sheet (or use an existing one)
 * 5. Copy the Sheet ID from the URL (the long string between /d/ and /edit)
 * 6. Replace 'YOUR_SHEET_ID_HERE' below with your Sheet ID
 * 7. Click "Deploy" > "New deployment"
 * 8. Select type: "Web app"
 * 9. Set "Execute as" to "Me"
 * 10. Set "Who has access" to "Anyone"
 * 11. Click "Deploy" and copy the Web App URL
 * 12. Paste the URL into coming-soon.html where it says YOUR_GOOGLE_APPS_SCRIPT_URL_HERE
 */

// Replace with your Google Sheet ID
const SHEET_ID = 'YOUR_SHEET_ID_HERE';

function doPost(e) {
  try {
    // Get the email from the form data
    const email = e.parameter.email || JSON.parse(e.postData.contents).email;
    const timestamp = e.parameter.timestamp || JSON.parse(e.postData.contents).timestamp || new Date().toISOString();
    
    if (!email) {
      return ContentService.createTextOutput(JSON.stringify({
        success: false,
        error: 'Email is required'
      })).setMimeType(ContentService.MimeType.JSON);
    }
    
    // Open the spreadsheet
    const sheet = SpreadsheetApp.openById(SHEET_ID).getActiveSheet();
    
    // If the sheet is empty, add headers
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(['Email', 'Timestamp', 'Date Added']);
    }
    
    // Append the data
    sheet.appendRow([email, timestamp, new Date()]);
    
    // Return success response
    return ContentService.createTextOutput(JSON.stringify({
      success: true,
      message: 'Email added successfully'
    })).setMimeType(ContentService.MimeType.JSON);
    
  } catch (error) {
    // Return error response
    return ContentService.createTextOutput(JSON.stringify({
      success: false,
      error: error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  // Handle GET requests (optional, for testing)
  return ContentService.createTextOutput('WebHouse Inc. Coming Soon Form - Backend is running!')
    .setMimeType(ContentService.MimeType.TEXT);
}

