import sys
import os
# 将项目根目录添加到 Python 路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import re
import pytest





qos.os
qos
print(123)


"""
import unittest
from unittest.mock import patch
import quickuse


class TestTools(unittest.TestCase):
    def test_import(self):
        import quickuse
        quickuse.tools


    def test_small(self):
        from quickuse.tools.small import exec_str
        codes = """x = 3+6"""
        local_vars = {}
        local_vars2 = exec_str(codes,local_vars)
        assert local_vars2 == {'x': 9}

    def test_re(self):
        from quickuse.tools.retools import extract_json_code,extract_python_code
        x = """
```json
work1
```
        """
        result = extract_json_code(x)
        self.assertEqual(result,['\nwork1\n'])
        y = """
```python
work3
```
        """
        result = extract_python_code(y)
        self.assertEqual(result,['\nwork3\n'])


if __name__ == '__main__':
    unittest.main()




if __name__ == "__main__":
    base_dir = "/Users/zhaoxuefeng/GitHub/work_new"
    tool = LocalFileTool(base_dir)

    # 获取当前目录下所有 .py 文件
    py_files = tool.get_file_list(include_extensions=['.py'])
    print("Python files in the repository:")
    for file in py_files:
        print(file)

    # 获取 src 目录下所有文件
    src_files = tool.get_file_list('module1')
    print("\nAll files in src directory:")
    for file in src_files:
        print(file)


    # 获取多个文件内容
    file_paths = [
        "module1/__factory.py",
        "module1/use.py",
        "./main.py"
    ]
    formatted_string = tool.get_multiple_files(file_paths)

    print(formatted_string)

    formatted_string2 = formatted_string.replace('pass','works')
    formatted_string3 = formatted_string2.replace('工厂模式','工厂模式ce')





    # 从格式化字符串写回多个文件
    tool.write_multiple_files_from_string(formatted_string3)


    # 获取与指定文件相关联的所有文件
    related_files = tool.get_related_files("./repc.py")
    print("Related files:")
    for file in related_files:
        print(file)


    # 获取所有相关文件的内容，格式化为注释标识的字符串
    formatted_string = tool.get_multiple_files(related_files)
    print("\nFormatted string of related files:")
    print(formatted_string)


"""

