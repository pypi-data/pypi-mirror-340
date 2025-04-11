import sys
import clr
from datetime import datetime
import winreg
import ctypes as c
import os
from logging import getLogger

logger = getLogger(__name__)

class IncaWrapper:
    def __init__(self, experimentObj) -> None:
        self.ExperimentObj = experimentObj
        if self.ExperimentObj is None:
            logger.error('请检查INCA COMAPI是否被其他工具占用！❌')
        else:
            logger.info('inca获取成功✅')
            
        self.calibration_log = []
        
    def write_calibration(self, element, value):
        CalibrationElementObj = self.ExperimentObj.GetCalibrationElement(element.name)
        CalibrationElementObj.OpenView()
        Inca().set_calibration(self.ExperimentObj, CalibrationElementObj.GetName(), value)
        self.calibration_log.append(CalibrationElementObj.GetName())

    def read_calibration(self, element):
        CalibrationElementObj = self.ExperimentObj.GetCalibrationElement(element.name)
        CalibrationElementObj.OpenView()
        value = Inca().get_calibration(self.ExperimentObj, CalibrationElementObj.GetName())
        return value

    def read_measurement(self, element):
        MeasurementElementObj = self.ExperimentObj.GetMeasureElement(element.name)
        MeasurementElementObj.OpenView()
        value = Inca().get_measure(self.ExperimentObj, MeasurementElementObj.GetName())
        return value
    
    def reset_calibration(self):
        for element in self.calibration_log:
            self.write_calibration(element, None)

