import cv2
import pywt
import numpy as np

def compress_video(input_video, output_video):

    # Définir la fonction de compression DWT
    def compress_frame(frame):
        # Appliquer la DWT sur chaque canal de couleur de l'image
        coeffs_R = pywt.dwt2(frame[:, :, 0], 'haar')
        coeffs_G = pywt.dwt2(frame[:, :, 1], 'haar')
        coeffs_B = pywt.dwt2(frame[:, :, 2], 'haar')

        # Garder uniquement les coefficients de la sous-bande LL
        LL_R, (LH_R, HL_R, HH_R) = coeffs_R
        LL_G, (LH_G, HL_G, HH_G) = coeffs_G
        LL_B, (LH_B, HL_B, HH_B) = coeffs_B

        coeffs = (LL_R, LL_G, LL_B), (
            np.zeros_like(LH_R), np.zeros_like(HL_R), np.zeros_like(HH_R)
        )

        # Reconstruire l'image compressée
        compressed_frame_R = pywt.idwt2(coeffs_R, 'haar')
        compressed_frame_G = pywt.idwt2(coeffs_G, 'haar')
        compressed_frame_B = pywt.idwt2(coeffs_B, 'haar')

        # Concaténer les canaux de couleur pour former une image en couleur
        compressed_frame = np.stack(
            [compressed_frame_R, compressed_frame_G, compressed_frame_B], axis=-1
        )

        # Convertir l'image en entiers non signés sur 8 bits
        compressed_frame = np.uint8(compressed_frame)
        return compressed_frame

    # Ouvrir le fichier vidéo en lecture
    vid = cv2.VideoCapture(input_video)

    # Obtenir le taux de trame de la vidéo
    fps = vid.get(cv2.CAP_PROP_FPS)

    # Obtenir la taille de l'image de la vidéo
    frame_width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Créer un objet d'écriture vidéo pour le fichier vidéo compressé
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_vid = cv2.VideoWriter(output_video, fourcc, fps,
                              (frame_width, frame_height), isColor=True)

    # Boucler à travers les images de la vidéo
    while vid.isOpened():
        # Lire l'image suivante
        ret, frame = vid.read()

        if ret == True:
            # Compresser l'image en utilisant DWT
            compressed_frame = compress_frame(frame)

            # Écrire l'image compressée dans l'objet d'écriture vidéo
            out_vid.write(compressed_frame)

        else:
            break

    # Libérer les objets de capture et d'écriture vidéo
    vid.release()
    out_vid.release()
