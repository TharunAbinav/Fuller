Make Sure Python is Installed

download these libraries in python
pip install pandas openpyxl

======================================================
   HOW TO RUN THE PXP EXCEL CONSOLIDATOR SCRIPT
======================================================

1. THE SETUP
------------------------------------------------------
* Ensure your Python script is saved on your computer (e.g., as 'excel_ex.py').
* Ensure all the PXP Excel reports you want to consolidate are placed together in one folder.

2. OPEN YOUR COMMAND PROMPT

3. NAVIGATE TO YOUR SCRIPT
------------------------------------------------------
You need to tell the command prompt where your Python file lives using the 'cd' (change directory) command. 

4. RUN THE COMMAND
------------------------------------------------------
To run the tool, you will type 'python', followed by the name of your script, followed by the path to the folder holding your Excel files. 

5. FIND YOUR RESULTS
------------------------------------------------------
When the script says "Success!", it will generate a new file named "Consolidated_PXP_Report.xlsx". 


Currently working on:
------------------------------------------------------
* ERROR: "Failed to extract any data"
  Fix: Open your target Excel files and ensure they follow the exact same structural layout (Tags in rows 7-25, Min/Max/Std in rows 64/67/84).