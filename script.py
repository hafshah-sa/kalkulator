from pyscript import document
from pyscript.ffi import create_proxy
from js import window, navigator
import re

display = document.getElementById("display")
history = document.getElementById("history")
copy_button = document.getElementById("copy-btn")

OPERATORS = {"+", "-", "*", "/", "%"}
ERROR_MESSAGES = ["Error", "Cannot divide by zero"]
MAX_DIGITS = 16

just_calculated = False

def get_last_number(current):
    """Mengambil angka terakhir setelah operator."""
    return re.split(r"[+\-*/%]", current)[-1] if current else ""

def refresh_display():
    resize_display()
    scroll_display()

def handle_operator(current, value):
    """Menangani input operator."""

    if not current:
        display.value = "0" + value
        refresh_display()
        return True

    if current[-1] in OPERATORS:
        display.value = current[:-1] + value
        refresh_display()
        return True

    return False

def handle_decimal(current, last_number):
    """Menangani input titik desimal."""

    if not current:
        display.value = "0."
        refresh_display()
        return True

    if current[-1] in OPERATORS:
        display.value += "0."
        refresh_display()
        return True

    if "." in last_number:
        return True

    return False

def handle_digit(current, last_number, value):
    """Menangani input angka."""

    digit_count = sum(c.isdigit() for c in last_number)

    if digit_count >= MAX_DIGITS:
        return True

    # Hindari leading zero
    if current == "0":
        display.value = value
        refresh_display()
        return True

    if last_number == "0":

        last_operator = max(
            current.rfind(op)
            for op in OPERATORS
        )

        display.value = current[:last_operator + 1] + value
        refresh_display()
        return True

    return False

def append(value):
    global just_calculated

    # Setelah hasil "="
    if just_calculated:
        if value.isdigit() or value == ".":
            display.value = ""
        just_calculated = False

    # Reset setelah error
    if display.value in ERROR_MESSAGES:
        display.value = ""

    current = display.value
    last_number = get_last_number(current)

    # Operator
    if value in OPERATORS:
        if handle_operator(current, value):
            return

    # Decimal
    elif value == ".":
        if handle_decimal(current, last_number):
            return

    # Digit
    elif value.isdigit():
        if handle_digit(current, last_number, value):
            return

    display.value += str(value)
    refresh_display()

def clear_display():
    global just_calculated

    display.value = "0"
    refresh_display()
    just_calculated = False

def delete_last():
    global just_calculated
    # User sudah mulai mengedit hasil
    just_calculated = False
    
    if display.value in ERROR_MESSAGES:
        display.value = "0"
        refresh_display()
        return

    if display.value:
        display.value = display.value[:-1]

    if not display.value:
        display.value = "0"

    refresh_display()

def calculate():
    global just_calculated
    expression = display.value.strip()

    # Jika kosong
    if not expression:
        return

    # Jika karakter terakhir adalah operator
    if expression[-1] in OPERATORS:
        return

    update_history(
        format_history(expression) + " ="
    )

    eval_expression = expression.replace("%", "/100")

    try:
        result = float(f"{eval(eval_expression):.12g}")

        if result.is_integer():
            result = int(result)

        display.value = str(result)
        refresh_display()
        just_calculated = True

    except ZeroDivisionError:
        display.value = "Cannot divide by zero"
        refresh_display()

    except Exception:
        display.value = "Error"
        refresh_display()

def copy_result():
    text = display.value.strip()

    if not text:
        return

    if text in ERROR_MESSAGES:
        return

    navigator.clipboard.writeText(text)

    copy_button.innerText = "✓"

    window.setTimeout(
        create_proxy(
            lambda: setattr(copy_button,"innerText","📋")
        ),
        1000
    )

def handle_key(event):

    key = event.key
    if key.isdigit():
        append(key)
        return

    if key in OPERATORS:
        append(key)
        return

    if key == ".":
        append(".")
        return

    if key == "Enter":
        event.preventDefault()
        calculate()
        return

    if key == "Backspace":
        event.preventDefault()
        delete_last()
        return

    if key == "Delete":
        event.preventDefault()
        clear_display()
        return

    if key == "Escape":
        event.preventDefault()
        clear_display()

def resize_display():
    length = sum(
        c.isdigit()
        for c in display.value
    )

    if length <= 10:
        size = "42px"

    elif length <= 13:
        size = "38px"

    elif length <= 16:
        size = "34px"

    elif length <= 19:
        size = "30px"

    else:
        size = "26px"

    display.style.fontSize = size

def scroll_display():
    display.scrollLeft = display.scrollWidth

def update_history(expression):
    history.innerText = expression

def format_history(expression):

    return (
        expression
        .replace("*", " × ")
        .replace("/", " ÷ ")
        .replace("+", " + ")
        .replace("-", " − ")
        .replace("%", " % ")
    )

# ---------- expose ke JavaScript ----------
window.append = create_proxy(append)
window.clear_display = create_proxy(clear_display)
window.delete_last = create_proxy(delete_last)
window.calculate = create_proxy(calculate)
window.copy_result = create_proxy(copy_result)
handle_key_proxy = create_proxy(handle_key)
document.addEventListener(
    "keydown",
    handle_key_proxy
)
refresh_display()