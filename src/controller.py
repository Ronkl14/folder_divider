import os
import shutil
import math
import threading

def copy_files_to_folder(group, source_folder, target_folder, update_progress):
    total_files = len(group)
    for idx, file_name in enumerate(group):
        shutil.copy(os.path.join(source_folder, file_name), target_folder)
        progress = (idx + 1) / total_files
        update_progress(progress) 

def copy_unknown_file(unknown_file, source_folder, target_folders):
    for target_folder in target_folders:
        shutil.copy(os.path.join(source_folder, unknown_file), target_folder)

def divide_and_copy_files(source_folder: str, target_folders: list, parallel_copying: bool, progress_callbacks):
    raw_files = [f for f in os.listdir(source_folder) if f.endswith('.raw')]
    
    num_groups = len(target_folders)
    group_size = math.ceil(len(raw_files) / num_groups)
    
    if parallel_copying:
        threads = []
        for i, target_folder in enumerate(target_folders):
            group = raw_files[i*group_size : (i+1)*group_size]
            thread = threading.Thread(
                target=copy_files_to_folder, 
                args=(group, source_folder, target_folder, progress_callbacks[i])
            )
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
    else:
        for i, target_folder in enumerate(target_folders):
            progress_callbacks 
            group = raw_files[i*group_size : (i+1)*group_size]
            copy_files_to_folder(group, source_folder, target_folder, progress_callbacks[i])
            progress_callbacks[i](1.0)

    unknown_files = [f for f in os.listdir(source_folder) if not f.endswith('.raw')]
    if unknown_files:
        unknown_file = unknown_files[0]  # Assuming there is only one unknown file
        for target_folder in target_folders:
            shutil.copy(os.path.join(source_folder, unknown_file), target_folder)