class Inca:
    method_executed = False

    def __init__(self,) -> None:
        pass

    def location(self,version):
        if not Inca.method_executed:
            if version == '<system default>' or version == 'system default':
                version7_3 = True
                version7_2 = True  
                try:
                    string = rf'SOFTWARE\ETAS\INCA\7.3\GenesisAutoGenereated'
                    handle = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, string, 0, (winreg.KEY_WOW64_64KEY + winreg.KEY_READ))
                except:
                    version7_3 = False
                if not version7_3:
                    try:
                        string = rf'SOFTWARE\ETAS\INCA\7.2\GenesisAutoGenereated'
                        handle = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, string, 0, (winreg.KEY_WOW64_64KEY + winreg.KEY_READ))
                    except:
                        version7_2 = False
                if not version7_2:
                    try:
                        string = rf'SOFTWARE\ETAS\INCA\7\GenesisAutoGenereated'
                        handle = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, string, 0, (winreg.KEY_WOW64_64KEY + winreg.KEY_READ)) 
                    except:
                        return False
            else:
                try:
                    string = rf'SOFTWARE\ETAS\INCA\{version}\GenesisAutoGenereated'
                    handle = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, string, 0, (winreg.KEY_WOW64_64KEY + winreg.KEY_READ))
                except:
                    return False
            location, _type = winreg.QueryValueEx(handle, "PRODINSTDIR")
            sys.path.append(r'C:\ETAS\INCA7.3\cebra')
            # sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            clr.AddReference('incacom')
            clr.AddReference('Etas.Base.ComSupport') 
            # dll = c.cdll.LoadLibrary('incacom.dll')
            
            # import de.etas.cebra.toolAPI.Inca as API
            Inca.method_executed = True
            
        else:
            print('方法已经执行过')
        return True

    # 实例化一个INCA
    def get_inca(self,version = '<system default>'):
        if self.location(version):
            # clr.AddReference('incacom')
            # clr.AddReference('Etas.Base.ComSupport') 
            import de.etas.cebra.toolAPI.Inca as API
            try:
                INCA = API.Inca(True)
            except Exception as e:
                print(e)
            return INCA
        else:
            return None
    
    # 退出当前的INCA
    def exit(self,INCA):
        if INCA == None:
            print('当前已无INCA进程')
        else:
            try:
                INCA.CloseTool()
            except Exception as e:
                print(e)
            print("INCA进程关闭成功")


    def stop_measurement(self,INCA):
        m_Experiment=INCA.GetOpenedExperiment()
        m_Experiment.StopMeasurement()


    # 测量暂时不用
    def start_measurement(self,INCA):
        m_Experiment=INCA.GetOpenedExperiment()
        m_Experiment.StartMeasurement()


    # 构建实验环境 
    def Environment(self,INCA,config):
        DB = INCA.GetCurrentDataBase()

        # 创建顶层文件夹
        if DB.GetIncaFolder(config.folder) is None:
            Folder = DB.AddIncaFolder(config.folder)
        else:
            Folder = DB.GetIncaFolder(config.folder)

        Experiment_name = []
        workspace_name = []
        asap2project_name = []

        # 获取该文件夹下所有组件，有也不一定是项目使用的那个组件
        allcomponents = Folder.GetAllComponents()
        for component in allcomponents:
            if component.IsExperimentEnvironment():
                Experiment_name.append(component.GetName())
            if component.IsHardwareConfiguration():
                workspace_name.append(component.GetName())
            if component.IsAsap2Project():
                asap2project_name.append(component.GetName())

        # 确定现存的experiment是否是配置中的，如果不是，则创建一个
        if config.experiment in Experiment_name:
            Experiment = Folder.GetComponent(config.experiment)
        else:
            Experiment = Folder.AddExperimentEnvironment(config.experiment)

        # 确定现存的workspace是否是配置中的，如果不是，则创建一个
        if config.workspace in workspace_name:
            HWConfig = Folder.GetComponent(config.workspace)
        else:
            HWConfig = Folder.AddHardwareConfiguration(config.workspace)
            
        device_name = config.ports[0].device
        print('device name:',device_name)
        
        HWWorkBase = self.Hardware(INCA,HWConfig,device_name)
        self.asap2_project(Folder,config,HWWorkBase,asap2project_name)

        #添加设备到workspace
        #设备添加项目和实验
        HWConfig.SetExperimentEnvironment(Experiment)
        #初始化硬件
        HWConfig.InitializeHardware()
        #打开实验
        ExperimentViewObj = Experiment.OpenExperiment()
        #获取实验
        ExperimentObj = ExperimentViewObj.GetExperiment()
        #获取实验设备
        ExpDeviceObj = ExperimentObj.GetDevice(device_name)
        #可以标定
        ExpDeviceObj.SwitchToWorkingPage()


    def Hardware(self,INCA,HWConfig,device_name):
        """查找Device名字是否能对应，不能对应则初始化一个Devcie"""
        # 这里有逻辑问题：如果部署了多个设备，而目标设备没有被激活，怎么办？目前找到目标设备就认为是激活的
        HWWorkBase = None
        HwSystems = HWConfig.GetAllSystems()            # [ES582.1]
        for HwSystem in HwSystems:
            HwSubSystems = HwSystem.GetAllSystems()     # [CAN:1]
            for HwSubSystem in HwSubSystems:
                HwDevices = HwSubSystem.GetAllDevices()
                for HwDevice in HwDevices:
                    if HwDevice.GetName() == device_name:
                        HWWorkBase = HwDevice
        # 查看有无设备，没有设备要添加一个设备
        # 获取设备描述 GetDeviceDescription
        if HWWorkBase is None:
            FHWSD = INCA.GetSystemDescription('ES582.1')
            SHWSD = FHWSD.GetSystemDescription('ES582_CAN')
            DevDescription = SHWSD.GetDeviceDescription('XCP')
            HWWorkBase = HWConfig.AddDevice(DevDescription)
            #修改设备名称
            HWWorkBase.SetName(device_name)
        return HWWorkBase
        
    
    def asap2_project(self,Folder,config,HWWorkBase,asap2project_name):
        """
        查看传输的字段是否含有a2l和hex文件地址：
        如果有则查看是否有相应project；
        如果没有则创建；
        如果既没有文件地址，也没有project，则激活失败
        """
        # 这里逻辑有点问题 to do
        # 查看有无a2l和hex文件，有文件，要创建一个新的project，没有文件，且 asap2project_name不为空，则认为已经配置好了
        a2lpath = config.ports[0].a2lFile
        hexpath = config.ports[0].hexFile
        reloadPST = config.ports[0].reloadPST
        project_name = a2lpath.split("/")[-1].split("\\")[-1].split('.a2l')[0]
        dataset_name = hexpath.split("/")[-1].split("\\")[-1].split('.s19')[0].split('.hex')[0]
        if reloadPST == 'Use existing dataset':
            if Folder.GetComponent(project_name) is None:
                ASAP2Project = Folder.ReadASAP2FileAndHexFile(a2lpath, hexpath)
            else:
                ASAP2Project = Folder.GetComponent(project_name)
            # HWWorkBase.SetProjectAndDataSet(ASAP2Project,dataset_name)
        elif reloadPST == 'Create new dataset':
            # to do
            if Folder.GetComponent(project_name) is None:
                ASAP2Project = Folder.ReadASAP2FileAndHexFile(a2lpath, hexpath)
            else:
                ASAP2Project = Folder.GetComponent(project_name)
            # Temp_folder = ASAP2Project.AddTopFolder('MIECU-Test-temp')
            # a = ASAP2Project.GetAllDataSets()
        elif reloadPST == 'Replace ASAP2 project':
            # 移除原来的project
            ASAP2Project = Folder.GetComponent(project_name)
            Folder.RemoveComponent(ASAP2Project)
            # 重新加载a2l和hex，生成新的project
            ASAP2Project = Folder.ReadASAP2FileAndHexFile(a2lpath, hexpath)
        HWWorkBase.SetProjectAndDataSet(ASAP2Project,dataset_name)

        
