from pyvis.network import Network
import networkx as nx
import textwrap

# Intentar importar la base de conocimiento
try:
    from base_conocimiento import base_conocimiento
except ImportError:
    print("Error: No se encontró 'base_conocimiento.py'.")
    exit()


def obtener_modulo(id_regla):
    """Clasificación de módulos (Misma lógica)"""
    i = id_regla + 1
    if 1 <= i <= 17: return "Sistema de Enfriamiento"
    if 18 <= i <= 26: return "Sistema de Combustible"
    if 27 <= i <= 31: return "Sistema de Encendido"
    if 32 <= i <= 35: return "Check Engine / General"
    if 36 <= i <= 37: return "Mecánica Mayor"
    if 38 <= i <= 41: return "Sensores y Encendido"
    if 42 <= i <= 47: return "Sistema de Lubricación"
    if 48 <= i <= 54: return "Sistema de Frenos"
    if 55 <= i <= 61: return "Sistema Eléctrico"
    if 62 <= i <= 69: return "Suspensión y Dirección"
    if 70 <= i <= 73: return "Sistema de Escape"
    if 74 <= i <= 77: return "Transmisión"
    if 78 <= i <= 90: return "Sensores (Avanzado)"
    if 91 <= i <= 105: return "Códigos de Falla (DTC)"
    if 106 <= i <= 120: return "Aire Acondicionado"
    if 121 <= i <= 135: return "Emisiones (EGR/EVAP)"
    if 136 <= i <= 148: return "Sistema Eléctrico (Luces)"
    if 149 <= i <= 152: return "Carrocería"
    return "Otros"


def formatear_texto(texto, ancho=30):
    """Divide un texto largo en varias líneas para que quepa en la bolita"""
    return "\n".join(textwrap.wrap(texto, width=ancho))


def generar_red_estatica():
    print("1. Construyendo estructura lógica...")

    # Usamos NetworkX para calcular las posiciones matemáticas primero
    G = nx.Graph()  # Grafo auxiliar para calcular posiciones

    # Nodo Central
    G.add_node("A.D.A.M.")

    # Listas para rastrear qué hemos agregado y evitar duplicados
    datos_nodos = {}  # Guardaremos colores y etiquetas aquí

    # Configurar nodo central
    datos_nodos["A.D.A.M."] = {"color": "#ffffff", "size": 60, "label": "A.D.A.M."}

    for i, regla in enumerate(base_conocimiento):
        nombre_modulo = obtener_modulo(i)

        # --- Nodos de Módulos ---
        if nombre_modulo not in datos_nodos:
            G.add_node(nombre_modulo)
            G.add_edge("A.D.A.M.", nombre_modulo)
            datos_nodos[nombre_modulo] = {"color": "#4aa3df", "size": 40, "label": formatear_texto(nombre_modulo, 15)}

        # --- Nodos de Diagnóstico ---
        diag_full = ""
        for cons in regla['entonces']:
            diag_full = cons[1]
            break

            # ID único para el diagnóstico
        diag_id = f"diag_{i}"

        # Aquí usamos el TEXTO COMPLETO formateado con saltos de línea
        label_diag = f"R{i + 1}: " + formatear_texto(diag_full, ancho=40)

        G.add_node(diag_id)
        G.add_edge(nombre_modulo, diag_id)
        datos_nodos[diag_id] = {"color": "#e74c3c", "size": 25, "label": label_diag, "shape": "box"}

        # --- Nodos de Síntomas ---
        for item in regla['si']:
            if isinstance(item, tuple):
                var, val = item
                if val in ["no", "no_se", "normal", "ok"]: continue

                sintoma_id = f"{var}: {val}"

                if sintoma_id not in datos_nodos:
                    G.add_node(sintoma_id)
                    datos_nodos[sintoma_id] = {"color": "#2ecc71", "size": 15, "label": formatear_texto(sintoma_id, 20)}

                G.add_edge(sintoma_id, diag_id)

    print(f"2. Calculando posiciones para {G.number_of_nodes()} nodos (esto congela el movimiento)...")

    # Algoritmo Kamada-Kawai: Es excelente para separar grupos y que no se encimen
    # scale=2000 separa mucho los puntos para que quepa el texto
    pos = nx.kamada_kawai_layout(G, scale=2500)

    print("3. Generando visualización interactiva...")

    # Crear red de Pyvis
    net = Network(height="90vh", width="100%", bgcolor="#222222", font_color="white")

    # ¡APAGAR LA FÍSICA! (Esto hace que no se mueva)
    net.toggle_physics(False)

    # Pasar los nodos de NetworkX a Pyvis con sus coordenadas fijas
    for node in G.nodes():
        x, y = pos[node]
        data = datos_nodos.get(node, {})

        net.add_node(
            node,
            x=x,
            y=y,
            label=data.get("label", node),
            color=data.get("color", "#999999"),
            size=data.get("size", 10),
            shape=data.get("shape", "dot"),
            font={"size": 14, "face": "arial"}  # Letra más legible
        )

    # Pasar las aristas (conexiones)
    for edge in G.edges():
        net.add_edge(edge[0], edge[1], color="#555555")

    # Guardar
    output_file = "red_adam.html"
    net.save_graph(output_file)

    # Abrir automáticamente (en Windows)
    import os
    os.startfile(output_file)
    print(f"¡Listo! Se abrió '{output_file}'.")


if __name__ == "__main__":
    generar_red_estatica()