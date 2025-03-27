import os
from rich.progress import Progress

def read_dictionary():
    dictionary = {
        "E": ["ie"],
        "En": ["iE", "_n"],
        "ai": ["a", "_i"],
        "ao": ["A", "_o"],
        "an": ["a", "_n"],
        "ang": ["A", "_ng"],
        "e": ["7"],
        "ei": ["e", "_i"],
        "en": ["E", "_n"],
        "eng": ["E", "_ng"],
        "er": ["ae", "_r"],
        "iao": ["iA", "_o"],
        "ian": ["iE", "_n"],
        "iang": ["iA", "_ng"],
        "in": ["i", "_n"],
        "ing": ["i", "_ng"],
        "iong": ["iO", "_ng"],
        "ong": ["O", "_ng"],
        "uai": ["ua", "_i"],
        "uan": ["ua", "_n"],
        "uang": ["uA", "_ng"],
        "ui": ["ue", "_i"],
        "un": ["u7", "_n"],
        "van": ["vE", "_n"],
        "vn": ["ve", "_n"]
    }
    return dictionary

def process_htk_lab(lab_path, dict_mapping):
    with open(lab_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) != 3:
            continue

        start, end, phoneme = parts
        if phoneme in dict_mapping:
            mapping = dict_mapping[phoneme]
            duration = (int(end) - int(start)) / len(mapping)
            current_start = int(start)
            for mapped_phoneme in mapping:
                new_end = round(current_start + duration)
                new_lines.append(f"{current_start} {new_end} {mapped_phoneme}\n")
                current_start = new_end
        else:
            new_lines.append(line)

    with open(lab_path, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)

# 批量处理HTK标签文件
def batch_process_htk_labs(folder_path):
    dict_mapping = read_dictionary()
    lab_files = [f for f in os.listdir(folder_path) if f.endswith('.lab')]
    
    with Progress() as progress:
        task = progress.add_task("[green]Processing HTK label files...", total=len(lab_files))
        
        for filename in lab_files:
            process_htk_lab(os.path.join(folder_path, filename), dict_mapping)
            progress.update(task, advance=1)

# 获取用户输入
folder_path = input("请输入包含HTK标签文件的文件夹路径：")

batch_process_htk_labs(folder_path)
