import sys
import argparse
from .install import install_atlisp
from .pull import pull
# from .search import search
parser = argparse.ArgumentParser(description='@lisp是一个运行于 AutoCAD、中望CAD、浩辰CAD及类似兼容的CAD系统中的应用管理器。')
parser.add_argument("pull",help="安装@lisp包")
parser.add_argument("install",help="安装@lisp Core到CAD")
parser.add_argument("list",help="列已安装的@lisp包")
parser.add_argument("search",help="搜索 @lisp包")

def main():
    """Entry point for the application script"""
    # target_function(*args,**kwargs)
    if len(sys.argv)>1:
        if sys.argv[1]  ==  "pull":
            if len(sys.argv)>2:
                print("安装  " + sys.argv[2] + "到CAD ")
            else:
                print("Usage: atlisp pull pkgname")
                print("请指定包名pkgname .")
                print("示例: atlisp pull at-pm")
        elif sys.argv[1]  ==  "install":
            print("安装@lisp到CAD中")
            install_atlisp();
        elif sys.argv[1]  ==  "list":
            print("列本地包 ")
        elif sys.argv[1]  ==  "search":
            if len(sys.argv)>2:
                print("搜索  " + sys.argv[2])
            else:
                 print("Usage: atlisp search keystr")
                 print("请给出要搜索的关键字")
                 print("示例: atlisp search pdf")
        else:
            print("未知命令 "+ sys.argv[1])
    else:
        parser.print_help()

    
    
