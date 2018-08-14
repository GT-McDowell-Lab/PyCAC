# title:inputClass.py
# description:Classes for use in input file creation
# author:chu.k@gatech.edu
# updated:2018/07/4
# version:0.2
# usage:N/A, CAC command list class declarations
# notes:McDowell Lab PyCAC. Version req for dictionary order preservation
# python_version:3.6.4
# =============================================================================
import math
from re import sub

class CommandList:
    # Class containing dictionary templates for all CAC commands.
    # See http://www.pycac.org/chapter5/ for detailed command syntax
    # command_list_instance = inputList()
    # command_list_instance.command['key']

    # CLASS METHODS
    def __init__(self):
        # Initialize default values. Set dict fields to 'None' if unspecified.
        # For consistency, use dict for ALL commands, even if single parameter.
        # It gets a little funky if you're specifying sequential integer values
        # like grain_ids: the dictionary key becomes the integer itself.
        # eg. grain_mat {'2': grain_2_info}

        self.restart = {'boolean_restart': 'f', 'boolean_restart_refine': 'f'}

        self.refine = {'all': [], 'group': []}

        self.simulator = {'type': 'dynamics'}

        self.minimize = {'mini_style': 'cg', 'max_iteration': 1000,
                         'tolerance': '1d-6'}

        self.dynamics = {'dyn_style': 'vv', 'energy_min_freq': 500,
                         'damping_coefficient': 1.}

        self.debug = {'boolean_debug': 'f', 'boolean_mpi': 'f'}

        # Grain Info

        self.grain_num = {'grain_number': 1}
        self.grain_dir = {'direction': 3, 'overlap': 0.}

        self.zigzag = {'boolean_x': 't', 'boolean_y': 't', 'boolean_z': 't'}

        self.grain_move = {'1': [0., 0., 0.]}

        self.grain_mat = {'1': {'x': [1., 0., 0.],
                                'y': [0., 1., 0.], 'z': [0., 0., 1.]}}

        self.subdomain = {'1': 1}

        # Per-subdomain Unit Definition
        self.unit_type = {}
        # {grain_id: {subdomain_id: unitype} }
        self.unit_num = {}
        # {grain_id: {subdomain_id: {x_num, y_num, z_num} }
        
        self.box_dir = {'x': [1., 0., 0.], 'y': [0., 1., 0.],
                        'z': [0., 0., 1.]}

        self.boundary = {'x': 'p', 'y': 'p', 'z': 'p'}

        # Modify Info
        self.modify_num = {'modify_number': 0}

        # Three different modify formats: delete/cg2at, dislocation, cutoff
        self.modify = dict()
        # {'modify_name' : {modify_params}}

        self.potential = dict.fromkeys(['potential_type'])

        self.lattice = dict.fromkeys(['chemical_element', 'lattice_structure',
                                      'lattice_constant'])

        self.mass = dict.fromkeys(['atomic_mass'])

        self.element = {'mass_matrix': 'lumped', 'intpo_depth': 2}

        self.limit = {'atom_per_cell_number': 100,
                      'atomic_neighbor_number': 100}

        self.neighbor = {'bin_size': 1., 'neighbor_freq': 200}

        self.run = {'total_step': 0, 'time_step': 0.002}

        self.dump = {'output_freq': 1000, 'reduce_freq': 1000,
                     'restart_freq': 5000, 'log_freq': 50}

        self.constrain = {'boolean': 'f', 'direction_vec': [0., 0., 1.]}

        self.temperature = {'boolean': 'f', 'temp': 10.}

        self.convert = {'direction_vec': [0., 0., 0.]}

        # Depending on def_num, can have multiple deform modes in the same
        # command. Make it an array of dicts.
        self.deform = dict()
         # {'1': {'xx': {'boolean_cg': 'f', 'boolean_at': 'f',
         #                            'def_rate': 10., 'stress_l': 3.,
         #                            'stress_u': 4., 'flip_frequency': 100},
         #                     'time': {'time_start': 0, 'time_always_flip': 100,
         #                              'time_end': 100},
                             # 'boolean_def': 'f'}}
        # {deform_number: {deform_mode: {deform params}
        #                   time: {time_params}
        #                   boolean_def: bool}
        #                   }
        # }

        # Group Info
        self.group_num = {'new_group_number': 0, 'restart_group_number': 0,
                          'fix_number': 0, 'cal_number': 0}

        self.group = dict()
        # {group_name: group_params_dict}

        #Restart group name tracking
        self.__restart_group_names = []

        self.fix = dict()
        # {group_name: {fix_params_dict}}

        self.cal = dict()
        # {group_name: {cal_variable}}

        self.errors = []
    # MUTATORS FOR INSTANCE VARIABLES

    # Standard edit, no nesting.
    def __edit_standard(self, command_name, parameter_list):
        temp_dict = getattr(self, command_name)
        if len(temp_dict) != len(parameter_list):
            err_string = ("Incorrect number of parameters provided to {0}"
                  .format(command_name))
            return(1, err_string)
        else:
            for i, val in enumerate(parameter_list):
                val = str(val)
                try:
                    parameter_list[i] = int(val)
                except ValueError:
                    try:
                        parameter_list[i] = float(val)
                    except ValueError:
                        pass
            temp_dict = dict(zip(temp_dict.keys(), parameter_list))
            setattr(self, command_name, temp_dict)
            return(0)

    # Custom command edits.
    def __edit_refine(self, parameter_list):
        if parameter_list[0] == 'all':
            self.refine['all'] = [(str(parameter_list[1]), 
                                    str(parameter_list[2]))]
            return(0)
        elif parameter_list[0] == 'group':
            self.refine['group'].append((str(parameter_list[1]), 
                                         str(parameter_list[2])))
            return(0)
        else:
            return(1, "Must be all or group")

    def __edit_grain_move(self, parameter_list):
        if self.grain_num['grain_number'] < parameter_list[0]:
            err_string = ("Specified grain does not exist. There are {0} grain(s)."
                  .format(self.grain_num['grain_number']))
            return(1, err_string)
        else:
            self.grain_move[str(parameter_list[0])] = parameter_list[1:]
            return(0)

    def __edit_grain_mat(self, parameter_list):
        n_grains = (len(parameter_list)/13)
        if self.grain_num['grain_number'] < parameter_list[0]:
            err_string = ("Specified grain does not exist. There are {0} grain(s)."
                  .format(self.grain_num['grain_number']))
            return(1, err_string)
        else:
            grain = str(parameter_list[0])
            temp_dict = {'x': parameter_list[2:5],
                         'y': parameter_list[6:9],
                         'z': parameter_list[10:13]
                         }
            if is_orthogonal(temp_dict['x'], temp_dict['y'], temp_dict['z']):
                self.grain_mat[grain] = temp_dict
                return(0)
            else:
                err_string = ("Specified basis for grain ({}) is not orthogonal".format(parameter_list[0]))
                return(1, err_string)

    def __edit_subdomain(self, parameter_list):
        if self.grain_num['grain_number'] < parameter_list[0]:
            err_string = ("Specified grain does not exist. There are {0} grain(s)."
                  .format(self.grain_num['grain_number']))
            return(1, err_string)
        else:
            grain = str(parameter_list[0])
            self.subdomain[grain] = parameter_list[1]
            return(0)

    def __edit_unit_type(self, parameter_list):
        grain = str(parameter_list[0])
        n_subdomain = str(parameter_list[1])
        if self.grain_num['grain_number'] < int(grain):
            err_string = ("Specified grain does not exist. There are ({0}) grain(s)."
                  .format(self.grain_num['grain_number']))
            return(1, err_string)
        elif self.subdomain[grain] < int(n_subdomain):
            err_string = ("Specified subdomain ({}) does not exist. There are ({}) subdomains in grain ({})"
                  .format(n_subdomain, self.subdomain[grain], grain))
            return(1, err_string)
        else:
            try:
                self.unit_type[grain][n_subdomain] = parameter_list[2]
            except KeyError:
                # This the first subdomain entry for grain, define this key
                self.unit_type[grain] = {n_subdomain: parameter_list[2]}
            return(0)

    def __edit_unit_num(self, parameter_list):
        grain = str(parameter_list[0])
        n_subdomain = parameter_list[1]
        if self.grain_num['grain_number'] < int(grain):
            err_string = ("Specified grain does not exist. There are ({0}) grain(s)."
                  .format(self.grain_num['grain_number']))
            return(1, err_string)
        elif self.subdomain[grain] < n_subdomain:
            err_string = ("Specified subdomain ({}) does not exist. There are ({}) subdomains in grain ({})"
                  .format(n_subdomain, self.subdomain[grain], grain))
            return(1, err_string)
        else:
            try:
                self.unit_num[grain][n_subdomain] = parameter_list[2:]
            except KeyError:
                # This the first subdomain entry for grain, define this key
                self.unit_num[grain] = {n_subdomain: parameter_list[2:]}
            return(0)

    def __edit_box_dir(self, parameter_list):
        # Check for orthonormal basis
        self.box_dir['x'] = parameter_list[0:3]
        self.box_dir['y'] = parameter_list[3:6]
        self.box_dir['z'] = parameter_list[6:9]

    def __edit_modify(self, parameter_list):

        name_string = parameter_list[0]

        style_string = parameter_list[1]
        self.modify[name_string] = {'modify_style': style_string}
        sub_dict = self.modify[name_string]
        # Check bound syntax
        for bound in (parameter_list[4:6] + parameter_list[10:12] 
                    + parameter_list[16:18]):
            if bound != 'inf':
                try:
                    float(bound)
                except ValueError:
                    err_string = ('upper bound and lower bound must be (inf) or real number')
                    return(1, err_string)

        if style_string == "delete" or style_string == "cg2at":
            sub_dict['modify_shape'] = parameter_list[2]
            sub_dict['x'] = {'lower_b': parameter_list[4],
                             'upper_b': parameter_list[5],
                             'orientation': parameter_list[6:9]}
            sub_dict['y'] = {'lower_b': parameter_list[10],
                             'upper_b': parameter_list[11],
                             'orientation': parameter_list[12:15]}
            sub_dict['z'] = {'lower_b': parameter_list[16],
                             'upper_b': parameter_list[17],
                             'orientation': parameter_list[18:21]}
            sub_dict['boolean_in'] = parameter_list[21]
            sub_dict['boolean_delete_filled'] = parameter_list[22]
            sub_dict['modify_axis'] = parameter_list[23]
            sub_dict['modify_centroid_x'] = parameter_list[24]
            sub_dict['modify_centroid_y'] = parameter_list[25]
            sub_dict['modify_centroid_z'] = parameter_list[26]
            sub_dict['modify_radius_large'] = parameter_list[27]
            sub_dict['modify_radius_small'] = parameter_list[28]
        # self.modify[name_string].update(sub_dict)

        elif style_string == "dislocation":
            err_string = "({}) ".format(name_string)
            if parameter_list[2] == parameter_list[3]:
                err_string += ("Dislocation line and plane normal axes cannot be the same. ")
                return(1, err_string)
                
            if not(-1 < float(parameter_list[8]) < 0.5):
                err_string += ("Isotropic poisson ratio for the material is out of range (-1 < v < 0.5). ")
                return(1, err_string)
            sub_dict['line_axis'] = parameter_list[2]
            sub_dict['plane_axis'] = parameter_list[3]
            sub_dict['modify_centroid_x'] = parameter_list[4]
            sub_dict['modify_centroid_y'] = parameter_list[5]
            sub_dict['modify_centroid_z'] = parameter_list[6]
            sub_dict['dis_angle'] = parameter_list[7]
            sub_dict['poisson_ratio'] = parameter_list[8]

        elif style_string == "cutoff":
            sub_dict['depth'] = parameter_list[2]
            sub_dict['tolerance'] = parameter_list[3]

        elif style_string == "add_atom":
            sub_dict['disp_x'] = parameter_list[2]
            sub_dict['disp_y'] = parameter_list[3]
            sub_dict['disp_z'] = parameter_list[4]
        return(0)

    def __edit_constrain(self, parameter_list):
        self.constrain['boolean'] = parameter_list[0]
        self.constrain['direction_vec'] = parameter_list[1:4]
        return(0)

    def __edit_convert(self, parameter_list):
        self.convert['direction_vec'] = parameter_list
        return(0)

    def __edit_deform(self, parameter_list):
        deform_num = str(parameter_list[1])
        self.deform[deform_num] = {'boolean_def': parameter_list[0]}
        curr_deform = self.deform[deform_num]
        curr_deform['boolean_def'] = parameter_list[0]

        # Deform mode definition should occur every 7 parameters, 2, 9, 16, etc
        i = 0
        while 2 + i * 7 < len(parameter_list):
            d_index = (2 + i * 7)
            if parameter_list[d_index] != "time":
                deform_mode = parameter_list[d_index]
                curr_deform[deform_mode] = {
                    'boolean_cg': parameter_list[d_index + 1],
                    'boolean_at': parameter_list[d_index + 2],
                    'def_rate': parameter_list[d_index + 3],
                    'stress_l': parameter_list[d_index + 4],
                    'stress_u': parameter_list[d_index + 5],
                    'flip_frequency': parameter_list[d_index + 6]}
            i += 1

        # Time should pick up where the last deform mode left off +7
        t_start = (2 + (i - 1) * 7)
        curr_deform[parameter_list[t_start]] = {
            'time_start': parameter_list[t_start + 1],
            'time_always_flip': parameter_list[t_start + 2],
            'time_end': parameter_list[t_start + 3]}
        return(0)

    def __edit_group_num(self, parameter_list):
        for n in range(parameter_list[0], parameter_list[0]+parameter_list[1]):
            g_name = "group_" + str(n+1)
            # Add restart group names to private var
            self.__restart_group_names.append(g_name)
        # Normal Edit
        self.__edit_standard('group_num', parameter_list)
        return(0)        

    def __edit_group(self, parameter_list):
        # Essentially same format as modify, without different forms
        if len(self.group) == self.group_num['new_group_number']:
            err_string = ("Too many new groups! Only ({}) are specified in 'group_num'"
                  .format(self.group_num['new_group_number']))
            return(1, err_string)
        elif parameter_list[0] in self.__restart_group_names:
            err_string = ("Name collision! ({}) is already defined as a restart group"
                  .format(parameter_list[0]))
            return(1, err_string)
        for bound in (parameter_list[5:7] + parameter_list[11:13] 
                    + parameter_list[17:19]):
            if bound != 'inf':
                try:
                    float(bound)
                except ValueError:
                    err_string = ('upper bound and lower bound must be (inf) or real number')
                    return(1, err_string)

        name_string = parameter_list[0]
        self.group[name_string] = {'style_cg': parameter_list[1],
                                   'style_at': parameter_list[2]}
        sub_dict = self.group[name_string]

        sub_dict['group_shape'] = parameter_list[3]
        sub_dict['x'] = {'lower_b': parameter_list[5],
                             'upper_b': parameter_list[6],
                             'orientation': parameter_list[7:10]}
        sub_dict['y'] = {'lower_b': parameter_list[11],
                             'upper_b': parameter_list[12],
                             'orientation': parameter_list[13:16]}
        sub_dict['z'] = {'lower_b': parameter_list[17],
                             'upper_b': parameter_list[18],
                             'orientation': parameter_list[19:22]}
        sub_dict['boolean_in'] = parameter_list[22]
        sub_dict['group_axis'] = parameter_list[23]
        sub_dict['group_centroid_x'] = parameter_list[24]
        sub_dict['group_centroid_y'] = parameter_list[25]
        sub_dict['group_centroid_z'] = parameter_list[26]
        sub_dict['group_radius_large'] = parameter_list[27]
        sub_dict['group_radius_small'] = parameter_list[28]

        return(0)

    def __edit_fix(self, parameter_list):
        if (len(self.fix) == self.group_num['fix_number'] and parameter_list[0] not in self.fix):
            err_string = ("Too many new fixes! Only ({}) are specified in 'group_num'"
                  .format(self.group_num['fix_number']))
            return(1, err_string)
        elif (parameter_list[0] in self.group.keys() or 
            parameter_list[0] in self.__restart_group_names):

            self.fix[parameter_list[0]] = {
                'boolean_release': parameter_list[1],
                'boolean_def': parameter_list[2],
                'assign_style': parameter_list[3],
                'assign_x': parameter_list[4],
                'assign_y': parameter_list[5],
                'assign_z': parameter_list[6],
                'disp_lim': parameter_list[7],
                'time': {'time_start': parameter_list[9],
                         'time_end': parameter_list[10]},
                'boolean_grad': parameter_list[11]}
            sub_dict = self.fix[parameter_list[0]]

            if sub_dict['boolean_grad'] == 'f':
                return(0)

            elif sub_dict['boolean_grad'] == 't':
                sub_dict.update({'grad_ref_axis': parameter_list[12],
                                 'grad_assign_axis': parameter_list[13],
                                 'grad_ref_l': parameter_list[14],
                                 'grad_ref_u': parameter_list[15]})
        else:
            # What if groups from restart file? Where do those get loaded...
            err_string = ("{} is not a defined group choice".format(parameter_list[0]))
            return(1, err_string)

    def __edit_cal(self, parameter_list):
        if self.group_num['cal_number'] == len(self.cal) and parameter_list[0] not in self.cal:
            err_string = ("Too many cals! Only ({}) are specified in 'group_num"
                  .format(self.group_num['cal_number']))
            return(1, err_string)            
        if (self.restart['boolean_restart'] == 'f'):
            if (parameter_list[0] in self.group.keys() or 
                parameter_list[0] in self.__restart_group_names):
                self.cal[parameter_list[0]] = {'cal_variable': 
                                                            parameter_list[1].lower()}
                return(0)
            else:
                err_string = ("{} is not a defined group".format(parameter_list[0]))
                return(1, err_string)

        elif self.restart['boolean_restart'] == 't':
            self.cal[parameter_list[0]] = {'cal_variable': parameter_list[1].lower()}

            return(0)

    # Consolidated function for all commands (EDITING)
    # Leveraging dict KeyError for default standard case
    edit_switch = {
        'standard': __edit_standard,
        'refine': __edit_refine,
        'grain_move': __edit_grain_move,
        'grain_mat': __edit_grain_mat,
        'subdomain': __edit_subdomain,
        'unit_type': __edit_unit_type,
        'unit_num': __edit_unit_num,
        'box_dir': __edit_box_dir,
        'modify': __edit_modify,
        'constrain': __edit_constrain,
        'convert': __edit_convert,
        'deform': __edit_deform,
        'group_num': __edit_group_num,
        'group': __edit_group,
        'fix': __edit_fix,
        'cal': __edit_cal
    }

    def edit_command(self, command_name, parameter_list):
        try:
            err = self.edit_switch[command_name](self, parameter_list)

        # Default value
        except KeyError:
            err = self.edit_switch['standard'](self, command_name, parameter_list)
        if err:
            self.errors.append((command_name, err[1]))
        

    # COMMAND PARSING TO STRING

    # Standard parse, no nesting.
    def __parse_standard(self, command_name):
        try:
            final_string = ("{: <16}".format(command_name) + ' '.join(str(v) for v in
                                                              getattr(self, command_name).values()))
            #Swap all exponentials to f90 format with re.sub
            return sub('e-', 'd-', final_string)
        except (AttributeError, TypeError):
            err_string = ("Error: '{0}' parameters must be defined before being parsed".format(command_name))
            return(1, err_string)

    # Custom command parse.
    def __parse_refine(self):
        final_string = ""
        for key in self.refine:
            if bool(self.refine[key]):
                for group, unitype in self.refine[key]:
                    command_string = ""
                    command_string += (str(key) + " " + group +  " " + unitype)
                    final_string += ("{: <16}{: <16}\n".format("refine", command_string))
        #print(final_string)
        return final_string


    def __parse_grain_move(self):
        command_string = ""
        for key in sorted(self.grain_move):
            command_string += (str(key) + " " + (' '.join(str(i)
                                                          for i in self.grain_move[key])) + " ")
        return "{: <16}{: <16}".format("grain_move", command_string)

    def __parse_grain_mat(self):
        command_string = ""
        for key in sorted(self.grain_mat):
            command_string += (str(key) + " ")
            for vec in sorted(self.grain_mat[key]):
                command_string += (str(vec) + " " + ' '.join(str(i)
                                                             for i in self.grain_mat[key][vec]) + " ")
        return "{: <16}{: <16}".format("grain_mat", command_string)

    def __parse_subdomain(self):
        command_string = ""
        for key in sorted(self.subdomain):
            command_string += (str(key) + " " + str(self.subdomain[key]) + " ")
        return "{: <16}{: <16}".format("subdomain", command_string)

    def __parse_unit_type(self):
        command_string = ""
        for key in sorted(self.unit_type):
            command_string += str(key) + " "
            for subdomain in sorted(self.unit_type[key]):
                command_string += str(subdomain) + " {} ".format(
                    self.unit_type[key][subdomain])

        return "{: <16}{: <16}".format("unit_type", command_string)

    def __parse_unit_num(self):
        command_string = ""
        for key in sorted(self.unit_num):
            command_string += str(key) + " "
            for subdomain in sorted(self.unit_num[key]):
                dir_vec = self.unit_num[key][subdomain]
                command_string += str(subdomain) + " x {} y {} z {} ".format(*dir_vec)
        return "{: <16}{: <16}".format("unit_num", command_string)

    def __parse_box_dir(self):
        command_string = ""
        for axis in sorted(self.box_dir):
            command_string += (str(axis) + " " + ' '.join(str(i)
                                                          for i in self.box_dir[axis]) + " ")
        return "{: <16}{: <16}".format("box_dir", command_string)

    def __parse_modify(self):
        if len(self.modify) < self.modify_num['modify_number']:
            err_string = ("Not enough modify commands. ({}) expected,  ({}) specified."
                .format(self.modify_num['modify_number'], len(self.modify)))
        final_string = ""
        for cmd in sorted(self.modify):
            command = self.modify[cmd]
            style = command['modify_style']
            command_string = (str(cmd) + " " + style + " ")
            if style == "cg2at" or style == "delete":

                # Command prefix params
                command_string += (command['modify_shape'] + " ")

                # Add boundaries
                command_string += ("x " + str(command['x']['lower_b']) + " " + str(command['x']['upper_b']) + " " + ' '.join(str(i) for i in command['x']['orientation']) + " ")
                command_string += ("y " + str(command['y']['lower_b']) + " " + str(command['y']['upper_b']) + " " +' '.join(str(j) for j in command['y']['orientation']) + " ")
                command_string += ("z " + str(command['z']['lower_b']) + " " + str(command['z']['upper_b']) + " " +' '.join(str(k) for k in command['z']['orientation']) + " ")
                # Boolean values
                command_string += (command['boolean_in'] + " "
                                   + command['boolean_delete_filled'] + " ")
                # Modify Axis
                command_string += (str(command['modify_axis']) + " ")
                #Centroid
                command_string += (str(command['modify_centroid_x']) + " ")
                command_string += (str(command['modify_centroid_y']) + " ")
                command_string += (str(command['modify_centroid_z']) + " ")

                # Radius parameters
                command_string += (" " + str(command['modify_radius_large'])
                                   + " " + str(command['modify_radius_small']))

                final_string += ("{: <16}{: <16}\n".format("modify", command_string))

            elif style == "dislocation":
                command_string += (str(command['line_axis']) + " "
                                   + str(command['plane_axis']) + " ")
                #Centroid
                command_string += (str(command['modify_centroid_x']) + " ")
                command_string += (str(command['modify_centroid_y']) + " ")
                command_string += (str(command['modify_centroid_z']) + " ")

                command_string += (str(command['dis_angle']) + " "
                                   + str(command['poisson_ratio']) + " ")
                final_string += ("{: <16}{: <16}\n".format("modify", command_string))

            elif style == "cutoff":
                #command_string += (str(cmd) + " " + style + " ")
                command_string += (str(command['depth']) + " "
                                   + str(command['tolerance']))
                final_string += ("{: <16}{: <16}\n".format("modify", command_string))
            elif style == "add_atom":
                command_string += (str(command['disp_x']) + " "
                                + str(command['disp_y']) + " "
                                + str(command['disp_y']))
                final_string += ("{: <16}{: <16}\n".format("modify", command_string))


        return final_string

    def __parse_constrain(self):
        command_string = self.constrain['boolean'] + " "
        command_string += (' '.join(str(v)
                                    for v in self.constrain['direction_vec']))

        return "{: <16}{: <16}".format("constrain", command_string)

    def __parse_convert(self):
        command_string = (' '.join(str(v)
                                   for v in self.convert['direction_vec']))
        return "{: <16}{: <16}".format("convert", command_string)

    def __parse_deform(self):

        final_string = ""

        for cmd in (sorted(self.deform)):
            command = self.deform[cmd]
            command_string = command['boolean_def'] + " " + str(cmd) + " "

            # Deform modes come before other keys in reverse alphanumeric sort
            # ignore boolean_def, already appended to command string
            for key in (reversed(sorted(command))):
                if key != "time" and key != "boolean_def":
                    mode_d = command[key]
                    command_string += (key + " " +
                                       str(mode_d['boolean_cg']) + " " +
                                       str(mode_d['boolean_at']) + " " +
                                       str(mode_d['def_rate']) + " " +
                                       str(mode_d['stress_l']) + " " +
                                       str(mode_d['stress_u']) + " " +
                                       str(mode_d['flip_frequency']) + " ")
                elif key == "time":
                    time_d = command[key]
                    command_string += ("time" + " " +
                                       str(time_d['time_start']) + " " +
                                       str(time_d['time_always_flip']) + " " +
                                       str(time_d['time_end']))
            final_string += ("{: <16}{: <16}\n".format("deform", command_string))
        return final_string

    def __parse_group(self):
        
        if len(self.group) != self.group_num['new_group_number']:
            err_string = ("Only ({}) valid groups are defined, when ({}) are expected".format(
                len(self.group), self.group_num['new_group_number']))
            return(1, err_string)
            
        final_string = ""
        for cmd in (self.group):
            command = self.group[cmd]
            command_string = (str(cmd) + " "
                              + command['style_cg'] + " "
                              + command['style_at'] + " ")
            # Command prefix params
            command_string += (command['group_shape'] + " ")

            # Add boundaries
            command_string += ("x " + str(command['x']['lower_b']) + " " + str(command['x']['upper_b']) + " " + ' '.join(str(i) for i in command['x']['orientation']) + " ")
            command_string += ("y " + str(command['y']['lower_b']) + " " + str(command['y']['upper_b']) + " " +' '.join(str(j) for j in command['y']['orientation']) + " ")
            command_string += ("z " + str(command['z']['lower_b']) + " " + str(command['z']['upper_b']) + " " +' '.join(str(k) for k in command['z']['orientation']) + " ")
            # Boolean values
            command_string += (command['boolean_in'] + " ")

            # Axis
            command_string += (str(command['group_axis']) + " ")

            #Centroid
            command_string += (str(command['group_centroid_x']) + " ")
            command_string += (str(command['group_centroid_y']) + " ")
            command_string += (str(command['group_centroid_z']) + " ")


            command_string += (" " + str(command['group_radius_large'])
                               + " " + str(command['group_radius_small']))

            final_string += ("{: <16}{: <16}\n".format("group", command_string))

        return final_string

    def __void(self):
        return("")

    def __parse_fix(self):
        if len(self.fix) != self.group_num['fix_number']:
            err_string = ("Only ({}) fixes are defined, when ({}) are expected".format(
                len(self.fix), self.group_num['fix_number']))
            return(1, err_string)
        final_string = ""
        for cmd in (sorted(self.fix)):
            curr_fix = self.fix[cmd]

            # Fix boolean params
            command_string = (str(cmd) + " "
                              + curr_fix['boolean_release'] + " "
                              + curr_fix['boolean_def'] + " ")

            # Assign parameters
            command_string += (curr_fix['assign_style'] + " "
                               + str(curr_fix['assign_x']) + " "
                               + str(curr_fix['assign_y']) + " "
                               + str(curr_fix['assign_z']) + " ")
            # displacement limiter
            command_string += str(curr_fix['disp_lim']) + " "

            # Time parameters
            command_string += ('time ' + str(curr_fix['time']['time_start'])
                               + " " + str(curr_fix['time']['time_end']) + " ")

            # Gradient parameters
            command_string += str(curr_fix['boolean_grad'])
            if curr_fix['boolean_grad'] == 't':
                command_string += (" " + str(curr_fix['grad_ref_axis']) + " "
                                   + str(curr_fix['grad_assign_axis']) + " "
                                   + str(curr_fix['grad_ref_l']) + " "
                                   + str(curr_fix['grad_ref_u']))
            final_string += ("{: <16}{: <16}\n".format("fix", command_string))

        return final_string

    def __parse_cal(self):
        if len(self.cal) != self.group_num['cal_number']:
            err_string = ("Only ({}) cals are defined, when ({}) are expected".format(
                len(self.cal), self.group_num['cal_number']))
            return(1, err_string)
        final_string = ""
        for cmd in (sorted(self.cal)):
            curr_cal = self.cal[cmd]

            # Fix boolean params
            command_string = (str(cmd) + " "
                              + curr_cal['cal_variable'] + " ")
            final_string += ("{: <16}{: <16}\n".format("cal", command_string))
        return final_string

    # Consolidated function for all commands (Parsing)
    parse_switch = {
        'standard': __parse_standard,
        'refine': __parse_refine,
        'grain_move': __parse_grain_move,
        'grain_mat': __parse_grain_mat,
        'subdomain': __parse_subdomain,
        'unit_type': __parse_unit_type,
        'unit_num': __parse_unit_num,
        'box_dir': __parse_box_dir,
        'modify': __parse_modify,
        'constrain': __parse_constrain,
        'convert': __parse_convert,
        'deform': __parse_deform,
        #Pass on non-command private var
        '_CommandList__restart_group_names': __void, 
        'errors': __void,
        'group': __parse_group,
        'fix': __parse_fix,
        'cal': __parse_cal
    }

    def parse_command(self, command_name):
        try:
            val = self.parse_switch[command_name](self)
            # err_string = (">parsed non-standard command {0}".format(command_name))
        # Default value
        except KeyError:
            val = self.parse_switch['standard'](self, command_name)
            # err_string = (">parsed standard command {0}".format(command_name))
        except TypeError:
            err_string = ("({}) is expecting a string as a parameter in one of its fields. You've likely supplied the wrong value while editing single parameters".format(command_name))
            return(1, err_string)

        if not isinstance(val, str):
            if val != None:
                self.errors.append((command_name, val[1]))
            return None
        else:
            return val


    # Edit single parameter in a given command
    def __edit_standard_command_param(self, command_name, parameter, value):
        # Standard single command dictionary, key-value pairing
        try:
            ref_dictionary = getattr(self, command_name)
        except AttributeError:
            err_string = ("({}) is not a valid command, check input".format(command_name))
            return(1, err_string)

        if parameter in ref_dictionary:
            ref_dictionary[parameter] = value
            return
        else:
            err_string = ("There is no parameter ({}) for the command ({})".format(parameter, command_name))
            return(1, err_string)


    def __edit_single_nested_param(self, command_name, parameters, value):
        # Singly nested. ie. fix = {fix_1: {key11: value11},
        #                           fix_2: {key21: value21, key22: value22}}
        try:
            ref_dictionary = getattr(self, command_name)
        except AttributeError:
            err_string = ("({}) is not a valid command, check input".format(command_name))
            return(1, err_string)
        # First nested. fix_1 = {key11: value11}
        if parameters[0] in ref_dictionary:
            nest_dict = ref_dictionary[parameters[0]]

            if parameters[1] in nest_dict and parameters[1] != 'modify_style':
                nest_dict[parameters[1]] = value
                           
            else:
                err_string = ("You shouldn't be changing this! Use edit_command instead if you'd like to change")
                return(1, err_string)
        else:
            err_string = ("There is no parameter ({}) for the command ({})".format(parameters[0], command_name))
            return(1, err_string)
    
    def __edit_double_nested_param(self, command_name, parameters, value):
        # Singly nested. ie. fix = {fix_1: {key11: value11},
        #                           fix_2: {key21: value21, key22: value22}}
        try:
            ref_dictionary = getattr(self, command_name)
        except AttributeError:
            err_string = ("({}) is not a valid command, check input".format(command_name))
            return(1, err_string)
        # First nested. fix_1 = {key11: value11}
        if parameters[0] in ref_dictionary:
            nest_dict = ref_dictionary[parameters[0]]
            if parameters[1] in nest_dict and parameters[1] != 'modify_style':
                nest_dict2 = nest_dict[parameters[1]]
                if parameters[2] in nest_dict2:
                    nest_dict2[parameters[2]] = value
                else:
                    err_string = ("There is no parameter ({}) for ({}) in ({})".format(parameters[2], parameters[1], parameters[0]))
                    return(1, err_string)
                           
            elif parameters[1] == 'modify_style':
                err_string = ("You shouldn't be changing modify style! Use edit_command instead if you'd like to change")
                return(1, err_string)
            else: 
                err_string = ("There is no parameter ({}) for the group ({})".format(parameters[1], parameters[0]))
                return(1, err_string)
        else:
            err_string = ("There is no parameter ({}) for the command ({})".format(parameters[0], command_name))
            return(1, err_string)


    def edit_parameter(self, command_name, parameters, value):
        if len(parameters) == 1: 
            return self.__edit_standard_command_param(command_name, parameters[0], value)
        elif len(parameters) == 2:
            return self.__edit_single_nested_param(command_name, parameters, value)
        elif len(parameters) == 3:
            return self.__edit_double_nested_param(command_name, parameters, value)

    # Edit single parameter in a given command
    def __get_standard_command_param(self, command_name, parameter):
        # Standard single command dictionary, key-value pairing
        try:
            ref_dictionary = getattr(self, command_name)
        except AttributeError:
            err_string = ("({}) is not a valid command, check input".format(command_name))
            return(1, err_string)

        if parameter in ref_dictionary:
            return ref_dictionary[parameter]
        else:
            err_string = ("There is no parameter ({}) for the command ({})".format(parameter, command_name))
            return(1, err_string)


    def __get_single_nested_param(self, command_name, parameters):
        # Singly nested. ie. fix = {fix_1: {key11: value11},
        #                           fix_2: {key21: value21, key22: value22}}
        try:
            ref_dictionary = getattr(self, command_name)

        except AttributeError:
            err_string = ("({}) is not a valid command, check input".format(command_name))
            return(1, err_string)

        # First nested. fix_1 = {key11: value11}
        try: 
            nest_dict = ref_dictionary[parameters[0]]

        except KeyError:
            #print(ref_dictionary.keys())
            err_string = ("There is no parameter ({}) for the command ({})".format(parameters[0], command_name))
            return(1, err_string)
        
        try:
            return nest_dict[parameters[1]]
        except KeyError:
            #print(nest_dict.keys())
            err_string = ("({}) is not a parameter for the named ({}) command: ({})".format(parameters[1], command_name, parameters[0]))
            return(1, err_string)

    def __get_double_nested_param(self, command_name, parameters):
    # Double nested. ie. group = {group1: {x: lower_b, upper_b, [i, j, k]
        try:
            ref_dictionary = getattr(self, command_name)

        except AttributeError:
            err_string = ("({}) is not a valid command, check input".format(command_name))
            return(1, err_string)

        # First nested. fix_1 = {key11: value11}
        try: 
            nest_dict = ref_dictionary[parameters[0]]
            #print(0, nest_dict)
        except KeyError:
            err_string = ("There is no parameter ({}) for the command ({})".format(parameters[0], command_name))
            return(1, err_string)
        # 2nd nested   
        try:
            nest_dict2 = nest_dict[parameters[1]]
            #print(1, nest_dict2)
        except KeyError:
            err_string = ("({}) is not a parameter for the named ({}) command: ({})".format(parameters[1], command_name, parameters[0]))
            return(1, err_string)

        try:
            return nest_dict2[parameters[2]]
        except KeyError:
            err_string = ("({}) is not a parameter for the named ({}) command: ({})".format(parameters[1], command_name, parameters[0]))
            return(1, err_string)

    def get_parameter(self, command_name, parameters):

        if len(parameters) == 1: 
            return self.__get_standard_command_param(command_name, parameters[0])
        elif len(parameters) == 2:
            return self.__get_single_nested_param(command_name, parameters)
        elif len(parameters) == 3:
            return self.__get_double_nested_param(command_name, parameters)




    # Overload Operators
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

