import gzip

max_size = 0

for red in range(32):
    for green in range(32):
        for blue in range(32):
            for alpha in range(2):
                data = []
                val = (red << 11) | (green << 5) | (blue << 1) | alpha
                major = (val >> 8) & 0xFF
                minor = val & 0xFF
                for px in range(32*32):
                    data.extend([major, minor])
                b_data = bytearray(data)
                comp = gzip.compress(b_data, compresslevel=9)
                if max_size < len(comp):
                    max_size = len(comp)
print(f"Max Size: {hex(max_size)}")
