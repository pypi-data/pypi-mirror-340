import re
import struct
from intelhex import IntelHex,NotEnoughDataError


def get_address_dec(e):
  return int(e[1],16)

data_type_byte_length = {'UBYTE':1, 'SBYTE':1, 'UWORD':2, 'SWORD':2, 'ULONG':4, 'SLONG':4,
                                      'A_UINT64':8, 'A_INT64':8, 'FLOAT32_IEEE':4, 'FLOAT64_IEEE':8}


def _data_len(cali_info):
    "返回信号的长度"
    data_type = cali_info['Deposit']['FNC_VALUES']['Datatype']
    byte_len = data_type_byte_length[data_type]
    if cali_info['Type'] == 'VALUE':
        return byte_len
    elif cali_info['Type'] == 'VAL_BLK':
        return byte_len * int(cali_info['NUMBER'])
    elif cali_info['Type'] == 'CURVE':
        return byte_len * int(cali_info['AXIS_DESCR'][0]['MaxAxisPoints'])
    elif cali_info['Type'] == 'MAP':
        return byte_len * int(cali_info['AXIS_DESCR'][0]['MaxAxisPoints']) * int(cali_info['AXIS_DESCR'][1]['MaxAxisPoints'])
    else:
        print(cali_info['Name']+"长度计算错误。")

def _axis_data_no_address(axis_info):
    """针对"AXIS_PTS_REF": {}的情况"""
    try:
        # 将字符串转换为浮点数
        MaxAxisPoints = int(axis_info['MaxAxisPoints'])
        LowerLimit = float(axis_info['LowerLimit'])
        UpperLimit = float(axis_info['UpperLimit'])
        # 计算步长
        step = (UpperLimit - LowerLimit) / (MaxAxisPoints - 1)
        # 生成数值数组
        data = [LowerLimit + i * step for i in range(MaxAxisPoints)]
        return data
    except ValueError as e:
        print("参数错误:", e)
        return None
    
def _axis_len(axis_info):
    """返回信号的长度"""
    if axis_info['AXIS_PTS_REF'] == {}:
        return 0
    data_type = axis_info['AXIS_PTS_REF']['Deposit']['AXIS_PTS']['Datatype']
    byte_len = data_type_byte_length[data_type]
    return byte_len * int(axis_info['MaxAxisPoints'])

def _hex_str_to_data( hex_str, data_type):
    data = []
    byte_str = bytes.fromhex(hex_str)
    byte_size = data_type_byte_length.get(data_type)
    if byte_size is None:
        print(data_type + '不存在')
        return None
    hex_len = len(hex_str)
    for i in range(0, hex_len, byte_size * 2):
        sub_hex_str = hex_str[i:i + byte_size * 2]
        byte_str = bytes.fromhex(sub_hex_str)
        if data_type == 'UBYTE':
            value = struct.unpack('<B', byte_str)[0]
        elif data_type == 'SBYTE':
            value = struct.unpack('<b', byte_str)[0]
        elif data_type == 'UWORD':
            value = struct.unpack('<H', byte_str)[0]
        elif data_type == 'SWORD':
            value = struct.unpack('<h', byte_str)[0]
        elif data_type == 'ULONG':
            value = struct.unpack('<I', byte_str)[0]
        elif data_type == 'SLONG':
            value = struct.unpack('<i', byte_str)[0]
        elif data_type == 'FLOAT32_IEEE' or data_type == 'FLOAT64_IEEE':
            value = struct.unpack('<f', byte_str)[0]
        elif data_type == 'DOUBLE':
            value = struct.unpack('<d', byte_str)[0]
        elif data_type == 'A_UINT64':
            value = struct.unpack('<Q', byte_str)[0]
        elif data_type == 'A_INT64':
            value = struct.unpack('<q', byte_str)[0]
        data.append(value)
    return data

