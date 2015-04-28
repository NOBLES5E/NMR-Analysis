__author__ = 'iceorange'

from collections import OrderedDict, defaultdict

import pickle
import copy

import nmrglue as ng
from numpy import asarray
import numpy as np
import math
import random

def _get_sorted_dic(dic):
    new_dic = OrderedDict()
    for id in sorted(dic):
        new_dic[id] = dic[id]
    return new_dic


QT_DATA_COLUMN_ENTRIES = ['DataNo.', 'Frequency', 'Field(H)', 'Pul.spw', 'Pul.fpw', 'Pul.tJ', 'Pul.t2',
                          'iteration', 'Samplingtime', 'Temp', 'level', 'gain', 'program', 'init_phase']

QT_BASIC_PROCESS_DIC = _get_sorted_dic(
    {'EchoType': 'Half', 'EchoPosition': 'auto', 'Phase': 'auto', 'PhaseMode': 'echo', 'PhaseFrom': '0 MS',
     'PhaseTo': '0 MS', 'PhaseErrorLimit': 0.01, 'EchoBaseLine': 'False', 'EchoBaseLineFrom': '0 MS',
     'EchoBaseLineTo': '0 MS', 'SpectrumBaseLine': 'False', 'SpectrumBaseLineFrom': '0 HZ',
     'SpectrumBaseLineTo': '0 HZ', 'Cut': 'False', 'CutFrom': '0 MS', 'CutTo': '0 MS'})

QT_ADVANCED_PROCESS_DIC = _get_sorted_dic({'EchoTreatment': 'none', 'SpectrumTreatment': 'none'})

QT_GLUE_INT_OPERATION_DIC = _get_sorted_dic({'GlueDelRow': '', 'GlueStep': 10000, 'IntType': 'Time', 'IntDelRow': '', 'Int_1': 'False', 'IntFrom_1': '0 MS', 'IntTo_1': '0 MS', 'Int_2': 'False',
     'IntFrom_2': '0 MS',
     'IntTo_2': '0 MS', 'Int_3': 'False', 'IntFrom_3': '0 MS', 'IntTo_3': '0 MS', 'Int_0': 'False', 'IntFrom_0': '0 MS',
     'IntTo_0': '0 MS', 'Int_x': 'DataNo.'})


class FileTypeError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Reader:
    def __init__(self, path=''):
        # set up class properties
        self.paths = []
        self.dics = []
        self.datas = []
        self.note = ''
        self._init_root_dic()
        if path:
            self.add_a_file(path)


    def clear_reader(self):
        self.__init__()

    def _init_root_dic(self):
        'initialize the root dic for GLUE and INT'
        dic = OrderedDict()
        new_dic = QT_GLUE_INT_OPERATION_DIC.copy()
        for entry in new_dic:
            dic.setdefault(entry, new_dic[entry])
        self.root_dic = dic

    def add_a_file(self, path):
        self.paths.append(path)
        new_dics, new_datas = _read_a_file(path)
        self.dics += new_dics
        self.datas += new_datas

    def save(self, path):
        with open(path, 'wb') as file:
            pickle.dump(self, file)

    def add_files(self, path_list):
        for path in path_list:
            self.add_a_file(path)

    def get_universal_entry_by_index(self, index):
        dic = self.dics[index][0]
        data = self.datas[index]
        data = _from_data_to_ndarray(data)
        dic = _from_dic_to_universal_dic(dic)
        return dic, data


    def get_pipe_entry_by_index(self, index):
        converter = ng.convert.converter()
        converter.from_universal(*self.get_universal_entry_by_index(index))
        return converter.to_pipe()

    def get_time_plot_dic_data(self, index):
        dic, data = self.get_pipe_entry_by_index(index)
        dic, data, diclist = time_process(dic, data, self.dics[index])
        return dic, data

    def get_freq_plot_dic_data(self, index):
        dic, data = self.get_pipe_entry_by_index(index)
        dic, data, diclist = freq_process(*time_process(dic, data, self.dics[index]))
        return dic, data

    def get_int_plot_dic(self):
        processed_dics, processed_datas = [], []
        for index in range(len(self.dics)):
            if self.root_dic['IntType'].lower == 'time':
                processed_dic, processed_data = self.get_time_plot_dic_data(index)
            else:
                processed_dic, processed_data = self.get_freq_plot_dic_data(index)
            processed_dics.append(processed_dic)
            processed_datas.append(processed_data)
        return int_process(processed_dics, processed_datas, self.dics, self.root_dic)

    def get_glue_plot_dic_data(self):
        processed_dics, processed_datas = [], []
        for index in range(len(self.dics)):
            processed_dic, processed_data = self.get_freq_plot_dic_data(index)
            processed_dics.append(processed_dic)
            processed_datas.append(processed_data)
        return glue_process(processed_dics, processed_datas, self.dics, self.root_dic)

