import os
import json
import hashlib

HASH_FILE = "hash_table.json"

def hash_file(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(4096):
            sha256.update(chunk)
    return sha256.hexdigest()

def traverse_directory(directory):
    hashes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            hashes[full_path] = hash_file(full_path)
    return hashes

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

    for path, old_hash in old_hashes.items():
        if path not in new_hashes:
            print(f"{path} was deleted.")
        elif new_hashes[path] != old_hash:
            print(f"{path} hash is INVALID.")
        else:
            print(f"{path} hash is VALID.")

    for path in new_hashes:
        if path not in old_hashes:
            print(f"New file detected: {path}")

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
