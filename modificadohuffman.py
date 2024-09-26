import heapq
from collections import Counter

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

mensaje_prueba_1 = "Hola Mundo! ¿Cómo estás?"
mensaje_prueba_2 = "Prueba de HUFFMAN: 100% eficaz @2024"

frecuencias_prueba_1 = Counter(mensaje_prueba_1)
arbol_huffman_1 = construir_arbol_huffman(frecuencias_prueba_1)
codigos_1 = generar_codigos(arbol_huffman_1)
mensaje_codificado_1 = codificar_mensaje(mensaje_prueba_1, codigos_1)
print(f"Mensaje codificado 1: {mensaje_codificado_1}")
mensaje_decodificado_1 = decodificar_mensaje(mensaje_codificado_1, arbol_huffman_1)
print(f"Mensaje decodificado 1: {mensaje_decodificado_1}")

frecuencias_prueba_2 = Counter(mensaje_prueba_2)
arbol_huffman_2 = construir_arbol_huffman(frecuencias_prueba_2)
codigos_2 = generar_codigos(arbol_huffman_2)
mensaje_codificado_2 = codificar_mensaje(mensaje_prueba_2, codigos_2)
print(f"Mensaje codificado 2: {mensaje_codificado_2}")
mensaje_decodificado_2 = decodificar_mensaje(mensaje_codificado_2, arbol_huffman_2)
print(f"Mensaje decodificado 2: {mensaje_decodificado_2}")
