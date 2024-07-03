
import os, shutil


def copy_stuff(src, dst):

    if not os.path.exists(dst):
        os.mkdir(dst)

    file_list = os.listdir(src)
    for file in file_list:
        from_path = os.path.join(src, file)
        to_path = os.path.join(dst, file)
        print(f" * {from_path} -> {to_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dst)
        else:
            copy_stuff(from_path, to_path)
        

    