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