###################################  Read  #####################################
    def get_measure(self,ExperimentObj,name):
        ScalarMeasureElementObj  = ExperimentObj.GetMeasureElement(name)
        MeasureScalarDataVObj  = ScalarMeasureElementObj.GetValue()
        try:
            MeasureValue = MeasureScalarDataVObj.GetDoublePhysValue()
        except:
            MeasureValue = MeasureScalarDataVObj.GetCharPhysValue()
        return MeasureValue


    def get_calibration(self,ExperimentObj,name):
        ScalarCalibrationElementObj = ExperimentObj.GetCalibrationElement(name)
        CalibrationScalarDataObj = ScalarCalibrationElementObj.GetValue()
        try:
            CalibrationValue = CalibrationScalarDataObj.GetDoublePhysValue()
        except:
            CalibrationValue = CalibrationScalarDataObj.GetCharPhysValue()
        return CalibrationValue


    def get_valblk_calibration(self, ExperimentObj, name):
        ArrayCalibrationElementObj = ExperimentObj.GetCalibrationElement(name)
        CalibrationArrayDataObj = ArrayCalibrationElementObj.GetValue()
        a = CalibrationArrayDataObj.GetSize()
        b = CalibrationArrayDataObj.GetMaxSize()
        SystemArrayData = CalibrationArrayDataObj.GetDoublePhysValue()
        CalibrationValue = [value for value in SystemArrayData]
        return CalibrationValue


    def get_curve_calibration(self,ExperimentObj,name):
        OneDTableCalibrationElementObj = ExperimentObj.GetCalibrationElement(name)
        CalibrationOneDTableDataObj = OneDTableCalibrationElementObj.GetValue()
        CalibrationOneDTableDataObj = CalibrationOneDTableDataObj.GetValue()
        SystemArrayData = CalibrationOneDTableDataObj.GetDoublePhysValue()
        CalibrationValue = [value for value in SystemArrayData]
        return CalibrationValue
        

    def get_map_calibration(self,ExperimentObj,name):
        TwoDTableCalibrationElementObj = ExperimentObj.GetCalibrationElement(name)
        CalibrationTwoDTableDataObj = TwoDTableCalibrationElementObj.GetValue()
        CalibrationMatrixDataObj = CalibrationTwoDTableDataObj.GetValue()
        SystemMatrixData = CalibrationMatrixDataObj.GetDoublePhysValue()
        CalibrationValue = [[value for value in row] for row in SystemMatrixData]
        return CalibrationValue
        

###################################  Write  #####################################
    def set_calibration(self,ExperimentObj,name,value):
        ScalarCalibrationElementObj = ExperimentObj.GetCalibrationElement(name)
        CalibrationScalarDataObj = ScalarCalibrationElementObj.GetValue()
        try:
            bSuccess = CalibrationScalarDataObj.SetDoublePhysValue(value)
        except:
            bSuccess = CalibrationScalarDataObj.SetCharPhysValue(value)
        return bSuccess
    
    
    def set_valblk_calibration(self,ExperimentObj, name, value:list):
        ArrayCalibrationElementObj = ExperimentObj.GetCalibrationElement(name)
        CalibrationArrayDataObj = ArrayCalibrationElementObj.GetValue()
        SystemArrayData = CalibrationArrayDataObj.GetDoublePhysValue()
        for i in value:
            SystemArrayData[int(i[0])] = i[1]
        bSuccess = CalibrationArrayDataObj.SetDoublePhysValue(SystemArrayData)
        return bSuccess
    

    def set_curve_calibration(self, ExperimentObj, name, value:list):
        OneDTableCalibrationElementObj = ExperimentObj.GetCalibrationElement(name)
        CalibrationOneDTableDataObj = OneDTableCalibrationElementObj.GetValue()
        CalibrationArrayDataObj = CalibrationOneDTableDataObj.GetValue()
        SystemArrayData = CalibrationArrayDataObj.GetDoublePhysValue()
        for i in value:
            SystemArrayData[int(i[0])] = i[1]
        CalibrationArrayDataObj.SetDoublePhysValue(SystemArrayData)
        bSuccess = CalibrationOneDTableDataObj.SetValue(CalibrationArrayDataObj)
        return bSuccess


    def set_map_calibration(self, ExperimentObj, name, value:list):
        TwoDTableCalibrationElementObj = ExperimentObj.GetCalibrationElement(name)
        CalibrationTwoDTableDataObj = TwoDTableCalibrationElementObj.GetValue()
        CalibrationMatrixDataObj = CalibrationTwoDTableDataObj.GetValue()
        SystemmMtrixData = CalibrationMatrixDataObj.GetDoublePhysValue()
        for i in value:
            SystemmMtrixData[int(i[0])][int(i[1])] = i[2]
        bSuccess = CalibrationMatrixDataObj.SetDoublePhysValue(SystemmMtrixData)
        return bSuccess
    

