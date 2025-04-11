import pandas

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

class GenChannelLib:
    def __init__(self,excel_path):
        self.excel_path = excel_path
        self.dataframe = pandas.read_excel(excel_path, sheet_name='Sheet1')
    
    def get_channel_lib(self):
        with open(r'lib\channellib.py', 'w') as f:
            for index,row in self.dataframe.iterrows():
                variable_name = row[0]
                variable_name = create_variable_name(variable_name)
                if variable_name is None:
                    continue
                f.write(variable_name+' = '+'\"'+str(row[1])+'\"'+'\n')

if __name__ == '__main__':
    excel_path = r'databases\channel\labcar.xlsx'
    gen_channel_lib = GenChannelLib(excel_path)
    gen_channel_lib.get_channel_lib()
