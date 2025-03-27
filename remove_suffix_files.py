import os

def keep_files_by_suffix(directory, suffix):
    """
    遍历指定目录并删除不具有特定后缀的所有文件。
    
    :param directory: 要清理的目标目录路径
    :param suffix: 要保留的文件的后缀名（包括点号，如 '.txt'）
    """
    # 检查提供的路径是否为目录
    if not os.path.isdir(directory):
        print(f"错误：'{directory}' 不是有效的目录路径")
        return
    
    affected_files = 0
    # 遍历目录中的所有文件和子文件夹
    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            # 如果文件不以指定后缀结尾，则构建完整路径并删除它
            if not filename.endswith(suffix):
                file_path = os.path.join(foldername, filename)
                try:
                    os.remove(file_path)
                    print(f"已删除: {file_path}")
                    affected_files += 1
                except Exception as e:
                    print(f"无法删除 {file_path}: {e}")
    
    if affected_files == 0:
        print(f"在 '{directory}' 中没有找到需要删除的文件。所有文件都符合保留的后缀 '{suffix}'。")
    else:
        print(f"操作完成，共删除 {affected_files} 个文件。")

if __name__ == "__main__":
    # 用户输入
    directory_path = input("请输入目标目录路径：")
    file_suffix = input("请输入想要保留的文件后缀（例如 .txt）：")
    
    # 调用函数
    keep_files_by_suffix(directory_path, file_suffix)