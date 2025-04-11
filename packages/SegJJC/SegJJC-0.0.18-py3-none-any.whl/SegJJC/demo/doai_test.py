from  SegJJC.train_json_solo import yoloit_test
import os
if __name__ == "__main__":
    # 获取当前脚本的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 将相对路径转换为绝对路径
    alljsondir = os.path.join(script_dir, 'cfg_test.json')
    yoloit_test(alljsondir,'test')
    # with open(jsonpath, 'r', encoding='utf-8', errors='ignore') as f:
    #     content = f.read()
    # content = json.loads(content)