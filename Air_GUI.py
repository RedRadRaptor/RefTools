import Tkinter as tk
import RefSys as RS
import os

def Air_GUI(Frame):
    frm_in = tk.Frame(Frame, width=225, height=200)
    frm_in.pack()
    
    #Entry drop down menus
    ddm_Air1_var = tk.StringVar(master=frm_in)
    ddm_Air1_var.set("TDB")
    ddm_Air1 = tk.OptionMenu(frm_in, ddm_Air1_var, "TDB", "TWB", "RH")
    ddm_Air1.place(x=0,y=0)
    
    ddm_Air2_var = tk.StringVar(master=frm_in)
    ddm_Air2_var.set("TWB")
    ddm_Air2 = tk.OptionMenu(frm_in, ddm_Air2_var, "TDB", "TWB", "RH")
    ddm_Air2.place(x=0,y=25)
    
    #3rd label that adjusts to the other two option menus
    lbl_Air3 = tk.Label(master=frm_in, text = "RH(%)", width = 5)
    lbl_Air3.place(x=0,y=60)
    
    #User inputs
    ent_Air1 = tk.Entry(master=frm_in, width = 6)
    ent_Air1.place(x=100,y=0)
    ent_Air1.insert(0,"0")
    
    ent_Air2 = tk.Entry(master=frm_in, width = 6)
    ent_Air2.place(x=100,y=25)
    ent_Air2.insert(0,"0")
    
    #output
    lbl_Air3_out = tk.Label(master=frm_in)
    lbl_Air3_out.place(x=100,y=60)
    
    def Air3():
        A1 = ddm_Air1_var.get()
        A2 = ddm_Air2_var.get()
        if (A1=="TDB" and A2=="TWB") or (A1=="TWB" and A2=="TDB"):
            lbl_Air3["text"]= "RH"
        elif (A1=="RH" and A2=="TDB") or (A1=="TDB" and A2=="RH"):
            lbl_Air3["text"]="TWB"
        elif (A1=="RH" and A2=="TWB") or (A1=="TWB" and A2=="RH"):
            lbl_Air3["text"]="TDB"
        elif (A1=="RH" and A2=="RH") or (A1=="TWB" and A2=="TWB") or (A1=="TDB" and A2=="TDB"):
            lbl_Air3["text"]="Error"
        Frame.after(100, Air3)
        
    def RH_calc(event):
        A1 = ddm_Air1_var.get()
        A2 = ddm_Air2_var.get()
        A1_ent = float(ent_Air1.get())
        A2_ent = float(ent_Air2.get())
        if (A1=="TDB" and A2=="TWB") or (A1=="TWB" and A2=="TDB"):
            if A1=="TDB":
                TDB = A1_ent
                TWB = A2_ent
                A3 = RS.T_or_RH("RH",TWB=TWB, TDB=TDB)
            else:
                TWB = A1_ent
                TDB = A2_ent
                A3 = RS.T_or_RH("RH",TWB=TWB, TDB=TDB)
        elif (A1=="RH" and A2=="TDB") or (A1=="TDB" and A2=="RH"):
            if A1=="TDB":
                TDB = A1_ent
                RH = A2_ent
                A3 = RS.T_or_RH("TWB",RH=RH, TDB=TDB)
            else:
                RH = A1_ent
                TDB = A2_ent
                A3 = RS.T_or_RH("TWB",RH=RH, TDB=TDB)
        elif (A1=="RH" and A2=="TWB") or (A1=="TWB" and A2=="RH"):
            if A1=="TWB":
                TWB = A1_ent
                RH = A2_ent
                A3 = RS.T_or_RH("TDB",RH=RH, TWB=TWB)
            else:
                RH = A1_ent
                TWB = A2_ent
                A3 = RS.T_or_RH("TDB",RH=RH, TWB=TWB)
        lbl_Air3_out["text"]=str(A3)
    
    button = tk.Button(master=frm_in,text="Enter")
    button.bind("<Button-1>", RH_calc)
    button.place(x=50, y=100)
    Air3()
    

if __name__ == "__main__":
    window = tk.Tk()
    work_direct = os.path.dirname(os.path.abspath(__file__))
    file = work_direct + r"\CTD_ico.ico"
    window.wm_iconbitmap(file)
    window.title("Air Calcs")
    Air_GUI(window)
    
    window.mainloop()