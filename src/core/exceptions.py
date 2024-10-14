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

price_type_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Вид цены номенклатуры не найден",
)

upload_image_exception = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Ошибка при загрузке изображения в S3.",
)

encoded_image_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Ошибка при преобразовании base64 строки в изображение.",
)

incorrect_in_stock_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="`in_stock` не может быть меньше 0.",
)

incorrect_contact_me_form_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Должно быть заполнено хотя бы одно из полей: `phone` или `email`.",
)

contact_me_form_exception = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Не удалось отправить форму обратной связи в 1С.",
)

invalid_creds_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Неверный логин или пароль.",
)

outlets_json_decode_exception = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Ошибка декодирования полученного списка торговых точек из 1С.",
)


outlets_validate_exception = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Ошибка валидации полученного списка торговых точек из 1С.",
)

outlets_1c_error_exception = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Ошибка получения списка торговых точек из 1С.",
)
