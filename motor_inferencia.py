#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
motor_inferencia.py

Este archivo contiene el motor de inferencia para el proyecto A.D.A.M.
Su función es:
1. Importar la base de conocimiento.
2. Recibir un conjunto de "hechos" iniciales (síntomas).
3. Aplicar las reglas de la base de conocimiento para inferir nuevos hechos.
4. Repetir el proceso hasta encontrar un diagnóstico final o no poder inferir más.

Cumple con el objetivo: "Implementar el motor de inferencia"[cite: 432].
"""

# Importamos la base de conocimiento que creamos
try:
    from base_conocimiento import base_conocimiento
except ImportError:
    print("ERROR: No se pudo encontrar el archivo 'base_conocimiento.py'")
    print("Asegúrese de que ambos archivos estén en el mismo directorio.")
    exit()


class MotorDiagnostico:
    """
    Clase que representa el motor de inferencia de A.D.A.M.
    """

    def __init__(self, base_conocimiento):
        self.reglas = base_conocimiento
        self.hechos = {}  # Almacena los hechos conocidos (ej: {"sintoma": "valor"})

    def _evaluar_condicion(self, condicion):
        """Evalúa una única condición (tupla) contra los hechos."""
        variable, valor_esperado = condicion
        if variable not in self.hechos:
            # Aún no conocemos este hecho.
            # En el futuro, aquí es donde le preguntaremos al usuario.
            return False
        return self.hechos[variable] == valor_esperado

    def _evaluar_regla(self, regla):
        """Evalúa la parte "si" de una regla."""
        condiciones = regla["si"]

        # Lógica para manejar operadores "y" y "o"
        # Por ahora, implementaremos una lógica simple de "y".
        # TODO: Expandir para manejar lógica "o" compleja.

        if "o" in condiciones:
            # Lógica para 'o'
            resultado_parcial = False
            for item in condiciones:
                if item == "o":
                    continue  # Ignoramos el operador por ahora
                if self._evaluar_condicion(item):
                    resultado_parcial = True
                    break  # Con un 'o', basta que una sea verdadera
            return resultado_parcial
        else:
            # Lógica para 'y' (implícita)
            resultado_parcial = True
            for item in condiciones:
                if item == "y":
                    continue  # Ignoramos el operador por ahora
                if not self._evaluar_condicion(item):
                    resultado_parcial = False
                    break  # Con un 'y', basta que una sea falsa
            return resultado_parcial

    def diagnosticar(self, hechos_iniciales):
        """
        Ejecuta el motor de inferencia.
        """
        self.hechos = hechos_iniciales
        print(f"--- Iniciando diagnóstico con hechos: {self.hechos} ---")

        nuevos_hechos_inferidos = True
        reglas_aplicadas = set()  # Para no repetir reglas

        while nuevos_hechos_inferidos:
            nuevos_hechos_inferidos = False

            for i, regla in enumerate(self.reglas):
                if i in reglas_aplicadas:
                    continue  # Esta regla ya se aplicó

                # 1. Evaluar si la regla se cumple
                if self._evaluar_regla(regla):

                    # 2. Si se cumple, "disparar" la regla (aplicar el consecuente)
                    print(f"[LOG] Regla {i + 1} disparada.")
                    for variable, valor in regla["entonces"]:
                        if variable not in self.hechos or self.hechos[variable] != valor:
                            self.hechos[variable] = valor
                            print(f"    -> Nuevo hecho inferido: {variable} = {valor}")
                            nuevos_hechos_inferidos = True
                            reglas_aplicadas.add(i)

                    # 3. Si encontramos un diagnóstico final, terminamos.
                    if "diagnostico_final" in self.hechos:
                        print("--- Diagnóstico Final Encontrado ---")
                        return self.hechos["diagnostico_final"]

        print("--- Diagnóstico No Concluyente ---")
        return "No se pudo llegar a un diagnóstico final con los síntomas proporcionados."


# --- SIMULACIÓN DE EJECUCIÓN ---
if __name__ == "__main__":
    # Caso 1: Simulación de Termostato Atascado (Regla 005)
    print("\n*** CASO 1: SIMULACIÓN DE TERMOSTATO ATASCADO ***")

    # Estos serían los síntomas que el usuario ingresaría
    hechos_termostato = {
        "indicador_temperatura": "ROJO",  # Dispara Regla 001
        "fuga_liquido_visible": "no",
        "nivel_anticongelante": "CORRECTO",
        "manguera_superior": "CALIENTE",
        "manguera_inferior": "FRIA"
    }

    adam = MotorDiagnostico(base_conocimiento)
    diagnostico = adam.diagnosticar(hechos_termostato)
    print(f"\nDIAGNÓSTICO DE A.D.A.M.:\n{diagnostico}")

    # Caso 2: Simulación de Falla de Alternador (Regla 057)
    print("\n*** CASO 2: SIMULACIÓN DE FALLA DE ALTERNADOR ***")

    hechos_alternador = {
        "luz_bateria": "ENCENDIDA_MIENTRAS_CONDUCE"
    }

    adam_alt = MotorDiagnostico(base_conocimiento)
    diagnostico_alt = adam_alt.diagnosticar(hechos_alternador)
    print(f"\nDIAGNÓSTICO DE A.D.A.M.:\n{diagnostico_alt}")