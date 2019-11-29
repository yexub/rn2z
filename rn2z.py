#!/usr/bin/python3
# -*- coding: UTF-8 -*-

''' 
The file designed to rotate n vector to z axis in crystall
The read_poscar function can read POSCAR file
The rot_angle function aims at calculate the angles of rotation
'''

from math import *
from numpy import array,dot
from numpy.linalg import inv,det
from os.path import isfile
import sys

def read_poscar(filename):
    with open(filename) as f:
        data=f.readlines()
    f.close()
    title=data[0]
    scale=float(data[1])
    lattice=[s.split() for s in data[2:5]]
    lattice=[float(a) for s in lattice for a in s]
    lattice=array(lattice).reshape((3,3))
    return title, scale,lattice

def cal_S(phi,theta):
    a=[cos(phi)*cos(theta),-sin(phi),cos(phi)*sin(theta)]
    b=[sin(phi)*cos(theta),cos(phi),sin(phi)*sin(theta)]
    c=[-sin(theta),0,cos(theta)]
    S=array([a,b,c])
    S=inv(S)/det(S)
    return S

def rot_angle(vector,lattice):
    vector=array([float(a) for a in vector.split()])
    vector=dot(vector,lattice)
    r=sqrt(sum([a*a for a in vector]))
    if vector[0]==0:
        if vector[1]==0:
            phi=0
        else:
            phi=pi/2
    else:
        phi=atan(vector[1]/vector[0])
    theta=acos(vector[2]/r)
    return phi,theta

def write_new_poscar(lattice_new,filename,new_file):
    with open(filename) as f:
        data=f.readlines()
    f.close()

    for i in [0,1,2]:
        data[i+2]=''.join(["%20.10f"%ls for ls in lattice_new[i]])+'\n'
    with open(new_file,'w') as f:
        for ls in data:
            f.write(ls)
    f.close()

def get_filename(sys_argv,filename='POSCAR',new_file='POSCAR_new.vasp'):
    if len(sys_argv)>=3:
        if isfile(sys_argv[1]):
            filename=sys_argv[1]
        new_file=sys_argv[2]
    elif len(sys_argv)==2:
        if isfile(sys_argv[1]):
            filename=sys_argv[1]
    return filename,new_file

if __name__=='__main__':
    filename,new_file=get_filename(sys.argv)
    print('\n\n*'+' Start one Calculation '.center(60,'-')+'*\n')
    print('\n\t*'+(" Reading '"+filename+"' file ").center(25,'-')+'*\n')
    print('\n\t*'+' Input set '.center(25,'-')+'*\n')
    vector=input("\tPlease input a vector as '1 2 3' :  ")
    vector1=array([float(a) for a in vector.split()])
    title,scale,lattice=read_poscar(filename)
    phi,theta=rot_angle(vector,lattice)
    S=cal_S(phi,theta)
    lattice_new=dot(S,lattice.T).T
    write_new_poscar(lattice_new,filename,new_file)
    a=dot(vector1,lattice_new)
    str=' + '.join([str(vector1[0])+' a',str(vector1[1])+' b',str(vector1[2])+' b'])
    print('\n\n\t*'+' Here is Results '.center(25,'-')+'*')
    print('\n\t'+'phi angle is :  '+"{:.2f}".format(degrees(phi))+' deg')
    print('\ttheta angle is :  '+"{:.2f}".format(degrees(theta))+' deg')
    print('\n\t'+'test the final vector : '+str)
    print('\n\t\t'+'\t'.join(["{:.10f}".format(i) for i in a])+'\n')
    print('\n\t*'+(" written to '"+new_file+"' file ").center(25,'-')+'*\n')
    print('\n*'+' The End '.center(60,'-')+'*\n\n')
