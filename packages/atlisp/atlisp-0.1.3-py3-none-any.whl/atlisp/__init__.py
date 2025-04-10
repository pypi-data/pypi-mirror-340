import sys
import argparse
from .atlisp import install_atlisp,pull,pkglist,search

# from .search import search
parser = argparse.ArgumentParser(
    prog="atlisp",usage="%(prog) command <pkgname/keystring>",
    description='@lisp是一个运行于 AutoCAD、中望CAD、浩辰CAD及类似兼容的CAD系统中的应用管理器。')
parser.add_argument("command",help="执行 atlisp 命令")

help_str = """usage: atlisp.exe command <pkgname/keystring>
@lisp是一个运行于 AutoCAD、中望CAD、浩辰CAD及类似兼容的CAD系统中的应用管理器。

command       function:
  pull        安装@lisp包 到 CAD
  install     安装@lisp Core 到 CAD
  list        列已安装的@lisp包
  search      联网搜索 @lisp 包

options:
  -h, --help  show this help message and exit
"""

def main():
    # target_function(*args,**kwargs)
    if len(sys.argv)>1:
        if sys.argv[1]  ==  "pull":
            if len(sys.argv)>2:
                print("安装  " + sys.argv[2] + "到CAD ")
                pull(sys.argv[2])
                print("......完成")
            else:
                print("Usage: atlisp pull pkgname")
                print("请指定包名pkgname")
                print("示例: atlisp pull at-pm")
        elif sys.argv[1]  ==  "install" or sys.argv[1]=="i":
            print("安装@lisp到CAD中")
            install_atlisp();
        elif sys.argv[1]  ==  "list" or sys.argv[1]=="l":
            print("已安装的应用包:")
            pkglist()
        elif sys.argv[1]  ==  "search" or sys.argv[1]=="s":
            if len(sys.argv)>2:
                print("搜索  " + sys.argv[2])
                search(sys.argv[2])
            else:
                 print("Usage: atlisp search keystring")
                 print("请给出要搜索的关键字")
                 print("示例: atlisp search pdf")
        elif sys.argv[1]=="-h" or sys.argv[1]=="--help":
            print(help_str)
        else:
            print("未知命令 "+ sys.argv[1])
    else:
        #parser.print_help()
        print(help_str)

    
