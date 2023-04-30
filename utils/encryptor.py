from Crypto.Cipher import AES
import os


def encrypt_video(input_video, encrypted_video, key):
    # Open the video file
    video = open(input_video, 'rb')

    # Generate a random IV
    iv = os.urandom(AES.block_size)

    # Pad the key to 16 bytes
    key = key.encode('utf-8')
    key = key + (b'\0' * (AES.block_size - len(key)))

    # Create the AES cipher in CBC mode with the given key and IV
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Open the output video file
    with open(encrypted_video, 'wb') as encrypted_video:
        # Write the IV to the output file
        encrypted_video.write(iv)

        # Encrypt and write each chunk of the input video to the output file
        while True:
            chunk = video.read(AES.block_size)
            if len(chunk) == 0:
                break
            elif len(chunk) % AES.block_size != 0:
                chunk += b' ' * (AES.block_size - len(chunk) % AES.block_size)
            encrypted_video.write(cipher.encrypt(chunk))

    # Release the resources
    video.close()