import imp
import json
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
        py_filename = os.path.basename(py)
        msg = json.dumps({
            "filename": py_filename,
            "_py_m_file": py_m_time.__str__(), "pyd_m_file": pyd_m_time.__str__()
        }, indent=4)

        if py_m_time > pyd_m_time:
            need = NeedCompile(need_compile=True, msg=f"{msg}")
            os.remove(pyd)
        else:
            need = NeedCompile(need_compile=False, msg=f"{msg}")
    else:
        need = NeedCompile(need_compile=True, msg=f"pyd not exist")

    return need


def compile_pyd(py_filepath, pyd_filepath):
    filepath_exclude_ext = os.path.splitext(py_filepath)[0]
    os.chdir(os.path.dirname(py_filepath))

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
    os.rename(filepath_exclude_ext + imp.get_suffixes()[0][0], filepath_exclude_ext + ".pyd")
    shutil.move(filepath_exclude_ext + ".pyd", pyd_filepath)
    print(f"complete     {pyd_filepath} \n-----------------------\n")

    os.chdir(os.path.dirname(__file__))
    return pyd_filepath


def clean_pyd(pyd_list):
    for pyd in pyd_list:
        os.remove(pyd)


def main():
    project_dir = r"./project"
    pyd_dir = r"./pyd_cache"

    project_dir = os.path.abspath(project_dir)
    pyd_dir = os.path.abspath(pyd_dir)

    pyd_map = {}
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            if file.endswith('.py'):
                py = os.path.join(root, file)
                pyd = (py + "d").replace(project_dir, pyd_dir)
                os.makedirs(os.path.dirname(pyd), exist_ok=True)
                pyd_map[py] = pyd

    use_cache = []
    for py, pyd in pyd_map.items():
        compile_check = need_compile(py, pyd)
        if compile_check.need_compile:
            print(f"prepare compile -> {os.path.basename(py)}")
            print(compile_check.msg)
            compile_pyd(py, pyd)
        else:
            use_cache.append(pyd)

    if use_cache:
        print("The blow files use cache:")
        for cache in use_cache:
            print(cache)


if __name__ == '__main__':
    main()
