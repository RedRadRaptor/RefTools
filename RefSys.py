import math
import sys
import CoolProp.CoolProp as CP
from CoolProp.CoolProp import PropsSI, HAPropsSI
import numpy as np
import pickle
import pandas as pd
import os

def Unit_Convert(value, unit, n_unit):
    
    value = float(value)
    if unit == "F" and n_unit == "C":
        conv_U = 5*(value - 32)/9
    elif unit == "F" and n_unit == "K":
        conv_U = ((value-32)*5)/9 + 273.15
    elif unit == "K" and n_unit == "F":
        conv_U = (value - 273.15) * (1.8) + 32
    elif unit == "C" and n_unit == "F":
        conv_U = (value * 1.8) + 32
    elif unit == "Pa" and n_unit == "psia":
        conv_U = value/6895
    elif unit == "psia" and n_unit == "Pa":
        conv_U = value * 6895
    elif unit == "J/kg" and n_unit == "BTU/lb":
        conv_U = value/2326
    elif unit == "BTU/lb" and n_unit == "J/kg":
        conv_U = value * 2326
    elif unit == "kg/m3" and n_unit == "lb/ft3":
        conv_U = value / 16.018
    elif unit == "lb/ft3" and n_unit == "kg/m3":
        conv_U = value * 16.018
    elif unit == "Pas" and n_unit == "lb/fts":
        conv_U = value * 0.671968994813
    elif unit == "lb/fts" and n_unit == "Pas":
        conv_U = value / 0.671968994813
    return conv_U

# function used to solve for either: dry bulb temperature (TBD), wet bulb temperature (TWB), or relative humidity (RH)
# Requires an output "condition" (required input)
# Requires a unit spec (either F/C)
def T_or_RH(condition, TDB = None, TWB = None, RH = None):
    
    if condition == "RH":
        TDB = Unit_Convert(TDB, "F","C")
        TWB = Unit_Convert(TWB, "F","C")
        if TWB is None or TDB is None:
            sys.exit("Entry Error - TBD or TWB is required to calculate RH")
        elif (TDB and TWB) is not None:
            output = 100*(math.exp(17.625*TWB/(243.04+TWB))/math.exp(17.625*TDB/(243.04+TDB)))
    elif condition == "TWB":
        TDB = Unit_Convert(TDB, "F","C")
        if TDB is None or RH is None:
            sys.exit("Entry Error - TBD or RH is required to calculate RH")
        elif (TDB and RH) is not None:
            output = 243.04*(math.log(RH/100)+((17.625*TDB)/(243.04+TDB)))/(17.625-math.log(RH/100)-((17.625*TDB)/(243.04+TDB)))
    elif condition == "TDB":
        TWB = Unit_Convert(TWB, "F","C")
        if TWB is None or RH is None:
            sys.exit("Entry Error - TWB or RH is required to calculate RH")
        elif (TWB and RH) is not None:
            output = 243.04*(((17.625*TWB)/(243.04+TWB))-math.log(RH/100))/(17.625+math.log(RH/100)-((17.625*TWB)/(243.04+TWB)))
    return output

def FluidCheck(Fluid):
    refrigs = ["R404A", "R134A", "R407C"]
    H20 = ["Prop_Gly", "Eth_Gly", "Water"]
    
    if Fluid in refrigs:
        F_Type = "REF"
    elif Fluid in H20:
        F_Type = "H20"
    return F_Type

#Colebrook White equation solving for friction factor
##Di: inner pipe diameter
##Re: Reynolds number
##rough: roughness of pipe material
def Colebrook(Di, Re, rough):
    friction = 0.08 #Starting Friction Factor
    rough = rough / 12
    while 1:
        leftF = 1 / friction**0.5 #Solve Left side of Eqn
        rightF = - 2 * math.log10(2.51/(Re * friction**0.5)+(rough)/(3.72*Di)) # Solve Right side of Eqn
        friction = friction - 0.000001 #Change Friction Factor
        if (rightF - leftF <= 0): #Check if Left = Right
            break
    return friction