###################################  Write  #####################################
    def finally_get_measure(self,ExperimentObj,name,time,value):
        MeasureElementObj  = ExperimentObj.GetMeasureElement(name)
        MeasureValueObj  = MeasureElementObj.GetValue()
        begin_time = datetime.now().timestamp()
        while True:
            try:
                MeasureValue=MeasureValueObj.GetDoublePhysValue()
            except:
                MeasureValue=MeasureValueObj.GetCharPhysValue()
            if MeasureValue == value:
                break
            if datetime.now().timestamp() - begin_time >= time:
                break
        print("Measure-Element: " + MeasureElementObj.GetName() + "; " +
            "Measure-Value: " + str(MeasureValue))
        return MeasureValue



    def finally_get_calibration(self,ExperimentObj,name,time,expression_value):
        CalibrationElementObj = ExperimentObj.GetCalibrationElement(name)
        CalibrationValueObj = CalibrationElementObj.GetValue()
        begin_time = datetime.now().timestamp()
        while True:
            try:
                CalibrationValue=CalibrationValueObj.GetDoublePhysValue()
            except:
                CalibrationValue=CalibrationValueObj.GetCharPhysValue()
            
            if CalibrationValue == expression_value:
                break
            if datetime.now().timestamp() - begin_time >= time:
                break
        print("Calibration-Element: " + CalibrationElementObj.GetName() + "; " +
            "Calibration-Value: " + str(CalibrationValue))
        return CalibrationValue
    


    # 读值，主要读观测量
    def get_value(self,ExperimentObj,mapping):
        mapping_type = mapping['mapping_type']
        name = mapping['id'].split('/')[-1]
        if mapping_type =='Meas':
            if mapping['xaccess']['array_size'] == '' or '_[' in name:
                return self.get_measure(ExperimentObj,name)
            else:
                values = []
                for i in range(int(mapping['xaccess']['array_size'])):
                    values.append(self.get_measure(ExperimentObj,name+f'_[{i}]'))
                return values
        elif mapping_type =='Cali':
            kind = mapping['xaccess']['kind']
            if kind == 'VALUE':
                return self.get_calibration(ExperimentObj,name)
            elif kind == 'VAL_BLK':
                if '_[' in name:
                    index = name.split('_[')[-1].split(']')[0]
                    return self.get_valblk_calibration(ExperimentObj,name)[index]
                else:
                    return self.get_valblk_calibration(ExperimentObj,name)
            elif kind == 'CURVE':
                return self.get_curve_calibration(ExperimentObj,name)       # 不管查哪一个，把数据全部得��。在和特定���置的数据对比
            elif kind == 'MAP':
                return self.get_map_calibration(ExperimentObj,name)
            else:
                print("Unknown kind")
    
    # 写值
    def set_value(self,ExperimentObj,mapping,value):
        """"""
        mapping_type = mapping['mapping_type']
        name = mapping['id'].split('/')[-1]
        
        if mapping_type =='Meas':
            "meas"
            return None
        elif mapping_type == 'Cali':
            kind = mapping['xaccess']['kind']
            if kind == 'VALUE':
                return self.set_calibration(ExperimentObj,name,value)
            elif kind == 'VAL_BLK':
                if '_[' in name:
                    index = name.split('_[')[-1].split(']')[0]
                    index_value = [index, value]
                    return self.set_valblk_calibration(ExperimentObj,name,index_value)
                else:
                    return self.set_valblk_calibration(ExperimentObj,name,value)
            elif kind == 'CURVE':
                return self.set_curve_calibration(ExperimentObj,name,value)
            elif kind == 'MAP':
                return self.set_map_calibration(ExperimentObj,name,value)
            else:
                print("Unknown kind")
        else:
            print("Unknown type")
            



