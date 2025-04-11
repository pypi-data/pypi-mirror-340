import importlib

try:
    import niveristand
except:
    print("niveristand library is not installed.")
    exit(-1)

# Function to import niveristand library if it's installed, otherwise print an error message
def import_niveristand():
    try:
        niveristand = importlib.import_module('niveristand')
        return niveristand
    except:
        print("niveristand library is not installed.")
        return None
    
from logging import getLogger

logger = getLogger(__name__)

niveristand = import_niveristand()

class Mapping_type:
    def __init__(self,type):
        self.id = ''
        self.description = None
        self.mapping_type = type
        self.auto_generated = False
        self.category = None
        self.label = None
        self.xaccess = {
            "model_key": "Plant model",
            "variable_path": "",    # Custom Devices/PROVEtechRBS/BodyCAN_Tx/ABA/ABA_BodyCAN_0x5EC/ABAActvBlstrlRiInfalteVavle
            "enum": {},
            "metric": {
                "data_type": "VALUE",
                "unit": "u_none",
                "value_type": "PHYS"
            }
        }
    def to_dict(self):
        return {
            'id': self.id,
            'description':self.description,
            'mapping_type': self.mapping_type,
            'auto_generated': self.auto_generated,
            'category': self.category,
            'label': self.label,
            'xaccess': self.xaccess
        }

if niveristand:
    import os
    import psutil
    from niveristand.legacy import NIVeriStand
    from niveristand.clientapi import  ChannelReference
    import time
    class VeriStand:
        def launch_NIVeriStand(path):
            """Launch NI VeriStand.exe from the installed location."""
            if not is_process_running('VeriStand.exe'):
                import subprocess
                NIpath = NIVeriStand._internal.base_assembly_path()
                # nivsprj_path = change_extension(path,'.nivsprj')
                nivsprj_path = path
                try:
                    veristand = os.path.join(NIpath, "VeriStand.exe")
                    subprocess.Popen(['start', veristand, nivsprj_path], shell=True)
                    NIVeriStand.WaitForNIVeriStandReady()
                    print(veristand)
                    time.sleep(5)
                except OSError:
                    raise NIVeriStand.NIVeriStandException(-307652, "Could not launch VeriStand.")
            else:
                print('VeriStand is running.')
        
        def explorer():
            NIVeriStand.LaunchNIVeriStand()

        def deploy(path,timeout = 120000):
            workspace = NIVeriStand.Workspace2("localhost")
            systemstate = workspace.GetSystemState()['state']
            nivssdf_path = change_extension(path,'.nivssdf')
            if systemstate == 0:
                try:
                    workspace.ConnectToSystem(nivssdf_path, True, timeout)
                except:
                    print('Could not connect to.')

        def disconnect():
            workspace = NIVeriStand.Workspace2("localhost")
            systemstate = workspace.GetSystemState()['state']
            if systemstate:
                try:
                    workspace.DisconnectFromSystem("", True)
                except:
                    print('Could not disconnect to.')

        def close_NIVeriStand():
            pid = is_process_running('VeriStand.exe')
            if pid:
                try:
                    process = psutil.Process(pid)
                    process.terminate()
                    process.wait()
                    return True
                except:
                    return False
            else:
                print('VeriStand is not running.')
                return True

        def write(xaccess,value): 
            # value 已经eval和enum过
            path = xaccess
            target = ChannelReference(path)
            logger.info(f"Writing {path} to {value}")
            try:
                target.value = value
                return 'Writing Success'
            except niveristand.errors.VeristandError as e:
                error_mes = e.args[0]
                mes = f"Error: '{path}' //"+error_mes.split("Message:")[-1].split("\r\n.")[0]
                return mes
            except TypeError:
                return f"TypeError: Channel '{path}' only accepts numbers:" +  str(type(value))
            
        def read(xaccess):
            path = xaccess
            target = ChannelReference(path)
            logger.info(f"Reading {path}")
            try:
                return target.value
            except niveristand.errors.VeristandError as e:
                error_mes = e.args[0]
                mes = f"Error: '{path}' //"+error_mes.split("Message:")[-1].split("\r\n.")[0]
                return mes

        def enum_num(enum,value):
            for i,j in enum.items():
                if j == value:
                    return int(i)
                elif i == value:
                    return int(i)
            return value

        def enum_char(enum,value):
            for i,j in enum.items():
                if j == value:
                    return value
                elif i == value:
                    return j
                elif int(i) == value:
                    return j
            return value
        
        def system_node_mapping():
            workspace = NIVeriStand.Workspace2("localhost")
            data = workspace.GetSystemNodeChannelList("")
            SystemNodeChanneldict = {}
            for item in data:
                if not item['isChannel'] or not item['isReadable']: # 跳过不能读写的
                    continue
                if item['isWritable']:
                    mapping = Mapping_type('xaModelValueVariable')
                else:
                    mapping = Mapping_type('xaModelSignal')
                var_path = item['path'].split('Targets/Controller/')[-1]
                lst = var_path.split('/')
                if len(lst) >= 3:
                    name = '/'.join(lst[-3:])
                else:
                    name = mapping.xaccess['model_key']+'/'+'/'.join(lst[:])
                mapping.label = lst[-1]
                mapping.id = name   # to do 保持两个/ 
                mapping.xaccess['variable_path'] = var_path
                if item['unit'] != '':          # 暂时默认 "data_type" = "VALUE",
                    mapping.xaccess['metric']['unit'] = item['unit']
                mapping = mapping.to_dict()
                current = SystemNodeChanneldict
                path = item['path'].split('/')
                for key in path:
                    if isinstance(current, dict):
                        if key not in current :
                            if key != path[-2]:
                                current[key] = {}
                            elif key == path[-2]:
                                current[key] = []
                        current = current[key]
                    else:
                        flag = False
                        for map in current:
                            if key == map['label']:
                                flag = True
                        if not flag:
                            current.append(mapping)
                        break
            return SystemNodeChanneldict

    def change_extension(path, extension):
        return os.path.splitext(path)[0] + extension
    
    def is_process_running(process_name):
        for process in psutil.process_iter():
            try:
                # 获取进程的名称
                name = process.name()
                # 如果进程的名称匹配，返回 pid
                if name == process_name:
                    return process.pid
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    pass