def _read_a_file(path):
    # set up storage
    dics = []
    datas = []
    dic = {}
    data_time = []
    data_re = []
    data_im = []

    # read the file
    with open(path, 'r') as file:
        for line in file:
            # encounter new data set
            if line.startswith('0\t') and len(dic) > 0:
                # add last set of data
                dic['size'] = len(data_re)
                dics.append(_turn_to_default_data_dic(dic))
                datas.append((data_re, data_im))
                # reset storage
                dic = {}
                data_time = []
                data_re = []
                data_im = []
            # encounter data entry
            if line.startswith(tuple(str(i) for i in range(10))):
                time, re, im = line.strip().split('\t')
                data_time.append(float(time.replace('E', 'e')))
                data_re.append(float(re.replace('E', 'e')))
                data_im.append(float(im.replace('E', 'e')))
            # encounter parameter entry
            else:
                name, value = _clean_para_line_string(line).split('\t')
                if name in QT_DATA_COLUMN_ENTRIES:
                    try:
                        dic[name] = float(value.replace('E', 'e'))
                    except Exception:
                        dic[name] = value
        # add final set of data
        dic['size'] = len(data_re)
        dics.append(_turn_to_default_data_dic(dic))
        datas.append((data_re, data_im))
    return dics, datas


def _clean_para_line_string(line):
    translator = str.maketrans({':': '', '\n': '', ' ': '', '=': ''})
    return line.translate(translator)


def _from_data_to_ndarray(data):
    re = data[0]
    im = data[1]
    return asarray([complex(couple[0], couple[1]) for couple in zip(re, im)])


def _from_dic_to_universal_dic(dic):
    new_dic = {}
    new_dic['car'] = 0
    new_dic['complex'] = True
    new_dic['encoding'] = 'states'
    new_dic['freq'] = False
    new_dic['label'] = 'Not Specified'
    new_dic['obs'] = dic['Frequency']
    new_dic['size'] = dic['size']
    new_dic['sw'] = 1 / dic['Samplingtime']
    new_dic['time'] = True
    return {'ndim': 1, 0: new_dic}


def _turn_to_default_data_dic(dic):
    dic1 = OrderedDict()
    dic2 = OrderedDict()
    for entry in QT_DATA_COLUMN_ENTRIES:
        if entry =='init_phase':
            dic.setdefault(entry, 0)
        else:
            dic.setdefault(entry, '')
    for entry in QT_BASIC_PROCESS_DIC:
        dic1.setdefault(entry, QT_BASIC_PROCESS_DIC[entry])
    for entry in QT_ADVANCED_PROCESS_DIC:
        dic2.setdefault(entry, QT_ADVANCED_PROCESS_DIC[entry])
    final = [dic, dic1, dic2]
    return final


# Processes

# Time Process

def time_process(ori_dic, ori_data, ori_dic_list):
    dic, data, dic_list = time_baseline_process(ori_dic, ori_data, ori_dic_list)
    dic, data, dic_list = time_cut_process(dic, data, dic_list)
    dic, data, dic_list = time_phase_process(dic, data, dic_list, ori_dic_list[0])
    return dic, data, dic_list


# Frequency Process

def freq_process(ori_dic, ori_data, ori_dic_list):
    dic, data, dic_list = ft_half_echo_move_process(ori_dic, ori_data, ori_dic_list)
    freq_dic, freq_data, dic_list = ft_process(dic, data, dic_list)
    dic, data, dic_list = ft_full_echo_mux_process(freq_dic, freq_data, dic, data, dic_list)
    return dic, data, dic_list


# Time Unit Process

def time_baseline_process(ori_dic, ori_data, ori_dic_list):
    dic, data, dic_list = copy.deepcopy((ori_dic, ori_data, ori_dic_list))
    basic_process = dic_list[1]
    if basic_process['EchoBaseLine'].lower() == 'true':
        uc = ng.pipe.make_uc(dic, data)
        left = uc(basic_process['EchoBaseLineFrom'])
        right = uc(basic_process['EchoBaseLineTo'])
        dic, data = ng.pipe_proc.cbf(dic, data, reg=slice(left, right + 1))
    return dic, data, dic_list


