import json,os
from a2lparser.a2lparser import A2LParser
from a2lparser.a2lparser_exception import A2LParserException

class GenA2lLib:
    def __init__(self, a2l_path):
        try:
            ast_dict = A2LParser(log_level="INFO").parse_file(a2l_path)
            self.ast = ast_dict[a2l_path.split('\\')[-1].split('/')[-1]]
            project = self.ast["PROJECT"]
            module = project["MODULE"]
            print(f"Project {project['Name']} with module: {module['Name']}")
            self.enum_dict = {}
            if not os.path.exists(r"databases\other\a2l_enum.json"):
                os.makedirs(r"databases\other", exist_ok=True)
                with open(r"databases\other\a2l_enum.json", "w") as f:
                    json.dump({}, f)
            


        except A2LParserException as e:
            print(e)
            self.ast = None
    
    def gen_compu_vtab_json(self):
        if self.ast is not None:
            self.enum_dict = {}
            compu = self.ast.find_sections("COMPU_VTAB")
            compu_vtab_list = compu["COMPU_VTAB"]
            print(f"Found {len(compu_vtab_list)} COMPU_VTAB sections.")
            for compu_vtab in compu_vtab_list:
                # print(compu_vtab.keys())
                key = '_'.join(compu_vtab['Name'].split('_')[2:])
                self.enum_dict[key] = []
                for i in range(int(compu_vtab['NumberValuePairs'])):
                    self.enum_dict[key].append(compu_vtab['InVal_OutVal'][i][1])
                        
            with open(r"databases\other\a2l_enum.json", "w") as f:
                json.dump(self.enum_dict, f)
        else:
            print("ast is None")
    
    def gen_measurement_lib(self):
        with open(r"databases\other\a2l_enum.json", "r") as f:
            self.enum_dict = json.load(f)
        if self.ast is not None:
            measurements = self.ast.find_sections("MEASUREMENT")
            measurements_list = measurements["MEASUREMENT"]
            print(f"Found {len(measurements_list)} MEASUREMENT sections.")
            with open(r"lib\a2llib.py", "w") as f:
                for measurement in measurements_list:
                    class_name = measurement['Name'].replace(".", "_") + "_M"
                    if measurement['CONVERSION'] in self.enum_dict:
                        f.write(f"class {class_name}:\n")
                        if len(self.enum_dict[measurement['CONVERSION']]) > 0:
                            for enum in self.enum_dict[measurement['CONVERSION']]:
                                f.write(f"\t{enum.replace('\"', '')} = {enum}\n")
                        # f.write(f"    def name():\n")
                        # f.write(f"        return '{measurement['Name']}'\n")
                        f.write(f"\tname = '{measurement['Name']}'\n")
                    else:
                        f.write(f"class {class_name}:\n")
                        f.write(f"\tname = '{measurement['Name']}'\n")

        else:
            print("ast is None")
    
    def gen_characteristic_lib(self):
        with open(r"databases\other\a2l_enum.json", "r") as f:
            self.enum_dict = json.load(f)
        if self.ast is not None:
            characteristics = self.ast.find_sections("CHARACTERISTIC")
            characteristics_list = characteristics["CHARACTERISTIC"]
            print(f"Found {len(characteristics_list)} CHARACTERISTIC sections.")

            with open(r"lib\a2llib.py", "a") as f:
                for characteristic in characteristics_list:
                    if characteristic['CONVERSION'] in self.enum_dict:
                        f.write(f"class {characteristic['Name']}_C:\n")
                        if len(self.enum_dict[characteristic['CONVERSION']]) > 0:
                            for enum in self.enum_dict[characteristic['CONVERSION']]:
                                f.write(f"\t{enum.replace('\"', '')} = {enum}\n")
                        # f.write(f"    def name():\n")
                        # f.write(f"        return '{characteristic['Name']}'\n")
                        f.write(f"\tname = '{characteristic['Name']}'\n")
                    else:
                        f.write(f"class {characteristic['Name']}_C:\n")
                        f.write(f"\tname = '{characteristic['Name']}'\n")
        else:
            print("ast is None")


if __name__ == "__main__":
    gen_a2l_lib = GenA2lLib(r"databases\a2l\FZCU_U_M_all_S000003428001.a2l")
    gen_a2l_lib.gen_compu_vtab_json()
    gen_a2l_lib.gen_measurement_lib()
    gen_a2l_lib.gen_characteristic_lib()
