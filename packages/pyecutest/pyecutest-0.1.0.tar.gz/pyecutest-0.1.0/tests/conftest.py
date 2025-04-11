import pytest
from core.executor import TestExecutor
import yaml
from logging import getLogger

@pytest.fixture(scope="session")
def executor():
    """
    创建一个session级别的executor fixture
    """
    tools_status = {
        "canoe":False,
        "inca":False,
        "veristand":False,
        "adb":False,
        "tsmaster":False,
        "mi_ant":False
    }
    tools = {
        "canoe":None,
        "inca":None,
        "veristand":None,
        "adb":None,
        "tsmaster":None,
        "mi_ant":None
    }
    with open(r'config\conf.yaml', 'r', encoding='utf8') as f:
        config = yaml.load(f.read(),Loader=yaml.FullLoader)
    logger = getLogger(__name__)
    
    if "canoe" in config['project']['tools']:
        try:
            from interfaces.canoe.canoe import canoe_inst
            from core.signal_mapper import SignalMapper
            signal_mapper = SignalMapper(r'databases\other\can_bus.json',r'databases\other\lin_bus.json')
            tools["canoe"] = [canoe_inst,signal_mapper]
            tools_status["canoe"] = True
        except Exception as e:
            print("canoe配置失败")
            tools["canoe"] = None
            tools_status["canoe"] = False
    
    if "inca" in config['project']['tools']:
        try:
            from interfaces.inca.inca import Inca, IncaWrapper
            inca= Inca().get_inca('<system default>')
            experiment_obj = inca.GetOpenedExperiment()
            print(experiment_obj)
            inca_wrapper = IncaWrapper(experiment_obj)
            tools["inca"] = [inca,inca_wrapper]
            tools_status["inca"] = True
        except Exception as e:
            print("inca配置失败")
            tools["inca"] = None
            tools_status["inca"] = False

    if "veristand" in config['project']['tools']:
        try:
            from interfaces.veristand.veristand import VeriStand
            veristand = VeriStand
            veristand.launch_NIVeriStand(config['veristand']['nivsprj_path'])
            veristand.deploy(config['veristand']['nivssdf_path'])
            tools["veristand"] = veristand
            tools_status["veristand"] = True
        except Exception as e:
            print("veristand配置失败")
            tools["veristand"] = None
            tools_status["veristand"] = False
    
    if "adb" in config['project']['tools']:
        try:
            from interfaces.adb.adb import adb
            tools["adb"] = adb(logger)
            tools_status["adb"] = True
        except Exception as e:
            print("adb配置失败")
            tools["adb"] = None
            tools_status["adb"] = False
    
    if "tsmaster" in config['project']['tools']:
        try:
            from interfaces.tsmaster.tsmaster import TSMaster
            from core.signal_mapper import SignalMapper
            signal_mapper = SignalMapper(r'databases\other\can_bus.json',r'databases\other\lin_bus.json')
            tools["tsmaster"] = [TSMaster(),signal_mapper]
            tools_status["tsmaster"] = True
        except Exception as e:
            print("tsmaster配置失败")
            tools["tsmaster"] = None
            tools_status["tsmaster"] = False
    
    if "mi_ant" in config['project']['tools']:
        try:
            from interfaces.mi_ant.mi_ant import mi_ant
            tools["mi_ant"] = mi_ant(config['mi_ant']['port'])
            tools_status["mi_ant"] = True
        except Exception as e:
            print("mi_ant配置失败")
            tools["mi_ant"] = None
            tools_status["mi_ant"] = False
    

    executor = TestExecutor(tools,tools_status,config,logger)
    yield executor
    # 测试结束后的清理工作
    # executor.cleanup() # 如果有清理方法的话
