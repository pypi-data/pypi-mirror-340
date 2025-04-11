class Comparison:
    def __init__(self,measurement="==",type_of_tolerance="absolute", tolerance_value=0.0, custom_function=None, type_of_timeoption=None, timeout=0, timeout_unit="s", duration=0, duration_unit="s"):
        self.measurement = measurement
        self.type_of_tolerance = type_of_tolerance
        self.tolerance_value = tolerance_value
        self.type_of_timeoption = type_of_timeoption
        self.timeout = timeout
        self.timeout_unit = timeout_unit
        self.duration = duration
        self.duration_unit = duration_unit
        self.timeout_calculation = self.time_calculation()

        if custom_function is not None:
            self.custom_function = custom_function
        else:
            self.custom_function = None

        valid_measurement = ["==",">=",">","<=","<","!="]
        if measurement not in valid_measurement:
            raise ValueError(f"Invalid measurement: {measurement}")

        if type_of_tolerance not in ["absolute","percentage"]:
            raise ValueError(f"Invalid type of tolerance: {type_of_tolerance}")

        if type_of_timeoption is not None and type_of_timeoption not in ["finallyTrueOption","generallyTrueOption","trueForWithinOption"]:
            raise ValueError(f"Invalid type of time option: {type_of_timeoption}")

        if type_of_tolerance == "absolute":
            if tolerance_value < 0:
                raise ValueError(f"Tolerance value must be non-negative for absolute tolerance")
        
        if type_of_tolerance == "percentage":
            if tolerance_value < 0 or tolerance_value > 100:
                raise ValueError(f"Percentage tolerance must be between 0 and 100")
        
        if self.custom_function is not None and not isinstance(self.custom_function,callable):
            raise ValueError(f"Custom function must be a callable")


            
    def evaluate(self,actual_value,expected_value):
        if actual_value is None or expected_value is None:
            raise ValueError(f"Actual value or expected value is None")
            # return False
        if self.custom_function is not None:
            return self.custom_function(actual_value,expected_value)
        elif self.measurement == "==":
            if isinstance(actual_value,str) and isinstance(expected_value,str):
                return actual_value == expected_value
            else:
                return self.tolerance_calculation(actual_value,expected_value)
        elif self.measurement == ">=":
            return actual_value >= expected_value
        elif self.measurement == ">":
            return actual_value > expected_value
        elif self.measurement == "<=":
            return actual_value <= expected_value
        elif self.measurement == "<":
            return actual_value < expected_value
        elif self.measurement == "!=":
            return actual_value != expected_value
            

    def tolerance_calculation(self,actual_value,expected_value):
        if self.type_of_tolerance == "absolute":
            return abs(actual_value - expected_value) <= self.tolerance_value
        elif self.type_of_tolerance == "percentage":
            return abs(actual_value - expected_value) / expected_value <= self.tolerance_value*0.01

    
    def time_calculation(self):
        if self.timeout_unit == "s":
            self.timeout = self.timeout
        elif self.timeout_unit == "ms":
            self.timeout = self.timeout / 1000
        elif self.timeout_unit == "min":
            self.timeout = self.timeout * 60
        elif self.timeout_unit == "h":
            self.timeout = self.timeout * 3600
        elif self.timeout_unit == "d":
            self.timeout = self.timeout * 86400
        else:
            raise ValueError(f"Invalid timeout unit: {self.timeout_unit}")
        
        if self.duration_unit == "s":
            self.duration = self.duration
        elif self.duration_unit == "ms":
            self.duration = self.duration / 1000
        elif self.duration_unit == "min":
            self.duration = self.duration * 60
        elif self.duration_unit == "h":
            self.duration = self.duration * 3600
        elif self.duration_unit == "d":
            self.duration = self.duration * 86400
        else:
            raise ValueError(f"Invalid duration unit: {self.duration_unit}")
            
        
        

