

from utils import *

directory = "./control_directory"

if __name__ == "__main__":
    import sys
    command = sys.argv[1]

    if command == "init":
        init_vcs()
    elif command == "commit":
        snapshot(directory)
    elif command == "reset":
        revert_to_snapshot(sys.argv[2], directory)

    elif command == "status":
        snapshots = get_all_snapshots()
        if len(snapshots) == 0:
            print("No snapshots found.")
            sys.exit()
        changes = get_changes(snapshots[-1], directory)
        print(changes)
    elif command == "log":
        snapshots = get_all_snapshots()
        for snapshot in snapshots:
            print(snapshot)
    else:
        print("Unknown command.")