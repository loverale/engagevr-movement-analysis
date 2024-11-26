import zipfile

print("todo:// implement")

newlist = []

def unzip_files_test(folder_path):
    with zipfile.ZipFile("./processed_files/stream0", 'r') as zr:
        zr.extractall("./unzip_tests/")
    print("testing unzipping")



unzip_files_test("./doesnt/matter")