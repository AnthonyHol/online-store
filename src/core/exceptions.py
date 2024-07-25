from fastapi import HTTPException, status


good_group_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Группа номенклатуры не найдена",
)

specification_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Характеристика номенклатуры не найдена",
)

good_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Номенклатура не найдена",
)

property_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Свойство не найдено",
)

upload_image_exception = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Ошибка при загрузке изображения в S3.",
)

encoded_image_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Ошибка при преобразовании base64 строки в изображение.",
)
