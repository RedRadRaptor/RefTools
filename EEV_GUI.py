import Tkinter as tk
import RefSys as RS
import os

def EEV_GUI(Frame):
    
    #Frame setup
    frm_userprops = tk.Frame(Frame, width=300, height=225)
    frm_userprops.pack()

    frm_output = tk.Frame(Frame, width=300, height=275, bg = "white")
    frm_output.pack()
    
    #Input Labels
    lbl_Ref = tk.Label(master=frm_userprops, text="Refrigerant:")
    lbl_Ref.place(x=0,y=0)
    
    lbl_MFG = tk.Label(master=frm_userprops, text="Valve Manufacturer:")
    lbl_MFG.place(x=0,y=30)
    
    lbl_Heat = tk.Label(master=frm_userprops, text="Heat Load (BTU/h):")
    lbl_Heat.place(x=0,y=60)
    
    lbl_SST = tk.Label(master=frm_userprops, text="SST(F):")
    lbl_SST.place(x=0,y=85)
    
    lbl_SCT = tk.Label(master=frm_userprops, text="SCT(F):")
    lbl_SCT.place(x=0,y=110)
    
    lbl_hpress = tk.Label(master=frm_userprops, text="High Side Press (psi):")
    lbl_hpress.place(x=0,y=135)
    
    lbl_dpress = tk.Label(master=frm_userprops, text="Dist. Press (psi):")
    lbl_dpress.place(x=0,y=160)
    
    # Input Drop down menus
    ddm_Ref_var = tk.StringVar(master=frm_userprops)
    ddm_Ref_var.set("R404A")
    ############Add more refrigerants##################
    ddm_Ref = tk.OptionMenu(frm_userprops, ddm_Ref_var, "R404A", "R452A")
    ddm_Ref.place(x=150,y=0)
    
    ddm_MFG_var = tk.StringVar(master=frm_userprops)
    ddm_MFG_var.set("Sporlan")
    ############Add more VLV MFGs##################
    ddm_MFG = tk.OptionMenu(frm_userprops, ddm_MFG_var, "Sporlan", "Danfoss")
    ddm_MFG.place(x=150,y=30)
    
    #Input Entries
    ent_Heat = tk.Entry(master=frm_userprops, width=10)
    ent_Heat.place(x=150,y=60)
    
    ent_SST = tk.Entry(master=frm_userprops, width=5)
    ent_SST.place(x=150,y=85)
    
    ent_SCT = tk.Entry(master=frm_userprops, width=5)
    ent_SCT.place(x=150,y=110)
    
    ent_hpress = tk.Entry(master=frm_userprops, width=5)
    ent_hpress.place(x=150,y=135)
    
    ent_dpress = tk.Entry(master=frm_userprops, width=5)
    ent_dpress.place(x=150,y=160)
    
    # Output Labels for Titles
    lbl_TVLVpress = tk.Label(master=frm_output, text="Valve Press Drop (psi):", bg="white")
    lbl_TVLVpress.place(x=0, y=0)

    lbl_VLV1 = tk.Label(master=frm_output, bg="white")
    lbl_VLV1.place(x=0, y=25)

    lbl_VLV2 = tk.Label(master=frm_output, bg="white")
    lbl_VLV2.place(x=0, y=50)

    lbl_VLV3 = tk.Label(master=frm_output, bg="white")
    lbl_VLV3.place(x=0, y=75)

    lbl_VLV4 = tk.Label(master=frm_output, bg="white")
    lbl_VLV4.place(x=0, y=100)

    lbl_VLV5 = tk.Label(master=frm_output, bg="white")
    lbl_VLV5.place(x=0, y=125)
    
    lbl_VLV6 = tk.Label(master=frm_output, bg="white")
    lbl_VLV6.place(x=0, y=150)
    
    lbl_VLV7 = tk.Label(master=frm_output, bg="white")
    lbl_VLV7.place(x=0, y=175)
    
    lbl_VLV8 = tk.Label(master=frm_output, bg="white")
    lbl_VLV8.place(x=0, y=200)
    
    lbl_VLV9 = tk.Label(master=frm_output, bg="white")
    lbl_VLV9.place(x=0, y=225)
    
    # output labels
    lbl_VLVpress = tk.Label(master=frm_output, bg="white")
    lbl_VLVpress.place(x=150, y=0)

    lbl_MDL1 = tk.Label(master=frm_output, bg="white")
    lbl_MDL1.place(x=150, y=25)

    lbl_MDL2 = tk.Label(master=frm_output, bg="white")
    lbl_MDL2.place(x=150, y=50)

    lbl_MDL3 = tk.Label(master=frm_output, bg="white")
    lbl_MDL3.place(x=150, y=75)

    lbl_MDL4 = tk.Label(master=frm_output, bg="white")
    lbl_MDL4.place(x=150, y=100)

    lbl_MDL5 = tk.Label(master=frm_output, bg="white")
    lbl_MDL5.place(x=150, y=125)
    
    lbl_MDL6 = tk.Label(master=frm_output, bg="white")
    lbl_MDL6.place(x=150, y=150)
    
    lbl_MDL7 = tk.Label(master=frm_output, bg="white")
    lbl_MDL7.place(x=150, y=175)
    
    lbl_MDL8 = tk.Label(master=frm_output, bg="white")
    lbl_MDL8.place(x=150, y=200)
    
    lbl_MDL9 = tk.Label(master=frm_output, bg="white")
    lbl_MDL9.place(x=150, y=225)

    def enter(event):
        Ref = ddm_Ref_var.get()
        MFG = ddm_MFG_var.get()
        Heat = float(ent_Heat.get())
        SST = float(ent_SST.get())
        SCT = float(ent_SCT.get())
        hpress = float(ent_hpress.get())
        dist_press = float(ent_dpress.get())
    
        EEVs = RS.EEV_Select(MFG, Ref, Heat, SST, SCT, hpress, dist_press)
        
        load = EEVs[1:,1]
        bg = []
        VLV_loads = []
        for i in load:
            VLV_load = round(float(i),3) * 100
            if VLV_load > 100:
                bg = bg + ["red"]
            elif 100>= VLV_load > 80:
                bg = bg + ["yellow"]
            elif 80 >= VLV_load > 50:
                bg = bg + ["green"]
            elif 50 >= VLV_load > 30:
                bg = bg + ["white"]
            elif 30 >= VLV_load > 0:
                bg = bg + ["cyan"]
            VLV_load = str(VLV_load)
            VLV_loads = VLV_loads + [VLV_load]
        if MFG == "Sporlan":
            #VLV Model
            lbl_VLV1["text"] = "SER-B(%):"
            lbl_VLV2["text"] = "SER-C(%):"
            lbl_VLV3["text"] = "SER-D(%):"
            lbl_VLV4["text"] = "SERI-G(%):"
            lbl_VLV5["text"] = "SERI-J(%):"
            lbl_VLV6["text"] = "SERI-K(%):"
            lbl_VLV7["text"] = "SERI-L(%):"
            lbl_VLV8["text"] = "SEHI-175(%):"
            lbl_VLV9["text"] = "SEHI-400(%):"
            
            # output labels
            lbl_VLVpress["text"] = str(round(float(EEVs[0,1]),3))
            lbl_MDL1["text"] = VLV_loads[0]
            lbl_MDL2["text"] = VLV_loads[1]
            lbl_MDL3["text"] = VLV_loads[2]
            lbl_MDL4["text"] = VLV_loads[3]
            lbl_MDL5["text"] = VLV_loads[4]
            lbl_MDL6["text"] = VLV_loads[5]
            lbl_MDL7["text"] = VLV_loads[6]
            lbl_MDL8["text"] = VLV_loads[7]
            lbl_MDL9["text"] = VLV_loads[8]
            
            lbl_MDL1["bg"] = bg[0]
            lbl_MDL2["bg"] = bg[1]
            lbl_MDL3["bg"] = bg[2]
            lbl_MDL4["bg"] = bg[3]
            lbl_MDL5["bg"] = bg[4]
            lbl_MDL6["bg"] = bg[5]
            lbl_MDL7["bg"] = bg[6]
            lbl_MDL8["bg"] = bg[7]
            lbl_MDL9["bg"] = bg[8]
        elif MFG == "Danfoss":
            #VLV Model
            lbl_VLV1["text"] = "ETS6-8(%):"
            lbl_VLV2["text"] = "ETS6-10(%):"
            lbl_VLV3["text"] = "ETS6-14(%):"
            lbl_VLV4["text"] = "ETS6-18(%):"
            lbl_VLV5["text"] = "ETS6-25(%):"
            lbl_VLV6["text"] = "ETS6-32(%):"
            lbl_VLV7["text"] = "ETS6-40(%):"
            
            # output labels
            lbl_VLVpress["text"] = str(round(float(EEVs[0,1]),3))
            lbl_MDL1["text"] = VLV_loads[0]
            lbl_MDL2["text"] = VLV_loads[1]
            lbl_MDL3["text"] = VLV_loads[2]
            lbl_MDL4["text"] = VLV_loads[3]
            lbl_MDL5["text"] = VLV_loads[4]
            lbl_MDL6["text"] = VLV_loads[5]
            lbl_MDL7["text"] = VLV_loads[6]
            
            lbl_MDL1["bg"] = bg[0]
            lbl_MDL2["bg"] = bg[1]
            lbl_MDL3["bg"] = bg[2]
            lbl_MDL4["bg"] = bg[3]
            lbl_MDL5["bg"] = bg[4]
            lbl_MDL6["bg"] = bg[5]
            lbl_MDL7["bg"] = bg[6]
    button = tk.Button(master=frm_userprops,text="Enter")
    button.bind("<Button-1>", enter)
    button.place(x=150, y=190)

if __name__ == "__main__":
    window = tk.Tk()
    work_direct = os.path.dirname(os.path.abspath(__file__))
    file = work_direct + r"\CTD_ico.ico"
    window.wm_iconbitmap(file)
    window.title("EEV Selection Tool")
    EEV_GUI(window)
    
    window.mainloop()