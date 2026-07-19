
"""
==================================================
Project : حضور
File    : face_recognizer.py
Author  : Reyhane Sarabi
Purpose : Face Recognition Engine
==================================================
"""

import cv2
import numpy as np
import pickle

from insightface.app import FaceAnalysis


class FaceRecognizer:
    """
    موتور تشخیص و استخراج ویژگی چهره
    """

    def __init__(self):

        self.app = FaceAnalysis(
            name="buffalo_l"
        )

        self.app.prepare(
            ctx_id=0,
            det_size=(640, 640)
        )

    # ==================================================
    # Get Face Encoding
    # ==================================================

    def get_encoding(
        self,
        image_path
    ):

        image = cv2.imread(
            image_path
        )

        if image is None:

            print("Image not found")

            return None

        faces = self.app.get(
            image
        )

        if len(faces) == 0:

            print("No face detected")

            return None

        # انتخاب بزرگ‌ترین چهره
        face = max(
            faces,
            key=lambda x: (
                x.bbox[2] - x.bbox[0]
            ) * (
                x.bbox[3] - x.bbox[1]
            )
        )

        embedding = face.embedding

        if embedding is None:

            return None

        norm = np.linalg.norm(
            embedding
        )

        if norm == 0:

            return None

        embedding = embedding / norm

        return embedding.astype(
            np.float32
        )

    # ==================================================
    # Get Face Information
    # ==================================================

    def get_face_info(
        self,
        image_path
    ):
        """
        تشخیص چهره و برگرداندن embedding و bbox
        """

        image = cv2.imread(
            image_path
        )

        if image is None:

            print("Image not found")

            return None

        faces = self.app.get(
            image
        )

        if len(faces) == 0:

            print("No face detected")

            return None

        # بزرگ‌ترین چهره
        face = max(
            faces,
            key=lambda x: (
                x.bbox[2] - x.bbox[0]
            ) * (
                x.bbox[3] - x.bbox[1]
            )
        )

        embedding = face.embedding

        if embedding is None:

            return None

        norm = np.linalg.norm(
            embedding
        )

        if norm == 0:

            return None

        embedding = (
            embedding / norm
        ).astype(
            np.float32
        )

        bbox = face.bbox.astype(
            int
        )

        return {
            "encoding": embedding,
            "bbox": (
                int(bbox[0]),
                int(bbox[1]),
                int(bbox[2]),
                int(bbox[3])
            )
        }

    # ==================================================
    # Serialize Encoding
    # ==================================================

    def serialize_encoding(
        self,
        encoding
    ):

        if encoding is None:

            return None

        return pickle.dumps(
            encoding
        )

    # ==================================================
    # Deserialize Encoding
    # ==================================================

    def deserialize_encoding(
        self,
        data
    ):

        if data is None:

            return None

        try:

            encoding = pickle.loads(
                data
            )

            if encoding is None:

                return None

            encoding = np.asarray(
                encoding,
                dtype=np.float32
            )

            norm = np.linalg.norm(
                encoding
            )

            if norm == 0:

                return None

            return encoding / norm

        except Exception as error:

            print(
                "Encoding load error:",
                error
            )

            return None

    # ==================================================
    # Compare Faces
    # ==================================================

    def compare(
        self,
        encoding1,
        encoding2
    ):

        if (
            encoding1 is None
            or encoding2 is None
        ):

            return 0.0

        encoding1 = np.asarray(
            encoding1,
            dtype=np.float32
        )

        encoding2 = np.asarray(
            encoding2,
            dtype=np.float32
        )

        norm1 = np.linalg.norm(
            encoding1
        )

        norm2 = np.linalg.norm(
            encoding2
        )

        if norm1 == 0 or norm2 == 0:

            return 0.0

        encoding1 = (
            encoding1 / norm1
        )

        encoding2 = (
            encoding2 / norm2
        )

        similarity = np.dot(
            encoding1,
            encoding2
        )

        return float(
            similarity
        )

    # ==================================================
    # Recognize User
    # ==================================================

    def recognize(
        self,
        image_path,
        users,
        threshold=0.55
    ):

        face_info = self.get_face_info(
            image_path
        )

        if face_info is None:

            return {
                "found": False,
                "user": None,
                "score": 0.0,
                "bbox": None
            }

        current_encoding = (
            face_info["encoding"]
        )

        bbox = face_info["bbox"]

        best_user = None
        best_score = 0.0

        for user in users:

            saved_encoding = (
                self.deserialize_encoding(
                    user["face_encoding"]
                )
            )

            if saved_encoding is None:

                continue

            score = self.compare(
                current_encoding,
                saved_encoding
            )

            if score > best_score:

                best_score = score
                best_user = user

        if (
            best_user is not None
            and best_score >= threshold
        ):

            return {
                "found": True,
                "user": best_user,
                "score": best_score,
                "bbox": bbox
            }

        return {
            "found": False,
            "user": None,
            "score": best_score,
            "bbox": bbox
        }

