import os
import json
from logging import getLogger
import yaml

class SignalMapper:
    def __init__(self, can_json_path, lin_json_path):
        self.can_json_file = can_json_path
        self.lin_json_file = lin_json_path
        self.can_json = {}
        self.lin_json = {}
        self.logger = getLogger(__name__)
        self.get_bus_json()
        self.get_config()
        
    def get_config(self):
        with open(r'config\conf.yaml', 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

    def get_bus_json(self):
        with open(self.can_json_file , 'r', encoding='utf-8') as f:
            self.can_json = json.load(f)
        with open(self.lin_json_file, 'r', encoding='utf-8') as f:
            self.lin_json = json.load(f)
    
    def get_signal_info(self, signal_name : classmethod):
        bus_list = list(self.can_json[signal_name.name][signal_name.node].keys())
        message_list = []
        for bus in bus_list:
            message_list.append(self.can_json[signal_name.name][signal_name.node][bus]['message_name'])
        return bus_list, message_list
    
            
if __name__ == '__main__':
    signal_mapper = SignalMapper(r'temp\can_bus.json', r'temp\lin_bus.json')
    signal_mapper.get_bus_json()
    signal_mapper.get_config()
    # source_can, source_message = signal_mapper.get_signal_info(buslib.PwrModSts_FZCU_can)
    # print(source_can, source_message)



