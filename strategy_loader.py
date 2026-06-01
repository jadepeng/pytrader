import importlib
import os

_modules = {}
custom_folder = 'custom_strategies'
imp_class = 'Strategy'


def new_module(module_name):
    return importlib.import_module('.' + module_name, custom_folder)


def load_strategy_class(code: str, name: str):
    """
    加载策略文件
    :param code:
    :param name:
    :return:
    """
    strategy_path = os.path.join(custom_folder, f"{name}.py")
    with open(strategy_path, 'w', encoding='utf8') as file:
        file.write(code)

    if name in _modules:
        strategy_module = _modules.get(name)
        strategy_module = importlib.reload(strategy_module)
    else:
        strategy_module = new_module(name)

    return getattr(strategy_module, imp_class)


if __name__ == '__main__':
    example_path = os.path.join('strategies', 'example.py')
    with open(example_path, 'r', encoding='utf8') as f:
        code = f.read()
    strategy_module_cls = load_strategy_class(code, 'test')
    print(strategy_module_cls)

