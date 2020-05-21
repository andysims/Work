"""
XY MAPS Upload Script
Reads specified folder contents to create Post request
Created: 5/8/2020 Andy Sims
Updated 5/12/2020 Andy Sims
"""

import os, requests

cityextentid = 'city-guid-id'
mainDirPath = "\\\\UNC\\Path\\To\\Local\\Files"

def get_sub_dirs():
    post_list = []
    if __name__ == "__main__":
        for (root, dirs, files) in os.walk(mainDirPath, topdown=True):
            if root != mainDirPath:
                post_dir = root.replace(mainDirPath, '').replace('\\\\', '/').replace('\\','/')
                file_list = [f for f in files]
                post_list.append({post_dir: file_list})
    return post_list

def post_file(file_path, file_name):
    url = 'https://api/location'
    path = mainDirPath + file_path + "/" + file_name
    postfiles = {'file': open(path, 'rb')}
    postdata = {'cityextentid': cityextentid, 'filepath': file_path}
    r = requests.post(url, files=postfiles, data=postdata)
    print(r.status_code)

def all_file_paths(file_list):
    for files in files_loc:
        for path, file in files.items():
            for f in file:
                print(path + '/' + f)
                post_file(path, f)

files_loc = get_sub_dirs()
all_file_paths(files_loc)