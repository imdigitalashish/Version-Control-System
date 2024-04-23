import os
import hashlib
import pickle

def init_vcs():
    os.makedirs(".apna_vcs", exist_ok=True)

def get_file_content(file_path):
    with open(file_path, 'rb') as f:
        return f.read()

def snapshot(directory):
    snapshot_hash = hashlib.sha256()
    snapshot_data = {'files': {}}

    for root, dirs, files in os.walk(directory):
        for file in files:
            if '.apna_vcs' in os.path.join(root, file):
                continue
            file_path = os.path.join(root, file)
            content = get_file_content(file_path)
            snapshot_hash.update(content)
            snapshot_data['files'][file_path] = content

    hash_digest = snapshot_hash.hexdigest()
    snapshot_data['file_list'] = list(snapshot_data['files'].keys())
    print(snapshot_data)
    with open(f'.apna_vcs/{hash_digest}', 'wb') as f:
        pickle.dump(snapshot_data, f)

    print(f"Snapshot created with hash {hash_digest}")

def revert_to_snapshot(hash_digest, directory):
    snapshot_path = f'.apna_vcs/{hash_digest}'
    if not os.path.exists(snapshot_path):
        print("Snapshot does not exist.")
        return

    with open(snapshot_path, 'rb') as f:
        snapshot_data = pickle.load(f)

    for file_path, content in snapshot_data['files'].items():
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(content)

    current_files = set()
    for root, dirs, files in os.walk(directory, topdown=True):
        if '.apna_vcs' in root:
            continue
        for file in files:
            current_files.add(os.path.join(root, file))

    snapshot_files = set(snapshot_data['file_list'])
    print(current_files)
    print(snapshot_files)

    # return
    files_to_delete = current_files - snapshot_files

    for file_path in files_to_delete:
        os.remove(file_path)
        print(f"Removed {file_path}")

    print(f"Reverted to snapshot {hash_digest}")


def get_all_snapshots():
    return os.listdir('.apna_vcs')

def get_changes(previous_snapshot, directory):
    snapshot_hash = hashlib.sha256()
    snapshot_data = {'files': {}}

    for root, dirs, files in os.walk(directory):
        for file in files:
            if '.apna_vcs' in os.path.join(root, file):
                continue
            file_path = os.path.join(root, file)
            content = get_file_content(file_path)
            snapshot_hash.update(content)
            snapshot_data['files'][file_path] = content

    hash_digest = snapshot_hash.hexdigest()
    snapshot_data['file_list'] = list(snapshot_data['files'].keys())
    current_snapshot = snapshot_data

    snapshot_path = f'.apna_vcs/{previous_snapshot}'
    with open(snapshot_path, 'rb') as f:
        previous_snapshot = pickle.load(f)
        
    changes = {}

    for file_path, current_content in current_snapshot['files'].items():
        if file_path in previous_snapshot['files']:
            previous_content = previous_snapshot['files'][file_path]
            if previous_content != current_content:
                changes[file_path] = (previous_content, current_content)
        else:
            changes[file_path] = (None, current_content)

    for file_path in previous_snapshot['files']:
        if file_path not in current_snapshot['files']:
            changes[file_path] = (previous_snapshot['files'][file_path], None)

    return changes.keys()