# demo.py

import json
from hone.hone import Hone

# 定义你的 CSV 文件路径
csv_filepath = 'examples/example_a.csv'

# 创建 Hone 实例
hone_instance = Hone()

# 转换 CSV 到 JSON 结构
json_structure = hone_instance.convert(csv_filepath)

# 打印结果 JSON 结构
print(json.dumps(json_structure, indent=2))
