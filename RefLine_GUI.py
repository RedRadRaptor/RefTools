import Tkinter as tk
import RefSys as RS
import numpy as np
import os

def REFline_GUI(Frame):

    frm_userprops = tk.Frame(Frame, width=500, height=275)
    frm_userprops.pack()

    frm_output = tk.Frame(Frame, width=500, height=300, bg = "white")
    frm_output.pack()

    # Input Labels
    lbl_Ref = tk.Label(master=frm_userprops, text="Refrigerant:")
    lbl_Ref.place(x=0,y=0)

    lbl_Ftemp = tk.Label(master=frm_userprops, text="Fluid Temp(F):")
    lbl_Ftemp.place(x=0,y=30)

    lbl_Ltype = tk.Label(master=frm_userprops, text="Line Type:")
    lbl_Ltype.place(x=0, y=55)

    lbl_SST = tk.Label(master=frm_userprops, text="Sat Suct Temp(F):")
    lbl_SST.place(x=0, y=80)

    lbl_SCT = tk.Label(master=frm_userprops, text="Sat Cond Temp(F):")
    lbl_SCT.place(x=0, y=105)

    lbl_SLT = tk.Label(master=frm_userprops, text="Liquid Temp(F):")
    lbl_SLT.place(x=0, y=130)

    lbl_material = tk.Label(master=frm_userprops, text="Material:")
    lbl_material.place(x=0, y=155)

    lbl_Len = tk.Label(master=frm_userprops, text="Length(ft):")
    lbl_Len.place(x=0, y=185)

    # Output Labels for Titles
    lbl_Dia = tk.Label(master=frm_output, text="OD(inch):", bg="white", font='bold')
    lbl_Dia.place(x=0, y=0)
    
    lbl_Vel = tk.Label(master=frm_output, text="Velocity(ft/min):", bg="white", font='bold')
    lbl_Vel.place(x=75, y=0)

    lbl_Press = tk.Label(master=frm_output, text="Pressure Drop(psig):", bg="white", font='bold')
    lbl_Press.place(x=200, y=0)

    lbl_Re = tk.Label(master=frm_output, text="Reynolds Num:", bg="white", font='bold')
    lbl_Re.place(x=375, y=0)

    lbl_HorM = tk.Label(master=frm_userprops)
    lbl_HorM.place(x=250, y=80)

    lbl_Dens = tk.Label(master=frm_userprops)
    lbl_Dens.place(x=250, y=105)

    # Input Drop down menus
    ddm_Ref_var = tk.StringVar(master=frm_userprops)
    ddm_Ref_var.set("R404A")
    ddm_Ref = tk.OptionMenu(frm_userprops, ddm_Ref_var, "R404A", "R134A", "R407C")
    ddm_Ref.place(x=150,y=0)

    ddm_Ltype_var = tk.StringVar(master=frm_userprops)
    ddm_Ltype_var.set("Suct")
    ddm_Ltype = tk.OptionMenu(frm_userprops, ddm_Ltype_var, "Suct", "Liq", "Disch")
    ddm_Ltype.place(x=150,y=50)

    ddm_material_var = tk.StringVar(master=frm_userprops)
    ddm_material_var.set("CU-L")
    #######################################################################################
    #ADDING SCH 80 STEEL FUNCTIONALITY ("STL-SCH80")
    ddm_material = tk.OptionMenu(frm_userprops, ddm_material_var, "CU-L")
    ddm_material.place(x=150,y=155)
    #######################################################################################

    ddm_HorM_var = tk.StringVar(master=frm_userprops)
    ddm_HorM_var.set("Heat (BTU/h)")
    ddm_HorM = tk.OptionMenu(frm_userprops, ddm_HorM_var, "Heat (BTU/h)", "Mass Flow (lb/h)")
    ddm_HorM.place(x=0,y=210)

    # Input Entries

    ent_Ftemp = tk.Entry(master=frm_userprops, width=5)
    ent_Ftemp.place(x=150,y=30)

    ent_SST = tk.Entry(master=frm_userprops, width=5)
    ent_SST.place(x=150,y=80)

    ent_SCT = tk.Entry(master=frm_userprops, width=5)
    ent_SCT.place(x=150,y=105)

    ent_SLT = tk.Entry(master=frm_userprops, width=5)
    ent_SLT.place(x=150,y=130)

    ent_Len = tk.Entry(master=frm_userprops, width=5)
    ent_Len.place(x=150,y=185)

    ent_Heat = tk.Entry(master=frm_userprops, width=10)
    ent_Heat.place(x=150,y=215)
    
    # output labels
    lbl_HorM_out = tk.Label(master=frm_userprops)
    lbl_HorM_out.place(x=375, y=80)

    lbl_Dens_out = tk.Label(master=frm_userprops)
    lbl_Dens_out.place(x=375, y=105)
    
    
   
    def enter(event):
        Ref = ddm_Ref_var.get()
        Ftemp = float(ent_Ftemp.get())
        Ltype = ddm_Ltype_var.get()
        SST = float(ent_SST.get())
        SCT = float(ent_SCT.get())
        SLT = float(ent_SLT.get())
        material = ddm_material_var.get()
        Len = float(ent_Len.get())
        lbl_Dens["text"] = "Density (lb/ft^3):"
        lbl_Dens["bg"] = "cyan"
        
        if material == "CU-L":
            oDs = [0.375, 0.50, 0.625, 0.750, 0.875, 1.125, 1.375, 1.625, 2.125, 2.625, 3.125, 4.125, 6.125]
            iDs = [0.315, 0.43, 0.545, 0.666, 0.785, 1.025, 1.265, 1.505, 1.985, 2.465, 2.981, 3.897, 5.881]
        elif material == "STL-SCH80":
            oDs = [0.375, 0.50, 0.750, 1, 1.25, 1.50, 1.625, 2, 2.5, 3, 4, 6]
            iDs = [0.42, 0.55, 0.74, 0.96, 0.785, 1.28, 1.5, 1.94, 2.32, 2.9, 3.36, 3.86, 5.76]
        
        if ddm_HorM_var.get() == "Heat (BTU/h)":
            Heat = float(ent_Heat.get())
            MassF = None
            lbl_HorM["text"] = "Mass Flow (lb/h):"
            lbl_HorM["bg"] = "cyan"
        elif ddm_HorM_var.get() == "Mass Flow (lb/h)":
            MassF = float(ent_Heat.get())
            Heat = None
            lbl_HorM["text"] = "Heat (BTU/h):"
            lbl_HorM["bg"] = "cyan"
        
        Lprops = ["oD","vel", "press_drop", "Re"]
        j = 0
        y = 20
        for i in iDs:
            oD = oDs[j]
            prop = RS.FLine(Ref, Ftemp, Ltype, SST, SCT, SLT, i, material, Len, "Imp", mass_flow = MassF, HeatLoad = Heat)
            Lprop = np.concatenate((oD, prop[0]),axis=None)
            Lprops = np.row_stack((Lprops, Lprop))
            
            #out labels
            lbl_OD = tk.Label(master=frm_output, text=str(oD), bg="white")
            lbl_OD.place(x=0,y=y)
            
            lbl_vel = tk.Label(master=frm_output, text=str(round(Lprop[1],2)), bg="white")
            lbl_vel.place(x=75,y=y)
            
            lbl_press = tk.Label(master=frm_output, text=str(round(Lprop[2],2)), bg="white")
            lbl_press.place(x=200,y=y)
            
            lbl_Re = tk.Label(master=frm_output, text=str(round(Lprop[3],2)), bg="white")
            lbl_Re.place(x=375,y=y)
            
            j = j + 1
            y = y + 20
        Fprops = np.row_stack((["HeatLoad", "mass_flow", "F_dens"], prop[1]))
        if ddm_HorM_var.get() == "Mass Flow (lb/h)":
            lbl_HorM_out["text"] = str(round(float(Fprops[1,0]), 2))
        elif ddm_HorM_var.get() == "Heat (BTU/h)":
            lbl_HorM_out["text"] = str(round(float(Fprops[1,1]), 2))
        lbl_Dens_out["text"] = str(round(float(Fprops[1,2]), 4))
        lbl_HorM_out["bg"] = "cyan"
        lbl_HorM["fg"] = "black"
        lbl_Dens_out["bg"] = "cyan"
    def Ent_Error(event):
        lbl_HorM["text"] = "ENTRY ERROR"
        lbl_HorM["fg"] = "red"
    def Is_Empty():
        
        Ftemp = ent_Ftemp.get()
        SST = ent_SST.get()
        SCT = ent_SCT.get()
        SLT = ent_SLT.get()
        Len = ent_Len.get()
        if Ftemp != "" or SST != "" or SLT != "" or Len != "":
            button.bind("<Button-1>", enter)
        else:
            button.bind("<Button-1>", Ent_Error)
        
        Frame.after(100, Is_Empty)
    
    
    button = tk.Button(master=frm_userprops,text="Enter")
    button.place(x=150, y=250)
    Is_Empty()

if __name__ == "__main__":
    window = tk.Tk()
    work_direct = os.path.dirname(os.path.abspath(__file__))
    file = work_direct + r"\CTD_ico.ico"
    window.wm_iconbitmap(file)
    window.title("Refrigerant Line Sizing")
    REFline_GUI(window)
    
    window.mainloop()