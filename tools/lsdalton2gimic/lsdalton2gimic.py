from __future__ import print_function

import os, sys,string, re


#Chandan Kumar
#Email - chandan.iiserk@gmail.com
#Date - 06/01/2017 (DD/MM/YYYY)
#To produce MOL and XDENS file
#MOLECULE.INP, CAODENS, XCAODENS and "basis set file" should be in the same directory
#Works for Atoms like H, B, C, N, O, F, S
#Works only for BASIS, not Atombasis 
#Works only upto F basis functions 
#To run this script-$ python lsdalton2gimic.py "basis set file"

header="""INTGRL        1    0    1    0    0    0    0    0    0
TURBOMOLE
              Generated by turbo2mol (TM)
%i    0            0.10E-08              0    0
9999.00      3.00"""

class Atomizer(object):
    def __init__(self,xyz_file, basis_set_file):
        self.xyz_file = xyz_file
        self.basis_set_file = basis_set_file
        self.atoms = list()
        self.coordinates = list()
        self.coordinate_x = list()
        self.coordinate_y = list()
        self.coordinate_z = list()
        self.periodic= ['H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar',
                        'K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br',
                        'Kr','Rb','Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Sb','Te',
                        'I','Xe']
        self.orbitals = ['S', 'P', 'D', 'F', 'G', 'H']
        self.raw_data = None
        self.refined_data = dict()
    
    def xdensfile(self):
    	try:
	    filecao=open('CAODENS', 'r')
	    filexcao=open('XCAODENS', 'r')
    	    cao=filecao.read()
    	    xcao=filexcao.read()
    	    filecao.close()
    	    filexcao.close()
    	    xdensfile=open('XDENS','w')
    	    xdensfile.write(cao)
    	    xdensfile.write(xcao)
    	    xdensfile.close()
    	except:
	    print('Error in producing XDENS file')
	    sys.exit(0)
    def xyz_reader(self):
	    def checker(words):
		    if len(words) ==4:
			    try:
				coordinates = [float(k) for k in words[1:]]
				coordinate_x = words[1]
				coordinate_y = words[2]
				coordinate_z = words[3]
				atom=words[0]
