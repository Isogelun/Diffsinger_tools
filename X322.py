import os
from rich.progress import Progress

def read_dictionary():
    # 将词典写入代码中，ai和ei的：i需要区分
    dictionary = {
        "E": ["ie"],
        "En": ["ie", ":n"],
        "a": ["aA"],
        "ai": ["a", ":i"],
        "ao": ["A", "U"],
        "an": ["a", ":n"],
        "ang": ["A", "N"],
        "e": ["7"],
        "ei": ["e", ":i"],
        "en": ["E", ":n"],
        "eng": ["E", "N"],
        "er": ["a", ":r"],
        "ia": ["iaA"],
        "iao": ["iA", "U"],
        "ian": ["ie", ":n"],
        "iang": ["iA", "N"],
        "in": ["i", ":n"],
        "ing": ["i", "N"],
        "iong": ["iU", "N"],
        "ong": ["U", "N"],
        "ua": ["uaA"],
        "uai": ["ua", ":i"],
        "uan": ["ua", ":n"],
        "uang": ["uA", "N"],
        "ui": ["ue", ":i"],
        "un": ["u7", ":n"],
        "van": ["ve", ":n"],
        "vn": ["v", ":n"]
    }
    return dictionary

def create_reverse_dictionary(dictionary):
    reverse_dict = {}
    for key, value in dictionary.items():
        reverse_dict[tuple(value)] = key
    return reverse_dict

def process_htk_lab(lab_path, reverse_dict):
    with open(lab_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    new_lines = []
    i = 0
    while i < len(lines):
        parts = lines[i].strip().split()
        if len(parts) != 3:
            new_lines.append(lines[i])
            i += 1
            continue

        start, end, phoneme = parts
        if (i + 1) < len(lines):
            next_parts = lines[i + 1].strip().split()
            if len(next_parts) == 3 and next_parts[0] == end:
                next_phoneme = next_parts[2]
                combined_phonemes = (phoneme, next_phoneme)
                if combined_phonemes in reverse_dict:
                    original_phoneme = reverse_dict[combined_phonemes]
                    new_lines.append(f"{start} {next_parts[1]} {original_phoneme}\n")
                    i += 2
                    continue

        new_lines.append(f"{start} {end} {phoneme}\n")
        i += 1

    with open(lab_path, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)

# 批量处理HTK标签文件
def batch_process_htk_labs(folder_path):
    dictionary = read_dictionary()
    reverse_dict = create_reverse_dictionary(dictionary)
    lab_files = [f for f in os.listdir(folder_path) if f.endswith('.lab')]
    
    with Progress() as progress:
        task = progress.add_task("[green]Processing HTK label files...", total=len(lab_files))
        
        for filename in lab_files:
            process_htk_lab(os.path.join(folder_path, filename), reverse_dict)
            progress.update(task, advance=1)

# 获取用户输入
folder_path = input("请输入包含HTK标签文件的文件夹路径：")

batch_process_htk_labs(folder_path)