def convert_phy_value( data, convert, data_type, LowerLimit, UpperLimit):
    convert_type = convert['ConversionType']
    convert_name = convert['Name']
    if convert_type == 'IDENTICAL':
        value_compute = data
    elif convert_type == 'RAT_FUNC':
        convert_format = convert['ConvertFormat'][0]
        convert_format_coeff = re.findall('\-?[\d\.]+', convert_format)
        if len(convert_format_coeff) == 6:
            if ((convert_format_coeff[0] == '0' or  convert_format_coeff[0] == '0.0') and
                (convert_format_coeff[1] == '1' or convert_format_coeff[1] == '1.0') and 
                (convert_format_coeff[2] == '0' or convert_format_coeff[2] == '0.0') and 
                (convert_format_coeff[3] == '0' or convert_format_coeff[3] == '0.0')and 
                (convert_format_coeff[4] == '0' or convert_format_coeff[4] == '0.0') and 
                (convert_format_coeff[5] == '1' or convert_format_coeff[5] == '1.0')):
                value_compute = data
            elif ((convert_format_coeff[0] == '0' or convert_format_coeff[0] == '0.0') and 
                  (convert_format_coeff[3] == '0' or convert_format_coeff[3] == '0.0')):
                f = lambda x: (float(x)*float(convert_format_coeff[5]) - float(convert_format_coeff[2])) / (float(convert_format_coeff[1]) - float(x)*float(convert_format_coeff[4]))
                value_compute = [f(x) for x in data]
            else:
                value_compute = [solve_for_x(x,convert_format_coeff, LowerLimit, UpperLimit) for x in data]
        else:
            value_compute = data
            print(f'The Convert name: {convert_name} in a2l file is invaild, will be ignore')
    elif convert_type == 'LINEAR':
        convert_format = convert['ConvertFormat'][0]
        convert_format_coeff = re.findall('\-?[\d\.]+', convert_format)
        if len(convert_format_coeff) == 2:
            f = lambda x: (x - float(convert_format_coeff[1]))/float(convert_format_coeff[0])
            value_compute = [f(x) for x in data]
        else:
            value_compute = data
            print(f'The Convert name: {convert_name} in a2l file is invaild, will be ignore')
    elif convert_type == 'TAB_VERB':
        value_compute = data
    return value_compute


def solve_for_x( y, convert_format_coeff, LowerLimit, UpperLimit, epsilon=1e-6):
    # 将系数转换为浮点数
    coeff = [float(c) for c in convert_format_coeff]
    # 定义目标函数
    def f(x):
        numerator = x ** 2 * coeff[0] + x * coeff[1] + coeff[2]
        denominator = x ** 2 * coeff[3] + x * coeff[4] + coeff[5]
        return numerator / denominator - y
    # 初始化搜索区间
    lower_bound = float(LowerLimit)  # 下界
    upper_bound = float(UpperLimit)   # 上界
    # 进行二分法搜索
    while upper_bound - lower_bound > epsilon:
        mid = (lower_bound + upper_bound) / 2
        if f(mid) < 0:
            lower_bound = mid
        else:
            upper_bound = mid
    # 返回解
    return (lower_bound + upper_bound) / 2



