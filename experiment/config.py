import pathlib
import numpy

DIR = pathlib.Path(__file__).parent.absolute()


def get_config():
    config_obj = {}
    proc_list = [['RP2', 'RP2', DIR / 'RCX_files' / 'bi_play_buf.rcx'],
                 ['RX81', 'RX8', DIR / 'RCX_files' / 'play_buf.rcx'],
                 ['RX82', 'RX8', DIR / 'RCX_files' / 'play_buf.rcx']]
    config_obj['proc_list'] = proc_list
    return config_obj
