import os
import json
import hashlib

HASH_FILE = "hash_table.json"

def hash_file(file_path):
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        data = f.read()
        hasher.update(data)
    return hasher.hexdigest()

def traverse_directory(directory):
    hash_table = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            hash_table[full_path] = hash_file(full_path)
    return hash_table

def generate_table(directory):
    hashes = traverse_directory(directory)
    with open(HASH_FILE, "w") as f:
        json.dump(hashes, f, indent=4)
    print("Hash table generated.")

def validate_hashes(directory):
    if not os.path.exists(HASH_FILE):
        print("No hash table found.")
        return

    with open(HASH_FILE, "r") as f:
        old_hashes = json.load(f)

    new_hashes = traverse_directory(directory)

    for path in old_hashes:
        if path not in new_hashes:
            print(path, "was deleted.")
        elif old_hashes[path] != new_hashes[path]:
            print(path, "hash is INVALID.")
        else:
            print(path, "hash is VALID.")

    for path in new_hashes:
        if path not in old_hashes:
            print("New file detected:", path)

def main():
    print("1) Generate Hash Table")
    print("2) Verify Hashes")
    choice = input("Select option: ")
    directory = input("Enter directory path: ")

    if choice == "1":
        generate_table(directory)
    elif choice == "2":
        validate_hashes(directory)
    else:
        print("Invalid option.")

if __name__ == "__main__":
    main()
