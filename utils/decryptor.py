from Crypto.Cipher import AES


def decrypt_video(input_video, decrypted_video, key):
    # Open the encrypted video file
    encrypted_video = open(input_video, 'rb')

    # Read the IV from the beginning of the file
    iv = encrypted_video.read(AES.block_size)

    # Pad the key to 16 bytes
    key = key.encode('utf-8')
    key = key + (b'\0' * (AES.block_size - len(key)))

    # Create the AES cipher in CBC mode with the given key and IV
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Open the output video file
    with open(decrypted_video, 'wb') as decrypted_video:
        # Decrypt and write each chunk of the encrypted video to the output file
        while True:
            chunk = encrypted_video.read(AES.block_size)
            if len(chunk) == 0:
                break
            decrypted_chunk = cipher.decrypt(chunk)
            decrypted_video.write(decrypted_chunk)

    # Release the resources
    encrypted_video.close()