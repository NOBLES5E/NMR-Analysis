__author__ = 'iceorange'
import nmr_analysis
from numpy import asarray
from collections import OrderedDict
import nmrglue as ng

# funcargs
def pytest_funcarg__reader(request):
    return nmr_analysis.Reader('testdata/test.txt')


def pytest_funcarg__test_file_path(request):
    return 'testdata/test.txt'


def pytest_funcarg__para_line_string(request):
    return 'DataNo. \t5\n'


def pytest_funcarg__data_entry_index(request):
    return 1


def pytest_funcarg__new_data_para(request):
    return ['Temp', 50]


def pytest_funcarg__raw_data(request):
    return [[1, 1, 1], [2, 2, 2]]


def pytest_funcarg__raw_dic(request):
    return {'Temp': 0.0, 'size': 8192, 'Pul.fpw': 1e-06, 'Pul.t2': 1.5e-05, 'Frequency': 165500000.0, 'Pul.tJ': 0.0001,
            'DataNo.': 1.0, 'Samplingtime': 2e-07, 'Field(H)': 0.0, 'iteration': 80.0, 'Pul.spw': 2e-06}

def pytest_funcarg__raw_path(request):
    return 'file:///home'

def pytest_funcarg__pipe_dic_data_diclist(request):
    reader = nmr_analysis.Reader('testdata/test.txt')
    dic, data = reader.get_pipe_entry_by_index(1)
    return dic, data, [{'Pul.t2': 3e-05, 'Field(H)': 0.0, 'size': 7, 'gain': '', 'Pul.tJ': 0.0015656065579431, 'Temp': 0.0, 'Samplingtime': 4e-08, 'Frequency': 163850000.0, 'DataNo.': 2.0, 'program': '', 'Pul.fpw': 3e-06, 'level': '', 'iteration': 800.0, 'Pul.spw': 6e-06},
                       OrderedDict([('Cut', 'True'), ('CutFrom', '0.0001 MS'), ('CutTo', '0.0002 MS'), ('EchoBaseLine', 'True'), ('EchoBaseLineFrom', '0 MS'), ('EchoBaseLineTo', '0 MS'), ('EchoPosition', '0.0001 MS'), ('EchoType', 'Half'), ('Phase', 'auto'), ('PhaseFrom', '0 MS'), ('PhaseMode', 'echo'), ('PhaseTo', '0 MS'), ('SpectrumBaseLine', 'True'), ('SpectrumBaseLineFrom', '0 HZ'), ('SpectrumBaseLineTo', '0 HZ')]),
                       OrderedDict([('EchoTreatment', 'none'), ('SpectrumTreatment', 'none')])]
def pytest_funcarg__array_data(request):
    return asarray([1,1,1,1,1])

# Test functions
def test__read_a_file(test_file_path):
    dics, datas = nmr_analysis._read_a_file(test_file_path)
    assert len(dics) == 20 and len(datas) == 20


def test__clean_para_line_string(para_line_string):
    assert nmr_analysis._clean_para_line_string(para_line_string) == 'DataNo.\t5'


def test__from_data_to_ndarray(raw_data):
    array = nmr_analysis._from_data_to_ndarray(raw_data)
    print(array)
    assert array.all() == asarray([complex(1, 2), complex(1, 2), complex(1, 2)]).all()


def test__from_dic_to_universal_dic(raw_dic):
    new_dic = nmr_analysis._from_dic_to_universal_dic(raw_dic)
    assert new_dic == {'ndim': 1,
                       0: {'sw': 5000000.0, 'complex': True, 'time': True, 'car': 0, 'label': 'Not Specified',
                           'obs': 165500000.0, 'freq': False, 'size': 8192, 'encoding': 'states'}}


def test__turn_to_default_data_dic():
    assert len(nmr_analysis._turn_to_default_data_dic({})[0]) == 13

def test__get_sorted_dic(raw_dic):
    assert nmr_analysis._get_sorted_dic(raw_dic).popitem()[0] == sorted(OrderedDict(raw_dic))[-1]

def test_time_baseline_process(pipe_dic_data_diclist):
    dic, data, dic_list =  nmr_analysis.time_baseline_process(pipe_dic_data_diclist[0], pipe_dic_data_diclist[1], pipe_dic_data_diclist[2])
    assert data[0] == 0

def test_time_cut_process(pipe_dic_data_diclist):
    dic, data, dic_list =  nmr_analysis.time_cut_process(pipe_dic_data_diclist[0], pipe_dic_data_diclist[1], pipe_dic_data_diclist[2])
    print(data, pipe_dic_data_diclist[1])
    assert data[0] != pipe_dic_data_diclist[1][0]

def test_time_phase_process(pipe_dic_data_diclist):
    dic, data, dic_list =  nmr_analysis.time_phase_process(pipe_dic_data_diclist[0], pipe_dic_data_diclist[1], pipe_dic_data_diclist[2])
    assert data.all() == pipe_dic_data_diclist[1].all()

def test_ft_half_echo_move_process(pipe_dic_data_diclist):
    dic, data, dic_list =  nmr_analysis.ft_half_echo_move_process(pipe_dic_data_diclist[0], pipe_dic_data_diclist[1], pipe_dic_data_diclist[2])
    assert data[-1] == 0

def test_ft_process(pipe_dic_data_diclist):
    dic, data, dic_list =  nmr_analysis.ft_process(pipe_dic_data_diclist[0], pipe_dic_data_diclist[1], pipe_dic_data_diclist[2])
    assert ng.pipe.guess_udic(dic, data)[0]['freq'] == True

def test_spectrum_baseline_process(pipe_dic_data_diclist):
    dic, data, dic_list = nmr_analysis.ft_process(pipe_dic_data_diclist[0], pipe_dic_data_diclist[1], pipe_dic_data_diclist[2])
    dic, data, dic_list = nmr_analysis.spectrum_baseline_process(dic, data, dic_list)
    assert data[3] == 0

def test_mux_data(array_data):
    print(array_data)
    print(nmr_analysis.mux_data(array_data, 1))

# Test Reader class
class TestReader:
    def test_add_a_file(self, reader):
        reader.add_a_file('testdata/test1.txt')
        assert len(reader.dics) == 40

    def test_get_universal_entry_by_index(self, reader, data_entry_index):
        dic, data = reader.get_universal_entry_by_index(data_entry_index)
        assert len(data) == dic[0]['size']

    def test_get_pipe_entry_by_index(self, reader, data_entry_index):
        dic, data = reader.get_pipe_entry_by_index(data_entry_index)
        assert dic, data

    def test__init_root_dic(self, reader):
        assert reader.root_dic

    def test_clear_reader(self, reader):
        reader.clear_reader()
        assert not reader.paths

    def test_add_files(self, reader):
        reader.add_files(['testdata/test1.txt'])
        assert len(reader.dics) == 40
