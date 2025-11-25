import pyodbc
from base_conocimiento import base_conocimiento

# --- CONFIGURACIÓN DE CONEXIÓN ---
# Ajusta 'SERVER' con el nombre de tu servidor (ej: 'LOCALHOST\SQLEXPRESS' o la IP)
CONNECTION_STRING = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=MIDKNIGHT;"  #MIDKNIGHT <--- CAMBIA ESTO POR TU SERVIDOR
    r"DATABASE=ADAM_DB;"
    r"Trusted_Connection=yes;"
)


def migrar_datos():
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()

        print("Conexión exitosa. Iniciando migración de 152 reglas...")

        # Limpiar tablas previas por seguridad (opcional)
        cursor.execute("DELETE FROM Consecuencias")
        cursor.execute("DELETE FROM Condiciones")
        cursor.execute("DELETE FROM Reglas")

        for i, regla in enumerate(base_conocimiento):
            # 1. Insertar la Regla
            # Usamos i+1 como referencia visual, aunque el ID sea autoincremental
            cursor.execute("INSERT INTO Reglas (Descripcion) VALUES (?)", (f"Regla {i + 1}",))

            # Obtener el ID generado para esta regla
            cursor.execute("SELECT @@IDENTITY")
            id_regla = cursor.fetchval()

            # 2. Procesar Condiciones ("si")
            # La lista es mixta: [('var', 'val'), 'y', ('var2', 'val2')]
            condiciones_lista = regla['si']
            orden = 1

            # Iteramos con un while para manejar tu estructura plana
            idx = 0
            while idx < len(condiciones_lista):
                elemento = condiciones_lista[idx]

                if isinstance(elemento, tuple):
                    variable, valor = elemento
                    operador_siguiente = None

                    # Mirar si el siguiente elemento es un operador ('y' / 'o')
                    if idx + 1 < len(condiciones_lista):
                        siguiente = condiciones_lista[idx + 1]
                        if isinstance(siguiente, str) and siguiente in ['y', 'o']:
                            operador_siguiente = siguiente
                            idx += 1  # Saltamos el operador en la próxima iteración

                    cursor.execute("""
                                   INSERT INTO Condiciones (ID_Regla, Variable, Valor, Operador_Siguiente, Orden)
                                   VALUES (?, ?, ?, ?, ?)
                                   """, (id_regla, variable, valor, operador_siguiente, orden))

                    orden += 1
                idx += 1

            # 3. Procesar Consecuencias ("entonces")
            for consec in regla['entonces']:
                variable_cons, valor_cons = consec
                cursor.execute("""
                               INSERT INTO Consecuencias (ID_Regla, Variable, Valor)
                               VALUES (?, ?, ?)
                               """, (id_regla, variable_cons, valor_cons))

        conn.commit()
        print("¡Migración completada con éxito!")
        print(f"Se procesaron {len(base_conocimiento)} reglas.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()


if __name__ == "__main__":
    migrar_datos()