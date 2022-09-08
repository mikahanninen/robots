import mmap


def find_in_file(filename, text_to_find):
    with open(filename, "rb", 0) as file, mmap.mmap(
        file.fileno(), 0, access=mmap.ACCESS_READ
    ) as s:
        if s.find(f"{text_to_find}".encode()) != -1:
            return True
    return False
