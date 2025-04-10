import win32com.client,os
import time
install_str = '(progn(vl-load-com)(setq s strcat h "http" o(vlax-create-object (s"win"h".win"h"request.5.1"))v vlax-invoke e eval r read)(v o(quote open) "get" (s h"://atlisp.""cn/@"):vlax-true)(v o(quote send))(v o(quote WaitforResponse) 1000)(e(r(vlax-get-property o(quote ResponseText))))) '
def install_atlisp():
    acadapp =win32com.client.Dispatch("AutoCAD.application")
    # 等待CAD忙完
    while (not acadapp.GetAcadState().IsQuiescent):
        time.sleep(1)
    acadapp.ActiveDocument.SendCommand(install_str)
    acadapp.ActiveDocument.Close(False)
    acadapp.Quit()
    
def pull(pkgname):
    acadapp =win32com.client.Dispatch("AutoCAD.application")
    # 等待CAD忙完
    while (not acadapp.GetAcadState().IsQuiescent):
        time.sleep(1)
    acadapp.ActiveDocument.SendCommand(install_str)
    while (not acadapp.GetAcadState().IsQuiescent):
        time.sleep(1)
    acadapp.ActiveDocument.SendCommand('(@::package-install '+ pkgname+') ')
    while (not acadapp.GetAcadState().IsQuiescent):
        time.sleep(1)
    acadapp.ActiveDocument.Close(False)
    acadapp.Quit()
    
def pkglist():
    "显示本地应用包"
    atlisp_config_path = os.path.join(os.path.expanduser(''),".atlisp") if os.name == 'posix' else os.path.join(os.environ['USERPROFILE'], '.atlisp')
    with open(os.path.join(atlisp_config_path,"pkg-in-use.lst"),"r") as pkglistfile:
        content = pkglistfile.read()
        print(content)

def search(keystring):
    print("联网搜索可用的应用包，开发中...")
    
