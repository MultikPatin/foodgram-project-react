from django.core.validators import RegexValidator


class UsernameValidator(RegexValidator):
    regex = r"^[\w.@+-]+\Z"
    message = _(
        "Имя пользователя может содержать только буквы, "
        "цифры и символы @/./+/-/_."
    )
    flags = 0