#			    	if atom in self.periodic and atom not in self.atoms:
			    	if atom in self.periodic:
				    self.atoms.append(atom)
				    self.coordinates.append(coordinates)
				    self.coordinate_x.append(coordinate_x)
				    self.coordinate_y.append(coordinate_y)
				    self.coordinate_z.append(coordinate_z)
			    except:
				return 
		    else:
			    return
	    with open(self.xyz_file,'r') as xyz_file:
		for line in xyz_file.readlines():
			checker(line.split())
	    if not len(self.atoms):
		print('No atoms')
		sys.exit()


    def basis_set_reader(self):
        if not len(self.atoms):
            self.xyz_reader()
        atom, orbital = None, None
        with open(self.basis_set_file, 'r') as basis_set_file:
            extract_P = False
            tmp = list()
            data = dict()
            for idx, line in enumerate(basis_set_file.readlines()):
                if '$ END OF BASIS' in line:
                    break
                words = line.split()
                if len(words) == 2 and (words[0] == 'a' or words[0] == 'A'):
                    try:
                        atom_number = int(words[1])
                        if atom_number >= len(self.periodic):
                            break
                        else:
                            atom = self.periodic[atom_number - 1]
                            if atom in self.atoms:
                                extract_P = True
                                data[atom] = dict()
                            else:
                                extract_P = False
                    except:
                        print('Illegal basis set format!')
                        sys.exit()

                elif extract_P and words[0] == '$' and '-TYPE FUNCTIONS' in line:
                    for orbital_i in self.orbitals:
                        if '$ ' + orbital_i + '-TYPE FUNCTIONS' in line:
                            orbital = orbital_i
                            data[atom][orbital] = list()
                elif extract_P and words[0] not in ['$', 'a', 'A']:
                    data[atom][orbital].append(words)

                else:
                    pass
        self.raw_data = data

    def converter(self):
        for a, atom in self.raw_data.iteritems():
            self.refined_data[a] = dict()
            for o, orbital in atom.iteritems():
                self.refined_data[a][o] = {0: list()}
                idx = 2
                for i, w in enumerate(orbital[1:]):
                    if idx < len(w) and eval(w[idx]) != 0:
                        idx += 1
                        self.refined_data[a][o][idx-2] = list()
                    self.refined_data[a][o][idx-2].append('  ' + w[0] + '   ' + w[idx-1])

    def writefile(self,filename):
	newfile=open(filename,'w')
	newfile.write("%s %s" %(header % (len(self.atoms)),'\n'))
	for i in range(0,len(self.atoms)):
	    x=i
            for atom in self.atoms[i]:
            	if atom in self.refined_data.keys():
			anumber=self.periodic.index(atom)+1
			value_of_dict=self.refined_data.get(atom)	
			lmax=len(value_of_dict)

	        	A = self.refined_data[atom]
			print('atom')
			print(atom)
			s_orbital='S'
			p_orbital='P'
			d_orbital='D'
			f_orbital='F'
			g_orbital='G'
			h_orbital='H'
			if lmax==1:
				length_of_S=len(self.refined_data[atom]['S'])
				print(length_of_S)
                		newfile.write("%s  %s %s %s %s %s" %(anumber,'    ', '1 ', lmax, length_of_S,  '\n'))
                		newfile.write("%s %s  %s %s %s %s %s %s" %(atom, '1 ',self.coordinate_x[x],'     ',self.coordinate_y[x],'      ',self.coordinate_z[x], '\n'))
            			for orbital in self.orbitals:
               	    			if orbital in A.keys():
                    				chunk = A[orbital]
                    				for local in chunk.values():
                            				newfile.write("%s  %s  %s  %s" %(' ', len(local), 1, '\n'))
                            				newfile.write('\n'.join(local)+'  '+'\n')
			elif lmax==2:
				length_of_S=len(self.refined_data[atom]['S'])
				print(length_of_S)
				length_of_P=len(self.refined_data[atom]['P'])
				print(length_of_P)
                		newfile.write("%s  %s %s %s %s %s %s" %(anumber,'    ', '1 ', lmax, length_of_S,length_of_P,  '\n'))
                		newfile.write("%s %s  %s %s %s %s %s %s" %(atom, '1 ',self.coordinate_x[x],'     ',self.coordinate_y[x],'      ',self.coordinate_z[x], '\n'))
            			for orbital in self.orbitals:
               	    			if orbital in A.keys():
                    				chunk = A[orbital]
                    				for local in chunk.values():
                            				newfile.write("%s  %s  %s  %s" %(' ', len(local), 1, '\n'))
                            				newfile.write('\n'.join(local)+'  '+'\n')
			elif lmax==3:
				length_of_S=len(self.refined_data[atom]['S'])
				print(length_of_S)
				length_of_P=len(self.refined_data[atom]['P'])
				print(length_of_P)
				length_of_D=len(self.refined_data[atom]['D'])
				print(length_of_D)
                		newfile.write("%s  %s %s %s %s %s %s %s" %(anumber,'    ', '1 ', lmax,length_of_S, length_of_P,length_of_D,  '\n'))
                		newfile.write("%s %s  %s %s %s %s %s %s" %(atom, '1 ',self.coordinate_x[x],'     ',self.coordinate_y[x],'      ',self.coordinate_z[x], '\n'))
            			for orbital in self.orbitals:
               	    			if orbital in A.keys():
                    				chunk = A[orbital]
                    				for local in chunk.values():
                            				newfile.write("%s  %s  %s  %s" %(' ', len(local), 1, '\n'))
                            				newfile.write('\n'.join(local)+'  '+'\n')
			elif lmax==4:
				length_of_S=len(self.refined_data[atom]['S'])
				length_of_P=len(self.refined_data[atom]['P'])
				length_of_D=len(self.refined_data[atom]['D'])
				length_of_F=len(self.refined_data[atom]['F'])
                		newfile.write("%s  %s %s %s %s %s %s %s %s" %(anumber,'    ', '1 ', lmax,length_of_S, length_of_P,length_of_D, length_of_F, '\n'))
                		newfile.write("%s %s  %s %s %s %s %s %s" %(atom, '1 ',self.coordinate_x[x],'     ',self.coordinate_y[x],'      ',self.coordinate_z[x], '\n'))
            			for orbital in self.orbitals:
               	    			if orbital in A.keys():
                    				chunk = A[orbital]
                    				for local in chunk.values():
                            				newfile.write("%s  %s  %s  %s" %(' ', len(local), 1, '\n'))
                            				newfile.write('\n'.join(local)+'  '+'\n')
			elif lmax==5:
				length_of_S=len(self.refined_data[atom]['S'])
				length_of_P=len(self.refined_data[atom]['P'])
				length_of_D=len(self.refined_data[atom]['D'])
				length_of_F=len(self.refined_data[atom]['F'])
				length_of_G=len(self.refined_data[atom]['G'])
                		newfile.write("%s  %s %s %s %s %s %s %s %s %s" %(anumber,'    ', '1 ', lmax,length_of_S, length_of_P,length_of_D, length_of_F,length_of_G, '\n'))
                		newfile.write("%s %s  %s %s %s %s %s %s" %(atom, '1 ',self.coordinate_x[x],'     ',self.coordinate_y[x],'      ',self.coordinate_z[x], '\n'))
            			for orbital in self.orbitals:
               	    			if orbital in A.keys():
                    				chunk = A[orbital]
                    				for local in chunk.values():
                            				newfile.write("%s  %s  %s  %s" %(' ', len(local), 1, '\n'))
                            				newfile.write('\n'.join(local)+'  '+'\n')
			elif lmax==6:
				length_of_S=len(self.refined_data[atom]['S'])
				length_of_P=len(self.refined_data[atom]['P'])
				length_of_D=len(self.refined_data[atom]['D'])
				length_of_F=len(self.refined_data[atom]['F'])
				length_of_G=len(self.refined_data[atom]['G'])
				length_of_H=len(self.refined_data[atom]['H'])
                		newfile.write("%s  %s %s %s %s %s %s %s %s %s %s" %(anumber,'    ', '1 ', lmax,length_of_S, length_of_P,length_of_D, length_of_F,length_of_G,length_of_H, '\n'))
                		newfile.write("%s %s  %s %s %s %s %s %s" %(atom, '1 ',self.coordinate_x[x],'     ',self.coordinate_y[x],'      ',self.coordinate_z[x], '\n'))
            			for orbital in self.orbitals:
               	    			if orbital in A.keys():
                    				chunk = A[orbital]
                    				for local in chunk.values():
                            				newfile.write("%s  %s  %s  %s" %(' ', len(local), 1, '\n'))
                            				newfile.write('\n'.join(local)+'  '+'\n')
			else:
				print('Error')





if __name__ == '__main__':
    A = Atomizer('MOLECULE.INP',sys.argv[1])
    A.xdensfile()
    A.xyz_reader()
    A.basis_set_reader()
    A.converter()
    A.writefile('MOL')