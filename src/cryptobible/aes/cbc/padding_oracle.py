from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from ...common import xor


def _brute_block(padding_oracle, previous_block, ciphertext):
    '''
    Bruteforces a block of ciphertext and returns the plaintext after block decryption
    Args:
        padding_oracle(iv, ct)  : the padding oracle function, returns True for correct padding and False otherwise
        previous_block          : the block before the ciphertext
        ciphertext              : single ciphertext block to be decrypted
    
    Returns:
        plaintext               : a single block of decrypted, padded plaintext
    '''
    known = bytearray()
    for i in reversed(range(16)): # Byte index of pt being bruted
        j = 16 - i # Current expected padding byte
        for b in range(0xff + 1):
            # Construct iv: empty + bruting_byte + xor(known_part, expected_padding_byte)
            iv = bytes(i) + b.to_bytes(1) + xor(known, j)[:len(known)]
            if padding_oracle(iv, ciphertext):
                # If the padding oracle returns True then the byte is correct
                byte = int.from_bytes(xor(b, j))
                known.insert(0, byte)
                break
        else:
            raise ValueError(f"Could not find byte for {i = }")

    return xor(previous_block, known)

def padding_oracle_attack(padding_oracle, iv: bytes, ciphertext: bytes) -> bytes:
    '''
    Args:
        padding_oracle(iv, ct)  : the padding oracle function, returns True for correct padding and False otherwise
        iv                      : initialisation vector
        ciphertext              : ciphertext to be decrypted
    
    Returns:
        plaintext               : the decrypted, padded plaintext
    '''
    plaintext = bytes()
    # separate ciphertext into blocks of size 16
    blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
    blocks.insert(0, iv) # iv will be used to decrypt block 0 of ciphertext

    for i in range(len(1, blocks) - 1):
        plaintext += _brute_block(blocks[i - 1], blocks[i])
    return plaintext

def test_block():
    pt = b'flag{TEST}\x06\x06\x06\x06\x06\x06'
    iv = b'abcd' * 4
    key = b'KEYWOW!!' * 2
    c = AES.new(key, AES.MODE_CBC, iv)
    ct = c.encrypt(pt)

    def oracle(iv, ct):
        # simple oracle function for padding oracle attack
        c = AES.new(key, AES.MODE_CBC, iv)
        try:
            unpad(c.decrypt(ct), 16)
        except ValueError:
            return False
        return True
    
    print(f'Result: {_brute_block(oracle, iv, ct)}')


if __name__ == '__main__':
    test()
