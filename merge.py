import os
import sys
from pydub import AudioSegment
import glob

def get_user_input():
    while True:
        audio_dir = input("请输入音频文件目录路径：").strip()
        if os.path.exists(audio_dir) and os.path.isdir(audio_dir):
            break
        print("错误：音频目录不存在或不是目录，请重新输入")

    while True:
        label_dir = input("请输入HTK标注文件目录路径：").strip()
        if os.path.exists(label_dir) and os.path.isdir(label_dir):
            break
        print("错误：标注目录不存在或不是目录，请重新输入")

    # 分开处理音频和标注的输出目录
    audio_output = input("请输入合并音频的输出目录（留空则使用当前目录）：").strip() or os.getcwd()
    label_output = input("请输入合并标注的输出目录（留空则使用当前目录）：").strip() or os.getcwd()

    for path in [audio_output, label_output]:
        if not os.path.exists(path):
            os.makedirs(path)

    while True:
        try:
            num_per_group = int(input("请输入每组要合并的音频数量（必须为正整数）："))
            if num_per_group > 0:
                break
            print("错误：请输入大于0的整数")
        except ValueError:
            print("错误：请输入有效的整数")

    return audio_dir, label_dir, audio_output, label_output, num_per_group

def main():
    audio_dir, label_dir, audio_output, label_output, num_per_group = get_user_input()

    # 创建输出目录（如果不存在）
    for path in [audio_output, label_output]:
        if not os.path.exists(path):
            os.makedirs(path)

    # 获取所有音频和标注文件
    audio_files = sorted(glob.glob(os.path.join(audio_dir, '*.wav')))
    label_files = sorted(glob.glob(os.path.join(label_dir, '*.lab')))

    # 验证文件数量一致
    if len(audio_files) != len(label_files):
        print(f"错误：音频文件({len(audio_files)})和标注文件({len(label_files)})数量不匹配")
        sys.exit(1)

    # 分组处理
    for group_idx in range(0, len(audio_files), num_per_group):
        current_audio_files = audio_files[group_idx:group_idx+num_per_group]
        merged_audio = AudioSegment.empty()
        merged_labels = []
        total_time = 0

        for audio_path in current_audio_files:
            base_name = os.path.splitext(os.path.basename(audio_path))[0] + '.lab'
            label_path = os.path.join(label_dir, base_name)
            
            if not os.path.exists(label_path):
                print(f"错误：缺少标注文件 {label_path}")
                sys.exit(1)

            # 合并音频
            audio = AudioSegment.from_wav(audio_path)
            merged_audio += audio
            duration = audio.duration_seconds * 1e7  # 转换为HTK时间单位（100ns）

            # 处理标注文件
            with open(label_path, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) < 3:
                        print(f"警告：无效标注行 {line.strip()}，已跳过")
                        continue
                    start = int(parts[0]) + total_time
                    end = int(parts[1]) + total_time
                    label = parts[2]
                    merged_labels.append(f"{start} {end} {label}\n")
            total_time += duration

        # 生成组编号
        group_id = group_idx // num_per_group + 1

        # 保存合并后的文件到不同目录
        output_audio = os.path.join(audio_output, f"group_{group_id}.wav")
        output_label = os.path.join(label_output, f"group_{group_id}.lab")

        merged_audio.export(output_audio, format="wav")
        with open(output_label, 'w') as f:
            f.writelines(merged_labels)

        print(f"第 {group_id} 组文件已生成：\n"
              f"音频：{output_audio}\n"
              f"标注：{output_label}")

if __name__ == "__main__":
    main()