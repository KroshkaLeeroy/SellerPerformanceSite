import uuid

import yookassa


#  Ключи для api уже заданы в config\__init__.py


def pay(amount: float, currency: str = "RUB", user_id: str = "не указано", desc_details: str = "") -> str:
    """ Метод принимает основную информацию о платеже и возвращает URL подтверждения
    Отправлять запрос на зачисление средств на счёт не нужно, т.к. указан параметр 'capture' """
    idempotence_key = uuid.uuid4()
    payment = yookassa.Payment.create(
        {
            "amount": {
                "value": f"{amount:.2f}",
                "currency": currency,  # трёхсимвольное обозначение валюты, например 'RUB'
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://mirasell.ru/payment",
            },
            "capture": True,
            "description": f"Оплата для id:{user_id} на сумму {amount} {currency}\n"
                           f"Дополнительная информация: {desc_details}"
        }, idempotence_key
    )
    return payment.confirmation.confirmation_url


def pay_by_autopay():
    return False
