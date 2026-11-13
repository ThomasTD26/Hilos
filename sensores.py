import time
import threading
import statistics
from time import perf_counter

sensores = [("a", 1.0), ("b", 2.0), ("c", 1.5)]

def leer(nombre, duracion, inicio, resultados):
    time.sleep(duracion)
    resultados[nombre] = perf_counter() - inicio

def secuencial():
    resultados = {}
    inicio = perf_counter()
    for nombre, duracion in sensores:
        leer(nombre, duracion, inicio, resultados)
    total = perf_counter() - inicio
    return total, resultados

def hilos_join_global():
    resultados = {}
    hilos = []
    inicio = perf_counter()
    
    for nombre, duracion in sensores:
        h = threading.Thread(target=leer, args=(nombre, duracion, inicio, resultados))
        hilos.append(h)
        h.start()
        
    for h in hilos:
        h.join()
        
    total = perf_counter() - inicio
    return total, resultados

def hilos_join_individual():
    resultados = {}
    hilos = []
    inicio = perf_counter()
    
    for nombre, duracion in sensores:
        h = threading.Thread(target=leer, args=(nombre, duracion, inicio, resultados))
        hilos.append(h)
        h.start()
        
    for i, h in enumerate(hilos):
        h.join()
        resultados[f"join_{sensores[i][0]}"] = perf_counter() - inicio
        
    total = perf_counter() - inicio
    return total, resultados

def probar(nombre, funcion):
    tiempos = []
    print(f"modo: {nombre}")
    for i in range(3):
        total, res = funcion()
        tiempos.append(total)
        marcas = {k: round(v, 2) for k, v in res.items()}
        print(f"  {i+1}. total: {total:.4f}s | marcas: {marcas}")
    print(f"  mediana: {statistics.median(tiempos):.4f}s\n")

if __name__ == "__main__":
    probar("secuencial", secuencial)
    probar("hilos join global", hilos_join_global)
    probar("hilos join individual", hilos_join_individual)