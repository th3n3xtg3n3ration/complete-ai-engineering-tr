"""Python temelleri için test edilebilir kişisel bütçe hesaplayıcı."""

from __future__ import annotations


def parse_non_negative_number(raw_value: str, field_name: str) -> float:
    """Metni sıfır veya pozitif bir sayıya dönüştürür."""
    try:
        value = float(raw_value.strip().replace(",", "."))
    except ValueError as exc:
        raise ValueError(f"{field_name} geçerli bir sayı olmalıdır.") from exc
    if value < 0:
        raise ValueError(f"{field_name} negatif olamaz.")
    return value


def calculate_balance(income: float, expenses: float) -> float:
    """Gelirden gideri çıkarır."""
    return income - expenses


def calculate_savings_rate(income: float, expenses: float) -> float:
    """Tasarruf oranını yüzde olarak döndürür."""
    if income == 0:
        return 0.0
    return calculate_balance(income, expenses) / income * 100


def classify_budget(balance: float) -> str:
    """Bütçe sonucunu kategoriye ayırır."""
    if balance > 0:
        return "fazla"
    if balance < 0:
        return "açık"
    return "dengeli"


def build_summary(income: float, expenses: float) -> str:
    """Kullanıcıya gösterilecek özeti üretir."""
    balance = calculate_balance(income, expenses)
    savings_rate = calculate_savings_rate(income, expenses)
    return (
        f"Gelir: {income:,.2f} TL\n"
        f"Gider: {expenses:,.2f} TL\n"
        f"Bakiye: {balance:,.2f} TL\n"
        f"Tasarruf oranı: %{savings_rate:.1f}\n"
        f"Durum: {classify_budget(balance)}"
    )


def main() -> None:
    print("Kişisel Bütçe Hesaplayıcı")
    try:
        income = parse_non_negative_number(input("Aylık gelir (TL): "), "Gelir")
        expenses = parse_non_negative_number(input("Aylık gider (TL): "), "Gider")
    except ValueError as error:
        print(f"Hata: {error}")
        return
    print("\n" + build_summary(income, expenses))


if __name__ == "__main__":
    main()
