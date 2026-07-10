from pyscript import document

# Mengambil elemen display
display = document.getElementById("display")

def append(value):
    """Menambahkan karakter ke display."""
    display.value += str(value)

def clear_display():
    """Menghapus seluruh isi display."""
    display.value = ""

def delete_last():
    """Menghapus satu karakter terakhir."""
    display.value = display.value[:-1]

def calculate():
    """Menghitung hasil ekspresi matematika."""
    expression = display.value.strip()
    if expression == "":
        return
    try:
        # Mengizinkan operasi dasar dan persen
        expression = expression.replace("%", "/100")
        result = eval(expression)
        # Jika hasil bilangan bulat, hilangkan .0
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        display.value = str(result)
    except ZeroDivisionError:
        display.value = "Error: ÷ 0"
    except Exception:
        display.value = "Error"