#Line sizing program that outputs properties associated to set points of the system and line size selected.
## return vector = [LineProp, FluidProp]
### LineProp = [line velocity, pressure drop, Reynolds #]
### FluidProp = [Heat load, Fluid mass flow, Fluid density]
## Inputs:
### Fluid: type of fluid under study (refrigerant, water, etc.)
### F_Temp: Fluid temperature 
### L_Type: Type of refrigerant line (Suct, Liq, Disch) -> suction, liquid, discharge, etc.
### SatSuct_T: Saturated suction temperature
### SatCond_T: Saturated condensing temperature
### SubLiq_T: Subcooled liquid temperature
### Di: Inner diameter of the pipe
### material: type of pipe material
### Len: length of pipe under study
### Units: Type of units input and output used (Imp/SI)
### HeatLoad: Heat load being transported by refrigerant system
### mass_flow: Mass flow moving through refrigerant line under study
### SupHeat: Superheat associated with suction line
def FLine(Fluid, F_Temp, L_Type, SatSuct_T, SatCond_T, SubLiq_T, Di, material, Len, Units, \
HeatLoad = None, mass_flow = None):
    
    if Units == "Imp":
        SatSuct_T = Unit_Convert(SatSuct_T, "F", "K")
        SatCond_T = Unit_Convert(SatCond_T, "F", "K")
        SubLiq_T = Unit_Convert(SubLiq_T, "F", "K")
        F_Temp = Unit_Convert(F_Temp, "F", "K")
    
    F_Type = FluidCheck(Fluid)
    Di_ft = Di/12
    
    if F_Type is "REF":
        
        SatCond_P = PropsSI("P", "T", SatCond_T, "Q", 0, Fluid)
        SatSuct_P = PropsSI("P", "T", SatSuct_T, "Q", 1, Fluid)
        SubLiq_H = Unit_Convert(PropsSI("H", "T|liquid", SubLiq_T, "P", SatCond_P, Fluid), "J/kg", "BTU/lb")
        SatSuct_H = Unit_Convert(PropsSI("H", "T", SatSuct_T, "Q", 1, Fluid), "J/kg", "BTU/lb")
        
        if L_Type == "Suct":
            F_dens = Unit_Convert(PropsSI("D", "T|gas", F_Temp, "P", SatSuct_P, Fluid), "kg/m3", "lb/ft3")
            F_visc = Unit_Convert(PropsSI("V", "T|gas", F_Temp, "P", SatSuct_P, Fluid), "Pas", "lb/fts")
        elif L_Type == "Liq":
            F_dens = Unit_Convert(PropsSI("D", "T|liquid", F_Temp, "P", SatCond_P, Fluid), "kg/m3", "lb/ft3")
            F_visc = Unit_Convert(PropsSI("V", "T|liquid", F_Temp, "P", SatCond_P, Fluid), "Pas", "lb/fts")
        elif L_Type == "Disch":
            F_dens = Unit_Convert(PropsSI("D", "T|gas", F_Temp, "P", SatCond_P, Fluid), "kg/m3", "lb/ft3")
            F_visc = Unit_Convert(PropsSI("V", "T|gas", F_Temp, "P", SatCond_P, Fluid), "Pas", "lb/fts")
        if HeatLoad is not None and mass_flow is None:
            mass_flow = HeatLoad/(SatSuct_H - SubLiq_H)
        elif HeatLoad is None and mass_flow is not None:
            HeatLoad = mass_flow * (SatSuct_H - SubLiq_H)
        elif HeatLoad is not None and mass_flow is not None:
            sys.exit("Entry Error - System is OVER constrained, use either mass flow \
            or heat load for inputs not both")
        elif HeatLoad is None and mass_flow is None:
            sys.exit("Entry Error - System is NOT constrained, use either mass flow \
            or heat load for inputs not both")
        Cross_A = ((math.pi/4) * (Di_ft**2))
        Vol_Flow = mass_flow/F_dens
    
    # Linear velocity [alternatively: vel = mass_flow/(dens*Cross_A)]
    ## units: ft/min
    vel = (Vol_Flow/Cross_A) / 60
    
    #absolute roughness of pipe material
    if material == "CU-L":
        rough = 0.00006
    elif material == "STL-SCH80":
        rough = 0.0018
    
    #Reynolds number (still needs adjustment, not accurate)
    vel_s = vel / 60
    SI_Di = Di_ft * 0.3048
    SI_dens = Unit_Convert(F_dens, "lb/ft3", "kg/m3")
    SI_vel = vel_s * 0.3048
    SI_visc = Unit_Convert(F_visc, "lb/fts", "Pas")
    Re = ((SI_dens * SI_vel * SI_Di)/ SI_visc)
    
    #Friction Factor
    if Re > 4000:
        ff = Colebrook(Di_ft, Re, rough)/4
    elif Re < 4000:
        ff = 64/Re
    
    SI_Len = Len * 0.3048
    
    SI_press_drop = ff * (SI_Len/SI_Di) * (2*SI_dens*(SI_vel**2))
    press_drop = SI_press_drop / 6895
    
    LineProp = [vel, press_drop, Re]
    FluidProp = [HeatLoad, mass_flow, F_dens]
    return [LineProp, FluidProp]


