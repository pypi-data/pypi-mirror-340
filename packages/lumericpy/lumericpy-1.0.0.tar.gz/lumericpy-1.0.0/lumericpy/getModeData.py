


def getMode(mode,name):
    """
    Get mode data from Lumerical MODE Solutions.
    This function retrieves various mode properties such as effective index, field distributions, and more.

    :param mode: Lumerical simulation object 
    :param name: mode name (FDE::data::mode1)
    :return: dictionary containing mode properties
    
    """
    results = ["neff", "E", "H", "P", "surface_normal", "dimension", "f", "ng", "loss", 
               "TE polarization fraction", "waveguide TE/TM fraction", "mode effective area", "x", "y", "z", 
               "Ex", "Ey", "Ez", "Hx", "Hy", "Hz", "Z0"]
    
    out = {result: mode.getresult(name, result) for result in results}
    out["x"] = out["x"][:, 0]
    out["y"] = out["y"][:, 0]
    out["z"] = out["z"]
    out["Ex"] = out["Ex"][:, :, 0, 0].T
    out["Ey"] = out["Ey"][:, :, 0, 0].T
    out["Ez"] = out["Ez"][:, :, 0, 0].T
    out["Hx"] = out["Hx"][:, :, 0, 0].T
    out["Hy"] = out["Hy"][:, :, 0, 0].T
    out["Hz"] = out["Hz"][:, :, 0, 0].T

    return out



def runAndGet2Modes(mode,t1=0.35,t2=0.65):
    """

    Runs and gets first TE and TM mode from solution via polarization fraction

    :param mode: Lumerical simulation object
    :param t1: threshold for TM mode (default=0.35)
    :param t2: threshold for TE mode (default=0.65)
    :return: mode1 and mode2 (TE and TM modes respectively)


    """

    # mode.switchtolayout()
    # mode.select("FDE")
    # #mode.set("search","in range")
    # #mode.set("use max index",False)
    # #mode.set("n1",2.1)
    # #mode.set("n2",1.8)
    
    # mode.set("search","near n")
    # mode.set("use max index",False)
    # mode.set("n",2.6)
    
    # mode.set("number of trial modes",2)
    # mode.set("wavelength",750e-9)

    # set_mode(mode,tensor)

    nmodes=mode.findmodes()

    

    if nmodes!=0:
        #Identify TM Mode
        mode1_result=mode.getresult("FDE::data::mode1","TE polarization fraction")
        mode2_result=mode.getresult("FDE::data::mode2","TE polarization fraction")
        if ((mode1_result>=t2) & (mode2_result<=t1)):
            out1=getMode(mode,"FDE::data::mode2")
            out2=getMode(mode,"FDE::data::mode1")
        elif((mode1_result<=t1) & (mode2_result>=t2)):
            out1=getMode(mode,"FDE::data::mode1")
            out2=getMode(mode,"FDE::data::mode2")
        else: 
            out1=0
            out2=0    
    else:
        out1=0
        out2=0
    return out1,out2
