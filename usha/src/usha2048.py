import struct

def left_rotate(x, c):return (x << c) | (x >> (32 - c))

# 1st layer of hashing #
def first_defense(input, rounds=100):
    if isinstance(input, str):
        message = input.encode('utf-8')
    
    
    a0, b0, c0, d0 = 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476
    original_byte_len = len(message)
    original_bit_len = original_byte_len * 8
    message += b'\x80'
    message += b'\x00' * ((56 - (original_byte_len + 1) % 64) % 64)
    message += struct.pack('<Q', original_bit_len)
    
    K = [0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
         0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be, 0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
         0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa, 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
         0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
         0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c, 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
         0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05, 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
         0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
         0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1, 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391]
    
    s = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
         5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
         4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
         6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]
    
    for _ in range(rounds):
        for i in range(0, len(message), 64):
            chunk = message[i:i + 64]
            M = struct.unpack('<16I', chunk)
            A, B, C, D = a0, b0, c0, d0
            for j in range(64):
                if 0 <= j <= 15:
                    F = (B & C) | (~B & D)
                    g = j
                elif 16 <= j <= 31:
                    F = (D & B) | (~D & C)
                    g = (5 * j + 1) % 16
                elif 32 <= j <= 47:
                    F = B ^ C ^ D
                    g = (3 * j + 5) % 16
                elif 48 <= j <= 63:
                    F = C ^ (B | ~D)
                    g = (7 * j) % 16
                F = (F + A + K[j] + M[g]) & 0xFFFFFFFF
                A, D, C, B = D, C, B, (B + left_rotate(F, s[j])) & 0xFFFFFFFF
            a0 = (a0 + A) & 0xFFFFFFFF
            b0 = (b0 + B) & 0xFFFFFFFF
            c0 = (c0 + C) & 0xFFFFFFFF
            d0 = (d0 + D) & 0xFFFFFFFF
    
    # Combine the hash values and salt
    final_hash = struct.pack('<4I', a0, b0, c0, d0).hex()
    return final_hash

# 2nd layer of hashing #
def second_defense(data): 
    hash_size = 256  # 64 bytes
    block_size = 256  # Block size in bytes
    initial_value = 0xbb53c4d54aec8238c1890101637c87ff8f8fa85d9045559b9a24008cb81c40fe50c96a6d67fc34
  # Example initial value fitting 64 bytes

    hash_value = bytearray(initial_value.to_bytes(hash_size, byteorder='big'))

    # Convert data to bytes if it's not already
    if isinstance(data, str):
        data = data.encode('utf-8')

    # Step 2: Padding
    original_length = len(data) * 8
    data += b'\x80'
    while (len(data) * 8 + 64) % 512 != 0:
        data += b'\x00'
    data += struct.pack('>Q', original_length)

    # Step 3: Processing
    def right_rotate(value, shift):
        return (value >> shift) | (value << (32 - shift)) & 0xFFFFFFFF

    def mix_function(block, hash_value):
        for i in range(len(block)):
            hash_value[i % hash_size] ^= block[i]
            hash_value = hash_value[-1:] + hash_value[:-1]  # Rotate right
            hash_value = bytearray((b ^ (b >> 1) ^ (b << 1) & 0xFF) for b in hash_value)  # Bitwise mixing
            # Additional mixing steps
            hash_value = bytearray((b ^ (b >> 2) ^ (b << 2) & 0xFF) for b in hash_value)
            hash_value = bytearray((b ^ (b >> 3) ^ (b << 3) & 0xFF) for b in hash_value)
            # Introduce more non-linear operations
            hash_value = bytearray((b ^ (b >> 4) ^ (b << 6) & 0xFF) for b in hash_value)
            hash_value = bytearray((b ^ (b >> 5) ^ (b << 5) & 0xFF) for b in hash_value)
            hash_value = bytearray((b ^ (b >> 6) ^ (b << 6) & 0xFF) for b in hash_value)
            hash_value = bytearray((b ^ (b >> 7) ^ (b << 7) & 0xFF) for b in hash_value)
        return hash_value

    # Increase the number of rounds to make it more computationally intensive
    num_rounds = 700
    for _ in range(num_rounds):
        for i in range(0, len(data), block_size):
            block = data[i:i + block_size]
            hash_value = mix_function(block, hash_value)
            hash_value = mix_function(block, hash_value)

    # Step 4: Finalization
    final_hash = bytes(hash_value[:hash_size])

    # Convert the final hash to a hexadecimal string
    return final_hash.hex()

# padding #
def pad_message(message):
    message = message.encode('utf-8')
    original_length = len(message) * 8
    message += b'\x80'
    while (len(message) * 8) % 786 != 722:
        message += b'\x00'
    message += struct.pack('>Q', original_length)
    return message

