from decimal import Decimal

class CurrencyService:
    @staticmethod
    def convert_to_base(amount: Decimal, rate: float) -> Decimal:
        """Пересчет суммы в базовую валюту по заданному курсу."""
        return amount * Decimal(str(rate))

    @staticmethod
    def convert_between(amount: Decimal, from_rate: float, to_rate: float) -> Decimal:
        """Пересчет между двумя валютами через базовую."""
        base_val = amount * Decimal(str(from_rate))
        return base_val / Decimal(str(to_rate))