class HexParser:
    def __init__(self,file_path) -> None:
        self.hex = IntelHex(file_path)

    def gets(self,name, address, data_len):
        try:
            data_bytes_str = self.hex.gets(address, data_len)
        except NotEnoughDataError:
            print(name +' hex data error. Easy-Test fills the area '+hex(address)+' with FillByte [ 0xFF ].')
            data_bytes_str = bytes.fromhex('FF'*data_len)
        return data_bytes_str
    
    def get_cali_init_value(self,cali_infos):
        init_value = {}
        for cali_info in cali_infos:
            init_value[cali_info['Name']] = {}
            data_type = cali_info['Deposit']['FNC_VALUES']['Datatype']
            data_len = _data_len(cali_info)
            address = int(cali_info["Address"], 16)
            data_bytes_str = self.gets(cali_info['Name'], address, data_len)
            data_hex_str = data_bytes_str.hex()
            if cali_info['Type'] == 'VALUE':
                temp_data = _hex_str_to_data(data_hex_str,data_type)
                value_list = convert_phy_value(temp_data,cali_info['Convert'],data_type,cali_info['LowerLimit'],cali_info['UpperLimit'])
                init_value[cali_info['Name']]['data'] = value_list[0]
            elif cali_info['Type'] == 'VAL_BLK':
                temp_data = _hex_str_to_data(data_hex_str,data_type)
                init_value[cali_info['Name']]['data'] = convert_phy_value(temp_data,cali_info['Convert'],data_type,cali_info['LowerLimit'],cali_info['UpperLimit'])
            elif cali_info['Type'] == 'CURVE':
                temp_data = _hex_str_to_data(data_hex_str,data_type)
                init_value[cali_info['Name']]['data'] = convert_phy_value(temp_data,cali_info['Convert'],data_type,cali_info['LowerLimit'],cali_info['UpperLimit'])
                axis_x_data_len = _axis_len(cali_info['AXIS_DESCR'][0])
                if axis_x_data_len != 0:
                    axis_x_info = cali_info['AXIS_DESCR'][0]
                    axis_data_type = axis_x_info['AXIS_PTS_REF']['Deposit']['AXIS_PTS']['Datatype']
                    axis_x_address = int(axis_x_info['AXIS_PTS_REF']['Address'], 16)
                    axis_x_bytes_str = self.gets(cali_info['Name']+' x-axis',axis_x_address, axis_x_data_len)
                    axis_x_hex_str = axis_x_bytes_str.hex()
                    temp_axis_x_data = _hex_str_to_data(axis_x_hex_str,axis_data_type)
                    init_value[cali_info['Name']]['axis_x'] = convert_phy_value(temp_axis_x_data,axis_x_info['Convert'],axis_data_type,axis_x_info['LowerLimit'],axis_x_info['UpperLimit'])
                else:
                    init_value[cali_info['Name']]['axis_x'] = _axis_data_no_address(cali_info['AXIS_DESCR'][0])
            elif cali_info['Type'] == 'MAP':
                temp_data = _hex_str_to_data(data_hex_str,data_type)
                init_value[cali_info['Name']]['data'] =[]
                temp_value = convert_phy_value(temp_data,cali_info['Convert'],data_type,cali_info['LowerLimit'],cali_info['UpperLimit'])
                axis_x_data_len = _axis_len(cali_info['AXIS_DESCR'][0])
                axis_y_data_len = _axis_len(cali_info['AXIS_DESCR'][1])
                for i in range(int(cali_info['AXIS_DESCR'][0]['MaxAxisPoints'])):
                    temp_x_value = []
                    for j in range(int(cali_info['AXIS_DESCR'][1]['MaxAxisPoints'])):
                        temp_x_value.append(temp_value[i*int(cali_info['AXIS_DESCR'][1]['MaxAxisPoints']) + j])
                    init_value[cali_info['Name']]['data'].append(temp_x_value)
                if axis_x_data_len != 0:
                    axis_x_info = cali_info['AXIS_DESCR'][0]
                    axis_data_type = axis_x_info['AXIS_PTS_REF']['Deposit']['AXIS_PTS']['Datatype']
                    axis_x_address = int(axis_x_info['AXIS_PTS_REF']['Address'], 16)
                    axis_x_bytes_str = self.gets(cali_info['Name']+' x-axis',axis_x_address, axis_x_data_len)
                    axis_x_hex_str = axis_x_bytes_str.hex()
                    temp_axis_x_data = _hex_str_to_data(axis_x_hex_str,axis_data_type)
                    init_value[cali_info['Name']]['axis_x'] = convert_phy_value(temp_axis_x_data,axis_x_info['Convert'],axis_data_type,axis_x_info['LowerLimit'],axis_x_info['UpperLimit'])
                else:
                    init_value[cali_info['Name']]['axis_x'] = _axis_data_no_address(cali_info['AXIS_DESCR'][0])
                if axis_y_data_len != 0:
                    axis_y_info = cali_info['AXIS_DESCR'][1]
                    axis_data_type = axis_y_info['AXIS_PTS_REF']['Deposit']['AXIS_PTS']['Datatype']
                    axis_y_address = int(axis_y_info['AXIS_PTS_REF']['Address'], 16)
                    axis_y_bytes_str = self.gets(cali_info['Name']+' y-axis',axis_y_address, axis_y_data_len)
                    axis_y_hex_str = axis_y_bytes_str.hex()
                    temp_axis_y_data = _hex_str_to_data(axis_y_hex_str,axis_data_type)
                    init_value[cali_info['Name']]['axis_y'] = convert_phy_value(temp_axis_y_data,axis_y_info['Convert'],axis_data_type,axis_y_info['LowerLimit'],axis_y_info['UpperLimit'])
                else:
                    init_value[cali_info['Name']]['axis_y'] = _axis_data_no_address(cali_info['AXIS_DESCR'][1])   
                # to do 需要弄成二维数组？
            else:
                print(cali_info['Name']+'类型错误')
        return init_value
    