def time_cut_process(ori_dic, ori_data, ori_dic_list):
    dic, data, dic_list = copy.deepcopy((ori_dic, ori_data, ori_dic_list))
    basic_process = dic_list[1].copy()
    if basic_process['Cut'].lower() == 'true':
        uc = ng.pipe.make_uc(dic, data)
        left = uc(basic_process['CutFrom'])
        right = uc(basic_process['CutTo'])
        dic, data = ng.pipe_proc.set(dic, data, c=0, x1=1, xn=left)
        dic, data = ng.pipe_proc.set(dic, data, c=0, x1=right)
    return dic, data, dic_list

def get_phase(dic, data, dic_list):
    basic_process = dic_list[1]
    error_limit = float(basic_process['PhaseErrorLimit'])
    if basic_process['Phase'].lower() == 'auto':
        if basic_process['PhaseMode'].lower() == 'echo':
            uc = ng.pipe.make_uc(dic, data)
            phase_from = uc(basic_process['PhaseFrom'])
            phase_to = uc(basic_process['PhaseTo'])
            return get_phase_raw(dic, data, phase_from, phase_to, error_limit, dic_list[0].get('init_phase', 0))
        else:
            freq_dic, freq_data, freq_dic_list = freq_process(dic, data, dic_list)
            uc = ng.pipe.make_uc(freq_dic, freq_data)
            phase_from = uc(basic_process['PhaseFrom'])
            phase_to = uc(basic_process['PhaseTo'])
            return get_phase_raw(dic, data, phase_from, phase_to, error_limit, dic_list[0].get('init_phase', 0))
    else:
        return float(basic_process['Phase'])

def get_phase_raw(ori_dic, ori_data, phase_from, phase_to, error_limit, phase_seed = 0):
    dic, data = copy.deepcopy((ori_dic, ori_data))
    err = get_phase_error(data, phase_from, phase_to)
    pace = 5
    ERRLIMIT = error_limit
    phase = phase_seed
    while err > ERRLIMIT:
        new_phase = phase + random.uniform(-pace, pace)
        new_dic, new_data = ng.pipe_proc.ps(dic, data, new_phase)
        new_err = get_phase_error(new_data, phase_from, phase_to)
        if(err/new_err>random.uniform(0, 1)):
            err = new_err
            if new_phase > 180:
                phase = new_phase-360
            elif new_phase < -180:
                phase = new_phase+360
            else:
                phase = new_phase
    if phase_should_flip(ng.pipe_proc.ps(dic, data, phase)[1], phase_from, phase_to):
        phase += 180
    return phase

def get_phase_error(data, phase_from, phase_to):
    return abs(np.sum(data.imag[phase_from:phase_to]))

def phase_should_flip(data, phase_from, phase_to):
    print(np.sum(data.real[phase_from:phase_to]) < 0)
    return np.sum(data.real[phase_from:phase_to]) < 0


def time_phase_process(ori_dic, ori_data, ori_dic_list, reader_dic = None):
    dic, data, dic_list = copy.deepcopy((ori_dic, ori_data, ori_dic_list))
    phase = get_phase(dic, data, dic_list)
    if reader:
        reader_dic['init_phase'] = phase
    dic, data = ng.pipe_proc.ps(dic, data, phase)
    return dic, data, dic_list


# FT Process
def ft_half_echo_move_process(ori_dic, ori_data, ori_dic_list):
    dic, data, dic_list = copy.deepcopy((ori_dic, ori_data, ori_dic_list))
    basic_process = dic_list[1]
    position = 1
    if basic_process['EchoType'].lower() == 'half':
        if basic_process['EchoPosition'].lower() == 'auto':
            position = get_echo_position(data)
        else:
            uc = ng.pipe.make_uc(dic, data)
            position = uc(basic_process['EchoPosition'])
        dic, data = ng.pipe_proc.ls(dic, data, position)
    return dic, data, dic_list


def ft_full_echo_mux_process(ori_freq_dic, ori_freq_data, ori_time_dic, ori_time_data, ori_dic_list):
    freq_dic, freq_data, dic_list = copy.deepcopy((ori_freq_dic, ori_freq_data, ori_dic_list))
    basic_process = dic_list[1]
    position = 1
    uc_time = ng.pipe.make_uc(ori_time_dic, ori_time_data)
    uc_freq = ng.pipe.make_uc(freq_dic, freq_data)
    if basic_process['EchoType'].lower() == 'full':
        if basic_process['EchoPosition'].lower() == 'auto':
            position = uc_time.us(get_echo_position(ori_time_data))
        else:
            position = uc_time.us(uc_time(basic_process['EchoPosition']))
        dx = position*10**(-6)*(abs(uc_freq.hz_limits()[0]-uc_freq.hz_limits()[1])/uc_freq._size)
        freq_data = mux_data(freq_data, 2*math.pi-dx*2*math.pi)
    return freq_dic, freq_data, dic_list