def EEV_Select(mfg, ref, HeatLoad, SatSuct_T, SatCond_T, upstr_press, dwnstr_press):
    
    if ref == "R452A":
        ref = "R404A"
    
    #Retrieving EEV data
    ##including additional mfgs and refrigerants
    ##Get current working directory and recreate file addresses
    work_direct = os.path.dirname(os.path.abspath(__file__))
    file_Parker = work_direct + r"\404A_ParkEEVs.pkl"
    file_Danfoss = work_direct + r"\404A_DanEEVs.pkl"
    
    if mfg == "Sporlan":
        if ref == "R404A":
            file = open(file_Parker, 'rb')
            VLV_data = pickle.load(file)
            
    elif mfg == "Danfoss":
        if ref == "R404A":
            file = open(file_Danfoss, 'rb')
            VLV_data = pickle.load(file)
    file.close()
    
    #Finding table associated with application
    VLV_data = VLV_data.to_numpy()
    VLV_fam = VLV_data[3:, 0]
    Evap_temps = VLV_data[1,1:]
    Evap_diff = abs(Evap_temps - SatSuct_T)
    close_evap = min(Evap_diff)
    Evap_temps = Evap_temps.tolist()
    Evap_diff = Evap_diff.tolist()
    Evap_temp_i = Evap_diff.index(close_evap)
    tbl_sect = VLV_data[2:,Evap_temp_i+1:Evap_temp_i+9]
    
    #Finding pressure drop across valve
    HeatLoad_Ton = HeatLoad/12000
    SatCond_T_SI = Unit_Convert(SatCond_T, "F", "K")
    SatSuct_T_SI = Unit_Convert(SatSuct_T, "F", "K")
    SatCond_P = Unit_Convert(PropsSI("P", "T", SatCond_T_SI, "Q", 0, ref), "Pa", "psia")
    SatSuct_P = Unit_Convert(PropsSI("P", "T", SatSuct_T_SI, "Q", 1, ref), "Pa", "psia")

    VLV_press_drop = (SatCond_P+upstr_press) - (SatSuct_P+dwnstr_press)
    
    if mfg == "Sporlan":
        #Finding table column associated with valve pressure drop
        row_press_drop = np.array(tbl_sect[0,:])
        close_press_arr = abs(row_press_drop - VLV_press_drop)
        close_press = min(close_press_arr)
        close_press_arr = close_press_arr.tolist()
        close_press_i = close_press_arr.index(close_press)
        col_HeatLoad = tbl_sect[1:, close_press_i]
    elif mfg == "Danfoss":
        row_SCT = np.array(tbl_sect[0,:])
        close_temp_arr = abs(row_SCT - SatCond_T)
        close_temp = min(close_temp_arr)
        close_temp_arr = close_temp_arr.tolist()
        close_temp_i = close_temp_arr.index(close_temp)
        col_HeatLoad = tbl_sect[1:, close_temp_i]
    
    #Percentage loading
    col_HeatLoad = np.array(col_HeatLoad)
    VLV_load = HeatLoad_Ton/col_HeatLoad
    data_out = np.array([0,0])
    for i,j in zip(VLV_fam, VLV_load):
        data_out = np.vstack((data_out,[i, j]))
    data_out = data_out[1:,:]
    data_out = np.vstack((["Valve Pressure Drop (psi)", VLV_press_drop], data_out))
    return data_out