import heapq
from collections import defaultdict, Counter

# Nodo del Árbol de Huffman
class NodoHuffman:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    # Método para comparar nodos (para la cola de prioridad)
    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

# Función para generar el Árbol de Huffman
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

# Función para generar los códigos de Huffman
def generar_codigos(nodo, codigo_actual="", codigos={}):
    if nodo is None:
        return
    if nodo.caracter is not None:
        codigos[nodo.caracter] = codigo_actual
    generar_codigos(nodo.izquierda, codigo_actual + "0", codigos)
    generar_codigos(nodo.derecha, codigo_actual + "1", codigos)
    return codigos

# Función para codificar un mensaje
def codificar_mensaje(mensaje, codigos):
    return ''.join(codigos[caracter] for caracter in mensaje)

# Función para decodificar un mensaje
def decodificar_mensaje(codificado, raiz):
    resultado = []
    nodo_actual = raiz
    for bit in codificado:
        nodo_actual = nodo_actual.izquierda if bit == '0' else nodo_actual.derecha
        if nodo_actual.caracter is not None:
            resultado.append(nodo_actual.caracter)
            nodo_actual = raiz
    return ''.join(resultado)

# Mensaje de entrada
mensaje = "este es un mensaje de prueba para el Árbol de Huffman"

# Calcular frecuencias
frecuencias = Counter(mensaje)

# Construir el Árbol de Huffman
arbol_huffman = construir_arbol_huffman(frecuencias)

# Generar los códigos de Huffman
codigos = generar_codigos(arbol_huffman)

# Codificar el mensaje
mensaje_codificado = codificar_mensaje(mensaje, codigos)
print(f"Mensaje codificado: {mensaje_codificado}")

# Decodificar el mensaje
mensaje_decodificado = decodificar_mensaje(mensaje_codificado, arbol_huffman)
print(f"Mensaje decodificado: {mensaje_decodificado}")
