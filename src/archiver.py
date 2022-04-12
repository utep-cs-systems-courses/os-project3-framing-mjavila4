NAME_BYTES = 1
CON_BYTES = 4
ALLOC_BYTES = NAME_BYTES + CON_BYTES


class Archiver:
    file_list = []

    def add_file(self, file):
        self.file_list.append(file)

    def add_file_list(self, f_list):
        for f in f_list:
            self.add_file(f)

    def set_file_list(self, fl):
        self.file_list = fl

    def get_file_list(self):
        return self.file_list


def pack(file_array):
    byte_array = bytearray()

    for f in file_array:
        file_con = f.read()
        file_name = get_file_name(f)
        file_name_len = ((len(file_name)) + 1).to_bytes(NAME_BYTES, 'big')
        file_contents_len = (len(file_con) + 1).to_bytes(CON_BYTES, 'big')
        byte_array += bytearray(file_name_len + file_contents_len + (file_name + file_con).encode())
        f.flush()
        f.close()

    return byte_array


def unpack(packet):
    file_listt = []

    while packet:
        file_name_byte_size = packet[0]
        file_name = packet[ALLOC_BYTES:file_name_byte_size + ALLOC_BYTES - 1].decode('utf-8')

        file_con_byte_size = int.from_bytes(packet[1:5], 'big')
        file_con_byte_size += file_name_byte_size + ALLOC_BYTES - 1

        file_con = packet[file_name_byte_size + ALLOC_BYTES - 1:file_con_byte_size].decode('utf-8')
        packet = packet[file_con_byte_size - 1:]

        f = open(file_name, "w+")
        f.write(file_con)
        f.seek(0)
        file_listt.append(f)
        f.flush()
        f.close()

    return file_listt


def get_file_name(file):
    file_name = file.name.split('/')
    return file_name[-1]
