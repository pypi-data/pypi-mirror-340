import re, hashlib, json
from pathlib import Path as lpath
from os import stat as os_stat
from os.path import abspath


this_dir = lpath(__file__).parent
files_dir = this_dir / 'ig_files'
file_hashes_file = this_dir / 'file_hashes.txt'


def 计算哈希网盘(rootpath: lpath):
    def loop(folder: lpath, deep: int):
        for son in folder.iterdir():
            if son.is_dir():
                yield deep, son
                yield from loop(son, deep+1)
            elif son.is_file():
                yield deep, son
    result = []
    for deep, obj in loop(rootpath, 0):
        if obj.is_file():
            print(f"\r{obj.name}", end='                                    ')
            info = {
                'size': os_stat(abspath(obj), follow_symlinks=False).st_size,
                'sha-512': hashlib.sha512(obj.read_bytes()).hexdigest(),
                'sha3-512': hashlib.sha3_512(obj.read_bytes()).hexdigest(),
            }
            info = f"    -info {json.dumps(info, ensure_ascii=False)}"
        else:
            info = ''
        name = f"{'    ' * deep}{obj.name}"
        width = len(name) + len(re.findall('[\u4e00-\u9fa5]', name))
        result.append((name, width, info))
    return result


result = 计算哈希网盘(files_dir)

if result:
    max_width = max(width for name, width, info in result)
    texts = '\n'.join(f"{name}{' ' * (max_width - width)}{info}" for name, width, info in result)
    file_hashes_file.write_text(texts, 'utf-8')


print('\n已更新哈希网盘')