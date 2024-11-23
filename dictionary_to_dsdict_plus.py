import argparse
import re
import yaml

def parse_pinyin_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    symbols = set()
    entries = []

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        parts = line.split()
        if len(parts) < 2:
            continue

        grapheme = parts[0]
        phonemes = parts[1:]

        entry = {
            'grapheme': grapheme,
            'phonemes': phonemes
        }
        entries.append(entry)

        for phoneme in phonemes:
            symbols.add(phoneme)

    return symbols, entries

def categorize_symbols(symbols):
    vowels = set('aeiouAEIOUVYaeiouAEIOUVY:')
    categorized_symbols = []

    for symbol in symbols:
        if any(char in vowels for char in symbol):
            categorized_symbols.append({'symbol': symbol, 'type': 'vowel'})
        else:
            categorized_symbols.append({'symbol': symbol, 'type': 'fricative'})

    return categorized_symbols

def generate_yaml_output(symbols, entries, output_file):
    output = {
        'symbols': symbols,
        'entries': entries
    }

    with open(output_file, 'w', encoding='utf-8') as file:
        yaml.dump(output, file, allow_unicode=True, default_flow_style=False)

def main():
    parser = argparse.ArgumentParser(description='Convert pinyin files to YAML format.')
    parser.add_argument('input_files', nargs='+', help='Input files to process')
    parser.add_argument('-o', '--output', required=True, help='Output YAML file path')

    args = parser.parse_args()

    all_symbols = set()
    all_entries = []

    for input_file in args.input_files:
        symbols, entries = parse_pinyin_file(input_file)
        all_symbols.update(symbols)
        all_entries.extend(entries)

    categorized_symbols = categorize_symbols(all_symbols)

    generate_yaml_output(categorized_symbols, all_entries, args.output)

if __name__ == '__main__':
    main()