# General LinAlg utility functions, maybe move these to a separate file
def vec_to_string(vector):
    try:
        return "{0} {1} {2}".format(*vector)
    except IndexError:
        err_string = ("This is not a vector")

def cross(a, b):
    c = [a[1]*b[2] - a[2]*b[1],
         a[2]*b[0] - a[0]*b[2],
         a[0]*b[1] - a[1]*b[0]]
    return c

def dot(a, b):
    c = a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
    # Roundoff for close to zero values
    return(round(c, 14))

def theta(a,b):
    return math.acos(dot(unit(a),unit(b)))

def magnitude(a):
    return math.sqrt(a[0]**2 + a[1]**2 + a[2]**2)

def unit(a):
    return [float(i)/magnitude(a) for i in a]

def is_orthogonal(a, b, c):
    normal = not bool(dot(a, b) + dot(b, c) + dot(a, c))
    right_hand = True
    # Truncation error? round to 10 test
    b3_test= (unit(cross(a,b)))
    b3 = (unit(c))
    for i in range(3):
        if round(b3_test[i], 14) != round(b3[i], 14):
            right_hand = False
            break
    return (normal and right_hand)

def matmult(a,b):
    zip_b = zip(*b)
    zip_b = list(zip_b)
    return [[sum(ele_a*ele_b for ele_a, ele_b in zip(row_a, col_b)) 
             for col_b in zip_b] for row_a in a]

