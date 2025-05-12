import matplotlib.pyplot as plt

class NodoDecision:
    def __init__(self, corte=None, izquierda=None, derecha=None, prediccion=None, mse=None):
        self.corte = corte
        self.izquierda = izquierda
        self.derecha = derecha
        self.prediccion = prediccion
        self.mse = mse

class ContadorNodos:
    def __init__(self, max_nodos):
        self.max_nodos = max_nodos
        self.contador = 0

    def permitir_corte(self):
        if self.contador < self.max_nodos:
            self.contador += 1
            return True
        return False

def mse(lista):
    if not lista:
        return 0
    media = sum(lista) / len(lista)
    return sum((y - media) ** 2 for y in lista) / len(lista)

def mse_ponderado(y_izq, y_der):
    total = len(y_izq) + len(y_der)
    if total == 0:
        return 0
    return (len(y_izq) / total) * mse(y_izq) + (len(y_der) / total) * mse(y_der)

# Cortes deseados en orden
cortes_deseados = [100, 50, 72, 115, 155]

def construir_arbol_manual(x, y, contador):
    if len(set(y)) == 1 or not contador.permitir_corte() or not cortes_deseados:
        return NodoDecision(prediccion=round(sum(y) / len(y), 2))

    corte = cortes_deseados.pop(0)
    x_izq = [x[i] for i in range(len(x)) if x[i] <= corte]
    y_izq = [y[i] for i in range(len(x)) if x[i] <= corte]
    x_der = [x[i] for i in range(len(x)) if x[i] > corte]
    y_der = [y[i] for i in range(len(x)) if x[i] > corte]

    if not y_izq or not y_der:
        return NodoDecision(prediccion=round(sum(y) / len(y), 2))

    izquierda = construir_arbol_manual(x_izq, y_izq, contador)
    derecha = construir_arbol_manual(x_der, y_der, contador)

    return NodoDecision(corte=corte, izquierda=izquierda, derecha=derecha, mse=round(mse_ponderado(y_izq, y_der), 4))

def imprimir_arbol(nodo, nivel=0, lado="Raíz"):
    sangria = "   " * nivel
    if nodo.prediccion is not None:
        print(f"{sangria}|-{lado}-> Hoja: predicción = {nodo.prediccion}")
    else:
        print(f"{sangria}|-{lado}-> Nodo (x <= {nodo.corte}) MSE: {nodo.mse}")
        imprimir_arbol(nodo.izquierda, nivel + 1, "Izq")
        imprimir_arbol(nodo.derecha, nivel + 1, "Der")

def dibujar_arbol(nodo, x=0.5, y=1.0, dx=0.2, dy=0.15, ax=None):
    if nodo is None:
        return
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_axis_off()
        dibujar_arbol(nodo, x, y, dx, dy, ax)
        plt.show()
        return

    if nodo.prediccion is not None:
        texto = f"Predicción:\n{nodo.prediccion}"
    else:
        texto = f"x <= {nodo.corte}\nMSE={nodo.mse}"

    ax.text(x, y, texto, ha='center', va='center',
            bbox=dict(boxstyle="round", fc="lightblue", ec="black"))

    if nodo.izquierda:
        ax.plot([x, x - dx], [y - 0.02, y - dy + 0.02], color='black')
        dibujar_arbol(nodo.izquierda, x - dx, y - dy, dx * 0.6, dy, ax)

    if nodo.derecha:
        ax.plot([x, x + dx], [y - 0.02, y - dy + 0.02], color='black')
        dibujar_arbol(nodo.derecha, x + dx, y - dy, dx * 0.6, dy, ax)

# === DATOS ===
x = [10, 20, 30, 70, 75, 80, 90, 110, 115, 125, 130, 180, 190, 200]
y = [40, 30, 45, 5, 10, 20, 10, 70, 60, 80, 70, 30, 20, 30]

# === CONSTRUIR ÁRBOL CON CORTES MANUALES ===
contador = ContadorNodos(max_nodos=5)
arbol = construir_arbol_manual(x, y, contador)

# === MOSTRAR EN CONSOLA ===
imprimir_arbol(arbol)

# === DIBUJAR CON MATPLOTLIB ===
dibujar_arbol(arbol)
