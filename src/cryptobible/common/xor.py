from .bytes_int import long_to_bytes

def xor(*args, cut=max):
    '''
    Inspired by pwn.xor() function, implements a simpler version.
    XORs any number of given bytestrings. Ignores empty strings.
    Args:
        *args   : any nymber of bytes, bytearray or list objects
        cut     : function which decides the result's length cutoff

    Returns:
        x       : the bytestrings XOR-ed with each other
    '''
    if len(args) == 0:
        raise ValueError("Must have something to xor")

    strs = [
        long_to_bytes(s) if isinstance(s, int) else bytearray(s)
        for s in args if s
    ]
    cutoff = cut(len(s) for s in strs)

    def xor_char(n):
        b = 0
        for s in strs:
            b ^= s[n % len(s)]
        return b

    return bytes(map(xor_char, range(cutoff)))

def test():
    msg = b'very_secret_message'
    key = b'secure_key'
    ct = xor(msg, key)
    print(f'Original message: {msg}')
    print(f'Encrypted: {ct.hex()}')
    print(f'Decrypted: {xor(ct, key)}')

if __name__ == '__main__':
    test()
