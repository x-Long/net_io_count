import os
import shutil
import subprocess
from datetime import datetime
from typing import NamedTuple


def get_m_time(file_path):
    timestamp = os.path.getmtime(file_path)
    return datetime.fromtimestamp(timestamp)


class NeedCompile(NamedTuple):
    msg: str
    need_compile: bool


def need_compile(py, pyd):
    """
    need=True:
        1. pyd不存在
        2. pyd存在但是py修改时间小于pyd修改时间
    need=False:
        1.pyd存在但是py修改时间大于pyd修改时间
    """

    if os.path.exists(pyd):
        py_m_time = get_m_time(py)
        pyd_m_time = get_m_time(pyd)

        if py_m_time > pyd_m_time:
            need = NeedCompile(
                need_compile=True,
                msg=f"需要重新编译，py 修改时间大于 pyd 修改时间 py {py_m_time} pyd {pyd_m_time}"
            )
            os.remove(pyd)
        else:
            need = NeedCompile(
                need_compile=False,
                msg=f"不需要重新编译，py 修改时间小于 pyd 修改时间 {py_m_time} pyd {pyd_m_time}"
            )
    else:
        need = NeedCompile(
            need_compile=True,
            msg="not exist"
        )

    return need


def compile_pyd(py_filepath, pyd_filepath):
    filepath_exclude_ext = os.path.splitext(py_filepath)[0]
    os.chdir(os.path.dirname(py_filepath))

    need = need_compile(py_filepath, pyd_filepath)
    print(need.msg)

    if not need.need_compile:
        print(f"not need compile {py_filepath} -> {pyd_filepath}\n")
    else:
        print(f"need compile {py_filepath} -> {pyd_filepath}")
        print(f"compiling... {py_filepath}")

        process = subprocess.Popen(
            f"easycython.exe --no-annotation {py_filepath}",
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
        print(f"complete {py_filepath} \n")

    os.chdir(os.path.dirname(__file__))
    return pyd_filepath


def clean_pyd(pyd_list):
    for pyd in pyd_list:
        os.remove(pyd)


def main():
    project_dir = r".\project"
    project_dir = os.path.abspath(project_dir)
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
