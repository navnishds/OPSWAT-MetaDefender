from metadefender_api import MetaDefenderApi
import hashlib
import sys
import os


# calculate hash value for the file
def calculate_hash(file_name):

    sha256_hash = hashlib.sha256()
    block_size = 4096
    with open(file_name, "rb") as f:
        # read and update hash string value in blocks of 4K
        for chunk in iter(lambda: f.read(block_size), b""):
            sha256_hash.update(chunk)
    f.close()

    return sha256_hash.hexdigest().upper()


# print scan report
def display_scan_report(scan_report):

    print("\nScan Report")

    if 'display_name' in scan_report['file_info']:
        print("\nfilename:", scan_report['file_info']['display_name'])
    print("overall_status:", scan_report['scan_results']['scan_all_result_a'])

    for engine, result in scan_report['scan_results']['scan_details'].items():
        print("\nengine:", engine)

        if result['scan_result_i'] == 0:
            print("threat_found: Clean")
        else:
            print('threat_found:', result['threat_found'])

        print("scan_result:", result['scan_result_i'])
        print("def_time:", result['def_time'])


# check if input file is valid and return file
def get_file():

    # check if file to be scanned is given as an argument
    if len(sys.argv) < 2:
        print("Error: Enter file name in same directory or path to file as a command line argument")
        sys.exit(1)

    # file to scan
    file_name = sys.argv[1]

    # check if file is valid or not
    try:
        open(file_name, 'r')
    except IOError:
        print("Error: File does not exist")
        sys.exit(1)

    # check if file size is greater than 140 MB
    file_size = os.path.getsize(file_name)
    # convert byte to megabyte
    file_size = file_size / (1024 * 1024.0)
    if file_size > 140.0:
        print("Error: File size greater than 140 MB")
        sys.exit(1)

    return file_name


def scan_file():

    file_name = get_file()

    # create MetaDefenderApi object
    meta_defender_api = MetaDefenderApi()

    # calculate hash value of the given file
    hash_value = calculate_hash(file_name)

    # check if there are previously cached results for the file
    scan_report = meta_defender_api.hash_lookup(hash_value)

    # if file is not scanned previously, upload file and get scan report
    if not scan_report:
        data_id = meta_defender_api.upload_file(file_name)
        scan_report = meta_defender_api.retrieve_scan_report(data_id)

    display_scan_report(scan_report)


scan_file()
