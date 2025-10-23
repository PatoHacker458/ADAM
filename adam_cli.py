#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Este script contiene el motor de inferencia y la interfaz de usuario
para manejar adecuadamente la adquisición de hechos y las variables internas.
"""

# 1. IMPORTACIÓN DE LA BASE DE CONOCIMIENTO

try:
    from base_conocimiento import base_conocimiento
except ImportError:
    print("ERROR AL IMPORTAR")
    exit()

# 2. MAPA DE PREGUNTAS

mapa_preguntas = {
    # Módulo 1: Enfriamiento
    "indicador_temperatura": "¿El indicador de temperatura está en la zona 'ROJA'?",
    "testigo_temperatura": "¿Tiene un testigo (luz) de temperatura 'ENCENDIDO' en el tablero?",
    "fuga_liquido_visible": "¿Observa una fuga o charco de líquido (verde, rosa, naranja) debajo del coche?",
    "vehiculo_estado": "¿El vehículo está actualmente 'DETENIDO'?",
    "ventilador_radiador": "¿El ventilador del radiador está 'APAGADO' (no gira) a pesar de que el motor está caliente?",
    "nivel_anticongelante": "¿El nivel de anticongelante en el depósito está 'BAJO' (por debajo del MÍNIMO)?",
    "manguera_superior": "¿La manguera SUPERIOR del radiador está 'CALIENTE'?",
    "manguera_inferior": "¿La manguera INFERIOR del radiador está 'FRIA' o tibia?",
    "nivel_anticongelante_baja": "¿Necesita rellenar el anticongelante 'BAJA_FRECUENTEMENTE'?",
    "olor_anticongelante_cabina": "¿Percibe un olor dulce a anticongelante DENTRO de la cabina?",
    "parabrisas_empanado_residuo": "¿El parabrisas se empaña con un residuo aceitoso?",
    "alfombra_pasajero_humeda": "¿La alfombra del lado del pasajero está 'HUMEDA'?",
    "humo_blanco_denso_escape": "¿Sale 'HUMO_BLANCO_DENSO' del escape de forma continua?",
    "aspecto_aceite_motor": "¿El aceite del motor (en la varilla) tiene un aspecto 'LECHOSO_O_CREMOSO' o 'CAFE_CON_LECHE_GRUMOSO'?",
    "residuos_color_motor": "¿Observa 'COSTRAS_O_RESIDUOS_DE_COLOR' en las mangueras o el motor?",
    "sintomas_internos_fuga": "¿Ha notado síntomas de fuga interna (humo blanco, aceite lechoso, olor en cabina)?",
    "sintomas_fuga_evidentes": "¿Ha notado algún síntoma de fuga (charcos, olores, humo, costras, etc.)?",
    "sobrecalentamiento_condicion": "¿El coche 'SOLO_SE_CALIENTA_EN_TRAFICO' o al estar detenido?",
    "ventilador_no_gira_caliente": "¿Puede confirmar que el ventilador NO GIRA aunque el motor esté caliente?",
    "ventilador_no_activa_con_ac": "¿El ventilador 'NO_SE_ACTIVA' al encender el Aire Acondicionado?",
    "fusible_ventilador": "¿Ha revisado el fusible del ventilador? ¿Está 'QUEMADO'?",
    "ventilador_rendimiento": "¿El ventilador 'GIRA_LENTO_O_HACE_RUIDO'?",

    # Módulo 2: Combustible
    "estado_motor": "¿El motor 'GIRA_PERO_NO_ARRANCA' (hace 'ñaca-ñaca' pero no enciende)?",
    "nivel_combustible": "¿El indicador de combustible marca 'VACIO_O_MUY_BAJO'?",
    "zumbido_bomba_combustible": "Al girar la llave a 'ON' (sin arrancar), ¿'NO_SE_ESCUCHA' el zumbido de la bomba de gasolina (que viene de atrás)?",
    "rendimiento_motor": "¿El motor 'PIERDE_POTENCIA_BAJO_CARGA' (al acelerar fuerte o en subidas)?",
    "mantenimiento_filtro_combustible": "¿El filtro de combustible es 'ANTIGUO_O_DESCONOCIDO' (más de 2 años o 40,000 km)?",
    "arranque_en_frio": "¿El arranque en frío es 'LENTO' o 'TARDA_MUCHO'?",
    "arranque_en_frio_normal": "¿El arranque en frío es 'NORMAL'?",  # Para REGLA 026

    # Módulo 3: Encendido
    "ralenti_motor": "¿El motor en ralentí (detenido) está 'INESTABLE_O_TEMBLOROSO'?",
    "mantenimiento_bujias": "¿El mantenimiento de las bujías es 'ANTIGUO_O_DESCONOCIDO'?",
    "estado_cables_bobinas": "¿Los cables de bujía o las bobinas se ven 'AGRIETADOS_O_DAÑADOS'?",
    "revoluciones_ralenti": "¿Las revoluciones en ralentí 'OSCILAN_SOLAS' (suben y bajan)?",
    "revoluciones_ralenti_estables": "¿Las revoluciones son 'ESTABLES_PERO_EL_MOTOR_TIEMBLA'?",  # Para REGLA 031
    "luz_check_engine": "¿La luz de 'Check Engine' está 'PARPADEANDO'?",
    "luz_check_engine_fija": "¿La luz de 'Check Engine' está 'ENCENDIDA_FIJA'?",
    "tapon_combustible": "¿Ha revisado el tapón de gasolina? ¿Estaba 'SUELTO_O_MAL_CERRADO'?",
    "tacometro_en_arranque": "Al intentar arrancar, ¿el tacómetro (aguja de RPM) 'NO_MARCA_RPM' (no se mueve)?",
    "consumo_combustible": "¿El consumo de combustible es 'ELEVADO'?",
    "rendimiento_motor_titubeo": "¿El motor 'TITUBEA_AL_ACELERAR'?",
    "humo_escape": "¿Nota que sale 'HUMO_NEGRO' del escape?",
    "rendimiento_combustible": "¿El rendimiento del combustible ha 'EMPEORADO_NOTABLEMENTE' o es 'POBRE'?",

    # Módulo 4: Mecánico
    "estado_motor_marcha": "¿El motor 'SE_APAGO_EN_MARCHA' (mientras conducía)?",
    "sonido_arranque": "Al intentar arrancarlo de nuevo, ¿el sonido del arranque es 'ANORMALMENTE_RAPIDO' o 'hueco'?",

    # Módulo 5: Lubricación
    "luz_presion_aceite": "¿La luz roja de 'PRESION_DE_ACEITE' (la aceitera) se enciende?",
    "ruido_motor": "¿Se escucha un 'RUIDO_DE_GOLPETEO_METALICO' (Knocking) o un 'RUIDO_DE_TAQUETES' (tic-tic-tic) en el motor?",
    "humo_escape_azul": "¿Sale 'HUMO_AZULADO' del tubo de escape?",
    "nivel_aceite": "¿La varilla de medir aceite muestra un nivel 'BAJO' constantemente?",
    "fuga_aceite_visible": "¿Hay 'MANCHAS_DE_ACEITE' debajo del coche?",
    "ruido_motor_normal": "¿El motor 'SUENA_NORMAL', sin ruidos metálicos?",  # Para REGLA 082, 083
    "nivel_aceite_correcto": "¿Verificó el nivel de aceite y está 'CORRECTO'?",  # Para REGLA 083

    # Módulo 6: Frenos
    "ruido_frenos": "¿Se escucha un 'CHILLIDO_AGUDO' o un 'RUIDO_DE_ROCE_METALICO' (grinding) al frenar?",
    "sensacion_pedal_freno": "¿El pedal de freno se siente 'ESPONJOSO', 'SE_VA_HASTA_EL_FONDO', 'VIBRA_O_PULSA' o está 'MUY_DURO'?",
    "comportamiento_vehiculo_frenar": "¿El coche 'SE_DESVIA_HACIA_UN_LADO' al frenar?",
    "luz_advertencia_frenos": "¿La luz de advertencia de 'FRENOS' está encendida?",
    "luz_advertencia_abs": "¿La luz de advertencia de 'ABS' está encendida?",

    # Módulo 7: Eléctrico (Batería/Alternador)
    "estado_arranque": "¿Al girar la llave, 'NO_HAY_LUCES_NI_SONIDO', solo se escucha un 'CLIC' o el motor gira 'LENTO_Y_CON_DIFICULTAD'?",
    "luz_bateria": "¿La luz de advertencia de la 'BATERIA' se enciende 'MIENTRAS_CONDUCE'?",
    "comportamiento_luces": "¿Las luces del coche 'BAJAN_DE_INTENSIDAD' al estar en ralentí?",
    "edad_bateria": "¿La batería tiene 'MAS_DE_4_AÑOS'?",
    "terminales_bateria": "¿Hay 'CORROSION_BLANCA_O_VERDOSA' en los terminales de la batería?",
    "comportamiento_post_arranque_puente": "¿Después de pasar corriente el coche 'SE_APAGA_AL_DESCONECTAR_LOS_CABLES'?",

    # Módulo 8: Suspensión y Dirección
    "ruido_suspension": "¿Se escucha un 'GOLPETEO_SECO' (clunk) en la parte delantera al pasar por baches?",
    "comportamiento_vehiculo": "¿El coche 'REBOTA_EXCESIVAMENTE' después de un bache o 'SE_DESVIA_HACIA_UN_LADO' en recta?",
    "sensacion_volante": "¿El volante 'VIBRA_A_CIERTAS_VELOCIDADES'?",
    "ruido_vehiculo": "¿Se escucha un 'ZUMBIDO_O_RUGIDO' que aumenta con la velocidad?",
    "ruido_direccion": "¿Se escucha un 'CHASQUIDO_O_TRONIDO' al girar por completo o un 'GEMIDO_O_ZUMBIDO' al girar el volante?",
    "desgaste_llantas": "¿Las llantas muestran un 'DESGASTE_IRREGULAR' (más por dentro o por fuera)?",

    # Módulo 9: Escape
    "ruido_escape": "¿El coche suena 'MUCHO_MAS_RUIDOSO' de lo normal, se escucha un 'CASCABEL_METALICO' debajo o suena 'TAPADO'?",
    "olor_cabina": "¿Se percibe 'OLOR_A_GASES_DE_ESCAPE' dentro de la cabina?",

    # Módulo 10: Transmisión
    "tipo_transmision": "¿Su transmisión es 'AUTOMATICA' o 'MANUAL'?",
    "cambio_marcha": "¿Siente un 'GOLPE_FUERTE' al cambiar de Parking a Drive/Reversa o los cambios son 'BRUSCOS_O_A_DESTIEMPO'?",
    "comportamiento_transmision": "¿El motor se 'ACELERA_PERO_EL_COCHE_NO_AVANZA' (patina) o se 'REVOLUCIONA_AL_ACELERAR' sin ganar velocidad?",
    "sensacion_clutch": "¿El pedal del 'CLUTCH_SE_SIENTE_ESPONJOSO' o se va al fondo?",

    # Módulo 11: Sensores
    "humo_escape_negro_arranque": "¿Sale 'HUMO_NEGRO' solo al arrancar en frío?",
    "ventilador_encendido_inmediato": "¿El motoventilador 'SE_ENCIENDE_INMEDIATAMENTE' al arrancar en frío o 'NO_SE_APAGA_NUNCA'?",
    "condicion_sobrecalentamiento": "¿El motor 'SE_SOBRECALIENTA'?",
    "ventilador_no_activa": "¿El motoventilador 'NO_SE_ACTIVA' aunque el motor esté caliente?",
    "rendimiento_motor_perezoso": "¿El motor se siente 'PEREZOSO'?",
    "ralenti_ligeramente_alto": "¿El ralentí es 'LIGERAMENTE_ALTO'?",
    "luz_presion_aceite_intermitente": "¿La luz de presión de aceite 'PARPADEA_O_SE_ENCIENDE' en ralentí?",
    "luz_presion_aceite_permanente": "¿La luz de presión de aceite 'PERMANECE_ENCENDIDA' después de arrancar?",
    "indicador_presion_aceite": "¿La aguja de presión de aceite 'MARCA_CERO_O_MAXIMO' de forma irreal?",
    "rendimiento_motor_aceleracion": "¿El coche 'ACELERA_DE_FORMA_ERRATICA' o 'DA_TIRONES' a velocidad constante?",
    "rendimiento_motor_respuesta_lenta": "¿El motor 'NO_ACELERA' o responde muy lentamente al pisar el pedal?",
    "ralenti_motor_alto": "¿El 'RALENTI_ES_MUY_ALTO' y no baja?",
    "problemas_conduccion_aceleracion": "¿Se presentan problemas de 'ACELERACION_Y_CAMBIOS_DE_MARCHA' erráticos?",
    "rendimiento_motor_potencia_intermitente": "¿El coche 'PARECE_PERDER_POTENCIA' repentinamente y luego la recupera?",

    # Módulo 12: Códigos de Falla (DTCs)
    "codigo_falla": "¿Ha escaneado el vehículo? ¿Tiene un código de falla (ej. 'P0300', 'P030X', 'P0420', 'P0171', 'P0172', 'P0401', 'P0404', 'P0442', 'P0455', 'P0443', 'P0456')?",
    "existen_otros_codigos_falla": "¿Existen 'OTROS_CODIGOS_DE_FALLA' además del P0420?",
    "diagnostico_bobina": "¿Ha intercambiado la bobina del cilindro [X] y confirmado que la 'BOBINA_ESTA_BIEN'?",
    "ruido_motor_silbido": "¿Se escucha un 'SILBIDO' en el compartimento del motor?",
    "fuga_vacio_aparente": "¿Ha revisado y confirmado que 'NO_HAY_FUGAS_DE_VACIO' aparentes?",
    "olor_escape": "¿Se percibe un fuerte 'OLOR_A_GASOLINA' en el escape?",

    # Módulo 13: Aire Acondicionado
    "ac_estado": "¿El A/C está 'ENCENDIDO'?",
    "ac_aire": "¿El aire que sale 'NO_ES_FRIO', es 'CALIENTE' o 'ENFRIA_DEBILMENTE'?",
    "ac_compresor": "¿El compresor 'NO_SE_ACTIVA' (no se oye el 'clic') o 'SE_ACTIVA_Y_DESACTIVA_MUY_RAPIDO' (ciclos cortos)?",
    "ac_rendimiento": "¿El rendimiento 'MEJORA_AL_ACELERAR_EL_COCHE' o 'ENFRIA_BIEN_EN_CARRETERA' pero 'DEJA_DE_ENFRIAR_EN_TRAFICO'?",
    "ac_linea_aluminio": "¿Una de las 'LINEAS_DE_ALUMINIO_DEL_A/C' en el motor está muy fría o congelada?",
    "ac_flujo_aire_ventilas": "¿El 'FLUJO_DE_AIRE' por las ventilas es muy débil?",
    "ac_aire_temperatura_desigual": "¿El 'AIRE_SALE_FRIO_POR_UN_LADO' y tibio o caliente por el otro?",
    "ac_ruido": "¿Se escucha un 'RUIDO_DE_ROZAMIENTO_O_ZUMBIDO_FUERTE' solo al encender el A/C?",
    "ac_ruido_polea": "¿Se escucha un 'RUIDO_DE_BALERO_O_CHILLIDO_CONSTANTE' proveniente de la zona del compresor, 'INCLUSO_CON_EL_A/C_APAGADO'?",
    "ac_ruido_clutch": "¿Al encender el A/C se escucha un 'GOLPETEO_METALICO' fuerte?",
    "ac_rendimiento_progresivo": "¿El sistema de A/C 'DEJO_DE_ENFRIAR_PROGRESIVAMENTE'?",
    "ac_fuga_visible": "¿Se observan 'MANCHAS_DE_ACEITE_VERDOSO_O_AMARILLENTO' en las conexiones del A/C?",
    "olor_cabina_ac": "¿Se percibe un 'OLOR_QUIMICO_DULZON' dentro de la cabina al usar el A/C?",
    "ac_control": "¿El 'BOTON_DEL_A/C_NO_SE_ILUMINA' o no responde?",
    "ac_ventilador_interior": "¿El 'VENTILADOR_INTERIOR_(SOPLADOR)_NO_FUNCIONA' en algunas velocidades, solo en la más alta?",

    # Módulo 14: Emisiones (EGR y EVAP)
    "ralenti_inestable_o_se_apaga": "¿El 'RALENTI_ES_MUY_INESTABLE' o el motor 'SE_APAGA_EN_BAJA'?",
    "rendimiento_motor_mejora_acelerar": "¿El problema 'MEJORA_AL_ACELERAR'?",
    "ruido_motor_cascabeleo": "¿Se escucha un 'RUIDO_DE_CASCABELEO_O_PINGING' en el motor al 'ACELERAR_O_SUBIR_PENDIENTES'?",
    "rendimiento_motor_normal": "¿El rendimiento es 'NORMAL' en otras condiciones?",
    "sintomas_conduccion": "¿Ha notado 'NO_HAY_SINTOMAS_DE_CONDUCCION' notables (el coche anda bien)?",
    "olor_vehiculo": "¿Se percibe un 'OLOR_A_COMBUSTIBLE' alrededor del vehículo?",
    "ralenti_inestable_post_carga": "¿El 'RALENTI_ES_INESTABLE' justo después de llenar el tanque de combustible?",
    "problema_carga_combustible": "¿La pistola de la gasolinera 'SE_BOTA_CONSTANTEMENTE' al intentar llenar el tanque?",
    "estado_arranque_post_carga": "¿El motor 'TIENE_DIFICULTAD_PARA_ARRANCAR' 'INMEDIATAMENTE_DESPUES_DE_LLENAR_EL_TANQUE'?",
    "hallazgo_inspeccion": "¿Se encuentran 'PEQUEÑAS_BOLITAS_NEGRAS' (gránulos de carbón) en las mangueras del sistema EVAP?",
    "resultado_verificacion": "¿El vehículo 'FALLA_LA_VERIFICACION_DE_EMISIONES'?",
    "codigo_falla_evap": "¿La luz de 'Check Engine' está 'ENCENDIDA' con un código EVAP?",

    # Módulo 15: Carrocería y Eléctricos Menores
    "falla_luz": "¿'UNA_SOLA_LUZ_EXTERIOR' no enciende, 'AMBAS_LUCES_BAJAS' no encienden (pero las altas sí), un 'GRUPO_DE_LUCES' no enciende, una 'LUZ_DIRECCIONAL_PARPADEA_MUY_RAPIDO' o la 'LUZ_INTERIOR_O_DE_CORTESIA' no enciende con una puerta?",
    "falla_electrica": "¿Un componente 'DEJA_DE_FUNCIONAR_REPENTINAMENTE', un fusible 'SE_QUEMA_INMEDIATAMENTE', 'SE_QUEMA_REPETIDAMENTE', 'UNA_SOLA_VENTANA_ELECTRICA' no funciona, una ventana 'SOLO_FUNCIONA_DESDE_CONTROL_MAESTRO', 'TODAS_LAS_VENTANAS_ELECTRICAS_DEJAN_DE_FUNCIONAR', las 'LUCES_INTERIORES_BAJAN_DE_INTENSIDAD' al usar la ventana, o un 'SEGURO_ELECTRICO' no funciona?",
    "ruido_carroceria": "¿Se escucha un 'SILBIDO_O_RUIDO_DE_VIENTO' desde una puerta, un 'RUIDO_DE_VIENTO' desde el parabrisas o un 'RUIDO_DE_AGUA_MOVIENDOSE' dentro de una puerta?",
    "filtracion_agua": "¿Se encuentra 'AGUA_O_HUMEDAD_EN_LA_ALFOMBRA' después de llover?",
}

# 3. MOTOR DE INFERENCIA

class MotorDiagnostico:

    def __init__(self, base_conocimiento, mapa_preguntas):
        self.reglas = base_conocimiento
        self.hechos = {}
        self.mapa_preguntas = mapa_preguntas
        self.variables_internas = {
            "condicion",
            "diagnostico_parcial",
            "diagnostico_final",
            "cilindro_afectado",
            "accion_recomendada",
            "diagnostico_bobina",
            "existen_otros_codigos_falla",
            "diagnostico_parcial",
            "P0420_DETECTADO",
            "MEZCLA_POBRE_P0171",
            "MEZCLA_RICA_P0172"
        }

    def _solicitar_hecho(self, variable, valor_esperado):

        if variable in self.hechos:
            return

        if variable in self.variables_internas:
            return

        if variable not in self.mapa_preguntas:
            print(
                f"[LOG_ERROR] No se encontró una pregunta para la variable: '{variable}'. Contactar al equipo de desarrollo.")
            self.hechos[variable] = "error_pregunta_no_encontrada"
            return

        # 1. Hacer la pregunta
        pregunta = self.mapa_preguntas[variable]
        print(f"\n[A.D.A.M.] {pregunta} (si/no/?)")
        respuesta = input("Usuario: ").strip().lower()

        # 2. Normalizar la respuesta
        if respuesta in ['s', 'si', 'y', 'yes', 'v', 'verdadero']:
            self.hechos[variable] = valor_esperado

        elif respuesta in ['n', 'no', 'f', 'falso']:
            self.hechos[variable] = "no"

        elif respuesta == '?':
            self.hechos[variable] = "no_se"

        else:
            self.hechos[variable] = respuesta.upper()

        print(f"[LOG] Hecho adquirido: {variable} = {self.hechos[variable]}")

    def _evaluar_condicion(self, condicion):
        variable, valor_esperado = condicion

        if variable not in self.hechos:
            self._solicitar_hecho(variable, valor_esperado)

        return self.hechos.get(variable) == valor_esperado

    def _evaluar_regla(self, regla):
        condiciones = regla["si"]

        if "o" in condiciones:
            resultado_parcial = False
            for item in condiciones:
                if item == "o":
                    continue
                if self._evaluar_condicion(item):
                    resultado_parcial = True
                    break
            return resultado_parcial
        else:
            resultado_parcial = True
            for item in condiciones:
                if item == "y":
                    continue
                if not self._evaluar_condicion(item):
                    resultado_parcial = False
                    break
            return resultado_parcial

    def diagnosticar(self):

        print("Iniciando A.D.A.M.")

        nuevos_hechos_inferidos = True
        reglas_aplicadas = set()

        while nuevos_hechos_inferidos:
            nuevos_hechos_inferidos = False

            for i, regla in enumerate(self.reglas):
                if i in reglas_aplicadas:
                    continue

                    # 1. Evaluar si la regla se cumple
                if self._evaluar_regla(regla):

                    print(f"\n[LOG] Regla {i + 1} disparada.")
                    reglas_aplicadas.add(i)

                    # 2. Si se cumple, "disparar" la regla
                    for variable, valor in regla["entonces"]:
                        if self.hechos.get(variable) != valor:
                            self.hechos[variable] = valor
                            print(f"    -> Hecho inferido: {variable} = {valor}")
                            nuevos_hechos_inferidos = True

                    # 3. Si encontramos un diagnóstico final, terminamos.
                    if "diagnostico_final" in self.hechos:
                        print("\n--- Diagnóstico Final Encontrado ---")
                        return self.hechos["diagnostico_final"]

        print("\n--- Diagnóstico No Concluyente ---")
        return "No se pudo llegar a un diagnóstico final con los síntomas proporcionados."


# 4. INTERFAZ DE USUARIO Y EJECUCIÓN

if __name__ == "__main__":
    print("======================================================")
    print("  Bienvenido a A.D.A.M.")
    print("  (Asistente de Diagnóstico Automotriz Mecánico)")
    print("======================================================")
    print("Por favor, responda a las siguientes preguntas para ayudarme a")
    print("diagnosticar el problema de su vehículo.")
    print("Responda con 'si', 'no' o '?' si no está seguro.")

    adam = MotorDiagnostico(base_conocimiento, mapa_preguntas)

    diagnostico_final = adam.diagnosticar()

    print("\n======================================================")
    print("  DIAGNÓSTICO DE A.D.A.M.:")
    print("======================================================")
    print(diagnostico_final)