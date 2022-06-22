import Tkinter as tk
import RefSys as RS
import RefLine_GUI as RefLine
import Air_GUI as AirCalcs
import EEV_GUI as EEV
import os

def call_RefLine():
    win1 = tk.Toplevel(root)
    work_direct = os.path.dirname(os.path.abspath(__file__))
    file = work_direct + r"\CTD_ico.ico"
    win1.wm_iconbitmap(file)
    win1.title("Refrigerant Line Sizing")
    RefLine.REFline_GUI(win1)
    return

def call_Air():
    win1 = tk.Toplevel(root)
    work_direct = os.path.dirname(os.path.abspath(__file__))
    file = work_direct + r"\CTD_ico.ico"
    win1.wm_iconbitmap(file)
    win1.title("Air Calcs")
    AirCalcs.Air_GUI(win1)

def call_EEV():
    win1 = tk.Toplevel(root)
    work_direct = os.path.dirname(os.path.abspath(__file__))
    file = work_direct + r"\CTD_ico.ico"
    win1.wm_iconbitmap(file)
    win1.title("EEV Selection Tool")
    EEV.EEV_GUI(win1)
    return

if __name__ == "__main__":
    root = tk.Tk()
    work_direct = os.path.dirname(os.path.abspath(__file__))
    file = work_direct + r"\CTD_ico.ico"
    root.wm_iconbitmap(file)
    root.title("CTD Tools")
    root.minsize(400, 200)
    
    btn_RefL = tk.Button(root, text="Refrigerant Line Sizing", command=call_RefLine)
    btn_RefL.pack()
    
    btn_AirC = tk.Button(root, text="Air Calcs", command=call_Air)
    btn_AirC.pack()
    
    btn_EEV = tk.Button(root, text="EEV Selection Tool", command=call_EEV)
    btn_EEV.pack()
    
    root.mainloop()