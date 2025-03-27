import os
from pathlib import Path

def process_wav_files(folder_path, output_folder):
    # 创建输出目录（如果不存在）
    output_dir = Path(output_folder)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    folder = Path(folder_path)
    
    for file in folder.iterdir():
        # 只处理wav文件
        if file.is_file() and file.suffix.lower() == '.wav':
            # 分离文件名和扩展名
            name_part = file.stem
            
            # 处理内容：下划线转空格 + 去除首尾空格
            content = name_part.replace('_', ' ').strip()
            
            # 生成lab文件名，并设置其位于output_dir中
            lab_file = output_dir / (file.stem + '.lab')
            
            # 写入lab文件
            with open(lab_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f'Created: {lab_file.name} (内容: "{content}")')

if __name__ == "__main__":
    input_path = input("请输入包含wav文件的文件夹路径：").strip('\"')
    
    while not os.path.exists(input_path):
        print(f"路径不存在：{input_path}")
        input_path = input("请重新输入有效的文件夹路径：").strip('\"')
    
    output_path = input("请输入保存lab文件的文件夹路径：").strip('\"')
    
    process_wav_files(input_path, output_path)
    print("\n处理完成！请检查生成的.lab文件")