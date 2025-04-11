import os
import sys
import json

# 获取当前文件所在目录的父级目录（api 文件夹的父级目录）
current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(current_dir)

# 然后再导入
from api.hex.srec19 import SRecord19
from pya2l.parser import A2lParser as Parser

class A2L:
    def __init__(self, file_path):
        self.file_path = file_path
        self.RECORD_LAYOUT_infos = {}
        self.COMPU_VTAB_infos = {}
        self.COMPU_METHOD_infos = {}
        self.CHARACTERISTIC_infos = []
        self.MEASUREMENT_infos = []
        self.Cali_Address_infos = []
        self.AXIS_PTS_infos = {}
        f = open(file_path, "r",encoding='gbk', errors='ignore')
        a2l_content = f.read()
        json_bytes = a2l_content.encode()
        self.a2l_tree = Parser().tree_from_a2l(json_bytes)

        
        self._parse_record_layout_info()
        self._parse_compu_vtab_info()
        self._parse_compu_method_info()
        self._parse_characteristic_info()
        self._parse_measurement_info()
        if self.Cali_Address_infos == []:
            self._sort_calib_address()

    def _sort_calib_address(self):
        address_min = "ffffffff"
        address_max = "00000000"

        for info in self.CHARACTERISTIC_infos:
            if info['Address'] < address_min:
                address_min = info['Address']
            if info['Address'] > address_max:
                address_max = info['Address']
        address_range_begin_hex = address_min
        address_range_begin_dec = int(address_range_begin_hex, 16)
        address_range_end_hex = address_max
        address_range_end_dec = int(address_range_end_hex, 16)
        tmp_dict = {'cali_begin_address_hex': address_range_begin_hex,
                        'cali_begin_address_dec': address_range_begin_dec,
                        'cali_end_address_hex': address_range_end_hex,
                        'cali_end_address_dec': address_range_end_dec}
        self.Cali_Address_infos.append(tmp_dict)

    def _parse_record_layout_info(self):
        for recode_layout in self.a2l_tree.PROJECT.MODULE[0].RECORD_LAYOUT:
            self.RECORD_LAYOUT_infos[recode_layout.Name.Value] = {
                    "Name": recode_layout.Name.Value,
                    "FNC_VALUES":{
                        "Position": str(recode_layout.FNC_VALUES.Position.Value),
                        "Datatype": recode_layout.FNC_VALUES.DataType.Value,
                        "IndexMode": recode_layout.FNC_VALUES.IndexMode,
                        "Addresstype": recode_layout.FNC_VALUES.AddressType.Value
                    }
                }
            
    def _parse_compu_vtab_info(self):
        for compu_vtab in self.a2l_tree.PROJECT.MODULE[0].COMPU_VTAB:
            self.COMPU_VTAB_infos[compu_vtab.Name.Value] = {
                'Name':compu_vtab.Name.Value,
                'LongIdentifier':compu_vtab.LongIdentifier.Value,
                'ConversionType':compu_vtab.ConversionType,
                'NumberValuePairs':compu_vtab.NumberValuePairs.Value,
                'ValuePairs':[f'{int(compu_vtab.InValOutVal[i].InVal.Value)} "{compu_vtab.InValOutVal[i].OutVal.Value}"' for i in range(len(compu_vtab.InValOutVal))]
                }
    
    def _parse_compu_method_info(self):
        for compu_method in self.a2l_tree.PROJECT.MODULE[0].COMPU_METHOD:
            if compu_method.ConversionType == 'RAT_FUNC':
                temp_ConvertFormat =[ f'{compu_method.COEFFS.A.Value} {compu_method.COEFFS.B.Value} {compu_method.COEFFS.C.Value} {compu_method.COEFFS.D.Value} {compu_method.COEFFS.E.Value} {compu_method.COEFFS.F.Value}']
            elif compu_method.ConversionType == 'TAB_VERB':
                temp_ConvertFormat = self.COMPU_VTAB_infos[compu_method.COMPU_TAB_REF.ConversionTable.Value]
            elif compu_method.ConversionType == 'LINEAR':
                temp_ConvertFormat = [f'{compu_method.FORMULA.FX.Value} {compu_method.FORMULA.FORMULA_INV.GX.Value}']
            else:
                temp_ConvertFormat = ['1']
            self.COMPU_METHOD_infos[compu_method.Name.Value] = {
                'Name':compu_method.Name.Value,
                'LongIdentifier':compu_method.LongIdentifier.Value,
                'ConversionType':compu_method.ConversionType,
                'Format':compu_method.Format.Value,
                'Unit':compu_method.Unit.Value,
                'ConvertFormat':temp_ConvertFormat
            }

    def get_compu_method_info(self,compu_method_name):
        if compu_method_name == 'NO_COMPU_METHOD':
            tmp = {'Name':'NO_COMPU_METHOD','LongIdentifier':'NO_COMPU_METHOD','ConversionType':'RAT_FUNC',
                        'Format':'','Unit':'','ConvertFormat':['0 1 0 0 0 1']}
        else:
            if compu_method_name in self.COMPU_METHOD_infos:
                tmp = self.COMPU_METHOD_infos[compu_method_name]
            else:
                tmp = {}
        return tmp
    
    def get_record_layout_info(self, record_layout_name):
        if record_layout_name in self.RECORD_LAYOUT_infos:
            tmp = self.RECORD_LAYOUT_infos[record_layout_name]
        else:
            tmp = {}
        return tmp 

    def get_axis_pts_info(self, axis_pts_name):
        if axis_pts_name in self.AXIS_PTS_infos:
            tmp = self.AXIS_PTS_infos[axis_pts_name]
        else:
            tmp = {}
        return tmp

    def _parse_axis_pts_info(self):
        for axis_pts in a2l.PROJECT.MODULE[0].AXIS_PTS:
            print(axis_pts.DepositR.Value)
            self.AXIS_PTS_infos[axis_pts.Name.Value] = {
                "Name": axis_pts.Name.Value ,
                "LongIdentifier": axis_pts.LongIdentifier.Value,
                "Address": hex(axis_pts.Address.Value),
                "InputQuantity": axis_pts.InputQuantity.Value,
                "Deposit": self.get_record_layout_info(axis_pts.DepositR.Value),
                "MaxDiff": str(axis_pts.MaxDiff.Value),
                "Convert": self.get_compu_method_info(axis_pts.Conversion.Value),
                "LowerLimit": str(axis_pts.LowerLimit.Value),
                "UpperLimit": str(axis_pts.UpperLimit.Value),
                "MaxAxisPoints": str(axis_pts.MaxAxisPoints.Value),
            }

    def _parse_axis_descr_info(self, AXIS_descr):
        if len(AXIS_descr) == 0:
            return []
        else:
            temp = []
            for i in range(len(AXIS_descr)):
                temp.append({
                    "Attribute": AXIS_descr[i].Attribute,
                    "InputQuantity": AXIS_descr[i].InputQuantity.Value,
                    "Convert": self.get_compu_method_info(AXIS_descr[i].Conversion.Value),
                    "MaxAxisPoints": str(AXIS_descr[i].MaxAxisPoints.Value),
                    "LowerLimit": str(AXIS_descr[i].LowerLimit.Value),
                    "UpperLimit": str(AXIS_descr[i].UpperLimit.Value),
                    "AXIS_PTS_REF": self.get_axis_pts_info(AXIS_descr[i].AXIS_PTS_REF.AxisPoints.Value)
                }) 
            return temp
        
    def _parse_characteristic_info(self):
        CHARACTERISTIC_lst = self.a2l_tree.PROJECT.MODULE[0].CHARACTERISTIC
        for i in range(len(CHARACTERISTIC_lst)):
            temp_dict = {
                "Name": CHARACTERISTIC_lst[i].Name.Value ,
                "LongIdentifier": CHARACTERISTIC_lst[i].LongIdentifier.Value,
                "Type": CHARACTERISTIC_lst[i].Type ,
                "Address": hex(CHARACTERISTIC_lst[i].Address.Value),
                "Deposit": self.get_record_layout_info(CHARACTERISTIC_lst[i].Deposit.Value),
                "MaxDiff": str(CHARACTERISTIC_lst[i].MaxDiff.Value),
                "Convert": self.get_compu_method_info(CHARACTERISTIC_lst[i].Conversion.Value),
                "LowerLimit": str(CHARACTERISTIC_lst[i].LowerLimit.Value),
                "UpperLimit": str(CHARACTERISTIC_lst[i].UpperLimit.Value),
                "NUMBER": str(CHARACTERISTIC_lst[i].NUMBER.Number.Value),
                "AXIS_DESCR": self._parse_axis_descr_info(CHARACTERISTIC_lst[i].AXIS_DESCR),
                "BIT_MASK": str(CHARACTERISTIC_lst[i].BIT_MASK.Mask.Value)
            }
            if temp_dict['Deposit'] == {} or temp_dict['Convert'] == {}:   # 排除一(些简单的错误, (to do 升级)
                print("标定量："+temp_dict['Name']+"被舍弃")
                continue
            self.CHARACTERISTIC_infos.append(temp_dict)
    
    def _parse_measurement_info(self):
        MEASUREMENT_lst = self.a2l_tree.PROJECT.MODULE[0].MEASUREMENT
        for i in range(len(MEASUREMENT_lst)):
            temp_dict = {
                "Name": MEASUREMENT_lst[i].Name.Value,
                "LongIdentifier": MEASUREMENT_lst[i].LongIdentifier.Value,
                "Datatype": MEASUREMENT_lst[i].DataType.Value,
                "Convert": self.get_compu_method_info(MEASUREMENT_lst[i].Conversion.Value),
                "Resolution": str(MEASUREMENT_lst[i].Resolution.Value),
                "Accuracy": str(MEASUREMENT_lst[i].Accuracy.Value),
                "LowerLimit": str(MEASUREMENT_lst[i].LowerLimit.Value),
                "UpperLimit": str(MEASUREMENT_lst[i].UpperLimit.Value),
                "ARRAY_SIZE": str(MEASUREMENT_lst[i].ARRAY_SIZE.Number.Value),
                "BIT_MASK": str(MEASUREMENT_lst[i].BIT_MASK.Mask.Value),
                "ECU_ADDRESS": hex(MEASUREMENT_lst[i].ECU_ADDRESS.Address.Value),
            }
            if temp_dict['Convert'] == {}:
                print("观测量："+temp_dict['Name']+"被舍弃")
                continue
            self.MEASUREMENT_infos.append(temp_dict)
#
if __name__ == '__main__':
  
    A2LPath = r'a2l\VCCD_U_M_all.a2l'
    s19Path = r'hex\CORTEXM_S32G399_car_sw.s19'
    a2l = A2L(A2LPath)
    s19 = SRecord19(s19Path,a2l.Cali_Address_infos)
    temp = s19.get_cali_init_value(a2l.CHARACTERISTIC_infos)
    with open("characteristic_init_info.json", "w", encoding="utf-8") as f:
        json.dump(temp, f, ensure_ascii=False, indent=4)

    """
    self.MEASUREMENT_infos = []
    self.MEASUREMENT_index_infos = {}
    self.CHARACTERISTIC_infos = []
    self.CHARACTERISTIC_index_infos = {}
    self.COMPU_METHOD_infos = []
    self.COMPU_METHOD_index_infos = {}
    self.COMPU_VTAB_infos = []
    self.COMPU_VTAB_index_infos = {}
    self.RECORD_LAYOUT_infos = []
    self.RECORD_LAYOUT_index_infos = {}
    self.AXIS_PTS_infos = []
    self.AXIS_PTS_index_infos = {}
    self.Cali_Address_infos = []
    """

        
