import uuid
from logging import error, warning, info

import yookassa

from application.payment.subscriptions import update_user_subscription


class PData:
    """
    Class representing object with payment data.
    Objects of that class is expected to be passed as an argument when Payment class instance is being initialized
    """

    def __init__(self):
        self._data = {
            "amount": {
                "value": "0.00",
                "currency": "RUB"
            },
            "payment_method_data": {
                "type": "None"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "None"
            },
            "description": "Пустой платёж"
        }

    def __init__(self, data: dict):
        try:
            self._data = {
                "amount": {
                    "value": data["amount"]["value"].format(".2f"),
                    "currency": data["amount"]["currency"]
                },
                "payment_method_data": {
                    "type": data["payment_method_data"]["type"]
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": data["payment_method_data"]["return_url"]
                },
                "description": data["description"]
            }
        except KeyError:
            error("Data dict passed to Payment object was invalid. Information was set to default.")
            self.__init__()

    def __init__(self, value: float, currency: str = "RUB", payment_method: str = "bank_card",
                 confirm_type: str = "redirect", return_url: str = "https://mirasell.ru/", description: str = ""):
        if value <= 0:
            super().__init__()
            return
        self._data = {
            "amount": {
                "value": format(value, ".2f"),
                "currency": currency
            },
            "payment_method_data": {
                "type": payment_method
            },
            "confirmation": {
                "type": confirm_type,
                "return_url": return_url
            },
            "description": description
        }

    def set_value(self, value: float, currency: str = "RUB"):
        self._data["amount"]["value"] = format(value, ".2f")
        self._data["amount"]["currency"] = currency

    def set_description(self, desc: str = ""):
        self._data["description"] = desc

    def get_data(self):
        return self._data


class Payment:
    """
    Class representing payment.
    Accepts payment data and allows to manipulate payment process
    """

    def __init__(self):
        self.__active_payment = yookassa.Payment
        self.endpoint = "https://api.yookassa.ru/v3/"
        self.__data = None
        self.__idempotence_key = str(uuid.uuid4())
        warning(
            "You didn't put PData object into Payment class instance! Initialize it or most of its functional won't "
            "work properly.")

    def __init__(self, data: PData):
        self.__active_payment = yookassa.Payment
        self.endpoint = "https://api.yookassa.ru/v3/"
        self.__idempotence_key = str(uuid.uuid4())
        self.__data = data
        self.validate_data()

    def validate_data(self):
        # TODO: написать валидацию в соответствии с API.
        return True

    def set_data(self, data: PData):
        self.__data = data
        self.validate_data()

    def pay(self) -> str | None:
        """Creates a payment object and returns a confirmation url. You should redirect user to it."""

        if self.__data is None:
            error("You are trying to make a payment without giving an information about it. Try to set PData object!")
            return None
        payment = yookassa.Payment.create(self.__data, self.__idempotence_key)
        self.__active_payment = payment
        return self.__active_payment.confirmation.confirmation_url

    def accept_payment(self):
        if self.__active_payment.status == "succeeded":
            info(f"Payment with id {self.__active_payment.id} succeeded. Updating user's subscription...")

        elif (self.__active_payment.status == "pending") or (self.__active_payment.status == "waiting_for_capture"):
            warning("Payment is still in process. Did you call recieve_responce method before confirmation?")
        else:
            info(f"Payment with id {self.__active_payment.id} cancelled.")

    def list(self) -> list[yookassa.Payment]:
        return self.__active_payment.list(self)

    def find_one(self, id0):
        return self.__active_payment.find_one(id0)


def check_payments():
    result = list()
    res = yookassa.Payment().list()["items"]
    for payment in res:
        if payment['status'] == "waiting_for_capture" and payment['paid'] == True:
            result.append(payment['id'])
            id0 = payment['id']
            idempotence_key = str(uuid.uuid4())
            response = yookassa.Payment.capture(
                id0,
                {
                    "amount": payment['amount']
                },
                idempotence_key
            )
    return result


def after_payment():
    pays = check_payments()
    for id0 in pays:
        payment = Payment(PData(0)).find_one(id0)
        if payment["status"] == "succeeded" and payment["paid"] == True:
            data = payment.description.replace('[Пользователь ', '').replace(']: Покупка плана \'', ' ').replace(
                '\' на', '') \
                .replace(' магазинов и', '').replace('месяцев. Автопродление ', '').replace('.', '').split(' ')
            update_user_subscription(int(data[0]), True, data[1], int(data[2]), int(data[3]), data[4])
