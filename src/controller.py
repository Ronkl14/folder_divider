from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import shutil
import threading
import math

def copy_file(source, target):
    shutil.copy(source, target)

def copy_files_to_folder(group, source_folder, target_folder, update_progress, file_extension_mode=None):
    total_files = len(group)
    with ThreadPoolExecutor() as executor:
        futures = []
        for idx, file_name in enumerate(group):
            source = os.path.join(source_folder, file_name)
            target = target_folder

            # If in .jp2 + .json mode, also copy the corresponding .json file
            if file_extension_mode == ".jp2 + .json":
                json_file_name = file_name.replace('.jp2', '.json')
                json_source = os.path.join(source_folder, json_file_name)
                futures.append(executor.submit(copy_file, json_source, target))

            futures.append(executor.submit(copy_file, source, target))
        
        for idx, future in enumerate(as_completed(futures)):
            future.result()
            progress = (idx + 1) / total_files
            update_progress(progress)

def divide_and_copy_files(source_folder: str, target_folders: list, parallel_copying: bool, progress_callbacks, file_extension_mode: str):
    if file_extension_mode == ".raw + .txt":
        raw_files = [f for f in os.listdir(source_folder) if f.endswith('.raw')]
        unknown_files = [f for f in os.listdir(source_folder) if f.endswith('.txt')]
    elif file_extension_mode == ".jp2 + .json":
        raw_files = [f for f in os.listdir(source_folder) if f.endswith('.jp2')]

    num_groups = len(target_folders)
    group_size = math.ceil(len(raw_files) / num_groups)

    if parallel_copying:
        threads = []
        for i, target_folder in enumerate(target_folders):
            group = raw_files[i*group_size : (i+1)*group_size]
            thread = threading.Thread(
                target=copy_files_to_folder, 
                args=(group, source_folder, target_folder, progress_callbacks[i], file_extension_mode)
            )
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
    else:
        for i, target_folder in enumerate(target_folders):
            group = raw_files[i*group_size : (i+1)*group_size]
            copy_files_to_folder(group, source_folder, target_folder, progress_callbacks[i], file_extension_mode)
            progress_callbacks[i](1.0)

    if file_extension_mode == ".raw + .txt" and unknown_files:
        unknown_file = unknown_files[0]  # Assuming there is only one unknown file
        for target_folder in target_folders:
            shutil.copy(os.path.join(source_folder, unknown_file), target_folder)