if __name__ == "__main__":
    INCA= Inca().get_inca('<system default>')
    ExperimentObj = INCA.GetOpenedExperiment()
    print(ExperimentObj)
    # MeasureElementObj  = ExperimentObj.GetMeasureElement('VCCDCanInPT_FrntMotChlg_hex_[0]')
    # MeasureElementObj.OpenView()

    # CalibrationElementObj = ExperimentObj.GetCalibrationElement('CKIE_ChrgnCalibVerSion_K_[2]')
    # CalibrationElementObj.OpenView()
    # Inca().get_valblk_calibration( ExperimentObj,'CKIE_ChrgnCalibVerSion_K_[2]')

    # ExperimentObj.StartMeasurement()

    # MeasureElementObj  = ExperimentObj.GetMeasureElement('VCCDCanInPT_FrntMotChlg_hex_[0]')
    # MeasureElementObj.OpenView()
    # Inca().get_measure(ExperimentObj,MeasureElementObj.GetName())

    # CalibrationElementObj = ExperimentObj.GetCalibrationElement('ESH_RodStkRollgRgnTgtLo_P')
    # CalibrationElementObj.OpenView()
    # Inca().get_calibration( ExperimentObj,'ESH_RodStkRollgRgnTgtLo_P')

    # CalibrationElementObj = ExperimentObj.GetCalibrationElement('ESH_StNoRecupMod_P')
    # CalibrationElementObj.OpenView()

    # Inca().get_valblk_calibration( ExperimentObj,'ESH_StNoRecupMod_P')

    # CalibrationElementObj = ExperimentObj.GetCalibrationElement('L2SSM_FrntMot4WMaxTq')
    # CalibrationElementObj.OpenView()
    # Inca().get_curve_calibration( ExperimentObj,'L2SSM_FrntMot4WMaxTq')

    # CalibrationElementObj = ExperimentObj.GetCalibrationElement('ObEM_EffBas_M')
    # CalibrationElementObj.OpenView()
    # Inca().get_map_calibration( ExperimentObj,'ObEM_EffBas_M')


    MeasureElementObj  = ExperimentObj.GetMeasureElement('SftyBltRmnd_CalDrvrSeatBltRmndBPVal')
    MeasureElementObj.OpenView()
    ExperimentObj.StartMeasurement()
    Inca().set_measurement(ExperimentObj,MeasureElementObj.GetName(),1)
    
    # CalibrationElementObj = ExperimentObj.GetCalibrationElement('DigKeyWPC_CalPwrModStsBPVal')
    # CalibrationElementObj.OpenView()
    # Inca().set_calibration( ExperimentObj,CalibrationElementObj.GetName(),'Enum_PwrModSts_OFF')

    # CalibrationElementObj = ExperimentObj.GetCalibrationElement('TTL_rWhlMinTqGrdtFltNeg_K')
    # CalibrationElementObj.OpenView()
    # Inca().set_calibration( ExperimentObj,CalibrationElementObj.GetName(),-200)

    # CalibrationElementObj = ExperimentObj.GetCalibrationElement('CKIE_ChrgnCalibVerSion_K_[2]')
    # CalibrationElementObj.OpenView()
    # Inca().get_valblk_calibration( ExperimentObj,'CKIE_ChrgnCalibVerSion_K_[2]')

    # CalibrationElementObj = ExperimentObj.GetCalibrationElement('CKIE_ChrgnCalibVerSion_K_[2]')
    # CalibrationElementObj.OpenView()
    # Inca().set_valblk_calibration( ExperimentObj,'CKIE_ChrgnCalibVerSion_K_[2]',[[1,255],[2,254],[3,253],[4,252],[5,251]],demension=16)


    # CalibrationElementObj = ExperimentObj.GetCalibrationElement('ESH_TiVehGearSwhDly_v')
    # CalibrationElementObj.OpenView()
    # Inca().set_curve_calibration( ExperimentObj,'ESH_TiVehGearSwhDly_v',[[2,100],[10,10]])


    # CalibrationElementObj = ExperimentObj.GetCalibrationElement('ESH_TqdHydBcsBrkPosGrdt2_v')
    # CalibrationElementObj.OpenView()
    # Inca().set_map_calibration( ExperimentObj,'ESH_TqdHydBcsBrkPosGrdt2_v', [[2,2,10],[4,5,20]])

    a = 1

