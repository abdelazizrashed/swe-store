from .firestore_db import bucket


class Utilities:

    @staticmethod
    def upload_img(img_path: str, db_path: str = None) -> str:
        if db_path is None:
            blob = bucket.blob(img_path.split('/')[-1])
        else:
            blob = bucket.blob(f"{db_path}/{img_path.split('/')[-1]}")
        blob.upload_from_filename(img_path)
        blob.make_public()
        return blob.public_url

    @staticmethod
    def upload_img_from_file(file, db_path: str = None) -> str:
        if db_path is None:
            blob = bucket.blob(file.filename)
        else:
            blob = bucket.blob(f"{db_path}/{file.filename}")
        blob.upload_from_file(file)
        blob.make_public()
        return blob.public_url

    @staticmethod
    def response(message: str,  status: int = 200,  success: bool = True,  data: dict = None):
        if success:
            return {
                "success": success,
                "message": message,
                "data": data
            }, status
        return {
            "success": success,
            "message": message,
        }, status
