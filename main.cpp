#include <iostream>
#include <queue>
#include <unordered_map>
#include <string>

using namespace std;

// Nodo del Árbol de Huffman
struct NodoHuffman {
    char caracter;
    int frecuencia;
    NodoHuffman* izquierda;
    NodoHuffman* derecha;

    NodoHuffman(char c, int f) : caracter(c), frecuencia(f), izquierda(nullptr), derecha(nullptr) {}
};

// Comparador para la cola de prioridad
struct comparar {
    bool operator()(NodoHuffman* izquierda, NodoHuffman* derecha) {
        return izquierda->frecuencia > derecha->frecuencia;
    }
};

// Función para calcular la frecuencia de cada carácter en el mensaje
void calcularFrecuencia(const string& mensaje, unordered_map<char, int>& frecuencia) {
    for (char c : mensaje) {
        frecuencia[c]++;
    }
}

// Función para construir el Árbol de Huffman
NodoHuffman* construirArbolHuffman(unordered_map<char, int>& frecuencia) {
    priority_queue<NodoHuffman*, vector<NodoHuffman*>, comparar> pq;

    // Insertar los caracteres y sus frecuencias en la cola de prioridad
    for (auto& par : frecuencia) {
        pq.push(new NodoHuffman(par.first, par.second));
    }

    // Construir el Árbol de Huffman
    while (pq.size() > 1) {
        NodoHuffman* izquierda = pq.top();
        pq.pop();
        NodoHuffman* derecha = pq.top();
        pq.pop();

        NodoHuffman* combinado = new NodoHuffman('\0', izquierda->frecuencia + derecha->frecuencia);
        combinado->izquierda = izquierda;
        combinado->derecha = derecha;

        pq.push(combinado);
    }

    return pq.top();
}

// Función para generar los códigos de Huffman
void generarCodigos(NodoHuffman* raiz, string codigo, unordered_map<char, string>& codigos) {
    if (!raiz) return;

    if (raiz->caracter != '\0') {
        codigos[raiz->caracter] = codigo;
    }

    generarCodigos(raiz->izquierda, codigo + "0", codigos);
    generarCodigos(raiz->derecha, codigo + "1", codigos);
}

// Función para codificar el mensaje
string codificarMensaje(const string& mensaje, unordered_map<char, string>& codigos) {
    string mensajeCodificado;
    for (char c : mensaje) {
        mensajeCodificado += codigos[c];
    }
    return mensajeCodificado;
}

// Función para decodificar el mensaje
string decodificarMensaje(const string& mensajeCodificado, NodoHuffman* raiz) {
    string mensajeDecodificado;
    NodoHuffman* nodoActual = raiz;
    for (char bit : mensajeCodificado) {
        if (bit == '0') {
            nodoActual = nodoActual->izquierda;
        } else {
            nodoActual = nodoActual->derecha;
        }

        if (!nodoActual->izquierda && !nodoActual->derecha) {
            mensajeDecodificado += nodoActual->caracter;
            nodoActual = raiz;
        }
    }
    return mensajeDecodificado;
}

// Función principal
int main() {
    string mensaje;
    cout << "Ingrese el mensaje: ";
    getline(cin, mensaje);

    unordered_map<char, int> frecuencia;
    calcularFrecuencia(mensaje, frecuencia);

    NodoHuffman* raiz = construirArbolHuffman(frecuencia);

    unordered_map<char, string> codigos;
    generarCodigos(raiz, "", codigos);

    string mensajeCodificado = codificarMensaje(mensaje, codigos);
    cout << "Mensaje codificado: " << mensajeCodificado << endl;

    string mensajeDecodificado = decodificarMensaje(mensajeCodificado, raiz);
    cout << "Mensaje decodificado: " << mensajeDecodificado << endl;

    return 0;
}
