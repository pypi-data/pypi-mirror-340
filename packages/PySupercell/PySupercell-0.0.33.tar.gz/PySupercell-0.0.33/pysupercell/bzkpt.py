#!/usr/bin/env python


#===========================================================================#
#                                                                           #
#  File:       bzkpt.py                                                     #
#  Usage:      proceed with the k points in the BZ                          #
#  Author:     Shunhong Zhang <szhang2@ustc.edu.cn>                         #
#  Date:       Feb 24, 2020                                                 #
#                                                                           #
#===========================================================================#



import os
import numpy as np

r3=np.sqrt(3)


def gen_mp_uniform_mesh(nkx,nky,nkz):
    mkx=np.linspace(0,1,nkx+1)[:-1]+0.5/float(nkx)
    mky=np.linspace(0,1,nky+1)[:-1]+0.5/float(nky)
    mkz=np.linspace(0,1,nkz+1)[:-1]+0.5/float(nkz)
    if nkx==1: mkx=np.zeros(nkx,float)
    if nky==1: mky=np.zeros(nky,float)
    if nkz==1: mkz=np.zeros(nkz,float)
    kx,ky,kz=np.meshgrid(mkx,mky,mkz,indexing='ij')
    mp_kmesh=np.transpose(np.array([kx,ky,kz]),(1,2,3,0)).reshape(nkx*nky*nkz,3)
    mp_kmesh[np.where(mp_kmesh>0.5)]-=1
    return mp_kmesh


def get_xsym_dic(ibrav):
    if ibrav==4:
        return {
        'G':[0.0, 0.0, 0.0],
        'M':[0.5, 0.0, 0.0],
        'K':[1./3.,1./3.,0.0],
        'A':[0.0, 0.0, 0.5] }
    elif ibrav==6:
        return {
        'G':[0.0, 0.0, 0.0],
        'X':[0.5, 0.0, 0.0],
        'M':[0.5, 0.5, 0.0],
        'Y':[0.0, 0.5, 0.0],
        'Z':[0.0, 0.0, 0.5] }
    else:
        print ( ('sorry! we do not have the label lib for this symmetry now!'))
        return None

      
def get_label_k(ibrav,kpt,eps=1e-4):
    xsym_dic = get_xsym_dic(ibrav)
    xsym_list=[kpt[0]]+[x for n, x in enumerate(kpt[:-1]) if np.linalg.norm(x-kpt[n+1])<eps]+[kpt[-1]]
    label_k_list=[]
    for xsym in xsym_list:
        for key in xsym_dic.keys():
            if np.linalg.norm(np.array(xsym)-np.array(xsym_dic[key]))<eps:
               label_k_list.append(key)
    return label_k_list
    #exit('The k point is not in the high symmetry k points set!')

def get_xsym(path,segment_nkpt): return  path[0::segment_nkpt].tolist()+[path[-1]]

def guess_xsym(path):  return [path[0]]+[x for n, x in enumerate(path) if x in path[:n]]+[path[-1]]

def gen_kp(weight=None):
    with open("KPOINTS") as f:
        f.readline()
        segment_nkpt=int(f.readline())
        line = f.readline()
        if line[0]!='l' and line[0]!='L':
            exit('please use line mode to generate the kpath')
        ctype = f.readline()
        if ctype[0]=='D' or ctype[0]=='d':
            print('direct coordinates for k points')
        elif ctype[0]=='C' or ctype[0]=='c':
            print('cartesian coordinates for k points')
        data = np.fromfile(f,sep=' ',dtype=float)
    data = data.reshape(data.shape[0]/3,3)
    xsym = np.vstack([data[::2],data[-1]])
    print("high symm kpts:\n",xsym)
    npath=len(xsym)-1
    weight = [1.0/npath/segment_nkpt for i in range(npath*segment_nkpt) if not weight]
    kpt=np.zeros((npath,segment_nkpt,3),float)
    for ipa in range(npath):
        kpt[ipath] = np.array([np.linspace(xsym[ipath,i], xsym[ipath+1,i], segment_nkpt) for i in range(3)]).T
    fmt="{:12.8f}"*3
    with open('kpath','w') as fw:
        for ipath in range(npath):
            print('\n'.join([fmt.format(*tuple(kpt[ipath,ikpt])) for ikpt in range(segment_nkpt)]), file=fw)
    return kpt


def plot_kpath(kpt):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    kpt=np.array(kpt)
    ax.plot(kpt[:,0],kpt[:,1],kpt[:,2],color='green',linewidth=1.5)
    return fig,ax


def map_irBZ_to_fullBZ(k_wedge):
    # mapping the kpts in the irreducible wedge to the uniform mesh in 1st BZ
    import outcar
    import phonopy.structure.grid_points as gp
    import bzkpt
    oc=outcar.outcar()
    struct=oc.get_outcar_struct()
    rotations,translations=bzkpt.get_symm_yaml(fil='symm.yaml')
    grid=np.array([len(set(k_wedge[:,i])) for i in range(3)])
    grid=grid*((grid!=1)+1)
    print ( 'k-point grid',grid)
    full_kpts=gp.GridPoints(grid,struct._reciprocal_cell(),is_time_reversal=False,q_mesh_shift=[0.5,0.5,0.])._ir_qpoints
    full_kpts_cart=np.dot(full_kpts,struct._reciprocal_cell())
    #for ik in  all_kpts._ir_qpoints: print ( ik)
    grid_kpts=gp.GridPoints(grid,struct._reciprocal_cell(),rotations=rotations,is_time_reversal=False,q_mesh_shift=[0.5,0.5,0.])
    kmap=grid_kpts._grid_mapping_table
    kmap=np.array([grid_kpts._ir_grid_points.tolist().index(item) for item in kmap])
    #print ( grid_kpts.__dict__.keys())
    #for ik in grid_kpts._ir_grid_points: print ( ik)
    k_diff=np.linalg.norm(grid_kpts._ir_qpoints-k_wedge,axis=1)
    if any(k_diff>1e-5): warning.warn('input and generated k wedge inconsistent!')
    print ('expand data from irr BZ ({0} points) to 1st BZ ({1} points)'.format(kpt.shape[0],full_kpts.shape[0]))
    with open('kmap','w') as fw:
        for i in range(100):
            line=kmap.reshape(100,100)[i]
            fw.write(' '.join(['{0:4d}'.format(item) for item in line])+'\n')
    return full_kpts,full_kpts_cart,kmap



if __name__ == "__main__":
    print('\nRunning script {0}\n'.format(__file__))
    from pysupercell.pysupercell import cryst_struct
    struct=cryst_struct.load_poscar('POSCAR')
    get_label_k(6,[0,0,0])
    gen_kp()
