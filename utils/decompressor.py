import cv2
import pywt
import numpy as np


def decompress_video(input_video, output_video):
    # Définir la fonction de décompression IDWT
    def decompress_frame(frame):
        # Extraire les canaux de couleur de l'image compressée
        compressed_frame_R = frame[:, :, 0]
        compressed_frame_G = frame[:, :, 1]
        compressed_frame_B = frame[:, :, 2]

        # Appliquer la IDWT sur chaque canal de couleur
        coeffs_R = pywt.dwt2(compressed_frame_R, 'haar')
        coeffs_G = pywt.dwt2(compressed_frame_G, 'haar')
        coeffs_B = pywt.dwt2(compressed_frame_B, 'haar')

        # Reconstruire chaque canal de couleur en utilisant les coefficients de la sous-bande LL
        LL_R, _ = coeffs_R
        LL_G, _ = coeffs_G
        LL_B, _ = coeffs_B

        decompressed_frame_R = pywt.idwt2(
            (LL_R, (np.zeros_like(LL_R), np.zeros_like(LL_R), np.zeros_like(LL_R))), 'haar')
        decompressed_frame_G = pywt.idwt2(
            (LL_G, (np.zeros_like(LL_G), np.zeros_like(LL_G), np.zeros_like(LL_G))), 'haar')
        decompressed_frame_B = pywt.idwt2(
            (LL_B, (np.zeros_like(LL_B), np.zeros_like(LL_B), np.zeros_like(LL_B))), 'haar')

        # Concaténer les canaux de couleur pour former une image en couleur
        decompressed_frame = np.stack(
            [decompressed_frame_R, decompressed_frame_G,
                decompressed_frame_B], axis=-1
        )

        # Convertir l'image en entiers non signés sur 8 bits
        decompressed_frame = np.uint8(decompressed_frame)
        return decompressed_frame

    # Ouvrir le fichier vidéo compressé en lecture
    vid = cv2.VideoCapture(input_video)

    # Obtenir le taux de trame de la vidéo
    fps = vid.get(cv2.CAP_PROP_FPS)

    # Obtenir la taille de l'image de la vidéo
    frame_width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Créer un objet d'écriture vidéo pour le fichier vidéo décompressé
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_vid = cv2.VideoWriter(output_video, fourcc, fps,
                              (frame_width, frame_height), isColor=True)

    # Boucler à travers les images de la vidéo compressée
    while vid.isOpened():
        # Lire l'image compressée suivante
        ret, frame = vid.read()

        if ret == True:
            # Décompresser l'image en utilisant IDWT
            decompressed_frame = decompress_frame(frame)

            # Écrire l'image décompressée dans l'objet d'écriture vidéo
            out_vid.write(decompressed_frame)

        else:
            break

    # Libérer les objets de capture et d'écriture vidéo
    vid.release()
    out_vid.release()