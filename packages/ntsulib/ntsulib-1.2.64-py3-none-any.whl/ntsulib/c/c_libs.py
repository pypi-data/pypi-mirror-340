from ctypes import *
from ..ncommon.nio import get_temp_path

__all__ = ['test_lib']


class external_libs:
    class _test_lib:
        # 旧版本 (备用)
        # def __init__(self):
        #     # 动态获取 DLL 路径（兼容普通运行和 PyInstaller 打包）
        #     if getattr(nsys, 'frozen', False):
        #         # PyInstaller 打包后，从临时目录 _MEIPASS 加载
        #         base_path = nsys._MEIPASS
        #     else:
        #         # 普通运行时，从库的安装目录加载
        #         base_path = os.path.dirname(os.path.abspath(__file__))
        #     # 构造 DLL 的完整路径
        #     dll_path = os.path.join(base_path, "libs", "ntsulib.dll")
        #     try:
        #         self._dll = cdll.LoadLibrary(dll_path)
        #     except Exception as e:
        #         raise RuntimeError(f"Failed to load DLL from {dll_path}: {e}")
        def __init__(self):
            dll_path = get_temp_path() + "/libs/ntsulib.dll"
            try:
                self._dll = cdll.LoadLibrary(dll_path)
            except Exception as e:
                raise RuntimeError(f"Failed to load DLL from {dll_path}: {e}")

        # c_print
        def func1(self, string:str):
            """ c_print """
            self._dll.c_print.argtypes = [c_char_p]  # 指定参数类型
            self._dll.c_print.restype = c_void_p
            # string必须编码再传给DLL
            self._dll.c_print(string.encode('utf-8'))

        def func2(self, a: int, b: int) -> int:
            """ c_sum """
            self._dll.c_sum.argtypes = [c_int, c_int]  # 指定参数类型
            self._dll.c_sum.restype = c_int
            return self._dll.c_sum(a, b)
        def func3(self) -> float:
            """ getTickCount """
            self._dll.getTickCount.argtypes = []  # 指定参数类型
            self._dll.getTickCount.restype = c_float
            return self._dll.getTickCount()
# 测试库
test_lib: "external_libs._test_lib" = external_libs._test_lib()
