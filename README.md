# Sample Task PDF Generation
1. Install NodeJS, Python.
2. Navigate to the folder `sample-task-pdf-generator` whivh contains sub-folders like db, public and so on.
3. Open cmd in the above path and run `npm install`
4. Once all packages are installed, run `npm run dev`.
5. You will be prompted to open up `http://localhost:3002/pdf-panel`
6. Open the above link and Enter `Basics` in Input field and click on generate.
7. 2 new windows will open up named `question_marks` and `solution_marks`.
8. If only 1 window is opened, it means that popup windows are blocked in your browser, please allow pop up windows to open up and then click on generate again (needs to be done only once).
9. Now, wait for 20 seconds on each tab for the contents like formulas, diagrams to get loaded and once done, download the same in pdf format.
10. After downloading both files, merge the 2 files -> 1st question and then solution and name the new pdf as whatever name you gave in input field in step 6.
11. Step 3 to step 10 should be automated using python script.
12. Now open following folder in file explorer - `sample-task-pdf-generator/db`
13. You will see 9 json files, step 6 to 10 needs to be repeated for all those 9 files in single python script.

# Sample Task Image Processing
Task Description - https://docs.google.com/document/u/0/d/1v2CE29myRvtOlDY1kVO-z-cWYJYGwmVyGi_VrS5jhDY/mobilebasic?pli=1

## How to Submit The Task:
We don't need the source code/script. Just screen record the working version of the script.
Document your approach in detail, and explain what are the edge cases that you have come across, which of them are solved and which could not.

Important: The script should be able to detect and separate question and diagram(s) from any question image provided. So in the screen recording, show the working version with multiple question images and not only with the sample image provided. 

Note: In case, you're not selected for the internship, you will reserve all the rights to your code/script. That's the reason, we are not asking you to submit any code.

Note: We'll give preference to candidates on a first come first serve basis.

# Deliverables: 
1. Finally, you need to zip the following things, 
    - 9 PDFs
    - single python script (.py file) of PDF Generation Task.
    - a readme.md file, which explains your code and flow of PDF Generation Task.
    - a document which explains your approach for the Image Processing Task.
2. A screen recording which shows the working version of PDF Generation Script (your approach should be explained clearly).
   Loom Video Link - (https://www.loom.com/share/f024ddfa38a54efd9cbea5ae21c169cc)
4. A screen recording which shows the working version of Image Processing Task (your approach should be explained clearly).
   Loom Video Link - (https://www.loom.com/share/732fd198628c414abdd94a02bfefb6c0)


- Mail the zip file and recordings to `***` and cc `***`
- Subject of the Mail should be - `Software Development - Sample Task`

- Note:
    - If required, upload the video recordings in drive and make sure the link is made public. If the link is not public, your attempt cannot be verified and hence it will be rejected.

# Evaluation Criteria:
- Correctness and functionality of the code.
- Code readability and structure.
- Proper exception handling.
- Efficient use of libraries (e.g., Selenium for web automation).
- Quality of documentation.
- Quality of recordings.

# README-TC-1
    Sample Task-1(Automated PDF Generator) Completed.
    
# README-TC-2
    Sample Task-2(Image Processing and OCR) Completed.
