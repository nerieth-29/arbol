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
    return (len(y_izq) / total) * mse(y_izq) + (len(y_der) / total) * mse(y_der)

def mejor_corte(x, y):
    mejores = {"mse": float("inf")}
    for i in range(1, len(x)):
        corte = (x[i - 1] + x[i]) / 2
        y_izq = [y[j] for j in range(len(x)) if x[j] <= corte]
        y_der = [y[j] for j in range(len(x)) if x[j] > corte]
        mse_p = mse_ponderado(y_izq, y_der)
        if mse_p < mejores["mse"]:
            mejores = {
                "corte": corte,
                "mse": round(mse_p, 4),
                "izq": [x[j] for j in range(len(x)) if x[j] <= corte],
                "der": [x[j] for j in range(len(x)) if x[j] > corte],
                "y_izq": y_izq,
                "y_der": y_der,
            }
    return mejores

def construir_arbol(x, y, contador):
    if len(set(y)) == 1 or not contador.permitir_corte():
        return NodoDecision(prediccion=round(sum(y) / len(y), 2))

    division = mejor_corte(x, y)
    if not division["izq"] or not division["der"]:
        return NodoDecision(prediccion=round(sum(y) / len(y), 2))

    izquierda = construir_arbol(division["izq"], division["y_izq"], contador)
    derecha = construir_arbol(division["der"], division["y_der"], contador)

    return NodoDecision(
        corte=division["corte"],
        izquierda=izquierda,
        derecha=derecha,
        mse=division["mse"]
    )

# Para dibujar el árbol con matplotlib
def dibujar_arbol(nodo, x=0.5, y=1.0, dx=0.2, dy=0.15, ax=None, nivel=0):
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
        dibujar_arbol(nodo.izquierda, x - dx, y - dy, dx * 0.6, dy, ax, nivel + 1)

    if nodo.derecha:
        ax.plot([x, x + dx], [y - 0.02, y - dy + 0.02], color='black')
        dibujar_arbol(nodo.derecha, x + dx, y - dy, dx * 0.6, dy, ax, nivel + 1)

# === DATOS ===
x = [10, 20, 30, 70, 75, 80, 90, 110, 115, 125, 130, 180, 190, 200]
y = [40, 30, 45, 5, 10, 20, 10, 70, 60, 80, 70, 30, 20, 30]

# === CONSTRUIR ÁRBOL DE DECISIÓN ===
contador = ContadorNodos(max_nodos=3)
arbol = construir_arbol(x, y, contador)
print(NodoDecision)

# === DIBUJAR ÁRBOL EN IMAGEN ===
dibujar_arbol(arbol)
