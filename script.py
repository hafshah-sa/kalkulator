from pyscript import document
from pyscript.ffi import create_proxy
from js import window

display = document.getElementById("display")


def append(value):
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