from os import getenv

if getenv("ENVIRONMENT") == "testing":
    from users.UserT import UserT

else:
    from bot_engine.users.UserT import UserT


access_levels = {
    "user": "student",
    "admin": "admin",
}


ADMINS: UserT = [
    {
        "real_name": "Дамир",
        "user_id": 331697498,
        "chat_id": 331697498,
        "access_level": access_levels["admin"], 
    },
    {
        "real_name": "Дамир (2)",
        "user_id": 7301044653,
        "chat_id": 7301044653,
        "access_level": access_levels["admin"],
    },
]

USERS: UserT = [
    {
        "real_name": "Кирилл",
        "last_name": "Кипчарский",
        "user_id": 782692408,
        "chat_id": 782692408,
        "payment_amount": 0,
        "max_lessons": 4,
        "access_level": access_levels["user"],
    },
    {
        "real_name": "Ярослав",
        "last_name": "Горбань",
        "user_id": 549683719,
        "chat_id": 549683719,
        "payment_amount": 195,
        "max_lessons": 8,
        "access_level": access_levels["user"],
    },
    {
        "real_name": "Ира",
        "last_name": "Гыра",
        "user_id": 1898742332,
        "chat_id": 1898742332,
        "payment_amount": 70,
        "max_lessons": 4,
        "access_level": access_levels["user"],
    },
    {
        "real_name": "Даня",
        "last_name": "Оврашко",
        "user_id": 1402095363,
        "chat_id": 1402095363,
        "payment_amount": 30,
        "max_lessons": 4,
        "access_level": access_levels["user"],
    },
    {
        "real_name": "Артём",
        "last_name": "Лысюк",
        "user_id": 5558192771,
        "chat_id": 5558192771,
        "payment_amount": 70,
        "max_lessons": 4,
        "access_level": access_levels["user"],
    },
    {
        "real_name": "Максим",
        "last_name": "Седюк",
        "user_id": 916570935,
        "chat_id": 916570935,
        "payment_amount": 70,
        "max_lessons": 4,
        "access_level": access_levels["user"],
    },
    {
        "real_name": "Назар",
        "last_name": "Сулима",
        "user_id": 736696668,
        "chat_id": 736696668,
        "payment_amount": 70,
        "max_lessons": 4,
        "access_level": access_levels["user"],
    },
    {
        "real_name": "Дима",
        "last_name": "Ляшенко",
        "user_id": 1356631201,
        "chat_id": 1356631201,
        "payment_amount": 70,
        "max_lessons": 4,
        "access_level": access_levels["user"],
    },
    {
        "real_name": "Илья",
        "last_name": "Слонь",
        "user_id": 1322753193,
        "chat_id": 1322753193,
        "payment_amount": 1700,
        "max_lessons": 4,
        "access_level": access_levels["user"],
    },
    {
        "real_name": "Андрей",
        "last_name": "Сидаш",
        "user_id": 837214225,
        "chat_id": 837214225,
        "payment_amount": 85,
        "max_lessons": 4,
        "access_level": access_levels["user"],
    },
    {
        "real_name": "Олег",
        "last_name": "Голованенко",
        "user_id": 782694924,
        "chat_id": 782694924,
        "payment_amount": 70,
        "max_lessons": 4,
        "access_level": access_levels["user"],
    },
]

INITIAL_USERS: list[UserT] = ADMINS + USERS