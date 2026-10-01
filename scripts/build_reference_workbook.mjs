import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const rawDir = path.join(root, "data", "raw");
const outDir = path.join(root, "reference");
const previewDir = path.join(root, "tmp_workbook", "previews");
const workbook = Workbook.create();
const accent = "#2F6B4F", dark = "#243B2F", pale = "#E8F1EB", line = "#CBD8CF";
const previewRanges = { "Start Here": "A1:F11" };

function parseCsv(text) {
  const lines = text.trimEnd().split(/\r?\n/);
  const headers = lines[0].split(",");
  const dateFields = new Set(["join_date", "gift_date", "send_date"]);
  const boolFields = new Set(["email_opt_in", "mail_opt_in", "household_member", "volunteer", "online", "recurring_gift", "soft_credit"]);
  const numericFields = new Set(["event_attendance_count", "gift_amount", "fiscal_year", "recipient_count", "creative_cost", "printing_cost", "distribution_cost", "platform_cost", "total_cost"]);
  const rows = lines.slice(1).map(line => line.split(",").map((value, i) => {
    const field = headers[i];
    if (value === "") return null;
    if (dateFields.has(field)) return new Date(`${value}T12:00:00`);
    if (boolFields.has(field)) return value.toLowerCase() === "true";
    if (numericFields.has(field)) return Number(value);
    return value;
  }));
  return { headers, rows };
}

function colLetter(n) {
  let s = "";
  while (n > 0) { n -= 1; s = String.fromCharCode(65 + (n % 26)) + s; n = Math.floor(n / 26); }
  return s;
}

function styleHeader(range) {
  range.format.fill = dark;
  range.format.font = { bold: true, color: "#FFFFFF", name: "Arial", size: 10 };
  range.format.horizontalAlignment = "center";
  range.format.verticalAlignment = "center";
  range.format.wrapText = true;
  range.format.rowHeight = 30;
}

function styleSheet(sheet, used) {
  used.format.font = { name: "Arial", size: 10, color: "#1F2933" };
  used.format.verticalAlignment = "top";
  sheet.freezePanes.freezeRows(1);
}

const start = workbook.worksheets.add("Start Here");
start.showGridLines = false;
start.getRange("A1:F1").merge();
start.getRange("A1").values = [["Fundraising analytics training reference"]];
start.getRange("A1").format.font = { bold: true, size: 18, color: dark, name: "Arial" };
start.getRange("A3:F3").values = [["Purpose", "Coding source", "Scale", "Period", "Team", "Important"]];
styleHeader(start.getRange("A3:F3"));
start.getRange("A4:F4").values = [["Practice solicitation ROI, trends, upgrade propensity, and attribution", "CSV files in data/raw", "3,000 donors; 9,000 gift rows", "2022–2025", "Five analysts plus coordinator", "All data is synthetic"]];
start.getRange("A6:B11").values = [
  ["Recommended order", "Action"], ["1", "Complete Lesson 1 setup"], ["2", "Complete the Polars notebook"],
  ["3", "Review table grain and keys"], ["4", "Complete your assigned workstream"], ["5", "Reconcile totals before interpretation"]
];
styleHeader(start.getRange("A6:B6"));
start.getRange("A4:F4").format.wrapText = true; start.getRange("A4:F4").format.rowHeight = 54;
start.getRange("A1:F11").format.font = { name: "Arial", size: 10, color: "#1F2933" };
start.getRange("A1:F1").format.font = { bold: true, size: 18, color: dark, name: "Arial" };
styleHeader(start.getRange("A3:F3")); styleHeader(start.getRange("A6:B6"));
start.getRange("A1:F11").format.borders = { preset: "outside", style: "thin", color: line };
start.getRange("A:F").format.columnWidth = 22;

const files = [
  ["donors", "Donors"], ["gifts", "Gifts"], ["solicitations", "Solicitations"],
  ["outreach_costs", "Outreach Costs"], ["website_sources", "Website Sources"]
];
for (const [file, sheetName] of files) {
  const { headers, rows } = parseCsv(await fs.readFile(path.join(rawDir, `${file}.csv`), "utf8"));
  const sheet = workbook.worksheets.add(sheetName);
  const matrix = [headers, ...rows];
  const endCol = colLetter(headers.length);
  sheet.getRangeByIndexes(0, 0, matrix.length, headers.length).values = matrix;
  styleSheet(sheet, sheet.getRange(`A1:${endCol}${matrix.length}`));
  styleHeader(sheet.getRange(`A1:${endCol}1`));
  sheet.tables.add(`A1:${endCol}${matrix.length}`, true, `${file.replaceAll("_", "")}Table`);
  previewRanges[sheetName] = `A1:${endCol}${Math.min(matrix.length, 25)}`;
  for (let i = 0; i < headers.length; i++) {
    const letter = colLetter(i + 1), name = headers[i];
    sheet.getRange(`${letter}:${letter}`).format.columnWidth = name.includes("campaign") || name.includes("source_response") ? 24 : 16;
    if (name.includes("date")) sheet.getRange(`${letter}2:${letter}${matrix.length}`).setNumberFormat("yyyy-mm-dd");
    if (name.includes("cost") || name === "gift_amount") sheet.getRange(`${letter}2:${letter}${matrix.length}`).setNumberFormat('"$"#,##0.00');
  }
}

