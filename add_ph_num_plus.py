import click
import csv
from tqdm import tqdm

def find_ph_num(i, phonemes_split, dict_set):
    ph_tmp = []
    left = i
    right = i
    for j in range(i, len(phonemes_split)):
        ph_tmp.append(phonemes_split[j])
        if tuple(ph_tmp) in dict_set:
            right = j
    return left, right

@click.command()
@click.option('-c', '--csv_path', required=True, help='Path to CSV file')
@click.option('-d', '--dictionary', required=True, help='Path to dictionary file')
def add_ph_num(csv_path, dictionary):
    ph_seq_index = 1
    phonemes_tmp = []

    # Read phonemes from CSV
    with open(csv_path, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        header = next(csv_reader)  # Save header row
        for row in csv_reader:
            phonemes_tmp.append(row)

    # Load dictionary into a set of tuples for faster lookup
    dict_set = set()
    with open(dictionary, 'r', encoding='utf-8') as f:
        for line in f:
            key, value = line.strip().split('\t')
            dict_set.add(tuple(value.split()))

    # Process phonemes and add phoneme numbers
    ph_num_str = []  # Initialize without header
    for phonemes_row in tqdm(phonemes_tmp, desc="Processing phonemes"):
        phonemes = phonemes_row[ph_seq_index]
        tmp = []
        phonemes_split = phonemes.split(' ')
        i = 0
        while i < len(phonemes_split):
            if phonemes_split[i] == "AP" or phonemes_split[i] == "SP":
                tmp.append("1")
                i += 1
            else:
                left, right = find_ph_num(i, phonemes_split, dict_set)
                tmp.append(str(right - left + 1))
                i = right + 1
        ph_num_str.append(' '.join(tmp))

    # Combine header and processed data
    header.append("ph_num")  # Add ph_num column to the header
    rows = [header]
    for row, ph_num in zip(phonemes_tmp, ph_num_str):
        row.append(ph_num)
        rows.append(row)

    # Write results back to CSV
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

if __name__ == '__main__':
    add_ph_num()






