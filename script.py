from pyscript import document
from pyscript.ffi import create_proxy
from js import window
import re

display = document.getElementById("display")

OPERATORS = "+-*/%"

def append(value):
    current = display.value

    # Operator pertama
    if value in OPERATORS:
        if current == "":
            display.value = "0" + value
            return

    # Jika karakter terakhir operator,
        # ganti operator sebelumnya
        if current[-1] in OPERATORS:
            display.value = current[:-1] + value
            return

    # Handle decimal point
    if value == ".":

        # Jika display kosong
        if current == "":
            display.value = "0."
            return

        # Jika karakter terakhir operator
        if current[-1] in OPERATORS:
            display.value += "0."
            return

        # Ambil angka terakhir setelah operator
        last_number = re.split(r"[+\-*/%]", current)[-1]

        # Jika angka terakhir sudah punya titik
        if "." in last_number:
            return

    display.value += str(value)


def clear_display():
    display.value = ""


def delete_last():
    display.value = display.value[:-1]


def calculate():
    expression = display.value.strip()

    if expression == "":
        return

    try:
        expression = expression.replace("%", "/100")
        result = eval(expression)

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        display.value = str(result)

    except ZeroDivisionError:
        display.value = "Error: ÷0"

    except Exception:
        display.value = "Error"


# ---------- expose ke JavaScript ----------

window.append = create_proxy(append)
window.clear_display = create_proxy(clear_display)
window.delete_last = create_proxy(delete_last)
window.calculate = create_proxy(calculate)