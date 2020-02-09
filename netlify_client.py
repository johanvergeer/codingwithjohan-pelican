import json
import os
import pprint
from typing import Iterable
from zipfile import ZipFile

import requests
from requests import Response


class NetlifyClient:
    def __init__(self, site: str, token: str):
        self.site = site
        self.token = token
        self.pp = pprint.PrettyPrinter(indent=4)

    def deploy(self, build_dir: str):
        zip_file = create_zip(build_dir)

        url = f"https://api.netlify.com/api/v1/sites/{self.site}.netlify.com/deploys"
        headers = {
            "Content-Type": "application/zip",
            "Authorization": f"Bearer {self.token}",
        }

        with open(zip_file.filename, "rb") as output:
            bytes_output = output.read()

            response: Response = requests.post(url, data=bytes_output, headers=headers)

            response_dict = json.loads(response.text)
            self.pp.pprint(response_dict)


# Declare the function to return all file paths of the particular directory
def retrieve_file_paths(dir_name: str) -> Iterable[str]:
    # setup file paths variable
    file_paths = []

    # Read all directory, subdirectories and file lists
    for root, directories, files in os.walk(dir_name):
        for filename in files:
            # Create the full filepath by using os module.
            file_path = os.path.join(root, filename)
            file_paths.append(file_path)

    # return all paths
    return file_paths


def create_zip(dir_name: str) -> ZipFile:
    # Call the function to retrieve all files and folders of the assigned directory
    file_path = retrieve_file_paths(dir_name)

    # printing the list of all files to be zipped
    print("The following list of files will be zipped:")
    for fileName in file_path:
        print(fileName)

    # writing files to a zipfile
    zip_file = ZipFile(dir_name + ".zip", "w")
    with zip_file:
        # writing each file one by one
        for file in file_path:
            zip_file.write(file)

    return zip_file
