def pack(file_name, file_con):
    file_name_len = ((len(file_name)) + 1).to_bytes(1, 'big')
    byte_array = bytearray(file_name_len + bytearray(file_name + file_con, 'utf-8'))
    return byte_array


def unpack(packet):
    file_name_byte_size = packet[0]
    file_name = packet[1:file_name_byte_size].decode('utf-8')
    file_con = packet[file_name_byte_size:].decode('utf-8')
    f = open(file_name, "w")
    f.write(file_con)
    return f
