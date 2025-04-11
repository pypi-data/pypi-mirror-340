import json,os
import cantools,ldfparser
from pathlib import Path

def create_variable_name(name):
    for c in name:
        if not c.isascii():
            return None
    # 替换所有非法字符为下划线
    rename = ''.join(c if c.isalnum() else '_' for c in name)
    # 确保不以数字开头
    if rename[0].isdigit():
        rename = '_' + rename
    # 处理Python关键字冲突
    python_keywords = ['False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class', 'continue', 
                    'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 
                    'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 
                    'raise', 'return', 'try', 'while', 'with', 'yield']
    if rename in python_keywords:
        rename = '_' + rename
    return rename

class GenBusJson:
    def __init__(self):
        
        self.signals = []
        self.can_json = {}
        self.lin_json = {}
        self.source_can = ''
        self.source_message = ''

    # 从DBC文件中解析出CAN总线和LIN总线信息存到JSON中
    def parse_dbc_files(self, dbc_dir):
        self.dbc_dir = Path(dbc_dir)
        for file in self.dbc_dir.glob('*.dbc'):
            db = cantools.db.load_file(str(file))
            can_name = str(db.buses[0]).split('\'')[1]
            for message in db.messages:
                if message.signals:
                    sender = message.senders[0]
                    for signal in message.signals:
                        if signal.name not in self.can_json:
                            self.can_json[signal.name] = {}
                        if sender not in self.can_json[signal.name]:
                            self.can_json[signal.name][sender] = {} 
                        self.can_json[signal.name][sender][can_name] = {
                            "name": signal.name,
                            "message_name": message.name,
                        }
                    
        for file in self.dbc_dir.glob('*.ldf'):
            ldf_db = ldfparser.parse_ldf_to_dict(str(file),encoding='utf-8')
            lin_name = file.stem.split('_')[2]+'_'+file.stem.split('_')[3]
            for message in ldf_db['frames']:
                sender = message['publisher'].split('_')[0]
                for signal in message['signals']:
                    signal_name = signal['signal']
                    if signal_name not in self.lin_json:
                        self.lin_json[signal_name] = {}
                    if sender not in self.lin_json[signal_name]:
                        self.lin_json[signal_name][sender] = {}
                    self.lin_json[signal_name][sender][lin_name] = {
                        "name": signal_name,
                        "message_name": message['name'],
                    }
                    
        with open(r'databases\other\can_bus.json', 'w', encoding='utf-8') as f:
            json.dump(self.can_json, f, ensure_ascii=False, indent=4)
        with open(r'databases\other\lin_bus.json', 'w', encoding='utf-8') as f:
            json.dump(self.lin_json, f, ensure_ascii=False, indent=4)
            

    
    def get_bus_mapping_by_name(self, name):
        with open(r'databases\other\can_bus.json', 'r', encoding='utf-8') as f:
            can_dict = json.load(f)
        with open(r'databases\other\lin_bus.json', 'r', encoding='utf-8') as f:
            lin_dict = json.load(f)
        can_list = list(can_dict[name].keys())
        senders_set = set()
        receivers_set = set()
        for can in can_list:
            senders_set.add(can_dict[name][can]['senders'])
            receivers_set.update(can_dict[name][can]['receivers'])
        intersection_set = senders_set & receivers_set
        intersection_list = list(intersection_set)
        source_list = list(senders_set - receivers_set)
        target_list = list(receivers_set - senders_set)
        print(source_list)
        print(can_list)
        print(intersection_list)
        for can in can_list:
            if can_dict[name][can]['senders'] == source_list[0]:
                source_can = can
                source_message = can_dict[name][can]['message_name']
                return source_can, source_message
            
    def gen_can_lib(self,dbc_dir):
        with open(r'lib\buslib.py', 'w', encoding='utf-8') as f:
            dbc_files = [f for f in os.listdir(dbc_dir) if f.endswith('.dbc')]
            if len(dbc_files) == 0:
                print('no dbc files')
                return
            for dbc_file in dbc_files:
                dbc_path = os.path.join(dbc_dir,dbc_file)
                db = cantools.database.load_file(dbc_path)
                for message in db.messages:
                    sender = message.senders[0]
                    for signal in message.signals:
                        class_name = str(signal.name+'_'+sender+'_'+'can').replace('/','_').replace(' ','_')
                        f.write("class "+class_name+':\n')
                        if signal.choices:
                            choices = signal.choices
                            for c in choices:
                                enum_value = str(choices[c])
                                enum_name = create_variable_name(enum_value)
                                if enum_name is None:
                                    continue
                                f.write("\t%s = %d\n"%(enum_name,c))
                        f.write("\tnode = \""+sender+"\"\n")
                        f.write("\tname = \""+signal.name+"\"\n")

    def gen_lin_lib(self,dbc_dir):
        with open(r'lib\buslib.py', 'a', encoding='utf-8') as f:
            ldf_files = [f for f in os.listdir(dbc_dir) if f.endswith('.ldf')]
            if len(ldf_files) == 0:
                print('no ldf files')
                return
            for ldf_file in ldf_files:
                ldf_path = os.path.join(dbc_dir,ldf_file)
                ldf_db = ldfparser.parse_ldf_to_dict(ldf_path,encoding='utf-8')
                for signal in ldf_db['signals']:
                    sender = signal["publisher"].split('_')[0]
                    f.write(signal["name"]+'_'+sender+'_'+'lin'+'='+ '\"'+signal["name"]+'\"'+'\n')
                # with open('ldf_db.json', 'w', encoding='utf-8') as ldffile:
                #     json.dump(ldf_db, ldffile, ensure_ascii=False, indent=4)
                # # for message in ldf_db.messages:
                # #     for signal in message.signals:
                # #         f.write(signal.name+'_'+message.senders[0]+'_'+'can'+'='+ '\"'+signal.name+'\"'+'\n')
                # for key,value in ldf_db.items():
                #     # f.write(key+'_'+value['senders'][0]+'_'+'can'+'='+ '\"'+key+'\"'+'\n')
                #     print(key,value)
            
            
            

            
if __name__ == '__main__':
    dbc_dir = r'D:\02_Project\CANoe\N3_E4\Databases'
    gen_bus_json = GenBusJson()
    gen_bus_json.parse_dbc_files(dbc_dir)
    # bus_list = gen_bus_json.get_bus_mapping_by_name('PwrModSts')
    # print(bus_list)
    gen_bus_json.gen_can_lib(dbc_dir)
    gen_bus_json.gen_lin_lib(dbc_dir)
    


