import os

import create_pyd


def shell_run(cmd):
    print(cmd)
    with os.popen(cmd) as fp:
        bf = fp._stream.buffer.read()
    try:
        return bf.decode().strip()
    except UnicodeDecodeError:
        return bf.decode('gbk').strip()


def create_spec(cmd):
    shell_run(cmd)


def change_spec():
    with open('流量监测.spec', 'r', encoding='utf-8') as file:
        content = file.read()

    new_text = """
#**********************************************************************
# from pprint import pprint
# pprint(a.pure)

project_name = "net_io_count"

un_embed_exe = [x[1] for x in a.pure if project_name in x[1]]
print(un_embed_exe)

a.pure = [x for x in a.pure if project_name not in x[1]]
#**********************************************************************
pyz = PYZ(a.pure)
"""

    # pyinstaller 4.10
    # pattern = re.compile(
    #     r"pyz = PYZ\(a\.pure, a\.zipped_data,.*?cipher=block_cipher\)", re.DOTALL
    # )
    # # 使用sub函数替换匹配到的内容
    # new_content = re.sub(pattern, new_text, content)

    # # pyinstaller 6.5.0
    new_content = content.replace("pyz = PYZ(a.pure)", new_text)

    with open('流量监测.spec', 'w', encoding='utf-8') as file:
        file.write(new_content)


def run_spec(cmd):
    un_embed_py_list = eval(shell_run(cmd))
    print(un_embed_py_list)
    return un_embed_py_list


if __name__ == '__main__':
    # 关键字符串 正式项目中应设为全局变量
    # 项目文件名 net_io_count
    # 入口文件名：流量监测
    # 代码目录：project
    # pyd目录：pyd_cache

    # step 1: 生成pyd
    create_pyd.main()

    # step 2
    cmd = """

E:\developTool\Python\Python38\Scripts\pyi-makespec.exe -D -w 流量监测.py 
--contents-directory bin
--icon=".\\project\\asset\\logo.ico"
--add-data ".\\project\\asset\\*;.\\project\\asset" 
--add-data ".\\pyd_cache\\;.\\project"

""".replace("\n", " ")
    create_spec(cmd)

    # step 3
    change_spec()

    # step 4
    cmd = """
    
E:\developTool\Python\Python38\Scripts\pyinstaller.exe 流量监测.spec 
--distpath=./bundle/dist --workpath=./bundle/build -y

""".replace("\n", " ")
    run_spec(cmd)

    # step 5
    # os.remove("流量监测.spec")