# initializing buffers #
def initialize_buffers():
    # Adding 70 more buffers for increased complexity
    return [
        0x6a09e667f3bcc908, 0xbb67ae8584caa73b, 0x3c6ef372fe94f82b, 0xa54ff53a5f1d36f1,
        0x510e527fade682d1, 0x9b05688c2b3e6c1f, 0x1f83d9abfb41bd6b, 0x5be0cd19137e2179,
        0xcbbb9d5dc1059ed8, 0x629a292a367cd507, 0x9159015a3070dd17, 0x152fecd8f70e5939,
        0x67332667ffc00b31, 0x8eb44a8768581511, 0xdb0c2e0d64f98fa7, 0x47b5481dbefa4fa4,
        0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2, 0x72be5d74f27b896f, 0x80deb1fe3b1696b1,
        0x9bdc06a725c71235, 0xc19bf174cf692694, 0xe49b69c19ef14ad2, 0xefbe4786384f25e3,
        0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65, 0x2de92c6f592b0275, 0x4a7484aa6ea6e483,
        0x5cb0a9dcbd41fbd4, 0x76f988da831153b5, 0x983e5152ee66dfab, 0xa831c66d2db43210,
        0xb00327c898fb213f, 0xbf597fc7beef0ee4, 0xc6e00bf33da88fc2, 0xd5a79147930aa725,
        0x06ca6351e003826f, 0x142929670a0e6e70, 0x27b70a8546d22ffc, 0x2e1b21385c26c926,
        0x4d2c6dfc5ac42aed, 0x53380d139d95b3df, 0x650a73548baf63de, 0x766a0abb3c77b2a8,
        0x81c2c92e47edaee6, 0x92722c851482353b, 0xa2bfe8a14cf10364, 0xa81a664bbc423001,
        0xc24b8b70d0f89791, 0xc76c51a30654be30, 0xd192e819d6ef5218, 0xd69906245565a910,
        0xf40e35855771202a, 0x106aa07032bbd1b8, 0x19a4c116b8d2d0c8, 0x1e376c085141ab53,
        0x2748774cdf8eeb99, 0x34b0bcb5e19b48a8, 0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb,
        0x5b9cca4f7763e373, 0x682e6ff3d6b2b8a3, 0x748f82ee5defb2fc, 0x78a5636f43172f60,
        0x84c87814a1f0ab72, 0x8cc702081a6439ec, 0x90befffa23631e28, 0xa4506cebde82bde9,
        0xbef9a3f7b2c67915, 0xc67178f2e372532b, 0xca273eceea26619c, 0xd186b8c721c0c207,
        0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178, 0x06f067aa72176fba, 0x0a637dc5a2c898a6,
        0x113f9804bef90dae, 0x1b710b35131c471b, 0x28db77f523047d84, 0x32caab7b40c72493,
        0x3c9ebe0a15c9bebc, 0x431d67c49c100d4c, 0x4cc5d4becb3e42b6, 0x597f299cfc657e2a,
        0x5fcb6fab3ad6faec, 0x6c44198c4a475817
    ]

# Compression #
def compression_function(block, buffers):
    for i in range(0, len(block), 99):
        chunk = block[i:i+99]
        for j in range(len(buffers)):
            buffers[j] ^= int.from_bytes(chunk[j*8:(j+1)*8], 'big')
            buffers[j] = (buffers[j] * 0x5bd1e995) & 0xFFFFFFFFFFFFFFFF  # Example non-linear operation
            buffers[j] = (buffers[j] >> 3) | (buffers[j] << (786 - 90))  
            buffers[j] = (buffers[j] + 0x6c44198c4a475817) & 0xFFFFFFFFFFFFFFFF 
            buffers[j] = (buffers[j] >> 3) | (buffers[j] << (786 - 78))  
            buffers[j] = (buffers[j] + 0xf57d4f7fee6ed178) & 0xFFFFFFFFFFFFFFFF 
            buffers[j] = (buffers[j] >> 3) | (buffers[j] << (786 - 156))  
            buffers[j] = (buffers[j] + 0x5fcb6fab3ad6faec) & 0xFFFFFFFFFFFFFFFF 
            buffers[j] = (buffers[j] >> 3) | (buffers[j] << (786 - 780))  
            buffers[j] = (buffers[j] + 0xa81a664bbc423001) & 0xFFFFFFFFFFFFFFFF 
            buffers[j] = (buffers[j] >> 3) | (buffers[j] << (786 - 167))  
            buffers[j] = (buffers[j] + 0xbb67ae8584caa73b) & 0xFFFFFFFFFFFFFFFF 
            buffers[j] = (buffers[j] >> 3) | (buffers[j] << (786 - 756))  
            buffers[j] = (buffers[j] + 0xb00327c898fb213f) & 0xFFFFFFFFFFFFFFFF 
    return buffers

#final layer of hashing
def hash_message(message, iterations=1000):
    message = pad_message(message)
    buffers = initialize_buffers()
    
    for _ in range(iterations): # repeatedly hashing data
        for i in range(0, len(message), 99):
            block = message[i:i+99]
            buffers = compression_function(block, buffers)
            block = message[i:i+99]
            buffers = compression_function(block, buffers)
            block = message[i:i+99]
            buffers = compression_function(block, buffers)
            block = message[i:i+99]
            buffers = compression_function(block, buffers)
            block = message[i:i+99]
            buffers = compression_function(block, buffers)
            block = message[i:i+99]
            buffers = compression_function(block, buffers)

    hash_value = b''.join(struct.pack('>Q', buffer) for buffer in buffers)
    return hash_value.hex()

