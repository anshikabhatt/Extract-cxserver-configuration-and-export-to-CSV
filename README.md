# Extract-cxserver-configuration-and-export-to-CSV
This is my submission to the task #T331201.

This is a Python script that extracts the supported language pairs from CXServer configuration files and exports them to a CSV file.
### Please consider the mt-defaults.wikimedia.yaml file and what its effect might be on the supported translation pairs and default translation engine for each pair.
 the mt-defaults.wikimedia.yaml file provides default settings for machine translation services used in Wikimedia projects, including the Content Translation service. While it does not directly determine the supported translation pairs, it can be used as a fallback if no other engine is specified for a particular pair.

# Requirements
 Python 
 PyYAML module
 OS module
 CSV module
 
# Usage
 1. Clone or download this repository to your local machine.
 2. Install all the necessary module.
 3. Open the extract_config.py file in a text editor.
 4. Modify the CONFIG_DIR variable in line 10 to point to the directory containing the CXServer configuration files.
 5. Run the script to execute the file.
 6. The script will generate a file named supported_pairs.csv in the same directory as the extract.py file. 

# License
  This project is licensed under the MIT License - see the LICENSE file for details.


