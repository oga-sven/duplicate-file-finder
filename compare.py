import os
import hashlib
import json
import sys
import time
import logging
from tqdm import tqdm
from string import Template

def calculate_hash(file_path, chunk_size=1024*1024):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(chunk_size):
            hasher.update(chunk)
    return hasher.hexdigest()

def preliminary_scan(directory):
    total_size = 0
    file_count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)
            file_count += 1
    return total_size, file_count

def find_duplicates(directory, total_size, verbose=False):
    hash_dict = {}
    duplicates_size = 0
    with tqdm(total=total_size, unit='B', unit_scale=True) as pbar:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash = calculate_hash(file_path)
                pbar.update(os.path.getsize(file_path))
                if file_hash in hash_dict:
                    hash_dict[file_hash].append(file_path)
                    duplicates_size += os.path.getsize(file_path)
                else:
                    hash_dict[file_hash] = [file_path]
    return {k: v for k, v in hash_dict.items() if len(v) > 1}, duplicates_size

def log_duplicates(duplicates, output_path):
    with open(os.path.join(output_path, 'duplicates.log'), 'w') as log_file:
        for paths in duplicates.values():
            log_file.write('\n'.join(paths))
            log_file.write('\n')

def json_duplicates(duplicates, output_path):
    with open(os.path.join(output_path, 'duplicates.json'), 'w') as json_file:
        json.dump(duplicates, json_file, indent=4)

def summary(duplicates, duplicates_size, total_size, file_count, directory, output_path):
    with open(os.path.join(output_path, 'results.txt'), 'w') as results_file:
        results_file.write(f"Scanned directory: {directory}\n")
        results_file.write(f"Total files scanned: {file_count}\n")
        results_file.write(f"Total size of files: {total_size / (1024*1024):.2f} MB\n")
        results_file.write(f"Total duplicates found: {len(duplicates)}\n")
        results_file.write(f"Total size of duplicates: {duplicates_size / (1024*1024):.2f} MB\n")


def generate_html(duplicates, duplicates_size, total_size, file_count, directory, output_path):
    with open('template.html', 'r') as template_file:
        template = Template(template_file.read())

    image_groups = ''
    for paths in duplicates.values():
        image_group = '<div class="image-group">\n'
        for path in paths:
            file_size = os.path.getsize(path) / 1024  # file size in KB
            image_group += f'<img src="file://{path}" width="100">\n'
            image_group += f'<div class="image-info">File: {os.path.basename(path)} | Path: {path} | Size: {file_size:.2f} KB <input type="checkbox" value="{path}" onclick="updateCommand()"></div>\n'
        image_group += '</div>\n'
        image_groups += image_group

    html = template.substitute(
        directory=directory,
        file_count=file_count,
        total_size=f'{total_size / (1024*1024):.2f}',
        duplicate_count=len(duplicates),
        duplicates_size=f'{duplicates_size / (1024*1024):.2f}',
        image_groups=image_groups
    )

    with open(os.path.join(output_path, 'duplicates.html'), 'w') as html_file:
        html_file.write(html)

def setup_logger(verbose, output_path):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(filename=os.path.join(output_path, 'script_log.log'), level=level,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def setup_output_folder(directory, output_path):
    folder_name = os.path.basename(os.path.normpath(directory))
    output_folder = os.path.join(output_path, folder_name)
    if os.path.exists(output_folder):
        for i in range(1, 1000):
            new_folder_name = f"{folder_name}_{i}"
            new_output_folder = os.path.join(output_path, new_folder_name)
            if not os.path.exists(new_output_folder):
                output_folder = new_output_folder
                break
    os.makedirs(output_folder, exist_ok=True)
    return output_folder

def main():
    directory = sys.argv[1] if len(sys.argv) > 1 else './'
    output_path = 'output' if len(sys.argv) <= 2 else sys.argv[2]
    verbose = '--verbose' in sys.argv

    total_size, file_count = preliminary_scan(directory)
    logging.info(f'Total files: {file_count}')
    logging.info(f'Total size: {total_size / (1024*1024):.2f} MB')
    print(f"Total files: {file_count}")
    print(f"Total size: {total_size / (1024*1024):.2f} MB")
    print("Estimated time: A long time...")
    proceed = input("Proceed? (y/n): ")
    if proceed.lower() != 'y':
        return

    output_folder = setup_output_folder(directory, output_path)
    setup_logger(verbose, output_folder)

    start_time = time.time()
    duplicates, duplicates_size = find_duplicates(directory, total_size, verbose)
    elapsed_time = time.time() - start_time
    logging.info(f'Elapsed time: {elapsed_time:.2f} seconds')

    log_duplicates(duplicates, output_folder)
    json_duplicates(duplicates, output_folder)
    summary(duplicates, duplicates_size, total_size, file_count, directory, output_folder)
    generate_html(duplicates, duplicates_size, total_size, file_count, directory, output_folder)

    print(f"Elapsed time: {elapsed_time:.2f} seconds")

if __name__ == '__main__':
    main()
