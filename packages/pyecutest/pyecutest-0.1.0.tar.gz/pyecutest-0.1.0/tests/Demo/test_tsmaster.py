import pytest
from lib import buslib
from core.executor import TestExecutor
import time


class TestClass:
    def setup_class(self):
        print("准备测试环境")

        # self.executor = TestExecutor()

    def teardown_class(self):
        print("\n清理测试环境")
        # self.INCA.CloseExperiment()
        # self.CANOE.stop_measurement()
        # self.VERISTAND.disconnect()

    def test_demo1(self, executor: TestExecutor):
        executor.write_bus(buslib.ThrdRowMidBucSts_XCD_can, 0)
        executor.read_bus(buslib.ThrdRowMidBucSts_XCD_can, expected_value=0)
        # time.sleep(1)

    def test_demo2(self, executor: TestExecutor):
        executor.write_bus(buslib.ThrdRowMidBucSts_XCD_can, 1)
        executor.read_bus(buslib.ThrdRowMidBucSts_XCD_can, expected_value=1)


if __name__ == '__main__':
    tester = TestClass()
    tester.test_DEMO()