const dict = workbook.worksheets.add("Data Dictionary");
const dictionary = [
  ["Table", "Field group", "Grain / definition", "Type", "May be blank", "Analytical use"],
  ["Donors", "donor_id", "One synthetic person; stable donor key", "Text", "No", "Join gifts to donor attributes"],
  ["Donors", "profile fields", "Membership, region, acquisition and engagement", "Mixed", "Age band only", "Segmentation and features"],
  ["Gifts", "gift_id", "One transaction before controlled duplicates", "Text", "No", "Deduplication and transaction count"],
  ["Gifts", "gift_amount", "Gift amount in US dollars", "Number", "No", "Revenue, thresholds and features"],
  ["Gifts", "solicitation_code", "Attributed solicitation code", "Text", "Yes", "Direct-response attribution"],
  ["Solicitations", "solicitation_code", "One outreach instance", "Text", "No", "Campaign and channel context"],
  ["Outreach Costs", "cost fields", "One cost record per solicitation", "Number", "No", "Net revenue and ROI"],
  ["Website Sources", "source_response_raw", "Self-elected response on website gift", "Text", "Yes", "Acquisition-source exploration"],
  ["Website Sources", "source_category_clean", "Normalized training category", "Text", "No", "Grouped reporting"]
];
dict.getRangeByIndexes(0, 0, dictionary.length, dictionary[0].length).values = dictionary;
styleSheet(dict, dict.getRange("A1:F10")); styleHeader(dict.getRange("A1:F1"));
dict.getRange("A:F").format.columnWidth = 22; dict.getRange("C:C").format.columnWidth = 38;
dict.getRange("A1:F10").format.wrapText = true;
previewRanges["Data Dictionary"] = "A1:F10";

const assignments = workbook.worksheets.add("Assignment Summary");
const assignmentRows = [
  ["Workstream", "Primary question", "Required outputs", "Estimated time", "Review gate"],
  ["1. Data quality", "Can the tables be joined and trusted?", "Issue log; donor profile", "3 hours", "Totals reconcile after deduplication"],
  ["2. Solicitation ROI", "Which channels generate net return?", "Solicitation and channel ROI", "4 hours", "Formulas and attribution documented"],
  ["3. Revenue trends", "When does revenue arrive?", "Monthly tables and two charts", "4 hours", "Monthly total equals gift total"],
  ["4. Upgrade propensity", "Who may be ready for a larger ask?", "Features, ranking, evaluation", "5–6 hours", "No post-cutoff feature leakage"],
  ["5. Large gifts", "Which outreach triggered major gifts?", "Attribution and dashboard inputs", "4 hours", "Every major gift classified once"],
  ["Coordinator", "Are definitions consistent and ready to integrate?", "Review log and partner questions", "Ongoing", "All five workstreams approved"]
];
assignments.getRangeByIndexes(0, 0, assignmentRows.length, assignmentRows[0].length).values = assignmentRows;
styleSheet(assignments, assignments.getRange("A1:E7")); styleHeader(assignments.getRange("A1:E1"));
assignments.getRange("A:E").format.columnWidth = 27; assignments.getRange("A1:E7").format.wrapText = true;
previewRanges["Assignment Summary"] = "A1:E7";

await fs.mkdir(outDir, { recursive: true }); await fs.mkdir(previewDir, { recursive: true });
console.log((await workbook.inspect({ kind: "table", sheetId: "Start Here", range: "A1:F11", include: "values,formulas", tableMaxRows: 12, tableMaxCols: 8 })).ndjson);
console.log((await workbook.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!", options: { useRegex: true, maxResults: 100 }, summary: "formula error scan" })).ndjson);
for (const name of ["Start Here", ...files.map(x => x[1]), "Data Dictionary", "Assignment Summary"]) {
  const preview = await workbook.render({ sheetName: name, range: previewRanges[name], autoCrop: "all", scale: 1, format: "png" });
  await fs.writeFile(path.join(previewDir, `${name.replaceAll(" ", "_")}.png`), new Uint8Array(await preview.arrayBuffer()));
}
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(path.join(outDir, "fundraising_training_reference.xlsx"));
console.log("Saved reference/fundraising_training_reference.xlsx");
