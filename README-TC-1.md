# PDF Automation with Selenium and Chrome DevTools Protocol (CDP)

# Overview
This Python script automates the generation of PDF documents from a local web application using Selenium WebDriver and Chrome DevTools Protocol (CDP). It loads JSON files from a database folder, interacts with a web panel to generate question pages, injects solution data dynamically via JavaScript, waits for MathJax to render math content, and saves the output as PDFs.

# Features
1. Loads JSON input filenames from a db folder.
2. Navigates to a local PDF panel web app.
3. Inputs the JSON filename and triggers PDF generation.
4. Waits for dynamic content (including MathJax) to fully render.
5. Injects solutions into question pages dynamically using JavaScript.
6. Generates PDFs via Chrome DevTools Protocol's Page.printToPDF.
7. Saves generated PDFs into organized folders.
8. Handles multiple browser windows, pop-ups, and cleans up properly.

# Prerequisites
- Python 3.7 or higher
- Google Chrome browser installed
- Internet connection (for downloading ChromeDriver via webdriver-manager)

# Installation
1. Run 'npm install' to install all node.js dependencies needed for the website.
2. Run 'pip install python selenium os webdriver-manager mathjax' to install all python based dependencies.

# Configuration
- The Chrome user profile directory can be set by modifying CHROME_USER_DATA_DIR.
- Adjust timeouts and sleep durations if your environment needs longer waits for rendering.

# Usage
1. Open terminal and navigate to the project using cd command.
    cd sample-task-pdf-generator
2. Run 'npm run start' in the terminal.
3. Open the new terminal without destroying the current terminal.
4. Ensure the local website is running on https://localhost:3002/pdf-panel.
5. Run 'python merge-pdf.py' in new terminal.
    - Iterate through all JSON files in the db folder.
    - Open the PDF panel page.
    - Enter the input name.
    - Click the "Generate" button.
    - Wait for the question window to open.
    - Inject solutions from JSON data into the question page.
    - Wait for dynamic rendering (including MathJax).
    - Generate and save PDFs to merged_pdfs/.

# Important Details

- Handling Dynamic Content and MathJax
    1. The script waits for the main container (#page) to be present.
    2. Then it waits an additional 20 seconds to ensure MathJax and other dynamic content fully render.
    3. After injecting solutions, it triggers MathJax re-typesetting via JavaScript.

- Window and Pop-up Management
    1. The script detects and switches to the newly opened question window.
    2. Unrelated pop-ups are automatically closed.
    3. The question window is closed after PDF generation.
    4. The original panel window is retained for the next iteration.

# Error Handling
- If the question window is not found, the script logs an error and moves to the next JSON file.
- During any unexpected exceptions, the script attempts to close all extra windows and continue cleanly.
- Browser is closed gracefully at the end of the run.

# Folder Structure Summary
sample-task-pdf-generator/
│
├── db/                     # Input JSON files
├── downloaded_pdfs/        # Temporary PDFs saved by CDP
├── merged_pdfs/            # Final PDFs after renaming
├── merge-pdf.py            # This automation script
README-TC.md                # Readme task completed file
README.md                   # Readme task file

# Notes
- The script uses Chrome DevTools Protocol to produce high-quality PDFs.
- It assumes a local web app serving question panels and solutions.
- Modify the JavaScript injection if your JSON structure or page layout changes.

