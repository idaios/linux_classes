#!/home/motoo/miniconda3/bin/python
import sys
import re

def parse_fasta(file_path):
    """Parse a FASTA file and return a dictionary with sequence names as keys and sequences as values."""
    sequences = {}
    with open(file_path, 'r') as file:
        sequence_name = None
        sequence_data = []
        for line in file:
            if line.startswith('>'):
                if sequence_name:
                    sequences[sequence_name] = ''.join(sequence_data)
                sequence_name = line.strip()
                #print(sequence_name)
                sequence_data = []
            else:
                sequence_data.append(line.strip())
        if sequence_name:
            sequences[sequence_name] = ''.join(sequence_data)
    return sequences

def merge_fasta(file_list):
    """Merge sequences from FASTA files listed in file_list and write to stdout in one-line FASTA format."""
    all_sequences = {}
    for fasta_file in file_list:
        fasta_file = fasta_file.strip()
        sequences = parse_fasta(fasta_file)
        
        for name, sequence in sequences.items():
            # Match only the sequence name (ignoring description if present)
            match = re.search(r'_([^_]+)_', name)
            if match:
                seq_name = match.group(1)
                #print(seq_name)
                if seq_name in all_sequences:
                    all_sequences[seq_name] += sequence  # Concatenate sequences if matched
                else:
                    all_sequences[seq_name] = sequence
            else:
                match2 = re.search(r'>([^_]+)', name)
                if match2:
                    seq_name = match2.group(1)
                    #print(seq_name)
                    if seq_name in all_sequences:
                        all_sequences[seq_name] += sequence  # Concatenate sequences if matched
                    else:
                        all_sequences[seq_name] = sequence


    # Write merged sequences to standard output in one-line FASTA format
    for name, sequence in all_sequences.items():
        sys.stdout.write(f">{name}\n{sequence}\n")

# Read file list from standard input and merge FASTA files
if __name__ == "__main__":
    file_list = sys.stdin.read().splitlines()
    merge_fasta(file_list)