def get_echo_position(data):
    return np.argmax(np.core.umath.absolute(data))

def ft_process(ori_dic, ori_data, ori_dic_list):
    dic, data, dic_list = copy.deepcopy((ori_dic, ori_data, ori_dic_list))
    dic, data = ng.pipe_proc.ft(dic, data)
    return dic, data, dic_list


# Spectrum Process
def spectrum_baseline_process(ori_dic, ori_data, ori_dic_list):
    dic, data, dic_list = copy.deepcopy((ori_dic, ori_data, ori_dic_list))
    basic_process = dic_list[1]
    if basic_process['SpectrumBaseLine'].lower() == 'true':
        uc = ng.pipe.make_uc(dic, data)
        left = uc(basic_process['SpectrumBaseLineFrom'])
        right = uc(basic_process['SpectrumBaseLineTo'])
        dic, data = ng.pipe_proc.cbf(dic, data, reg=slice(left, right + 1))
    return dic, data, dic_list


# Glue
def glue_process(processed_dics, processed_datas, reader_list_dics, ori_root_dic):
    glue_step = ori_root_dic['GlueStep']
    glue_del_row = ori_root_dic['GlueDelRow'].split()
    glue_del_row = [(int(row)-1) for row in glue_del_row]

    freq_list = [dic_list[0]['Frequency'] for dic_list in reader_list_dics]
    freq_left_index = np.argmin(freq_list)
    freq_right_index = np.argmax(freq_list)
    freq_left_boundary = reader_list_dics[freq_left_index][0]['Frequency']+get_freq_boundary(processed_dics[freq_left_index], processed_datas[freq_left_index])[1]
    freq_right_boundary = reader_list_dics[freq_right_index][0]['Frequency']+get_freq_boundary(processed_dics[freq_right_index], processed_datas[freq_right_index])[0]

    new_x_array = np.array([freq_left_boundary + glue_step*count for count in range(int((freq_right_boundary-freq_left_boundary)/glue_step))])
    new_y_list = []
    for index in range(len(reader_list_dics)):
        if index not in glue_del_row:
            uc = ng.pipe.make_uc(processed_dics[index], processed_datas[index])
            x = uc.hz_scale()
            x += reader_list_dics[index][0]['Frequency']
            new_y_list.append(np.interp(new_x_array, x[::-1], processed_datas[index].real[::-1], 0, 0)+1j*np.interp(new_x_array, x[::-1], processed_datas[index].imag[::-1], 0, 0))
    return new_x_array, sum(new_y_list), new_y_list

def get_freq_boundary(dic, data):
    uc = ng.pipe.make_uc(dic, data)
    return uc.hz_limits()


# Int
def int_process(ori_pipe_dics, ori_pipe_datas, ori_dics, ori_root_dic):
    int_del_row = ori_root_dic['IntDelRow'].split()
    int_del_row = [int(row)-1 for row in int_del_row]
    root_dic = copy.deepcopy(ori_root_dic)
    def new_plot_unit():
        return [[], []]
    int_plot_dic = defaultdict(new_plot_unit)


    for index, pipe_dic in enumerate(ori_pipe_dics):
        if index not in int_del_row:
            data = ori_pipe_datas[index]
            for int_index in range(4):
                if root_dic['Int_' + str(int_index)].lower() != 'false':
                    int_plot_dic[int_index][0].append(ori_dics[index][0][root_dic['Int_x']])
                    int_plot_dic[int_index][1].append(get_int_value(pipe_dic, data, root_dic['IntFrom_' + str(int_index)], root_dic['IntTo_'+str(int_index)]))
    for key in int_plot_dic:
        int_plot_dic[key] = [sorted(int_plot_dic[key][0]), list(zip(*sorted(zip(*int_plot_dic[key]), key= lambda member: member[0])))[1]]
    return int_plot_dic

def get_int_value(pipe_dic, pipe_data, int_from, int_to):
    uc = ng.pipe.make_uc(pipe_dic, pipe_data)
    left = min(uc(int_from), uc(int_to))
    right = max(uc(int_from), uc(int_to))
    return sum(pipe_data[left:right])

def mux_data(data, dx):
    new_data = []
    for i in range(len(data)):
        new_data.append(data[i]*np.exp(i*dx*1j))
    return asarray(new_data)

reader = Reader()