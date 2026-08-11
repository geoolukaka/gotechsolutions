/**
 * GoTech Solutions — Contact Form Backend
 * ----------------------------------------
 * This script receives contact-form submissions (POST requests) from the
 * website and appends them as a new row in a Google Sheet, acting as a
 * free, no-server "database" for contact/lead data.
 *
 * SETUP (one-time):
 * 1. Create a new Google Sheet (e.g. "GoTech Contact Submissions").
 * 2. In the Sheet, go to Extensions > Apps Script.
 * 3. Delete any starter code and paste in this entire file.
 * 4. Click "Deploy" > "New deployment".
 *      - Select type: "Web app"
 *      - Description: "GoTech contact form"
 *      - Execute as: "Me"
 *      - Who has access: "Anyone"
 * 5. Click Deploy, authorize the script when prompted, and copy the
 *    "Web app URL" it gives you.
 * 6. Paste that URL into assets/js/main.js as the value of
 *    CONTACT_SCRIPT_URL.
 * 7. Re-deploy (Deploy > Manage deployments > Edit > New version) any time
 *    you change this script.
 *
 * The first time the form submits, this script auto-creates a header row:
 * Timestamp | Name | Phone | Email | Service | Message | Page URL
 */

const SHEET_NAME = "Submissions";

function doPost(e) {
  try {
    const data = parseRequest(e);
    const sheet = getOrCreateSheet();

    sheet.appendRow([
      new Date(),
      data.name || "",
      data.phone || "",
      data.email || "",
      data.service || "",
      data.message || "",
      data.page || ""
    ]);

    return jsonResponse({ status: "success" });
  } catch (err) {
    return jsonResponse({ status: "error", message: err.message });
  }
}

// Optional: lets you open the Web App URL in a browser to sanity-check it's live.
function doGet(e) {
  return jsonResponse({ status: "ok", message: "GoTech contact endpoint is live." });
}

function parseRequest(e) {
  if (e && e.postData && e.postData.contents) {
    try {
      return JSON.parse(e.postData.contents);
    } catch (err) {
      // Fall back to form-encoded params if not JSON
    }
  }
  if (e && e.parameter) {
    return e.parameter;
  }
  return {};
}

function getOrCreateSheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
    sheet.appendRow([
      "Timestamp",
      "Name",
      "Phone",
      "Email",
      "Service",
      "Message",
      "Page URL"
    ]);
    sheet.setFrozenRows(1);
  }
  return sheet;
}

function jsonResponse(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
