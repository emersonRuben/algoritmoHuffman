import heapq
from collections import Counter
import tkinter as tk
from tkinter import messagebox

class NodoHuffman:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

def construir_arbol_huffman(frecuencias):
    heap = [NodoHuffman(caracter, frecuencia) for caracter, frecuencia in frecuencias.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        nodo_izq = heapq.heappop(heap)
        nodo_der = heapq.heappop(heap)
        nodo_combinado = NodoHuffman(None, nodo_izq.frecuencia + nodo_der.frecuencia)
        nodo_combinado.izquierda = nodo_izq
        nodo_combinado.derecha = nodo_der
        heapq.heappush(heap, nodo_combinado)
    
    return heap[0]

def generar_codigos(nodo, codigo_actual="", codigos={}):
    if nodo is None:
        return
    if nodo.caracter is not None:
        codigos[nodo.caracter] = codigo_actual
    generar_codigos(nodo.izquierda, codigo_actual + "0", codigos)
    generar_codigos(nodo.derecha, codigo_actual + "1", codigos)
    return codigos

def codificar_mensaje(mensaje, codigos):
    return ''.join(codigos[caracter] for caracter in mensaje)

def decodificar_mensaje(codificado, raiz):
    resultado = []
    nodo_actual = raiz
    for bit in codificado:
        nodo_actual = nodo_actual.izquierda if bit == '0' else nodo_actual.derecha
        if nodo_actual.caracter is not None:
            resultado.append(nodo_actual.caracter)
            nodo_actual = raiz
    return ''.join(resultado)

def manejar_cifrado():
    mensaje = entrada_mensaje.get()
    if not mensaje:
        messagebox.showwarning("Advertencia", "Debe ingresar un mensaje.")
        return
    
    frecuencias = Counter(mensaje)
    arbol_huffman = construir_arbol_huffman(frecuencias)
    codigos = generar_codigos(arbol_huffman)
    
    mensaje_codificado = codificar_mensaje(mensaje, codigos)
    
    resultado_label.config(text=f"Mensaje codificado: {mensaje_codificado}")
    resultado_decodificado.config(text="")

    global arbol_global, mensaje_codificado_global
    arbol_global = arbol_huffman
    mensaje_codificado_global = mensaje_codificado

def manejar_descifrado():
    if arbol_global is None or mensaje_codificado_global is None:
        messagebox.showwarning("Advertencia", "Primero debe cifrar un mensaje.")
        return
    
    mensaje_decodificado = decodificar_mensaje(mensaje_codificado_global, arbol_global)
    
    resultado_decodificado.config(text=f"Mensaje decodificado: {mensaje_decodificado}")

arbol_global = None
mensaje_codificado_global = None

# Interfaz de usuario con tkinter
ventana = tk.Tk()
ventana.title("Cifrado de Huffman")

tk.Label(ventana, text="Ingrese el mensaje:").pack(pady=5)
entrada_mensaje = tk.Entry(ventana, width=50)
entrada_mensaje.pack(pady=5)

tk.Button(ventana, text="Cifrar", command=manejar_cifrado).pack(pady=5)
tk.Button(ventana, text="Descifrar", command=manejar_descifrado).pack(pady=5)

resultado_label = tk.Label(ventana, text="")
resultado_label.pack(pady=10)

resultado_decodificado = tk.Label(ventana, text="")
resultado_decodificado.pack(pady=10)

ventana.mainloop()
