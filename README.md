# OPSWAT MetaDefender

**Program to scan file using OPSWAT MetaDenfer API.**
Program takes file input that needs to be scanned. It calculates the hash value of the given file and perfom hash lookup and see if the file was scanned previously. If true, retieve and print the scan report. If not scanned, upload the file to meta defender and store the unique data_id obtained from upload. Using the data_id retreive the scan report.

### To run this program
* Requires python 3
* Enter your API key in metadefender_api.py file
* File to be scanned should be in scanfile directory
* To install packages run the command in root directory:
    * Unix/macOS: python3 -m pip install -r requirements.txt
    * Windows: py -m pip install -r requirements.txt
* To scan file, cd scanfile and enter command:
    * Unix/macOS: python3 scan_file.py file_to_scan.extension
    * Windows: py scan_file.py file_to_scan.extension
