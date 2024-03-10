import os
import shutil
import subprocess


def need_compile(py, pyd):
    """
    need=True:
        1. pyd不存在
        2. pyd存在但是py修改时间小于pyd创建时间
    need=False:
        1.pyd存在但是py修改时间大于pyd创建时间
    """
    if os.path.exists(pyd):
        if os.path.getmtime(py) > os.path.getctime(pyd):
            need = True
            os.remove(pyd)
        else:
            need = False
    else:
        need = True

    return need


def compile_pyd(py_filepath, pyd_filepath):
    filepath_exclude_ext = os.path.splitext(py_filepath)[0]
    os.chdir(os.path.dirname(py_filepath))

    if not need_compile(py_filepath, pyd_filepath):
        print(f"not need compile {py_filepath} -> {pyd_filepath}")
    else:
        print(f"need compile {py_filepath} -> {pyd_filepath}")

        # os.popen(f"easycython --no-annotation {py_filepath}").read()
        process = subprocess.Popen(
            f"E:\developTool\Python\Python38\Scripts\easycython.exe --no-annotation {py_filepath}",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            # shell==True 接收字符串,shell==False 接收数组
            shell=True
        )

        stdout, stderr = process.communicate()

        # # TODO：异常处理
        # if process.returncode != 0:
        #     return

        shutil.rmtree("build")
        os.remove(filepath_exclude_ext + ".c")
        os.rename(filepath_exclude_ext + ".cp38-win_amd64.pyd", filepath_exclude_ext + ".pyd")
        shutil.move(filepath_exclude_ext + ".pyd", pyd_filepath)

    os.chdir(os.path.dirname(__file__))
    return pyd_filepath


def clean_pyd(pyd_list):
    for pyd in pyd_list:
        os.remove(pyd)


def main():
    project_dir = r".\project"
    project_dir = os.path.abspath(project_dir)
    print(project_dir)
    py_files = []
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            if file.endswith('.py'):
                py_files.append(os.path.join(root, file))

    pyd_files = []
    for py_file in py_files:
        dir_name = os.path.dirname(py_file).replace("project", "pyd_cache")
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        filename_exclude_ext = os.path.splitext(os.path.basename(py_file))[0]
        pyd_filename = filename_exclude_ext + ".pyd"
        pyd_files.append(os.path.join(dir_name, pyd_filename))

    pyd_map = dict(zip(py_files, pyd_files))
    for py, pyd in pyd_map.items():
        compile_pyd(py, pyd)


if __name__ == '__main__':
    main()
