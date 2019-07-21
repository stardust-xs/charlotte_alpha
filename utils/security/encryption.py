"""
Global encryption for Charlotte
===============================

It encrypts the data, file OR whatever you ask for.

See https://github.com/xames3/charlotte for complete documentation.
"""
from .. fluids.paths import FILE


# https://nitratine.net/blog/post/encryption-and-decryption-in-python/
def keygen(passcode: str, save_to_file: bool = True) -> bytes:
    """
    Definition
    ----------
        Generates a key with salt and saves it to `./key.xai` file if needed.

    Parameters
    ----------
        passcode : string, mandatory
            The password that you would like to encrypt using the salt.

        save_to_file : boolean, optional
            If chosen as True, the key will be stored in a file,
            `./user/key.xai`.

    Returns
    -------
        key : bytes, default
            Byte encrypted key.

    Notes
    -----
        This password is the master password that would be used with the other
        cipher and decipher functions.
    """
    from base64 import urlsafe_b64encode
    from os import urandom

    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.hashes import SHA512
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

    password = passcode.encode()
    kdf = PBKDF2HMAC(algorithm=SHA512(),
                     length=32,
                     salt=urandom(128),
                     iterations=100000,
                     backend=default_backend()
                     )
    key = urlsafe_b64encode(kdf.derive(password))
    if save_to_file is False:
        return key
    else:
        key_file = open(FILE['key'], 'wb')
        key_file.write(key)
        key_file.close()


def cipher(message: str, key: bytes) -> str:
    """
    Definition
    ----------
        Encrypts the message.

    Parameters
    ----------
        message : string, mandatory
            Message OR String that needs to be encrypted.

        key : bytes, mandatory
            Key that will be used for encrypting the message.

    Returns
    -------
        encode.decode() : string, default
            Encrypted text in string format.

    Notes
    -----
        You can choose to return the ciphered text if you want to.
        Just change `encode.decode()` to `encode`
    """
    from cryptography.fernet import Fernet

    to_encode = message.encode()
    fernet_key = Fernet(key)
    encode = fernet_key.encrypt(to_encode)
    super_encode = fernet_key.encrypt(encode)
    return super_encode.decode()


def decipher(ciper_text: str, key: bytes) -> str:
    """
    Definition
    ----------
        Decrypts the message.

    Parameters
    ----------
        ciper_text : string, mandatory
            Encrypted text that needs to be decrypted.

        key : bytes, mandatory
            Key that will be used for decrypting the message.

    Returns
    -------
        decode.decode() : string, default
            Original text in string format.

    Notes
    -----
        Function takes string input for decryption. However if you pass bytes
        text you need to change `ciper_text.encode()` to `ciper_text`
    """
    from cryptography.fernet import Fernet

    fernet_key = Fernet(key)
    decode = fernet_key.decrypt(ciper_text.encode())
    super_decode = fernet_key.decrypt(decode)
    return super_decode.decode()
