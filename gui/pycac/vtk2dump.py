#vtk2dump python implementation

import os
import linecache
import numpy as np

def converter(directory, step, parameters, ng_node, itype):
	'''
	 parameters = [bool_cg, bool_at, 
					x_bound_type, x_bool, x_lower, x_upper
					y_bound_type, y_bool, y_lower, y_upper,
					z_bound_type, z_bool, z_lower, z_upper]
	'''
	step = str(step)
	file_cg = os.path.join(directory,"cac_cg_{}.vtk".format(step))
	file_at = os.path.join(directory,"cac_atom_{}.vtk".format(step))

	file_out = os.path.join(directory, "dump.{}".format(step))
	bool_cg = parameters[0]
	bool_at = parameters[1]
	ret_val = False
	if not os.path.isfile(file_cg) and bool_cg:
		ret_val = (1, "Cannot find coarse-grain data for timestep: {}".format(step))
		bool_cg = False
	if not os.path.isfile(file_at) and bool_at:
		ret_val = (2, "Cannot find atom data for timestep: {}".format(step))
		bool_at = False

	boundary = []; axis_bool = []; box_l = []; box_h = []
	params = [boundary, axis_bool, box_l, box_h]
	[[a.append(parameters[(2+j)+ 4*i]) for i in range(3)] for j, a in enumerate(params)] 

	'''
	Open files to initialize numpy calculation structures
	'''
	try:
		# Initialize counts to zero
		atom_num = 0
		ia = 0
		node_num = 0
		ele_num = 0
		atomp_num = 0
		# Read cg values from file if bool_cg
		if bool_cg:
			atomp_num = atom_num
			with open(file_cg) as cg_fp:
				curr = 0
				for i, line in enumerate(cg_fp):
					if i == 4:
						node_num = int(line.split()[1])
						if node_num%ng_node:
							return(1, "mod(node_num, ng_node) should be zero")
						else:
							ele_num = int(node_num / ng_node)
							ele_size = np.zeros(ele_num)
							r_cg = np.zeros((3, node_num))
							curr = 0
					# POINTS file block
					elif 4 < i < (node_num+5):
						r_cg[:, i-5] = np.array([np.float(i) for i in line.split()]).transpose()
					# Node num is undefined before i = 4
					elif i > 5:
						# CELLS and CELL_TYPES file block 
						if node_num + 5 < i < (node_num+5 + 8 + (2*ele_num)):
							j = i - (node_num+5) + 1
							if j == 2 or j == 4 + ele_num or j == 6+2*ele_num:
								ie = int(line.split()[1])
								if ie != ele_num:
									return(1, "Ie {} should equal ele_num {}".format(ie, ele_num))
						# CELL_DATA file block
						elif (node_num+5 + 8 + (2*ele_num)) <= i < (node_num+5 + 8 + (3*ele_num)):
							k = i - (node_num+5 + 8 + (2*ele_num))
							k_ele = int(line.split()[0])
							if k_ele%2:
								return(1, "Ele_size {} of element {} must be even".format(k_ele, k+1))
							elif k_ele < 4:
								return(1, "Ele_size {} of element {} cannot be less than 4".format(k_ele, k+1))
							else:
								ele_size[k] = k_ele
								atomp_num += (ele_size[k]+1)**3
				a_interpo = np.zeros((ng_node, (int(np.max(ele_size))+1)**3))
				print("Coarse grain file parsing complete...")
	# Read atoms if bool_at
		if bool_at:
			with open(file_at) as at_fp:
				for i, line in enumerate(at_fp):
					if i == 4:
						print(line.split())
						atom_num = int(line.split()[1])
						atomp_num += atom_num
						r_at = np.zeros((3, atom_num))
					elif 4 < i < atom_num + 5:
						k = i - 5
						r_at[:, k] = np.array([np.float(i) for i in line.split()]).transpose()
					elif (atom_num) + 5 < i < (atom_num+5 + 8 + (2*atom_num)):
						j = i - (atom_num + 5) + 1
						if j == 2 or j == 4 + atom_num or j == 6+2*atom_num:
							ia = int(line.split()[1])
							if ia != atom_num:
								return(1, "Ia {} should equal atom_num {}".format(ia, ele_num))
			print("Atomistic file parsing complete...")


	except FileNotFoundError:
		return(1, "Could not find the VTK files for timestep: {}".format(step))

	'''
	Begin Box Boundary Definitions
	'''

	# cg was not empty
	if ele_num != 0:
		box_cg_l = np.amin(r_cg, 1)
		box_cg_h = np.amax(r_cg, 1)
	else:
		box_cg_l = np.zeros(3)
		box_cg_h = np.zeros(3)
	# at was not empty
	if atom_num != 0:
		box_atom_l = np.amin(r_at, 1)
		box_atom_h = np.amax(r_at, 1)
	else:
		box_atom_l = np.zeros(3)
		box_atom_h = np.zeros(3)

	box_bd = np.zeros(6)
	lim_small = np.finfo(np.float).eps

	for i, custom_axis in enumerate(axis_bool):
		# Default to calculated range. Only set user values in NOT 'inf'
		box_bd[2*i] = min(box_cg_l[i], box_atom_l[i]) - lim_small
		box_bd[2*i+1] = max(box_cg_h[i], box_atom_h[i]) + lim_small
		if custom_axis == 't':
			if box_l[i] != 'inf':
				box_bd[2*i] = box_l[i]
			if box_h[i] != 'inf':
				box_bd[2*i+1] = box_h[i]


	'''
	Begin Interpolation
	'''
	print("Start interpolation")

	if os.path.isfile(file_out):
		print("Overwriting {}".format(file_out))

	with open(file_out, 'w+') as dump_fp:
		dump_fp.write("ITEM: TIMESTEP\n{}\n".format(step))
		dump_fp.write("ITEM: NUMBER OF ATOMS\n{}\n".format(int(atomp_num)))
		dump_fp.write('''ITEM: BOX BOUNDS {}{} {}{} {}{}\n{}\t{}\n{}\t{}\n{}\t{}\n'''.format(boundary[0], boundary[0],
							boundary[1], boundary[1],
							boundary[2], boundary[2],
							*box_bd))
		dump_fp.write("ITEM: ATOMS id type x y z\n")
		# Conversion to dump format
		iatomap = 0
		if ele_num != 0:
			ip = 0
			for ie in range(ele_num):
				ip += ng_node
				iatom = 0
				esize = int(ele_size[ie])
				for iz in range(esize+1):
					dt = (iz + 1 - (esize/2. + 1.)) / (esize / 2.)
					for iy in range(esize + 1):
						ds = (iy + 1 - (esize / 2. + 1.)) / (esize / 2.)
						for ix in range(esize + 1):
							dr = (ix + 1 - (esize / 2. + 1.)) / (esize / 2.)
							
							eshape = interpolate(ng_node, dr, ds, dt)
							
							a_interpo[:, iatom] = eshape

							iatom += 1

				for iatom in range((esize+1)**3):
					iatomap += 1
					eshape = a_interpo[:, iatom]
					r_in = np.zeros(3)
					for inod in range(ng_node):
						jp = ip - ng_node + inod

						r_in = np.add(r_in, np.multiply(eshape[inod], r_cg[:,jp]))

					dump_fp.write("{}\t{}\t{}\t{}\t{}\n".format(iatomap+ia, itype, *(r_in[0:3].tolist())))

		if atom_num != 0:
			for ia in range(atom_num):
				dump_fp.write("{}\t{}\t{}\t{}\t{}\n".format(iatomap+ia, itype, *(r_at[0:3, ia].tolist())))
	print("\tFinished writing {}".format(file_out))
	if ret_val:
		return ret_val
	else:
		return(0, file_out)

def interpolate(ng_node, dr, ds, dt):
	'''
	interpolate for element ng_node. 
	NOTE: Currently ONLY for ng_node = 8
	'''
	eshape = np.zeros(ng_node)

	eshape[0] = (1. - dr) * (1. - ds) * (1. - dt) / ng_node

	eshape[1] = (1. + dr) * (1. - ds) * (1. - dt) / ng_node

	eshape[2] = (1. + dr) * (1. + ds) * (1. - dt) / ng_node

	eshape[3] = (1. - dr) * (1. + ds) * (1. - dt) / ng_node

	eshape[4] = (1. - dr) * (1. - ds) * (1. + dt) / ng_node

	eshape[5] = (1. + dr) * (1. - ds) * (1. + dt) / ng_node

	eshape[6] = (1. + dr) * (1. + ds) * (1. + dt) / ng_node

	eshape[7] = (1. - dr) * (1. + ds) * (1. + dt) / ng_node

	return(eshape)

def main():
	params = [True, False, 'p', 't', -10, 15,
							 's', 'f', 0, 0,
							 's', 'f', 12, 45]
	stat, out = converter(os.getcwd(), 34, params, 8, 1)

if __name__ == '__main__':
	main()