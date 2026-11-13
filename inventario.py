import threading
import sys

inventario = 1
lock = threading.Lock()

def caja_sin_lock(nombre, barrera, resultados):
    global inventario
    saldo = inventario
    venta = saldo > 0    
    barrera.wait()

    if venta:
        inventario -= 1
        resultados.append(f"venta aprobada por {nombre}")
    else:
        resultados.append(f"venta rechazada por {nombre}")

def caja_con_lock(nombre, resultados):
    global inventario
    with lock:
        if inventario > 0:
            inventario -= 1
            resultados.append(f"venta aprobada por {nombre}")
        else:
            resultados.append(f"venta rechazada por {nombre}")

if __name__ == "__main__":

    print("1.version sin lock")
    inventario = 1
    resultados1 = []
    barrera = threading.Barrier(2)

    h1 = threading.Thread(target=caja_sin_lock, args=("Caja 1", barrera, resultados1))
    h2 = threading.Thread(target=caja_sin_lock, args=("Caja 2", barrera, resultados1))
    h1.start()
    h2.start()
    h1.join()
    h2.join()
    
    print(f"resultados: {resultados1}")
    print(f"inventario final: {inventario}")
    print("error:Se vendieron mas unidades no disponibles\n")

    print("2.version con lock")
    inventario = 1
    resultados2 = []
    
    h3 = threading.Thread(target=caja_con_lock, args=("Caja 1", resultados2))
    h4 = threading.Thread(target=caja_con_lock, args=("Caja 2", resultados2))
    h3.start()
    h4.start()
    h3.join()
    h4.join()
    
    print(f"resultados: {resultados2}")
    print(f"inventario final: {inventario}\n")

    print("3.verificacion")
    ventas = sum(1 for r in resultados2 if "aprobada" in r)
    
    assert ventas == 1, "error en la cantidad de ventas"
    assert inventario == 0, "error en el inventario final"
    
    print("Verificacion correcta: una venta aprobada y el inventario quedo en cero.")
    print("""Explicacion: la verificacion y el descuento deben estar dentro del lock o si no ambos hilos
leerian que hay [1] unidad disponible y decidirian vender. Esto causaria una inconsistencia,
ya que se registrarian 2 ventas pero el inventario quedaria en [-1], lo cual es imposible""")