"""
This module encrypts and decrypts any string using a key.

    Functions list:
        - keygen     : Generates key and stores it as an environment variable.
        - encrypt    : Encrypts the data (string).
        - decrypt    : Decrypts the data (string).

See https://github.com/xames3/charlotte for cloning the repository.
"""
from sys import exc_info


def keygen(passcode: str) -> None:
    # https://nitratine.net/blog/post/encryption-and-decryption-in-python/
    """
    Definition
    ----------
        Generates a key with salt and strores it in an environment variable.

    Parameters
    ----------
        passcode : string, mandatory
            The password that you would like to encrypt using the salt.

    Notes
    -----
        This password is the master password that would be used with the other
        encrypt and decrypt functions.
    """
    from base64 import urlsafe_b64encode
    from os import urandom
    from subprocess import call

    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.hashes import SHA512
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

    try:
        password = passcode.encode()
        kdf = PBKDF2HMAC(algorithm=SHA512(),
                         length=32,
                         salt=urandom(128),
                         iterations=100000,
                         backend=default_backend()
                         )
        key = urlsafe_b64encode(kdf.derive(password)).decode(encoding='utf-8')
        call(f"setx CHARLOTTE_MASTER_KEY {key}", shell=True)
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} on line {exc_info()[-1].tb_lineno}.')


def encrypt(message: str, key: str) -> str:
    """
    Definition
    ----------
        Encrypts the message.

    Parameters
    ----------
        message : string, mandatory
            Message OR String that needs to be encrypted.

        key : string, mandatory
            Key that will be used for encrypting the message.

    Returns
    -------
        encode.decode() : string, default
            Encrypted text in string format.

    Notes
    -----
        You can choose to return the encrypted text if you want to.
        Just change `encode.decode()` to `encode`
    """
    from cryptography.fernet import Fernet

    try:
        to_encode = message.encode()
        fernet_key = Fernet(key.encode(encoding='utf-8'))
        encode = fernet_key.encrypt(to_encode)
        super_encode = fernet_key.encrypt(encode)
        return super_encode.decode()
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} on line {exc_info()[-1].tb_lineno}.')


def decrypt(encrypted_text: str, key: str) -> str:
    """
    Definition
    ----------
        Decrypts the message.

    Parameters
    ----------
        encrypted_text : string, mandatory
            Encrypted text that needs to be decrypted.

        key : string, mandatory
            Key that will be used for decrypting the message.

    Returns
    -------
        decode.decode() : string, default
            Original text in string format.

    Notes
    -----
        Function takes string input for decryption. However if you pass bytes
        text you need to change `encrypted_text.encode()` to `encrypted_text`
    """
    from cryptography.fernet import Fernet

    try:
        fernet_key = Fernet(key.encode(encoding='utf-8'))
        decode = fernet_key.decrypt(encrypted_text.encode())
        super_decode = fernet_key.decrypt(decode)
        return super_decode.decode()
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} on line {exc_info()[-1].tb_lineno}.')