class SRecord19:
    def __init__(self, file_path, Cali_Address_infos=[]):
        self.record_type = 'S3'
        self.data_type_byte_length = {'UBYTE':1, 'SBYTE':1, 'UWORD':2, 'SWORD':2, 'ULONG':4, 'SLONG':4,
                                      'A_UINT64':8, 'A_INT64':8, 'FLOAT32_IEEE':4, 'FLOAT64_IEEE':8}
        
        self.s19_file_path = file_path
        self.new_file_path = re.sub('\.s19$','_replaced.s19',file_path)
        
        f = open(file_path, "r",encoding='gbk')
        self.s19_str = f.read()
        self.s19_str_new = self.s19_str
        f.close()
        self.cali_address_infos = []
        self.all_address_infos = []
        self.address_infos = re.findall('(?<=' + self.record_type + ')(?P<ByteCount>[0-9A-Fa-f]{2})(?P<address>[0-9A-F]{8})(?P<data>[0-9A-F]+)(?P<checksum>[0-9A-F]{2})', self.s19_str)
        self.s19_str_new = self.s19_str

        for info in Cali_Address_infos:
            tmp_dict = info
            find_info_tmp = list(filter(lambda x: (info['cali_end_address_dec'] >= int(x[1],16) and info['cali_begin_address_dec'] < int(x[1],16) + int(x[0],16)-5), self.address_infos))
            find_info_tmp.sort(key=get_address_dec)
            tmp_dict['address_info']=find_info_tmp
            data_str = ''
            for index, add_info in enumerate(find_info_tmp):
                if index == 0:
                    data_str = add_info[2]
                else:
                    data_str_new = add_info[2]
                    address_new = int(add_info[1],16)
                    address_old = int(find_info_tmp[index-1][1],16)
                    data_len_old = int(find_info_tmp[index-1][0],16)-5
                    if address_new == address_old + data_len_old:
                        data_str = data_str + data_str_new
                    else:
                        raise ValueError('Address: "' + add_info[1] + '" is invaild!')
            tmp_dict['address_data']=data_str

            self.cali_address_infos.append(tmp_dict)
    
    def get_cali_init_value(self,cali_infos):
        """得到所有标定量的初始值"""
        init_value = {}
        for cali_info in cali_infos:
            init_value[cali_info['Name']] = {}
            data_type = cali_info['Deposit']['FNC_VALUES']['Datatype']
            data_len = _data_len(cali_info)
            data_hex_str = self.get_cali_address_data_direct(cali_info['Address'],data_len)
            if cali_info['Type'] == 'VALUE':
                temp_data = _hex_str_to_data(data_hex_str,data_type)
                value_list = convert_phy_value(temp_data,cali_info['Convert'],data_type,cali_info['LowerLimit'],cali_info['UpperLimit'])
                init_value[cali_info['Name']]['data'] = value_list[0]
            elif cali_info['Type'] == 'VAL_BLK':
                temp_data = _hex_str_to_data(data_hex_str,data_type)
                init_value[cali_info['Name']]['data'] = convert_phy_value(temp_data,cali_info['Convert'],data_type,cali_info['LowerLimit'],cali_info['UpperLimit'])

            elif cali_info['Type'] == 'CURVE':
                temp_data = _hex_str_to_data(data_hex_str,data_type)
                init_value[cali_info['Name']]['data'] = convert_phy_value(temp_data,cali_info['Convert'],data_type,cali_info['LowerLimit'],cali_info['UpperLimit'])
                axis_x_data_len = _axis_len(cali_info['AXIS_DESCR'][0])
                if axis_x_data_len != 0:
                    axis_x_info = cali_info['AXIS_DESCR'][0]
                    axis_data_type = axis_x_info['AXIS_PTS_REF']['Deposit']['AXIS_PTS']['Datatype']
                    axis_x_hex_str = self.get_cali_address_data_direct(axis_x_info['AXIS_PTS_REF']['Address'],axis_x_data_len)
                    temp_axis_x_data = _hex_str_to_data(axis_x_hex_str,axis_data_type)
                    init_value[cali_info['Name']]['axis_x'] = convert_phy_value(temp_axis_x_data,axis_x_info['Convert'],axis_data_type,axis_x_info['LowerLimit'],axis_x_info['UpperLimit'])
                else:
                    init_value[cali_info['Name']]['axis_x'] = _axis_data_no_address(cali_info['AXIS_DESCR'][0])
            elif cali_info['Type'] == 'MAP':
                temp_data = _hex_str_to_data(data_hex_str,data_type)
                init_value[cali_info['Name']]['data'] =[]
                temp_value = convert_phy_value(temp_data,cali_info['Convert'],data_type,cali_info['LowerLimit'],cali_info['UpperLimit'])
                axis_x_data_len = _axis_len(cali_info['AXIS_DESCR'][0])
                axis_y_data_len = _axis_len(cali_info['AXIS_DESCR'][1])
                for i in range(int(cali_info['AXIS_DESCR'][0]['MaxAxisPoints'])):
                    temp_x_value = []
                    for j in range(int(cali_info['AXIS_DESCR'][1]['MaxAxisPoints'])):
                        temp_x_value.append(temp_value[i*int(cali_info['AXIS_DESCR'][1]['MaxAxisPoints']) + j])
                    init_value[cali_info['Name']]['data'].append(temp_x_value)
                if axis_x_data_len != 0:
                    axis_x_info = cali_info['AXIS_DESCR'][0]
                    axis_data_type = axis_x_info['AXIS_PTS_REF']['Deposit']['AXIS_PTS']['Datatype']
                    axis_x_hex_str = self.get_cali_address_data_direct(axis_x_info['AXIS_PTS_REF']['Address'],axis_x_data_len)
                    temp_axis_x_data = _hex_str_to_data(axis_x_hex_str,axis_data_type)
                    init_value[cali_info['Name']]['axis_x'] = convert_phy_value(temp_axis_x_data,axis_x_info['Convert'],axis_data_type,axis_x_info['LowerLimit'],axis_x_info['UpperLimit'])
                else:
                    init_value[cali_info['Name']]['axis_x'] = _axis_data_no_address(cali_info['AXIS_DESCR'][0])
                if axis_y_data_len != 0:
                    axis_y_info = cali_info['AXIS_DESCR'][1]
                    axis_data_type = axis_y_info['AXIS_PTS_REF']['Deposit']['AXIS_PTS']['Datatype']
                    axis_y_hex_str = self.get_cali_address_data_direct(axis_y_info['AXIS_PTS_REF']['Address'],axis_y_data_len)
                    temp_axis_y_data = _hex_str_to_data(axis_y_hex_str,axis_data_type)
                    init_value[cali_info['Name']]['axis_y'] = convert_phy_value(temp_axis_y_data,axis_y_info['Convert'],axis_data_type,axis_y_info['LowerLimit'],axis_y_info['UpperLimit'])
                else:
                    init_value[cali_info['Name']]['axis_y'] = _axis_data_no_address(cali_info['AXIS_DESCR'][1])   
 
                # to do 需要弄成二维数组？
            else:
                print(cali_info['Name']+'类型错误')

        return init_value
    
    def get_cali_address_data_direct(self, address_str, data_len):
        address_str_upper = address_str.upper()
        address_str_pure = re.sub('^0X','',address_str_upper)
        address_str_begin_actual = re.sub('[^0-9A-F]','',address_str_pure)
        address_num_begin_actual_dec = int(address_str_begin_actual, 16)
        find_info_tmp = list(filter(lambda x: (x['cali_end_address_dec'] >= address_num_begin_actual_dec) and (x['cali_begin_address_dec'] <= address_num_begin_actual_dec), self.cali_address_infos))
        address_data_raw = find_info_tmp[0]['address_data']
        address_begin_dec = find_info_tmp[0]['cali_begin_address_dec']
        address_input_dec = int(address_str, 16)
        if len(address_str_begin_actual) == 8:
            result_str = address_data_raw[(address_input_dec-address_begin_dec)*2:(address_input_dec-address_begin_dec+data_len)*2]
            return result_str
        else:
            raise ValueError('Address: "' + address_str + '" is invaild!')  