def matadd(a,b):
    s = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]
    for r in range(0,3):
        for c in range(0,3):
            s[r][c] = a[r][c] + b[r][c]
    return s

def rotated_bases(a, b, set_i):
    # https://math.stackexchange.com/questions/180418
    # Calculate a new rotated orthogonal basis from a single vector rotation
    # set = {x: [xi,xj,xk], y: [yi,yj,yk], z: [zi,zj,zk]}
    v_x = cross(unit(a),unit(b))

    c = (math.cos(theta(a,b)))

    #Skew-symmetric cross-product matrix of cross(initial, final)
    v_ss = [[0, -v_x[2], v_x[1]],
            [v_x[2], 0, -v_x[0]],
            [-v_x[1], v_x[0], 0]]
    
    iden = [[1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]]

    v_ss_square = matmult(v_ss, v_ss)

    const = 1. / (1 + c)

    v_ss_square_prod = [[const*v_ss_square[i][j] for i in range(3)] for j in range(3)]

    rotation_mat = matadd(matadd(iden, v_ss), v_ss_square_prod)
    #print(rotation_mat)


    set_f = dict()

    for b, vec in set_i.items():
        #print(b_vec)
        b_col = [[vec[0]], [vec[1]], [vec[2]]]
        result = matmult(rotation_mat, b_col)
        result = [result[0][0], result[1][0], result[2][0]]
        #print(result)
        set_f[b] = unit(result)
    
    return set_f
