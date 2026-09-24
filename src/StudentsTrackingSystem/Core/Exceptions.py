class BllError(Exception):
    """Базовое исключение BLL. Ловить в общем обработчике."""
    pass


class NotFoundError(BllError):
    """Запись не найдена."""
    pass


class ConflictError(BllError):
    """Дубликат / занятое значение."""
    pass


class BusinessValidationError(BllError):
    """Ошибка бизнес-валидации (не Pydantic)."""
    pass


class PermissionDeniedError(BllError):
    """Нет прав на действие."""
    pass