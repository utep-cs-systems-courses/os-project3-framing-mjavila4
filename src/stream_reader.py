import archiver


class StreamReader:
    file_name_len = 0
    file_con_len = 0
    file_name_parsed = True
    temp_stream = bytearray()

    def listen(self, stream):
        self.temp_stream += stream
        file_names = []
        file_name = None

        while len(self.temp_stream) != 0:

            if self.file_name_len == 0:
                self.file_name_len = self.temp_stream[0]
                self.temp_stream = self.temp_stream[1:]
                self.file_con_len = int.from_bytes(self.temp_stream[:4], 'big')
                self.temp_stream = self.temp_stream[4:]

            if self.file_name_parsed and len(self.temp_stream) >= self.file_name_len:
                self.file_name_parsed = False
                file_name = self.temp_stream[:self.file_name_len].decode()
                self.temp_stream = self.temp_stream[self.file_name_len:]
                file_names.append(file_name)

            if len(self.temp_stream) >= self.file_con_len:
                self.file_name_parsed = True
                self.temp_stream = self.temp_stream[self.file_con_len:]
                self.file_name_len = 0
                self.file_con_len = 0

            else:
                break

        if file_name:
            return file_names
        else:
            return 0
