import os
import hashlib
import json
import argparse
import warnings
import re
import pickle
import base64

BLUE = "\033[1;34m"
RESET = "\033[0m"


class ModuleLoader:
    __isinstance = False

    def __init__(self,flag_save_param, disable_warning, root_dir=None, naming_mode='HASH'):
        # if root dir is passed by the args input, then directly set root_dir
        # else let the user select root_dir with GUI
        self.root_dir = None
        # if not root_dir:
        #     warnings.warn("No root directory is specified.")
        self.root_dir = root_dir
        if root_dir:
            print(f"{BLUE}INFO:Root directory set as {self.root_dir}{RESET}")
        self.naming_mode = naming_mode
        self.flag_save_param = flag_save_param
        if self.flag_save_param:
            raise Exception("The current Verithon version has removed support for .json params saving")
        self.abstract_module_list = []
        self.module_func_list = []
        self.module_function_definition_dict= {}
        self.module_file_name_list = dict()
        self.aux_module_file_name_list = dict()
        self.rtl_folder_name = "RTL_GEN"
        self.param_folder_name = "PARAM"
        self.rtl_folder_path = str()
        self.param_folder_path = str()
        if self.root_dir:
             self.rtl_folder_path, self.param_folder_path = self.make_path()
             print(f"{BLUE}INFO:RTL files will be saved at {self.rtl_folder_path}{RESET}")
             if self.flag_save_param:
                 print(f"{BLUE}INFO:PARAM files will be saved at {self.param_folder_path}{RESET}")
        self.inst_idx = dict()
        # passing inst info
        self.file_tree = dict()
        self.inst_verilog_code = str()
        self.verilog_code = str()
        self.module_dict_tree = dict()
        self.concrete_module_name = str()
        self.add_cnt = 0
        self.disable_warning = disable_warning
        self.module_params = dict()
        self.nested_module_params = dict()
        self.module_verilog_code=dict()
        # dictionary for storing module port definitions; key is module_name + hash value of param string
        self.module_verilog_ports = dict()
        self.language = "VERILOG"
        self.debug_mode = True
        self.look_ahead_speedup = False

        # For compile time optimization
        # dict for storing lines with irrelevant variables, key is abstract module name
        self.irrelevant_lineno_dict = dict()
        self.irrelevant_lineno_aux_module_dict = dict()

        # For test
        self.module_generation_time = 0
        self.module_instantiate_time = 0
        self.add_module_inst_info_time = 0
        self.judge_module_exist_time = 0
        self.n_func_new_enter = 0
        # For test

    def __new__(cls, *args, **kwargs):
        if cls.__isinstance:
            return cls.__isinstance
        cls.__isinstance = object.__new__(cls)
        return cls.__isinstance

    def make_path(self, level=1):
        rtl_folder_path = self.root_dir
        param_folder_path = self.root_dir
        if level > 1:
            rtl_folder_path = os.path.join(self.root_dir, self.rtl_folder_name)
            param_folder_path = os.path.join(self.root_dir, self.param_folder_name)
        if not os.path.exists(rtl_folder_path):
            os.makedirs(rtl_folder_path)
        if not os.path.exists(param_folder_path):
            os.makedirs(param_folder_path)
        return rtl_folder_path, param_folder_path

    # load the module based on the abstract module name and the parameter value
    # returns a boolean value to indicate whether the module is already generated or not, and the module file name
    def load_module(self, abstract_module_name, module_param_dict, module_verilog_code="", module_file_name_aux=str()):
        moduleExists = True
        module_param_dict_cut = dict()
        for key in module_param_dict.keys():
            if (not key == "PORTS") and (not key == 'INST_NAME') and (not key == 'MODULE_NAME'):
                module_param_dict_cut[key] = module_param_dict[key]
        abstractmoduleExists = abstract_module_name in self.abstract_module_list
        if not abstractmoduleExists:
            self.abstract_module_list.append(abstract_module_name)
            self.module_file_name_list[abstract_module_name] = []
            self.aux_module_file_name_list[abstract_module_name] = []
            self.nested_module_params[abstract_module_name] = []
        module_file_name = abstract_module_name
        module_file_name = self.generate_module_file_name(abstract_module_name)
        self.module_verilog_code[module_file_name_aux] = module_verilog_code
        # if self.naming_mode == 'HASH':
        #     hash_val = self.generate_dict_hash(module_param_dict)
        #     module_file_name += hash_val

        if module_file_name_aux not in self.aux_module_file_name_list[abstract_module_name]:
            moduleExists = False
            self.aux_module_file_name_list[abstract_module_name].append(module_file_name_aux)
            self.module_file_name_list[abstract_module_name].append(module_file_name)
            self.inst_idx[module_file_name_aux] = 0
            self.module_params[module_file_name] = module_param_dict_cut
            self.nested_module_params[abstract_module_name].append({module_file_name:module_param_dict_cut})
        else:
            # print(f"XXXXXXXXXX")
            self.inst_idx[module_file_name_aux] += 1
            # print(self.inst_idx[module_file_name_aux])
            module_index = self.aux_module_file_name_list[abstract_module_name].index(module_file_name_aux)
            module_file_name = self.module_file_name_list[abstract_module_name][module_index]
        inst_idx_out_str = self.int_to_hex_string(self.inst_idx[module_file_name_aux]+1)
        return moduleExists, module_file_name, inst_idx_out_str


    def generate_module_file_name(self,abstract_module_name):
        # module_param_dict = dict()
        # for key in module_param_dict_in.keys():
        #     if (not key == "PORTS") and (not key == 'INST_NAME') and (not key == 'MODULE_NAME'):
        #         val_ori =  module_param_dict_in[key]
        #         val_in_byte = pickle.dumps(val_ori)
        #         val_in_str = base64.b64encode(val_in_byte).decode('utf-8')
        #         module_param_dict[key] = module_param_dict_in[key] = val_in_str
        module_file_name = abstract_module_name
        # print(f"abstract_module_name in moduleloader:{abstract_module_name}")
        naming_mode = self.naming_mode
        # module_param_dict.pop('INST_NAME', None)
        # module_param_dict.pop('PORTS',None)
        #param_string = self.dict_to_string(module_param_dict)
        module_file_name_aux = str()
        # if naming_mode == 'HASH':
        #     module_file_name += self.get_hash(param_string)
        #     module_file_name_aux = module_file_name
        # elif naming_mode == 'MD5_SHORT':
        #     module_file_name += self.get_short_md5(param_string)
        #     module_file_name_aux = module_file_name
        if naming_mode == 'SEQUENTIAL':
            #module_file_name_aux = module_file_name + self.get_hash(param_string)
            naming_cnt = len(self.module_file_name_list[abstract_module_name])+1
            module_file_name += self.int_to_hex_string(naming_cnt)
        # print(f"module_file_name_aux in moduleloader:{module_file_name_aux}")
        # print(f"param string in moduleloader: {param_string}")
        return module_file_name#, module_file_name_aux

    def judge_module_exists(self, abstract_module_name, module_param_dict_in):
        moduleExists = False
        module_param_dict = dict()
        for key in module_param_dict_in.keys():
            if (not key == "PORTS") and (not key == 'INST_NAME') and (not key == 'MODULE_NAME'):
                val_ori = module_param_dict_in[key]
                val_in_byte = pickle.dumps(val_ori)
                val_in_str = base64.b64encode(val_in_byte).decode('utf-8')
                module_param_dict[key] = module_param_dict_in[key] = val_in_str
        module_file_name = abstract_module_name
        # naming_mode = self.naming_mode
        # module_param_dict.pop('INST_NAME', None)
        # module_param_dict.pop('PORTS',None)
        param_string = self.dict_to_string(module_param_dict)
        module_file_name_aux = abstract_module_name+self.get_hash(param_string)
        if abstract_module_name in self.aux_module_file_name_list.keys():
            if module_file_name_aux in self.aux_module_file_name_list[abstract_module_name]:
                moduleExists = True
        # print(f"module_file_name_aux in decorator:{module_file_name_aux}")
        # print(f"param string in decorator: {param_string}")
        return moduleExists, module_file_name_aux

    def judge_module_exists_optimized(self, top_func_name, lineno):
        module_exists = False
        module_file_name_aux = str()
        if lineno in self.irrelevant_lineno_aux_module_dict[top_func_name].keys():
            module_exists = True
            module_file_name_aux = self.irrelevant_lineno_aux_module_dict[top_func_name][lineno]
        return module_exists, module_file_name_aux


    def dict_to_string(self, input_dict):
        # 将字典转为 JSON 字符串
        # TEST:
        # print(input_dict)
        dict_string = json.dumps(input_dict, sort_keys=True)
        # 生成哈希值 (这里使用SHA-256算法)
        # TEST
        # print(hash_value)
        return dict_string

    def get_short_md5(self, message, length=8):
        return hashlib.md5(message.encode()).hexdigest()[:length]

    def get_hash(self, message):
        hash_object = hashlib.sha256(message.encode())
        hash_value = hash_object.hexdigest()
        return hash_value

    def int_to_hex_string(self,number):
        # 定义最大可表示的整数值（10位16进制）
        max_value = 0xFFFFFFFFFF  # 10位16进制可以表示的最大值
        # 检查输入是否在有效范围内
        if number < 0 or number > max_value:
            raise ValueError("数字超过表示范围或为负数")
        # 转换为十六进制字符串，并去掉前缀0x
        hex_string = hex(number)[2:].upper()
        # 填充前导零以保持位数为10位
        hex_string = hex_string.zfill(10)
        return hex_string

    # writes the module verilog code to the file
    # returns a boolean value to indicate whether the module is generated or not
    def generate_module(self, abstract_module_name, module_param_dict, module_verilog_code, module_exists=False, module_file_name_aux=str()):
        # print(f"module_exists:{module_exists}")
        if not self.root_dir:
            raise Exception("Error:Unspecified root directory.")
        moduleGenerated = False
        moduleExists,module_file_name,inst_idx_str = self.load_module(abstract_module_name, module_param_dict, module_verilog_code, module_file_name_aux)
        if not module_exists:
            suffix = self.get_file_suffix()
            module_file_name_v = module_file_name
            module_file_name_v += suffix
            vfile_path = os.path.join(self.rtl_folder_path, module_file_name_v)
            with open(vfile_path, "w") as f:
                module_verilog_code = self.replace_module_name(module_verilog_code, module_file_name)
                f.write(module_verilog_code)
            moduleGenerated = True
            print(f"{BLUE}INFO:Writing into module file {module_file_name}{RESET}")
            # if the params are to be saved
            if self.flag_save_param:
                # print(self.flag_save_param)
                self.save_params_to_json(module_file_name, module_param_dict)
        return moduleGenerated, module_file_name, inst_idx_str

    def generate_file_tree(self, file_tree_in):
        self.file_tree = file_tree_in
        output_str = self.visualize_tree(file_tree_in)
        tree_file_name = "module_structure.txt"
        tree_file_path = os.path.join(self.rtl_folder_path, tree_file_name)
        if self.language == "VERILOG" or self.language == "verilog":
            with open(tree_file_path, "w") as f:
                f.write(output_str)


    def visualize_tree(self, tree, parent=None, indent='                  '):
        output_str = str()
        if isinstance(tree, dict):
            for key, value in tree.items():
                output_str += f"{indent}-> {key}\n"
                output_str += self.visualize_tree(value, key, indent + '                  ')
        elif isinstance(tree, list):
            for item in tree:
                output_str += self.visualize_tree(item, parent, indent + '                   ')
        else:
            output_str += f"{indent}{parent} -> {tree}\n"
        return output_str

    def set_root_dir(self, root_dir, dir_level=1):
        self.root_dir = root_dir
        self.rtl_folder_path, self.param_folder_path = self.make_path(level=dir_level)
        print(f"{BLUE}INFO:Root directory set as {root_dir}{RESET}")
        print(f"{BLUE}INFO:RTL files will be saved at {self.rtl_folder_path}{RESET}")
        if self.flag_save_param:
           print(f"{BLUE}INFO:PARAM files will be saved at {self.param_folder_path}{RESET}")

    def set_naming_mode(self, mode='HASH'):
        self.naming_mode = mode

    def set_root_dir_usr(self, root_dir):
        self.root_dit = root_dir

    def set_language_mode(self,my_language):
        self.language = my_language

    def set_debug_mode(self,my_mode):
        self.debug_mode = my_mode

    def set_look_ahead_speedup(self, mode:bool):
        self.look_ahead_speedup = mode


    def get_file_suffix(self):
        if self.language == "CPP" or self.language == "cpp":
            suffix = ".cpp"
        elif self.language == "CPP_HEADER" or self.language == "cpp_header":
            suffix = ".h"
        elif self.language == "VERILOG" or self.language == "verilog":
            suffix = ".v"
        elif self.language == "PYTHON" or self.language == "python":
            suffix = ".py"
        else:
            raise Exception(f"Language mode {self.language} is not supported")
        return suffix


    def save_params_to_json(self,module_name, module_param_dict):
        # module_param_dict.pop('INST_NAME', None)
        # module_param_dict.pop('PORTS', None)
        # 将 module_name 中的无效字符替换为下划线
        sanitized_module_name = module_name.replace(" ", "_").replace("/", "_")
        # 生成 JSON 文件名
        json_file_name = f"{sanitized_module_name}.json"
        json_file_path = os.path.join(self.param_folder_path, json_file_name)
        # 将字典保存为 JSON 文件
        with open(json_file_path, 'w') as json_file:
            json.dump(module_param_dict, json_file, indent=4)  # indent用于格式化输出

        print(f"{BLUE}INFO:Saving PARAMS at {json_file_path}{RESET}")

    def add_module_func(self, module_func_name):
        if "Module" not in module_func_name:
            warnings.warn(f"The function '{module_func_name}' is decorated with converter but not prefixed with 'Module'")

        modulefuncExists = False
        if module_func_name in self.module_func_list:
            modulefuncExists = True
        else:
            self.module_func_list.append(module_func_name)
        return modulefuncExists


    def add_module_inst_info(self, inst_verilog_code, verilog_code, module_dict_tree, concrete_module_name, func_name):
        self.inst_verilog_code = inst_verilog_code
        self.verilog_code = verilog_code
        self.module_dict_tree = module_dict_tree
        self.concrete_module_name = concrete_module_name
        # print(func_name)
        # print(concrete_module_name)
        # print("\n")
        self.add_cnt = self.add_cnt + 1
        # print(self.add_cnt)

    def add_irrelevant_lineno(self,lineno_list,func_name):
        self.irrelevant_lineno_dict[func_name] = lineno_list
        self.irrelevant_lineno_aux_module_dict[func_name] = dict()
        # for lineno in lineno_list:
        #     self.irrelevant

    def add_irrelevant_aux_name_dict(self, top_func_name, lineno, aux_module_file_name):
        self.irrelevant_lineno_aux_module_dict[top_func_name][lineno] = aux_module_file_name


    def empty_irrelevant_aux_name_dict(self, top_func_name):
        self.irrelevant_lineno_aux_module_dict[top_func_name]=dict()

    def extract_module_inst_info(self):
        return self.inst_verilog_code, self.verilog_code, self.module_dict_tree, self.concrete_module_name

    def disEnableWarning(self):
        self.disable_warning = True

    def saveParams(self):
        raise Exception("The current Verithon version has removed support for .json params saving")
        self.flag_save_param = True


    def replace_module_name(self, verilog_code, new_module_name):
        # 正则表达式匹配模块定义
        pattern = r'module\s+(\w+)\s*'

        # 查找模块名
        match = re.search(pattern, verilog_code)
        if match:
            old_module_name = match.group(1)  # 旧模块名
            # 替换模块名
            updated_code = re.sub(pattern, f'module {new_module_name} ', verilog_code)
            return updated_code
        else:
            return "Module Definition Not Found"

    def getParams(self,module_name):
        if module_name in self.nested_module_params.keys():
            return self.nested_module_params[module_name]
        elif module_name in self.module_params.keys():
            return self.module_params[module_name]
        if not self.disable_warning:
            warnings.warn("The received key is neither an abstract module name nor a module file name")
        return None

    def get_latest_module_name(self, abstract_module_name):
        module_dict_list = self.getParams(abstract_module_name)
        latest_module_name = list(module_dict_list[-1].keys())[0]
        return latest_module_name


    def reset(self):
        self.abstract_module_list = []
        self.module_func_list = []
        self.module_file_name_list = dict()
        self.aux_module_file_name_list = dict()
        self.inst_idx = dict()
        self.file_tree = dict()
        self.inst_verilog_code = str()
        self.verilog_code = str()
        self.module_dict_tree = dict()
        self.concrete_module_name = str()
        self.add_cnt = 0
        self.module_params = dict()
        self.nested_module_params = dict()




# 解析命令行参数
parser = argparse.ArgumentParser(description="设置模块加载器参数")
parser.add_argument('--naming_mode', type=str, default='HASH', help='RTL文件命名模式 (如：HASH)')
parser.add_argument('--root_dir', type=str, help='RTL文件保存路径')
parser.add_argument('--flag_save_param', action='store_true', default=False, help='是否保存参数文件')
parser.add_argument('--disable_warning', action='store_true', default=False, help='是否展示警告')
args = parser.parse_args()


# Create singleton of moduleloader
root_dir = args.root_dir
naming_mode = args.naming_mode
flag_save_param = args.flag_save_param
disable_warning = args.disable_warning
# disable_warning = True
# flag_save_param = True
# root_dir = "C:\信道编码\AutoGeneration\Voldelog\\test_save0928"
# naming_mode = 'SEQUENTIAL'
ModuleLoader_Singleton = ModuleLoader(flag_save_param, disable_warning, root_dir, naming_mode)
moduleloader = ModuleLoader_Singleton
