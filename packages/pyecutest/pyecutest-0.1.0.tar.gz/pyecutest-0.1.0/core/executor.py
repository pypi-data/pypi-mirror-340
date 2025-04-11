import pytest
import yaml
import time
from logging import Logger
import inspect
import re
from core.evaluation import Comparison

class TestExecutor:
    """
    测试执行器
    """
    def __init__(self, tools, tools_status, config, logger, Dev_Mode=False):
        self.tools = tools
        self.tools_status = tools_status
        self.config = config
        self.logger: Logger = logger
        self.Dev_Mode = Dev_Mode

        self.canoe_status = tools_status["canoe"]
        if self.canoe_status:
            self.canoe = tools["canoe"][0]
            self.signal_mapper = tools["canoe"][1]
            # 部分工程无法自动识别通道，需要手动配置
            # channel_mapping = self.__canoe_network_channel_mapping(self.config['canoe']['project_file'])
            # for k, v in channel_mapping.items():
            #     self.config['canoe'][k] = v
        
        self.tsmaster_status = tools_status["tsmaster"]
        if self.tsmaster_status:
            self.tsmaster = tools["tsmaster"][0]
            self.signal_mapper = tools["tsmaster"][1]
            # channel_mapping = self.__tsmaster_network_channel_mapping(self.config['tsmaster']['project_file'])
            # for k, v in channel_mapping.items():
            #     self.config['tsmaster'][k] = v

        self.inca_status = tools_status["inca"]
        if self.inca_status:
            self.inca = tools["inca"][0]
            self.inca_wrapper = tools["inca"][1]

        self.veristand_status = tools_status["veristand"]
        if self.veristand_status:
            self.veristand = tools["veristand"]

        self.adb_status = tools_status["adb"]
        if self.adb_status:
            self.adb = tools["adb"]

        self.mi_ant_status = tools_status["mi_ant"]
        if self.mi_ant_status:
            self.mi_ant = tools["mi_ant"]

        

    def __read_bus(self, signal_name: classmethod, tool="canoe") -> float:
        file_name, line_number = self.__report_filename_and_linenumber_info(
            depth=2)  # __read_bus只能被read_bus所调用,因此栈中的函数从栈顶开始数应该是test_case, read_bus, __read_bus, __report_filename_and_linenumber_info
        if self.canoe_status or self.tsmaster_status:
            source_can_list, source_message_list = self.signal_mapper.get_signal_info(signal_name)
            signal_value_list = []
            for i in range(len(source_can_list)):
                if tool == "canoe" and source_can_list[i] in self.config['canoe']:
                    channel = self.config['canoe'][source_can_list[i]]
                    signal_value_list.append(
                        self.canoe.get_signal_value('CAN', channel, source_message_list[i], signal_name.name))
                elif tool == "tsmaster" and source_can_list[i] in self.config['tsmaster']:
                    channel = self.config['tsmaster'][source_can_list[i]]
                    signal_value_list.append(
                        self.tsmaster.get_signal_value(channel, source_can_list[i], signal_name.node,
                                                       source_message_list[i], signal_name.name, 0))
            if len(set(signal_value_list)) > 1:
                self.logger.error(
                    f"信号值不一致：{signal_value_list}, signal name:{signal_name}, file:{file_name}, line:{line_number}")
                return None
            elif len(set(signal_value_list)) == 0:
                self.logger.error(f"信号值只在在总线{source_can_list}上进行发送,请检查已有通道是否配置以上总线,signal name:{signal_name}, file:{file_name}, line:{line_number}")
                return None
            else:
                return signal_value_list[0]

        else:
            raise Exception(f"读写总线工具未配置, file:{file_name}, line:{line_number}")

    def read_bus(self, signal_name: classmethod, expected_value=None,
                 measurement="==",type_of_tolerance="absolute", tolerance_value=0.0, custom_function=None,
                 type_of_timeoption=None, timeout=0, timeout_unit="s", duration=0, duration_unit="s") -> float:
        """ 读取指定总线信号的值,并进行评估。

        Args:
            signal_name (classmethod): 期望读取的信号名
            expected_value (float, 可选): 期望读取的信号值。若为None,则不进行评估。 默认值为None。
            measurement (str, 可选): 评估标准。支持以下参数："==",">=",">","<=","<","!="。 默认值为"=="。
            type_of_tolerance (str, 可选): 误差计算方式。支持以下参数："absolute","percentage"。 默认值为"absolute"。
                                            absolute: 绝对误差。
                                            percentage: 百分比误差。
            tolerance_value (float, 可选): 误差值。若type_of_tolerance为"absolute",则误差值范围为[0,+∞]。若type_of_tolerance为"percentage",则误差值范围为[0,100]。 默认值为0.0。
            custom_function (callable, 可选): 自定义评估函数。 默认值为None。
            type_of_timeoption (str, 可选): 时间评估方式。支持以下参数："finallyTrueOption","generallyTrueOption","trueForWithinOption"。 默认值为None。
                                            finallyTrueOption: 在超时时间内,若读取信号值满足期望,则认为评估成功。
                                            generallyTrueOption: 在持续时间内,若读取信号值满足期望,则认为评估成功。
                                            trueForWithinOption: 在超时时间内,若读取信号值满足期望,且持续时间满足期望,则认为评估成功。
            timeout (int, 可选): 超时时间。默认值为0。
            timeout_unit (str, 可选): 超时时间单位。支持以下参数："ms","s","min","h","d"。 默认值为"s"。
            duration (int, 可选): 持续时间。 默认值为0。
            duration_unit (str, 可选): 持续时间单位。支持以下参数："ms","s","min","h","d"。 默认值为"s"。

        Raises:
            Exception: 读写总线工具未配置时,抛出异常。
            Exception: 评估失败时,抛出异常。

        Returns:
            float: 读取的信号值。
        """
        file_name, line_number = self.__report_filename_and_linenumber_info(depth=1)
        if not isinstance(expected_value, (float, int, type(None))):
            self.logger.error(f"expected_value必须是float或int类型,file:{file_name},line:{line_number}")
            raise Exception("expected_value必须是float或int类型")
        error_reason = ""
        if self.canoe_status:
            tool = "canoe"
        elif self.tsmaster_status:
            tool = "tsmaster"
        else:
            raise Exception("读写总线工具未配置,文件：{file_name},行号：{line_number}")
        comparison = Comparison(measurement,type_of_tolerance,tolerance_value,custom_function,type_of_timeoption,timeout,timeout_unit,duration,duration_unit)
        if self.canoe_status or self.tsmaster_status:
            if expected_value is None: #不需要进行评估
                return self.__read_bus(signal_name, tool=tool), None
            else:
                if type_of_timeoption is None: #不需要进行时间处理,直接进行判断
                    value = self.__read_bus(signal_name, tool=tool)
                    if value is None:
                        error_reason = "CANoe读取信号不一致"
                    else:
                        evaluation = comparison.evaluate(value,expected_value)
                    if evaluation == False:
                        error_reason = "读取超时"
                    pytest.assume(evaluation,f"实际结果：{value},预期结果：{expected_value}, 文件：{file_name}, 行号：{line_number}, 错误原因：{error_reason}")
                    return value, evaluation
                elif type_of_timeoption == "finallyTrueOption": #需要进行超时判断
                    timeout_start_time = time.time()
                    evaluation = False
                    value = self.__read_bus(signal_name, tool=tool)# 保证value一定被赋值,CANoe偶发读取时间过长bug
                    while (time.time() - timeout_start_time) < comparison.timeout:
                        if value is None:  # 此时CANoe读取信号持续不一致,则不进行判断
                            value = self.__read_bus(signal_name, tool=tool)
                            continue
                        if comparison.evaluate(value,expected_value):
                            evaluation = True
                            break
                        value = self.__read_bus(signal_name, tool=tool)
                    if evaluation == False:#若读取逻辑没有走上述循环或者CANoe读取信号持续不一致,需要重新执行评估
                        value = self.__read_bus(signal_name, tool=tool)
                        evaluation = comparison.evaluate(value,expected_value)
                    if evaluation == False:#分析故障原因
                        if value is not None:
                            error_reason = "读取超时"
                        else:
                            error_reason = "CANoe读取信号不一致"
                    if evaluation == False:
                        error_reason = "读取超时"
                    pytest.assume(evaluation,f"实际结果：{value},预期结果：{expected_value}, 文件：{file_name}, 行号：{line_number}, 错误原因：{error_reason}")
                    return value, evaluation
                elif type_of_timeoption == "generallyTrueOption": #需要进行持续时间判断
                    duration_start_time = time.time()
                    evaluation = True
                    value = self.__read_bus(signal_name, tool=tool)# 保证value一定被赋值,CANoe偶发读取时间过长bug
                    while (time.time() - duration_start_time) < comparison.duration:
                        if value is None: # 此时CANoe读取信号持续不一致,则不进行判断
                            value = self.__read_bus(signal_name, tool=tool)
                            continue
                        if not comparison.evaluate(value,expected_value):
                            evaluation = False
                            break
                        value = self.__read_bus(signal_name, tool=tool)
                    if evaluation == True:  # 若读取逻辑没有走上述循环或者CANoe读取信号持续不一致,需要重新执行评估
                        value = self.__read_bus(signal_name, tool=tool)
                        evaluation = comparison.evaluate(value,expected_value)
                    if evaluation == False:#分析故障原因
                        if value is not None:
                            error_reason = "持续时间内信号值不满足期望"
                        else:
                            error_reason = "CANoe读取信号不一致"
                    pytest.assume(evaluation,f"实际结果：{value},预期结果：{expected_value}, 文件：{file_name}, 行号：{line_number}, 错误原因：{error_reason}")
                    return value, evaluation
                elif type_of_timeoption == "trueForWithinOption": #需要进行持续时间判断
                    timeout_start_time = time.time()
                    duration_start_time = time.time()
                    timeout_evaluation = False
                    duration_evaluation = False
                    value = self.__read_bus(signal_name, tool=tool)# 保证value一定被赋值,CANoe偶发读取时间过长bug
                    t = time.time()
                    while (t - timeout_start_time) < comparison.timeout and (t - duration_start_time) < comparison.duration:
                        t = time.time()
                        if value is None: # 此时CANoe读取信号持续不一致,则不进行判断
                            value = self.__read_bus(signal_name, tool=tool)
                            continue
                        if timeout_evaluation == False:#若在超时时间内,超时评估条件还未满足,则重置持续时间
                            duration_start_time = time.time()
                        if timeout_evaluation == False and ((comparison.timeout + timeout_start_time - t) < comparison.duration): #剩余时间<最小持续时间,且超时评估条件还未满足,则直接失败
                            # self.logger.info(f"剩余时间<最小持续时间,且超时评估条件还未满足,则直接失败")
                            break
                        elif timeout_evaluation == True and ((t - duration_start_time) > comparison.duration): #超时评估条件满足,且持续时间满足,则直接成功
                            # self.logger.info(f"超时评估条件满足,且持续时间满足,则直接成功")
                            duration_evaluation = True
                            break
                        timeout_evaluation = comparison.evaluate(value,expected_value)
                        value = self.__read_bus(signal_name, tool=tool)
                        # self.logger.info(f"real value:{value}")

                    # self.logger.info(f"timeout_evaluation:{timeout_evaluation}, duration_evaluation:{duration_evaluation}")
                    if timeout_evaluation and duration_evaluation:#只有两者都为True,才认为评估成功
                        evaluation = True
                    elif timeout_evaluation and not duration_evaluation: #超时评估条件满足,但持续时间不满足,则重新评估
                        evaluation = False
                        error_reason = "持续时间内信号值不满足期望"
                    elif not timeout_evaluation:
                        evaluation = False
                        error_reason = "读取超时"
                    elif value is None:
                        evaluation = False
                        error_reason = "CANoe读取信号不一致"
                    else:
                        evaluation = False
                        error_reason = "未知故障"
                    pytest.assume(evaluation,f"实际结果：{value},预期结果：{expected_value}, 文件：{file_name}, 行号：{line_number}, 错误原因：{error_reason}")
                    return value, evaluation
        else:
            raise Exception("读写总线工具未配置,文件：{file_name},行号：{line_number}")
    
    def __write_bus(self, signal_name: classmethod, value: float, tool="canoe"):
        file_name, line_number = self.__report_filename_and_linenumber_info(depth=2)
        if self.canoe_status:
            tool = "canoe"
            channel_list = self.config['canoe']
        elif self.tsmaster_status:
            tool = "tsmaster"
            channel_list = self.config['tsmaster']

        if self.canoe_status or self.tsmaster_status:
            # self.logger.info(f"write_bus: {signal_name.name}, {value}")
            source_can_list, source_message_list = self.signal_mapper.get_signal_info(signal_name)
            #写入总线信号
            for i in range(len(source_can_list)):
                channel = channel_list[source_can_list[i]]
                if tool == "canoe":
                    self.canoe.set_signal_value('CAN', channel, source_message_list[i], signal_name.name, value)
                elif tool == "tsmaster":
                    self.tsmaster.set_signal_value(channel, source_can_list[i], signal_name.node,
                                                   source_message_list[i], signal_name.name, value)
            return source_can_list, source_message_list
        else:
            raise Exception(f"读写总线工具未配置,文件：{file_name},行号：{line_number}")

    def write_bus(self, signal_name: classmethod, value: float, timeout=5, tolerance_value=0.1, type_of_tolerance="absolute"):
        """写入指定总线信号

        Args:
            signal_name (classmethod): 期望写入的信号名
            value (float): 期望写入的信号值
            timeout (int, optional): 超时时间。默认值为5。
            tolerance_value (float, optional): 误差值。默认值为0.1。
            type_of_tolerance (str, optional): 误差计算方式。默认值为"absolute"。

        Raises:
            Exception: 读写总线工具未配置时,抛出异常。
            Exception: 写入失败时,抛出异常。
        """
        file_name, line_number = self.__report_filename_and_linenumber_info(depth=1)
        if not isinstance(value, (float, int)):
            self.logger.error(f"value必须是float或int类型,file:{file_name},line:{line_number}")
            raise Exception("value必须是float或int类型")
        if self.canoe_status:
            tool = "canoe"
        elif self.tsmaster_status:
            tool = "tsmaster"
        else:
            raise Exception("读写总线工具未配置,文件：{file_name},行号：{line_number}")
        comparison = Comparison(measurement="==",type_of_tolerance=type_of_tolerance,tolerance_value=tolerance_value,timeout=timeout,timeout_unit="s", type_of_timeoption="finallyTrueOption")
        self.__write_bus(signal_name,value,tool)
        #重新读取总线信号,检查是否成功写入
        start_time = time.time()
        real_value = self.__read_bus(signal_name,tool=tool)#读取时间过长补偿首次读取
        while time.time() - start_time < comparison.timeout:
            if real_value is None:  # 此时CANoe读取信号持续不一致,则不进行判断
                real_value = self.__read_bus(signal_name, tool=tool)
                continue
            if comparison.evaluate(real_value,value):
                break
            real_value = self.__read_bus(signal_name,tool=tool)
        if real_value is None or comparison.evaluate(real_value,value)==False:
            real_value = self.__read_bus(signal_name,tool=tool)#读取时间过长补偿最后一次读取
        if not comparison.evaluate(real_value,value):
            self.logger.error(f"无法正确写入总线信号{signal_name.name},real value:{real_value},value:{value},文件：{file_name},行号：{line_number}")
            raise Exception(f"无法正确写入总线信号{signal_name.name},real value:{real_value},value:{value},文件：{file_name},行号：{line_number}")

    def __read_calibration(self, signal_name: classmethod):
        if self.inca_status:
            return self.inca_wrapper.read_calibration(signal_name)
        else:
            raise Exception("INCA工具未配置")
    
    def read_calibration(self, signal_name: classmethod, expected_value=None,
                 measurement="==",type_of_tolerance="absolute", tolerance_value=0.0, custom_function=None,
                 type_of_timeoption=None, timeout=0, timeout_unit="s", duration=0, duration_unit="s"):
        """ 读取指定标定信号的值,并进行评估。

        Args:
            signal_name (classmethod): 期望读取的信号名
            expected_value (float, 可选): 期望读取的信号值。若为None,则不进行评估。 默认值为None。
            measurement (str, 可选): 评估标准。支持以下参数："==",">=",">","<=","<","!="。 默认值为"=="。
            type_of_tolerance (str, 可选): 误差计算方式。支持以下参数："absolute","percentage"。 默认值为"absolute"。
                                            absolute: 绝对误差。
                                            percentage: 百分比误差。
            tolerance_value (float, 可选): 误差值。若type_of_tolerance为"absolute",则误差值范围为[0,+∞]。若type_of_tolerance为"percentage",则误差值范围为[0,100]。 默认值为0.0。
            custom_function (callable, 可选): 自定义评估函数。 默认值为None。
            type_of_timeoption (str, 可选): 时间评估方式。支持以下参数："finallyTrueOption","generallyTrueOption","trueForWithinOption"。 默认值为None。
                                            finallyTrueOption: 在超时时间内,若读取信号值满足期望,则认为评估成功。
                                            generallyTrueOption: 在持续时间内,若读取信号值满足期望,则认为评估成功。
                                            trueForWithinOption: 在超时时间内,若读取信号值满足期望,且持续时间满足期望,则认为评估成功。
            timeout (int, 可选): 超时时间。默认值为0。
            timeout_unit (str, 可选): 超时时间单位。支持以下参数："ms","s","min","h","d"。 默认值为"s"。
            duration (int, 可选): 持续时间。 默认值为0。
            duration_unit (str, 可选): 持续时间单位。支持以下参数："ms","s","min","h","d"。 默认值为"s"。

        Raises:
            Exception: INCA工具未配置时,抛出异常。
            Exception: 评估失败时,抛出异常。

        Returns:
            float: 读取的信号值。
        """
        file_name, line_number = self.__report_filename_and_linenumber_info(depth=1)
        if not isinstance(expected_value, (float, int, str,type(None))):
            self.logger.error(f"expected_value必须是float,int或str类型,file:{file_name},line:{line_number}")
            raise Exception("expected_value必须是float,int或str类型")
        comparison = Comparison(measurement,type_of_tolerance,tolerance_value,custom_function,type_of_timeoption,timeout,timeout_unit,duration,duration_unit)
        if self.inca_status:
            if expected_value is None:
                return self.__read_calibration(signal_name), None
            else:
                value, evaluation, error_reason = self.__read_with_evaluation(signal_name, self.__read_calibration, expected_value, comparison)
                pytest.assume(evaluation,f"实际结果：{value},预期结果：{expected_value}, 文件：{file_name}, 行号：{line_number}, 错误原因：{error_reason}")
                return value, evaluation
        else:
            raise Exception("INCA工具未配置,文件：{file_name},行号：{line_number}")


    def __write_calibration(self, signal_name: classmethod, value):
        if self.inca_status:
            self.inca_wrapper.write_calibration(signal_name, value)
        else:
            raise Exception("INCA工具未配置")
    
    def write_calibration(self, signal_name: classmethod, value, timeout=5, tolerance_value=0.1, type_of_tolerance="absolute"):
        """写入指定标定量

        Args:
            signal_name (classmethod): 期望写入的信号名
            value (float): 期望写入的信号值
            timeout (int, optional): 超时时间。默认值为5。
            tolerance_value (float, optional): 误差值。默认值为0.1。
            type_of_tolerance (str, optional): 误差计算方式。默认值为"absolute"。

        Raises:
            Exception: INCA工具未配置时,抛出异常。
            Exception: 写入失败时,抛出异常。
        """
        file_name, line_number = self.__report_filename_and_linenumber_info(depth=1)
        if not isinstance(value, (float, int, str)):
            self.logger.error(f"value必须是float,int或str类型,file:{file_name},line:{line_number}")
            raise Exception("value必须是float,int或str类型")
        if self.inca_status:
            comparison = Comparison(measurement="==", type_of_tolerance=type_of_tolerance, tolerance_value=tolerance_value, timeout=timeout, timeout_unit="s", type_of_timeoption="finallyTrueOption")
            self.__write_calibration(signal_name, value)
            real_value, evaluation, error_reason = self.__read_with_evaluation(signal_name, self.__read_calibration, value, comparison)
            if not evaluation:
                self.logger.error(f"无法正确写入标定量{signal_name.name},real value:{real_value},value:{value},文件：{file_name},行号：{line_number},错误原因：{error_reason}")
                raise Exception(f"无法正确写入标定量{signal_name.name},real value:{real_value},value:{value},文件：{file_name},行号：{line_number},错误原因：{error_reason}")
        else:
            raise Exception("INCA工具未配置,文件：{file_name},行号：{line_number}")


    def __read_measurement(self, signal_name: classmethod) -> float:
        if self.inca_status:
            return self.inca_wrapper.read_measurement(signal_name)
        else:
            raise Exception("INCA工具未配置")
    
    def read_measurement(self, signal_name: classmethod, expected_value=None,
                 measurement="==",type_of_tolerance="absolute", tolerance_value=0.0, custom_function=None,
                 type_of_timeoption=None, timeout=0, timeout_unit="s", duration=0, duration_unit="s"):
        """ 读取指定测量信号的值,并进行评估。

        Args:
            signal_name (classmethod): 期望读取的信号名
            expected_value (float, 可选): 期望读取的信号值。若为None,则不进行评估。 默认值为None。
            measurement (str, 可选): 评估标准。支持以下参数："==",">=",">","<=","<","!="。 默认值为"=="。
            type_of_tolerance (str, 可选): 误差计算方式。支持以下参数："absolute","percentage"。 默认值为"absolute"。
                                            absolute: 绝对误差。
                                            percentage: 百分比误差。
            tolerance_value (float, 可选): 误差值。若type_of_tolerance为"absolute",则误差值范围为[0,+∞]。若type_of_tolerance为"percentage",则误差值范围为[0,100]。 默认值为0.0。
            custom_function (callable, 可选): 自定义评估函数。 默认值为None。
            type_of_timeoption (str, 可选): 时间评估方式。支持以下参数："finallyTrueOption","generallyTrueOption","trueForWithinOption"。 默认值为None。
                                            finallyTrueOption: 在超时时间内,若读取信号值满足期望,则认为评估成功。
                                            generallyTrueOption: 在持续时间内,若读取信号值满足期望,则认为评估成功。
                                            trueForWithinOption: 在超时时间内,若读取信号值满足期望,且持续时间满足期望,则认为评估成功。
            timeout (int, 可选): 超时时间。默认值为0。
            timeout_unit (str, 可选): 超时时间单位。支持以下参数："ms","s","min","h","d"。 默认值为"s"。
            duration (int, 可选): 持续时间。 默认值为0。
            duration_unit (str, 可选): 持续时间单位。支持以下参数："ms","s","min","h","d"。 默认值为"s"。

        Raises:
            Exception: INCA工具未配置时,抛出异常。
            Exception: 评估失败时,抛出异常。

        Returns:
            float: 读取的信号值。
        """
        file_name, line_number = self.__report_filename_and_linenumber_info(depth=1)
        if not isinstance(expected_value, (float, int, str, type(None))):
            self.logger.error(f"expected_value必须是float,int或str类型,file:{file_name},line:{line_number}")
            raise Exception("expected_value必须是float,int或str类型")
        comparison = Comparison(measurement,type_of_tolerance,tolerance_value,custom_function,type_of_timeoption,timeout,timeout_unit,duration,duration_unit)
        if self.inca_status:
            if expected_value is None:
                return self.__read_measurement(signal_name), None
            else:
                value, evaluation, error_reason = self.__read_with_evaluation(signal_name, self.__read_measurement, expected_value, comparison)
                pytest.assume(evaluation,f"实际结果：{value},预期结果：{expected_value}, 文件：{file_name}, 行号：{line_number}, 错误原因：{error_reason}")
                return value, evaluation
        else:
            raise Exception("INCA工具未配置,文件：{file_name},行号：{line_number}")

    def write_veristand(self, signal_name: str, value: float, timeout=5, tolerance_value=0.1, type_of_tolerance="absolute"):
        """写入指定VeriStand信号

        Args:
            signal_name (classmethod): 期望写入的信号名
            value (float): 期望写入的信号值
            timeout (int, optional): 超时时间。默认值为5。
            tolerance_value (float, optional): 误差值。默认值为0.1。
            type_of_tolerance (str, optional): 误差计算方式。默认值为"absolute"。

        Raises:
            Exception: VeriStand工具未配置时,抛出异常。
            Exception: 写入失败时,抛出异常。
        """
        file_name, line_number = self.__report_filename_and_linenumber_info(depth=1)
        if not isinstance(signal_name, str):
            self.logger.error(f"signal_name必须是str类型,file:{file_name},line:{line_number}")
            raise Exception("signal_name必须是str类型")
        if not isinstance(value, (float, int)):
            self.logger.error(f"value必须是float或int类型,file:{file_name},line:{line_number}")
            raise Exception("value必须是float或int类型")
        if self.veristand_status:
            self.logger.info(f"write_veristand: {signal_name}, {value}")
            self.veristand.write(signal_name, value)
            comparison = Comparison(measurement="==", type_of_tolerance=type_of_tolerance, tolerance_value=tolerance_value, timeout=timeout, timeout_unit="s", type_of_timeoption="finallyTrueOption")
            real_value, evaluation, error_reason = self.__read_with_evaluation(signal_name, self.__read_veristand, value, comparison)
            if not evaluation:
                self.logger.error(
                    f"无法正确写入VeriStand信号,real value:{real_value},value:{value},文件：{file_name},行号：{line_number},错误原因：{error_reason}")
                raise Exception(
                    f"无法正确写入VeriStand信号,real value:{real_value},value:{value},文件：{file_name},行号：{line_number},错误原因：{error_reason}")
        else:
            raise Exception("VeriStand工具未配置,文件：{file_name},行号：{line_number}")

    def __read_veristand(self, signal_name: str):
        file_name, line_number = self.__report_filename_and_linenumber_info(depth=2)
        if self.veristand_status:
            value = self.veristand.read(signal_name)
            return value
        else:
            raise Exception(f"VeriStand工具未配置, file:{file_name}, line:{line_number}")

    def read_veristand(self, signal_name: str, expected_value=None,
                 measurement="==",type_of_tolerance="absolute", tolerance_value=0.0, custom_function=None,
                 type_of_timeoption=None, timeout=0, timeout_unit="s", duration=0, duration_unit="s"):
        """ 读取指定VeriStand信号的值,并进行评估。

        Args:
            signal_name (classmethod): 期望读取的信号名
            expected_value (float, 可选): 期望读取的信号值。若为None,则不进行评估。 默认值为None。
            measurement (str, 可选): 评估标准。支持以下参数："==",">=",">","<=","<","!="。 默认值为"=="。
            type_of_tolerance (str, 可选): 误差计算方式。支持以下参数："absolute","percentage"。 默认值为"absolute"。
                                            absolute: 绝对误差。
                                            percentage: 百分比误差。
            tolerance_value (float, 可选): 误差值。若type_of_tolerance为"absolute",则误差值范围为[0,+∞]。若type_of_tolerance为"percentage",则误差值范围为[0,100]。 默认值为0.0。
            custom_function (callable, 可选): 自定义评估函数。 默认值为None。
            type_of_timeoption (str, 可选): 时间评估方式。支持以下参数："finallyTrueOption","generallyTrueOption","trueForWithinOption"。 默认值为None。
                                            finallyTrueOption: 在超时时间内,若读取信号值满足期望,则认为评估成功。
                                            generallyTrueOption: 在持续时间内,若读取信号值满足期望,则认为评估成功。
                                            trueForWithinOption: 在超时时间内,若读取信号值满足期望,且持续时间满足期望,则认为评估成功。
            timeout (int, 可选): 超时时间。默认值为0。
            timeout_unit (str, 可选): 超时时间单位。支持以下参数："ms","s","min","h","d"。 默认值为"s"。
            duration (int, 可选): 持续时间。 默认值为0。
            duration_unit (str, 可选): 持续时间单位。支持以下参数："ms","s","min","h","d"。 默认值为"s"。

        Raises:
            Exception: VeriStand工具未配置时,抛出异常。
            Exception: 评估失败时,抛出异常。

        Returns:
            float: 读取的信号值。
        """
        file_name, line_number = self.__report_filename_and_linenumber_info(depth=1)
        if not isinstance(signal_name, str):
            self.logger.error(f"signal_name必须是str类型,file:{file_name},line:{line_number}")
            raise Exception("signal_name必须是str类型")
        if not isinstance(expected_value, (float, int, type(None))):
            self.logger.error(f"expected_value必须是float或int类型,file:{file_name},line:{line_number}")
            raise Exception("expected_value必须是float或int类型")
        comparison = Comparison(measurement,type_of_tolerance,tolerance_value,custom_function,type_of_timeoption,timeout,timeout_unit,duration,duration_unit)
        if self.veristand_status:
            if expected_value is None:
                return self.__read_veristand(signal_name), None
            else:
                value, evaluation, error_reason = self.__read_with_evaluation(signal_name, self.__read_veristand, expected_value, comparison)
                pytest.assume(evaluation,f"实际结果：{value},预期结果：{expected_value}, 文件：{file_name}, 行号：{line_number}, 错误原因：{error_reason}")
                return value, evaluation
        else:
            raise Exception(f"VeriStand工具未配置, file:{file_name}, line:{line_number}")

    def __read_sys_var(self, var_name):
        if self.canoe_status:
            sys_variable = self.canoe.get_sys_variable(var_name)
            return sys_variable
        else:
            raise Exception("读写总线工具未配置")
    
    def read_sys_var(self, var_name, expected_value=None,
                 measurement="==",type_of_tolerance="absolute", tolerance_value=0.0, custom_function=None,
                 type_of_timeoption=None, timeout=0, timeout_unit="s", duration=0, duration_unit="s"):
        """ 读取指定系统变量的值,并进行评估。

        Args:
            signal_name (classmethod): 期望读取的信号名
            expected_value (float, 可选): 期望读取的信号值。若为None,则不进行评估。 默认值为None。
            measurement (str, 可选): 评估标准。支持以下参数："==",">=",">","<=","<","!="。 默认值为"=="。
            type_of_tolerance (str, 可选): 误差计算方式。支持以下参数："absolute","percentage"。 默认值为"absolute"。
                                            absolute: 绝对误差。
                                            percentage: 百分比误差。
            tolerance_value (float, 可选): 误差值。若type_of_tolerance为"absolute",则误差值范围为[0,+∞]。若type_of_tolerance为"percentage",则误差值范围为[0,100]。 默认值为0.0。
            custom_function (callable, 可选): 自定义评估函数。 默认值为None。
            type_of_timeoption (str, 可选): 时间评估方式。支持以下参数："finallyTrueOption","generallyTrueOption","trueForWithinOption"。 默认值为None。
                                            finallyTrueOption: 在超时时间内,若读取信号值满足期望,则认为评估成功。
                                            generallyTrueOption: 在持续时间内,若读取信号值满足期望,则认为评估成功。
                                            trueForWithinOption: 在超时时间内,若读取信号值满足期望,且持续时间满足期望,则认为评估成功。
            timeout (int, 可选): 超时时间。默认值为0。
            timeout_unit (str, 可选): 超时时间单位。支持以下参数："ms","s","min","h","d"。 默认值为"s"。
            duration (int, 可选): 持续时间。 默认值为0。
            duration_unit (str, 可选): 持续时间单位。支持以下参数："ms","s","min","h","d"。 默认值为"s"。

        Raises:
            Exception: 读写总线工具未配置时,抛出异常。
            Exception: 评估失败时,抛出异常。

        Returns:
            float: 读取的信号值。
        """
        file_name, line_number = self.__report_filename_and_linenumber_info(depth=1)
        if not isinstance(var_name, str):
            self.logger.error(f"var_name必须是str类型,file:{file_name},line:{line_number}")
            raise Exception("var_name必须是str类型")
        if not isinstance(expected_value, (float, int, type(None))):
            self.logger.error(f"expected_value必须是float或int类型,file:{file_name},line:{line_number}")
            raise Exception("expected_value必须是float或int类型")
        comparison = Comparison(measurement,type_of_tolerance,tolerance_value,custom_function,type_of_timeoption,timeout,timeout_unit,duration,duration_unit)
        if self.canoe_status:
            if expected_value is None:
                return self.__read_sys_var(var_name), None
            else:
                value, evaluation, error_reason = self.__read_with_evaluation(var_name, self.__read_sys_var, expected_value, comparison)
                pytest.assume(evaluation,f"实际结果：{value},预期结果：{expected_value}, 文件：{file_name}, 行号：{line_number}, 错误原因：{error_reason}")
                return value, evaluation
        else:
            raise Exception("读写总线工具未配置")

    def __write_sys_var(self, var_name, var_value):
        if self.canoe_status:
            self.canoe.set_sys_variable(var_name, var_value)
        else:
            raise Exception("读写总线工具未配置")
    
    def write_sys_var(self, var_name, var_value, timeout=5, tolerance_value=0.1, type_of_tolerance="absolute"):
        """写入指定系统变量

        Args:
            signal_name (classmethod): 期望写入的信号名
            value (float): 期望写入的信号值
            timeout (int, optional): 超时时间。默认值为5。
            tolerance_value (float, optional): 误差值。默认值为0.1。
            type_of_tolerance (str, optional): 误差计算方式。默认值为"absolute"。

        Raises:
            Exception: 读写总线工具未配置时,抛出异常。
            Exception: 写入失败时,抛出异常。
        """
        file_name, line_number = self.__report_filename_and_linenumber_info(depth=1)
        if not isinstance(var_name, str):
            self.logger.error(f"var_name必须是str类型,file:{file_name},line:{line_number}")
            raise Exception("var_name必须是str类型")
        if not isinstance(var_value, (float, int)):
            self.logger.error(f"var_value必须是float或int类型,file:{file_name},line:{line_number}")
            raise Exception("var_value必须是float或int类型")
        if self.canoe_status:
            comparison = Comparison(measurement="==", type_of_tolerance=type_of_tolerance, tolerance_value=tolerance_value, timeout=timeout, timeout_unit="s", type_of_timeoption="finallyTrueOption")
            self.__write_sys_var(var_name, var_value)
            value, evaluation, error_reason = self.__read_with_evaluation(var_name, self.__read_sys_var, var_value, comparison)
            if not evaluation:
                self.logger.error(f"无法正确写入系统变量{var_name},real value:{value},value:{var_value},文件：{file_name},行号：{line_number},错误原因：{error_reason}")
                raise Exception(f"无法正确写入系统变量{var_name},real value:{value},value:{var_value},文件：{file_name},行号：{line_number},错误原因：{error_reason}")
        else:
            raise Exception("读写总线工具未配置,文件：{file_name},行号：{line_number}")

    def read_sys_var_array(self, var_name):
        if self.canoe_status:
            sys_variable_array = self.canoe.get_sys_variable_array(var_name)
            return sys_variable_array
        else:
            raise Exception("读写总线工具未配置")

    def write_sys_var_array(self, var_name, var_value):
        if self.canoe_status:
            return self.canoe.set_sys_variable_array(var_name, var_value)
        else:
            raise Exception("读写总线工具未配置")

    def write_mi_ant(self, signal_name: classmethod, signal_value):
        if self.mi_ant_status:
            self.mi_ant.write_signal(signal_name, signal_value)
        else:
            raise Exception("mi_ant未配置")

    def read_mi_ant(self, signal_name: classmethod, expected_value=None):
        if self.mi_ant_status:
            value = self.mi_ant.read_signal(signal_name)
            if expected_value is not None:
                pytest.assume(value == expected_value)
            return value, value==expected_value
        else:
            raise Exception("mi_ant未配置")

    def close_mi_ant(self):
        if self.mi_ant_status:
            self.mi_ant.close_client()
        else:
            raise Exception("mi_ant未配置")

    def adb_tap(self, x: int, y: int):
        """adb点击，具体命令为：adb shell input tap {x} {y}

        Args:
            x (int): 点击坐标x
            y (int): 点击坐标y

        Raises:
            Exception: adb未配置时,抛出异常。
        """
        if self.adb_status:
            self.adb.adb_tap(x, y)
        else:
            raise Exception("adb未配置")

    def adb_swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: int):
        """adb滑动，具体命令为：adb shell input swipe {start_x} {start_y} {end_x} {end_y} {duration}

        Args:
            start_x (int): 滑动起始坐标x
            start_y (int): 滑动起始坐标y
            end_x (int): 滑动结束坐标x
            end_y (int): 滑动结束坐标y
            duration (int): 滑动持续时间

        Raises:
            Exception: adb未配置时,抛出异常。
        """
        if self.adb_status:
            self.adb.adb_swipe(start_x, start_y, end_x, end_y, duration)
        else:
            raise Exception("adb未配置")
    
    def adb_input(self, text: str):
        """adb输入，具体命令为：adb shell input {text}

        Args:
            text (str): 输入内容

        Raises:
            Exception: adb未配置时,抛出异常。
        """
        if self.adb_status:
            self.adb.adb_input(text)
        else:
            raise Exception("adb未配置")

    def adb_pull(self, remote_path: str, local_path: str):
        """adb拉取文件，具体命令为：adb pull {remote_path} {local_path}

        Args:
            remote_path (str): 远程路径
            local_path (str): 本地路径

        Raises:
            Exception: adb未配置时,抛出异常。
        """
        if self.adb_status:
            self.adb.adb_pull(remote_path, local_path)
        else:
            raise Exception("adb未配置")

    def adb_push(self, local_path: str, remote_path: str):
        """adb推送文件，具体命令为：adb push {local_path} {remote_path}

        Args:
            local_path (str): 本地路径
            remote_path (str): 远程路径

        Raises:
            Exception: adb未配置时,抛出异常。
        """
        if self.adb_status:
            self.adb.adb_push(local_path, remote_path)
        else:
            raise Exception("adb未配置")

    def adb_devices(self):
        """获取adb设备列表，具体命令为：adb devices

        Raises:
            Exception: adb未配置时,抛出异常。

        Returns:
            str: adb设备列表
        """
        if self.adb_status:
            return self.adb.adb_devices()
        else:
            raise Exception("adb未配置")

    def adb_connect(self, device_id: str):
        """连接adb设备，具体命令为：adb connect {device_id}

        Args:
            device_id (str): 设备id

        Raises:
            Exception: adb未配置时,抛出异常。
        """
        if self.adb_status:
            self.adb.adb_connect(device_id)
        else:
            raise Exception("adb未配置")
    
    def adb_disconnect(self, device_id: str):
        """断开adb设备，具体命令为：adb disconnect {device_id}

        Args:
            device_id (str): 设备id

        Raises:
            Exception: adb未配置时,抛出异常。
        """
        if self.adb_status:
            self.adb.adb_disconnect(device_id)
        else:
            raise Exception("adb未配置")

    def adb_custom_command(self, command: str):
        """执行adb自定义命令，具体命令为：adb {command}

        Args:
            command (str): 自定义命令

        Raises:
            Exception: adb未配置时,抛出异常。
        """
        if self.adb_status:
            self.adb.adb_custom_command(command)
        else:
            raise Exception("adb未配置")

    def __report_filename_and_linenumber_info(self, depth):
        stack_frame = inspect.stack()[depth + 1]
        file_name = stack_frame.filename.split('\\')[-1]
        line_number = stack_frame.lineno
        return file_name, line_number

    def __canoe_network_channel_mapping(self, file_path):
        with open(file_path, 'r', encoding="ISO-8859-1") as f:
            contents = f.read()
        # 定义正则表达式模式
        pattern = r'ILConfiguration::VNetwork\s+\d+\s+Begin_Of_Object\n(.*?)\nEnd_Of_Object ILConfiguration::VNetwork\s+\d+'

        # 使用re.DOTALL标志使.能匹配换行符
        matches = re.finditer(pattern, contents, re.DOTALL)

        results = []
        for match in matches:
            # 获取匹配内容并按行分割
            content = match.group(1)
            # 将每行转换为参数（去除空行和空白）
            params = [line.strip() for line in content.split('\n') if line.strip()]
            results.append(params)
        channel_info = {}
        for info in results:
            channel_info[info[1]] = int(info[2])
        return channel_info

    def __tsmaster_network_channel_mapping(self, file_path):
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
        # 提取[RBSCAN]部分的内容
        rbscan_pattern = r'\[RBSCAN\](.*?)(?=\[|$)'
        rbscan_match = re.search(rbscan_pattern, content, re.DOTALL)
        
        if not rbscan_match:
            raise Exception("tsmaster配置文件中没有找到通道映射部分")
        
        # 提取通道映射
        channel_pattern = r'N\d+=CH(\d+)_(\w+)'
        channel_map = {}
        
        # 在[RBSCAN]部分中查找所有通道映射
        for line in rbscan_match.group(1).split('\n'):
            match = re.search(channel_pattern, line)
            if match:
                channel_num = int(match.group(1))
                network_name = match.group(2)
                channel_map[network_name] = channel_num
                
        return channel_map
    
    def __read_with_evaluation(self, signal_name, read_function, expected_value, comparison: Comparison):
        error_reason = ""
        value = None
        if comparison.type_of_timeoption is None:
            value = read_function(signal_name)
            evaluation = comparison.evaluate(value,expected_value)
            if evaluation==False:
                error_reason = "读取超时"
        elif comparison.type_of_timeoption == "finallyTrueOption":
            timeout_start_time = time.time()
            evaluation = False
            value = read_function(signal_name)
            while (time.time() - timeout_start_time) < comparison.timeout:
                evaluation = comparison.evaluate(value,expected_value)
                if evaluation==True:
                    break
                value = read_function(signal_name)
            if evaluation==False:
                error_reason = "读取超时"
        elif comparison.type_of_timeoption == "generallyTrueOption":
            duration_start_time = time.time()
            evaluation = True
            value = read_function(signal_name)
            while (time.time() - duration_start_time) < comparison.duration:
                evaluation = comparison.evaluate(value,expected_value)
                if evaluation==False:
                    break
                value = read_function(signal_name)
            if evaluation==False:
                error_reason = "持续时间不满足"
        elif comparison.type_of_timeoption == "trueForWithinOption":
            timeout_start_time = time.time()
            duration_start_time = time.time()
            timeout_evaluation = False
            duration_evaluation = False
            value = read_function(signal_name)
            t = time.time()
            while (t - timeout_start_time) < comparison.timeout and (t - duration_start_time) < comparison.duration:
                t = time.time()
                if timeout_evaluation == False:
                    duration_start_time = time.time()
                if timeout_evaluation == False and ((comparison.timeout + timeout_start_time - t) < comparison.duration):
                    break
                elif timeout_evaluation == True and ((t - duration_start_time) > comparison.duration):
                    duration_evaluation = True
                    break
                timeout_evaluation = comparison.evaluate(value,expected_value)
                value = read_function(signal_name)
            if timeout_evaluation and duration_evaluation:
                evaluation = True
            elif timeout_evaluation and not duration_evaluation:
                evaluation = False
                error_reason = "持续时间内信号值不满足期望"
            elif not timeout_evaluation:
                evaluation = False
                error_reason = "读取超时"
            else:
                evaluation = False
                error_reason = "未知故障"
        return value, evaluation, error_reason
    