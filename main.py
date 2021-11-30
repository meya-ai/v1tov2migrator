import os
import sys

from converter import convert, load_yaml

if __name__ == "__main__":
    dir_path = sys.argv[1]
    files = os.listdir(dir_path)
    for file in files:
        filename = file.split('.')[0]
        file_extension = file.split('.')[-1]
        if file_extension != "yaml":
            continue

        os.rename(f"{dir_path}/{filename}.yaml", f"{dir_path}/{filename}_converting.yaml")

        try:
            v1_yaml_obj = load_yaml(f"{dir_path}/{filename}_converting.yaml")
            if not convert(v1_yaml_obj, f"{dir_path}/{filename}.yaml"):
                os.rename(f"{dir_path}/{filename}_converting.yaml", f"{dir_path}/{filename}.yaml")
                continue

            os.rename(f"{dir_path}/{filename}_converting.yaml", f"{dir_path}/{filename}_old.yaml")
            print(f"{file}: successfully converted")

        except Exception as e:
            os.rename(f"{dir_path}/{filename}_converting.yaml", f"{dir_path}/{filename}.yaml")
            print(f"{file}: Convertion failed - {str(e)}")
#