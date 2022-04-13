NAME_BYTES = 1
CON_BYTES = 4


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
        file_name = f.name.split('/')[-1].strip().encode()
        file_con_len = len(file_con).to_bytes(CON_BYTES, 'big')
        file_name_len = len(file_name).to_bytes(NAME_BYTES, 'big')
        byte_array += bytearray(file_name_len + file_con_len + file_name + file_con)
        f.flush()
        f.seek(0)

    return byte_array


def unpack(packet):
    f_list = []

    while packet:
        file_name_len = packet[0]
        packet = packet[NAME_BYTES:]
        file_con_len = int.from_bytes(packet[:CON_BYTES], 'big')
        packet = packet[CON_BYTES:]
        file_name = packet[:file_name_len].decode()
        packet = packet[file_name_len:]
        file_con = packet[:file_con_len]
        packet = packet[file_con_len:]

        f = open(file_name, "wb")
        f.write(file_con)
        f.flush()
        f.seek(0)
        f_list.append(f)

    return f_list
