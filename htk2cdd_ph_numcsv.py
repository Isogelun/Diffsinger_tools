import os
import csv
from decimal import Decimal, getcontext
import click
from tqdm import tqdm

getcontext().prec = 10

def process_lab_file(filepath):
    ph_seq = []
    ph_dur = []
    
    with open(filepath, 'r') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            parts = lines[i].strip().split()
            start_time = Decimal(parts[0])
            end_time = Decimal(parts[1])
            phoneme = parts[2]
            
            duration = (end_time - start_time) * Decimal('0.0000001')
            
            ph_seq.append(phoneme)
            ph_dur.append(duration)
    
    return ph_seq, ph_dur

def process_lab_files_in_directory(directory):
    data = []
    
    for filename in os.listdir(directory):
        if filename.endswith(".lab"):
            filepath = os.path.join(directory, filename)
            name = os.path.splitext(filename)[0]
            ph_seq, ph_dur = process_lab_file(filepath)
            data.append([name, ' '.join(ph_seq), ' '.join(map(str, ph_dur))])
    
    return data

def save_to_csv(data, output_filepath):
    with open(output_filepath, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['name', 'ph_seq', 'ph_dur'])
        csvwriter.writerows(data)

def find_ph_num(i, phonemes_split, dict_set):
    ph_tmp = []
    left = i
    right = i
    for j in range(i, len(phonemes_split)):
        ph_tmp.append(phonemes_split[j])
        if tuple(ph_tmp) in dict_set:
            right = j
    return left, right

def add_ph_num_to_csv(csv_path, dictionary):
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

@click.command()
@click.argument('lab_directory', type=click.Path(exists=True, file_okay=False))
@click.option('-o', '--output', type=click.Path(), default=None, help='Output CSV file path')
@click.option('-d', '--dictionary', required=True, help='Path to dictionary file')
def process_labs_and_add_ph_num(lab_directory, output, dictionary):
    if output is None:
        output = os.path.join(os.path.dirname(lab_directory), 'transcriptions.csv')
    elif os.path.isdir(output):
        output = os.path.join(output, 'transcriptions.csv')

    # Step 1: Process .lab files and save to CSV
    data = process_lab_files_in_directory(lab_directory)
    save_to_csv(data, output)
    click.echo(f"Saved CSV file to {output}.")

    # Step 2: Add phoneme numbers to the CSV file
    add_ph_num_to_csv(output, dictionary)
    click.echo(f"Added phoneme numbers to {output}.")

if __name__ == "__main__":
    process_labs_and_add_ph_num()