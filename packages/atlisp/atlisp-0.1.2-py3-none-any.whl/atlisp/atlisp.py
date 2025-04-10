import win32com.client
import time

def install_atlisp():
    acadapp =win32com.client.Dispatch("AutoCAD.application")
    # 等待CAD忙完
    while (not acadapp.GetAcadState().IsQuiescent):
        time.sleep(1)
    acadapp.ActiveDocument.SendCommand('(progn(vl-load-com)(setq s strcat h "http" o(vlax-create-object (s"win"h".win"h"request.5.1"))v vlax-invoke e eval r read)(v o(quote open) "get" (s h"://atlisp.""cn/@"):vlax-true)(v o(quote send))(v o(quote WaitforResponse) 1000)(e(r(vlax-get-property o(quote ResponseText))))) ')
    acadapp.ActiveDocument.Close(False)
    acadapp.Quit()
    
