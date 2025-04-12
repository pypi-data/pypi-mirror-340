Cryptcrro
=================

``Cryptcrro`` is a python cryptographic library.

``Cryptcrro`` includes both asymetric and symetric encryption, for encryption the protocols is asymetric ECIES + Chacha20 or RSA + Chacha20, for signing the protocols is ECDSA or RSA.

``Cryptcrro`` also provide symmetric encryption protocols as:
       -AES-256_CTR

       -ChaCha20

       -Sha256_CTR

``Cryptcrro`` provide high level recipe through the ``crro`` module.

For example, symetric encryption can be done like that:

.. code-block:: pycon

    >>> from cryptcrro.symetric import crro 
    >>> plaintext = "Chancellor on brink of second bailout for banks"
    >>> key = scrro.generate_key()
    >>> ciphertext = scrro.encrypt(key, message)
    >>> decrypted_ciphertext = scrro.decrypt(key, ciphertext)

Or, asymetric encryption:

.. code-block:: pycon

    >>> from cryptcrro.asymetric import crro
    >>> private_key = crro.generate_private_key()
    >>> public_key = crro.generate_public_key(private_key)
    >>> plaintext = "Chancellor on brink of second bailout for banks"
    >>> ciphertext = crro.encrypt(public_key, message) 
    >>> decrypted_ciphertext = crro.decrypt(private_key, encrypted_message) 
