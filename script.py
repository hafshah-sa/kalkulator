from pyscript import document
from pyscript.ffi import create_proxy
from js import window
import re

display = document.getElementById("display")

OPERATORS = {"+", "-", "*", "/", "%"}
ERROR_MESSAGES = ["Error", "Cannot divide by zero"]
MAX_DIGITS = 16

def append(value):
    # Reset jika display sedang menampilkan pesan error,
    # mulai input baru
    if display.value in ERROR_MESSAGES:
        display.value = ""

    current = display.value

    # Ambil angka terakhir
    last_number = re.split(r"[+\-*/%]", current)[-1] if current else ""

    # Handle Operator 
    if value in OPERATORS:
        # Jika operator pertama
        if not current:
            display.value = "0" + value
            return

        # ganti operator sebelumnya
        if current[-1] in OPERATORS:
            display.value = current[:-1] + value
            return

    # Handle decimal point
    if value == ".":

        # Jika display kosong
        if not current:
            display.value = "0."
            return

        # Jika karakter terakhir operator
        if current[-1] in OPERATORS:
            display.value += "0."
            return

        # Jika angka terakhir sudah punya titik
        if "." in last_number:
            return

    # Hindari angka nol di depan (leading zero)
    if value.isdigit():
        # Hitung jumlah digit (titik tidak dihitung)
        digit_count = sum(c.isdigit() for c in last_number)

        # Maksimum digit per angka
        if digit_count >= MAX_DIGITS:
            return

        # Kasus: display hanya berisi "0"
        if current == "0":
            display.value = value
            return

        # Kasus: angka terakhir setelah operator adalah "0"
        if last_number == "0":

            last_operator = max(
                current.rfind(op) for op in OPERATORS
            )

            display.value = current[:last_operator + 1] + value
            return
    # Tambahkan karakter
    display.value += str(value)
    # Auto Scroll Display
    display.scrollLeft = display.scrollWidth

def clear_display():
    display.value = ""

def delete_last():
    display.value = display.value[:-1]

def calculate():
    expression = display.value.strip()

    # Jika kosong
    if expression == "":
        return

    # Jika karakter terakhir adalah operator
    if expression[-1] in OPERATORS:
        return

    try:
        expression = expression.replace("%", "/100")
        result = eval(expression)

        # Hilangkan .0
        if isinstance(result, float) and result.is_integer():
            result = int(result)

        display.value = str(result)

    except ZeroDivisionError:
        display.value = "Cannot divide by zero"

    except Exception:
        display.value = "Error"

# ---------- expose ke JavaScript ----------
window.append = create_proxy(append)
window.clear_display = create_proxy(clear_display)
window.delete_last = create_proxy(delete_last)
window.calculate = create_proxy(calculate)