import dill
variable_path = "~/GitHub/test1/variable.dill"

def push():
    # 将变量保存到本地文件
    with open(variable_path, "wb") as f:
        dill.dump({k:v for k,v in globals().items() if not k.startswith('__')}, f)

def pull():
    # 加载变量
    with open(variable_path, "rb") as f:
        loaded_vars = dill.load(f)
    # 将变量注入到当前命名空间
    globals().update(loaded_vars)

