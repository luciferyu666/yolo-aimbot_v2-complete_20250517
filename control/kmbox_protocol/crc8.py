
def crc8(data: bytes) -> int:
    poly = 0x1D
    crc = 0
    for b in data:
        crc ^= b
        for _ in range(8):
            crc = (crc<<1) ^ poly if (crc & 0x80) else (crc<<1)
            crc &= 0xFF
    return crc
