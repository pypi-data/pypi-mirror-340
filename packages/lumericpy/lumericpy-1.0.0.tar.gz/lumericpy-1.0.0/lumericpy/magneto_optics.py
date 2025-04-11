import numpy as np

def getModifiedTensor(eps_x,eps_y,eps_z,Mx=0,My=0,Mz=0,Verdet=0):
    """
    Returns Permittivity tensor for a magneto-optic material.

    :param eps_x: permittivity in x direction
    :param eps_y: permittivity in y direction
    :param eps_z: permittivity in z direction
    :param Mx: magnetization in x direction (default=0)
    :param My: magnetization in y direction (default=0)
    :param Mz: magnetization in z direction (default=0)
    :param Verdet: Verdet constant (default=0)
    :return: forward and backward permittivity tensors
    """
    eps=np.array([[eps_x,0,0],[0,eps_y,0],[0,0,eps_z]])
    
    
    magnetization = np.array([[0, Mz, -My],[-Mz,0,Mx],[My,-Mx,0]])
    forward_tensor = eps@np.identity(3)+Verdet*1j*magnetization
    backward_tensor = eps@np.identity(3)-Verdet*1j*magnetization
    return forward_tensor, backward_tensor


def add_mat(mode,eig,mat_name,l=750e-9):
    """
    Adds a anisotropic material to the Lumerical MODE Solutions simulation environment.
    
    :param mode: Lumerical simulation object
    :param eig: eigenvalues of the material
    :param mat_name: name of the material to be added
    :param l: wavelength to add at(default=750 nm)
    :return: None
    
    """

    mode.switchtolayout()
    out=int(mode.materialexists(mat_name))

    arr = np.concatenate([np.array([3e8/l]),eig]).reshape(1,4)
    #print(arr)
    if out==0: #Material Does not exist
        myMat=mode.addmaterial("Sampled 3D Data")
        mode.setmaterial(myMat,"name","Pseudo2DMat")
        mode.setmaterial("Pseudo2DMat","Anisotropy",1)

        mode.setmaterial("Pseudo2DMat","sampled 3d data",arr)

        #mode.setmaterial("Pseudo2DMat","Refractive Index",np.real(eig))
        #mode.setmaterial("Pseudo2DMat","Imaginary Refractive Index",np.imag(eig))
    elif out==1: #Material exists
        mode.setmaterial("Pseudo2DMat","sampled 3d data",arr)
        #mode.setmaterial("Pseudo2DMat","Refractive Index",np.real(eig))
        #mode.setmaterial("Pseudo2DMat","Imaginary Refractive Index",np.imag(eig))
    else:
        print("Error in adding material")
