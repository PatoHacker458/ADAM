#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
base_conocimiento.py

Este archivo contiene la base de conocimiento completa para el proyecto
A.D.A.M (Asistente de Diagnóstico Automotriz Mecánico).
Las 152 reglas están estructuradas como una lista de diccionarios,
listas para ser procesadas por el motor de inferencia.

Formato de Regla:
{
    "si": [ (variable, valor), "operador", (variable, valor), ... ],
    "entonces": [ (variable_a_establecer, nuevo_valor), ... ]
}
"""

base_conocimiento = [
    # --- MÓDULO 1: SISTEMA DE ENFRIAMIENTO ---

    # Falla 1: Sobrecalentamiento del motor
    {  # REGLA 001
        "si": [("indicador_temperatura", "ROJO"), "o", ("testigo_temperatura", "ENCENDIDO")],
        "entonces": [("condicion", "SOBRECALENTAMIENTO_ACTIVO")]
    },
    {  # REGLA 002
        "si": [("condicion", "SOBRECALENTAMIENTO_ACTIVO"), "y", ("fuga_liquido_visible", "si")],
        "entonces": [("diagnostico_final",
                      "Fuga activa en el sistema de enfriamiento. Causa probable: Manguera rota, radiador perforado o bomba de agua defectuosa. Detenga el motor inmediatamente.")]
    },
    {  # REGLA 003
        "si": [("condicion", "SOBRECALENTAMIENTO_ACTIVO"), "y", ("vehiculo_estado", "DETENIDO"), "y",
               ("ventilador_radiador", "APAGADO")],
        "entonces": [("diagnostico_final",
                      "Posible falla en el motoventilador. Causa probable: Fusible quemado, relevador defectuoso o motor del ventilador dañado.")]
    },
    {  # REGLA 004
        "si": [("condicion", "SOBRECALENTAMIENTO_ACTIVO"), "y", ("nivel_anticongelante", "BAJO")],
        "entonces": [("diagnostico_final",
                      "Nivel bajo de anticongelante. Puede deberse a una fuga pequeña no visible o evaporación. Rellenar con el anticongelante especificado y monitorear el nivel.")]
    },
    {  # REGLA 005
        "si": [
            ("condicion", "SOBRECALENTAMIENTO_ACTIVO"), "y",
            ("fuga_liquido_visible", "no"), "y",
            ("nivel_anticongelante", "CORRECTO"), "y",
            ("manguera_superior", "CALIENTE"), "y",
            ("manguera_inferior", "FRIA")
        ],
        "entonces": [("diagnostico_final",
                      "Síntomas consistentes con un termostato atascado en posición cerrada. Impide la circulación del anticongelante hacia el radiador.")]
    },
    {  # REGLA 006
        "si": [
            ("condicion", "SOBRECALENTAMIENTO_ACTIVO"), "y",
            ("fuga_liquido_visible", "no"), "y",
            ("nivel_anticongelante", "CORRECTO"), "y",
            ("ventilador_radiador", "CORRECTAMENTE")
        ],
        "entonces": [("diagnostico_final",
                      "Causa de sobrecalentamiento no evidente. Posibles causas avanzadas: Radiador obstruido interna o externamente, bomba de agua con propela dañada o junta de culata soplada. Se requiere inspección profesional.")]
    },

    # Falla 2: Pérdida o Consumo de anticongelante
    {  # REGLA 007
        "si": [("nivel_anticongelante", "BAJA_FRECUENTEMENTE"), "y", ("olor_anticongelante_cabina", "si")],
        "entonces": [("diagnostico_final",
                      "Fuga probable en el radiador de la calefacción (heater core). Requiere inspección del tablero y el piso del pasajero.")]
    },
    {  # REGLA 008
        "si": [
            ("nivel_anticongelante", "BAJA_FRECUENTEMENTE"), "y",
            ("parabrisas_empanado_residuo", "si"), "y",
            ("alfombra_pasajero_humeda", "si")
        ],
        "entonces": [("diagnostico_final",
                      "Fuga confirmada en el radiador de la calefacción (heater core). Se debe reemplazar.")]
    },
    {  # REGLA 009
        "si": [("nivel_anticongelante", "BAJA_FRECUENTEMENTE"), "y", ("humo_blanco_denso_escape", "si")],
        "entonces": [("diagnostico_final",
                      "Indicio de fuga interna de anticongelante hacia los cilindros. Causa probable: junta de culata dañada. Se recomienda no usar el vehículo y buscar atención mecánica especializada.")]
    },
    {  # REGLA 010
        "si": [("aspecto_aceite_motor", "LECHOSO_O_CREMOSO")],
        "entonces": [("diagnostico_final",
                      "Contaminación de aceite con anticongelante confirmada. Causa: junta de culata dañada o fisura en el bloque/culata. El motor está en riesgo de daño severo. No lo encienda.")]
    },
    {  # REGLA 011
        "si": [
            ("nivel_anticongelante", "BAJA_FRECUENTEMENTE"), "y",
            ("sintomas_internos_fuga", "no"), "y",
            ("residuos_color_motor", "si")
        ],
        "entonces": [("diagnostico_final",
                      "Fuga externa pequeña por evaporación. Inspeccionar la zona de los residuos para localizar el punto exacto (manguera, abrazadera, radiador, bomba de agua) y reparar.")]
    },
    {  # REGLA 012
        "si": [("nivel_anticongelante", "BAJA_FRECUENTEMENTE"), "y", ("sintomas_fuga_evidentes", "no")],
        "entonces": [("diagnostico_final",
                      "Pérdida de anticongelante no localizada. Puede ser una fisura muy pequeña o la tapa del radiador/depósito defectuosa que no mantiene la presión. Se recomienda realizar una prueba de presión al sistema de enfriamiento en un taller.")]
    },

    # Falla 3: Fallos del Motoventilador
    {  # REGLA 013
        "si": [("sobrecalentamiento_condicion", "SOLO_EN_TRAFICO")],
        "entonces": [("diagnostico_parcial", "SOSPECHA_FALLA_VENTILADOR")]
    },
    {  # REGLA 014
        "si": [("diagnostico_parcial", "SOSPECHA_FALLA_VENTILADOR"), "y", ("ventilador_no_gira_caliente", "si")],
        "entonces": [("diagnostico_final",
                      "Falla confirmada en el sistema del motoventilador. El ventilador no se está activando cuando es necesario. Proceder a revisar componentes.")]
    },
    {  # REGLA 015
        "si": [
            ("diagnostico_parcial", "SOSPECHA_FALLA_VENTILADOR"), "y",
            ("ventilador_no_activa_con_ac", "si"), "y",
            ("fusible_ventilador", "QUEMADO")
        ],
        "entonces": [("diagnostico_final",
                      "Causa probable: Fusible del motoventilador quemado. Reemplace el fusible por uno de idéntico amperaje. Si se quema de nuevo, existe un cortocircuito que requiere revisión profesional.")]
    },
    {  # REGLA 016
        "si": [
            ("diagnostico_parcial", "SOSPECHA_FALLA_VENTILADOR"), "y",
            ("ventilador_no_activa_con_ac", "si"), "y",
            ("fusible_ventilador", "OK")
        ],
        "entonces": [("diagnostico_final",
                      "La falla puede estar en el relevador (relay) del ventilador, el sensor de temperatura que lo activa (Sensor ECT), o el propio motor del ventilador. Se requiere un diagnóstico eléctrico.")]
    },
    {  # REGLA 017
        "si": [("diagnostico_parcial", "SOSPECHA_FALLA_VENTILADOR"), "y",
               ("ventilador_rendimiento", "GIRA_LENTO_O_HACE_RUIDO")],
        "entonces": [("diagnostico_final",
                      "El motor del ventilador presenta desgaste. Su rendimiento es insuficiente para enfriar el motor de forma efectiva. Se recomienda el reemplazo de la unidad del ventilador.")]
    },

    # --- MÓDULO 2: SISTEMA DE COMBUSTIBLE ---

    # Falla 4: El motor gira pero no arranca
    {  # REGLA 018
        "si": [("estado_motor", "GIRA_PERO_NO_ARRANCA"), "y", ("nivel_combustible", "VACIO_O_MUY_BAJO")],
        "entonces": [("diagnostico_final",
                      "El vehículo no tiene combustible. Esta es la causa más probable del problema. Añada al menos 5-10 litros de combustible para asegurar que la bomba pueda succionar.")]
    },
    {  # REGLA 019
        "si": [("estado_motor", "GIRA_PERO_NO_ARRANCA"), "y", ("nivel_combustible", "OK")],
        "entonces": [("diagnostico_parcial", "SOSPECHA_FALTA_ENTREGA_COMBUSTIBLE")]
    },
    {  # REGLA 020
        "si": [("diagnostico_parcial", "SOSPECHA_FALTA_ENTREGA_COMBUSTIBLE"), "y",
               ("zumbido_bomba_combustible", "NO_SE_ESCUCHA")],
        "entonces": [("diagnostico_final",
                      "No se oye la activación de la bomba de combustible. La causa probable es un fusible quemado (buscar 'FUEL PUMP'), un relevador (relay) defectuoso o la bomba de combustible dañada. Revise la caja de fusibles como primer paso.")]
    },
    {  # REGLA 021
        "si": [("diagnostico_parcial", "SOSPECHA_FALTA_ENTREGA_COMBUSTIBLE"), "y",
               ("zumbido_bomba_combustible", "SI_SE_ESCUCHA")],
        "entonces": [("diagnostico_final",
                      "La bomba de combustible parece activarse. El problema podría ser un filtro de combustible completamente obstruido que impide el paso de la gasolina, o una falla en el sistema de encendido. Se sugiere verificar el filtro de combustible.")]
    },

    # Falla 5: Pérdida de potencia
    {  # REGLA 022
        "si": [("rendimiento_motor", "PIERDE_POTENCIA_BAJO_CARGA")],
        "entonces": [("diagnostico_parcial", "SOSPECHA_RESTRICCION_COMBUSTIBLE")]
    },
    {  # REGLA 023
        "si": [("diagnostico_parcial", "SOSPECHA_RESTRICCION_COMBUSTIBLE"), "y",
               ("mantenimiento_filtro_combustible", "ANTIGUO_O_DESCONOCIDO")],
        "entonces": [("diagnostico_final",
                      "El principal sospechoso es un filtro de combustible obstruido. Es un componente de mantenimiento económico y su reemplazo suele solucionar la pérdida de potencia. Se recomienda empezar por aquí.")]
    },
    {  # REGLA 024
        "si": [("diagnostico_parcial", "SOSPECHA_RESTRICCION_COMBUSTIBLE"), "y",
               ("mantenimiento_filtro_combustible", "RECIENTE")],
        "entonces": [("diagnostico_parcial", "POSIBLE_FALLA_BOMBA_O_INYECTORES")]
    },
    {  # REGLA 025
        "si": [("diagnostico_parcial", "POSIBLE_FALLA_BOMBA_O_INYECTORES"), "y", ("arranque_en_frio", "LENTO")],
        "entonces": [("diagnostico_final",
                      "La combinación de síntomas apunta a una bomba de combustible débil que no mantiene la presión, o a inyectores sucios. Se recomienda una prueba de presión de combustible en un taller.")]
    },
    {  # REGLA 026
        "si": [("diagnostico_parcial", "POSIBLE_FALLA_BOMBA_O_INYECTORES"), "y", ("arranque_en_frio", "NORMAL")],
        "entonces": [("diagnostico_final",
                      "La causa más probable es una bomba de combustible fallando bajo alta demanda. Menos probable, pero posible, son los inyectores sucios. Se requiere diagnóstico profesional para confirmar.")]
    },

    # --- MÓDULO 3: SISTEMA DE ENCENDIDO ---

    # Falla 6: Ralentí inestable
    {  # REGLA 027
        "si": [("ralenti_motor", "INESTABLE_O_TEMBLOROSO")],
        "entonces": [("diagnostico_parcial", "SOSPECHA_FALLA_ENCENDIDO_MISFIRE")]
    },
    {  # REGLA 028
        "si": [("diagnostico_parcial", "SOSPECHA_FALLA_ENCENDIDO_MISFIRE"), "y",
               ("mantenimiento_bujias", "ANTIGUO_O_DESCONOCIDO")],
        "entonces": [("diagnostico_final",
                      "La causa más probable son bujías desgastadas. Son un componente de mantenimiento y su reemplazo es el primer paso recomendado para corregir un fallo de encendido.")]
    },
    {  # REGLA 029
        "si": [("diagnostico_parcial", "SOSPECHA_FALLA_ENCENDIDO_MISFIRE"), "y",
               ("estado_cables_bobinas", "AGRIETADOS_O_DAÑADOS")],
        "entonces": [("diagnostico_final",
                      "Los cables de bujía o las bobinas están en mal estado, provocando una fuga de corriente. Esto causa una chispa débil o nula. Deben ser reemplazados.")]
    },
    {  # REGLA 030
        "si": [("diagnostico_parcial", "SOSPECHA_FALLA_ENCENDIDO_MISFIRE"), "y",
               ("revoluciones_ralenti", "OSCILAN_SOLAS")],
        "entonces": [("diagnostico_final",
                      "Los síntomas apuntan directamente a una válvula IAC sucia o defectuosa. Frecuentemente, una limpieza de este componente puede solucionar el problema sin necesidad de reemplazarlo.")]
    },
    {  # REGLA 031
        "si": [
            ("diagnostico_parcial", "SOSPECHA_FALLA_ENCENDIDO_MISFIRE"), "y",
            ("estado_cables_bobinas", "EN_BUEN_ESTADO"), "y",
            ("revoluciones_ralenti", "ESTABLES_PERO_TIEMBLA")
        ],
        "entonces": [("diagnostico_final",
                      "La falla podría ser una bobina de encendido específica o un inyector de combustible sucio. Se recomienda escanear el vehículo para obtener los códigos de falla y determinar el cilindro exacto del problema.")]
    },

    # Falla 7: Check Engine
    {  # REGLA 032
        "si": [("luz_check_engine", "ENCENDIDA_FIJA")],
        "entonces": [("diagnostico_final",
                      "El sistema ha detectado una falla. No es una emergencia crítica, pero indica un problema que afecta las emisiones o el rendimiento del motor. Se recomienda escanear los códigos de falla (DTCs) para un diagnóstico preciso.")]
    },
    {  # REGLA 033
        "si": [("luz_check_engine", "ENCENDIDA_FIJA"), "y", ("tapon_combustible", "SUELTO_O_MAL_CERRADO")],
        "entonces": [("diagnostico_final",
                      "Una causa muy común para la luz de Check Engine es un tapón de combustible mal cerrado. Apriételo correctamente. La luz puede tardar varios ciclos de conducción en apagarse por sí sola.")]
    },
    {  # REGLA 034
        "si": [("luz_check_engine", "PARPADEANDO")],
        "entonces": [("condicion", "FALLA_CRITICA_MISFIRE_SEVERO")]
    },
    {  # REGLA 035
        "si": [("condicion", "FALLA_CRITICA_MISFIRE_SEVERO")],
        "entonces": [("diagnostico_final",
                      "¡ADVERTENCIA GRAVE! La luz parpadeante indica un fallo de encendido severo que puede destruir el catalizador. Reduzca la velocidad y evite acelerar bruscamente. Si es posible, detenga el vehículo en un lugar seguro y apague el motor. Se requiere atención mecánica urgente.")]
    },

    # (Continuación Módulo 3: Sensores)
    {  # REGLA 038
        "si": [("estado_motor", "GIRA_PERO_NO_ARRANCA"), "y", ("tacometro_en_arranque", "NO_MARCA_RPM")],
        "entonces": [("diagnostico_final",
                      "Falla probable en el Sensor de Posición del Cigüeñal (CKP). El computador no detecta que el motor está girando y no activa la chispa ni la inyección.")]
    },
    {  # REGLA 039
        "si": [
            ("arranque_en_frio", "TARDA_MUCHO"), "y",
            ("ralenti_motor", "INESTABLE"), "y",
            ("luz_check_engine", "ENCENDIDA_FIJA")
        ],
        "entonces": [("diagnostico_final",
                      "Síntomas consistentes con una falla en el Sensor de Posición del Árbol de Levas (CMP). Se requiere escaneo para confirmar.")]
    },
    {  # REGLA 040
        "si": [
            ("consumo_combustible", "ELEVADO"), "y",
            ("rendimiento_motor", "TITUBEA_AL_ACELERAR"), "y",
            ("humo_escape", "NEGRO")
        ],
        "entonces": [("diagnostico_final",
                      "Posible falla en el Sensor de Flujo de Aire (MAF) o el Sensor de Oxígeno (O2), causando una mezcla de combustible incorrecta (demasiado rica).")]
    },
    {  # REGLA 041
        "si": [("luz_check_engine", "ENCENDIDA_FIJA"), "y", ("rendimiento_combustible", "EMPEORADO_NOTABLEMENTE")],
        "entonces": [("diagnostico_final",
                      "Un Sensor de Oxígeno (O2) defectuoso es una causa común. Este sensor es crucial para la eficiencia del combustible.")]
    },

    # --- MÓDULO 4: PROBLEMAS MECÁNICOS MAYORES ---

    # Falla 8: Correa de distribución
    {  # REGLA 036
        "si": [("estado_motor", "SE_APAGO_EN_MARCHA"), "y", ("sonido_arranque", "ANORMALMENTE_RAPIDO")],
        "entonces": [("diagnostico_parcial", "SOSPECHA_ALTA_CORREA_DISTRIBUCION_ROTA")]
    },
    {  # REGLA 037
        "si": [("diagnostico_parcial", "SOSPECHA_ALTA_CORREA_DISTRIBUCION_ROTA")],
        "entonces": [("diagnostico_final",
                      "¡ALERTA MÁXIMA! Los síntomas son altamente consistentes con una correa de distribución rota. NO INTENTE ARRANCAR EL MOTOR DE NUEVO. Si su motor es de tipo 'interferencia', cada intento de arranque puede causar daños catastróficos al golpear los pistones con las válvulas. El vehículo necesita ser remolcado a un taller para inspección. Esta es una falla mecánica grave.")]
    },

    # --- MÓDULO 5: SISTEMA DE LUBRICACIÓN (ACEITE) ---
    {  # REGLA 042
        "si": [("luz_presion_aceite", "ENCENDIDA")],
        "entonces": [("diagnostico_final",
                      "¡PELIGRO! DETENGA EL MOTOR INMEDIATAMENTE. Conducir sin presión de aceite causará daños catastróficos al motor. Verifique el nivel de aceite. Si el nivel es correcto, no arranque el motor y solicite asistencia.")]
    },
    {  # REGLA 043
        "si": [("ruido_motor", "GOLPETEO_METALICO_KNOCKING")],
        "entonces": [("diagnostico_final",
                      "Ruido grave que puede indicar nivel de aceite muy bajo, falla de la bomba de aceite o desgaste severo de componentes internos como los cojinetes de biela. Revise el nivel de aceite urgentemente.")]
    },
    {  # REGLA 044
        "si": [("humo_escape", "AZULADO")],
        "entonces": [("diagnostico_final",
                      "El motor está quemando aceite. Causa probable: anillos de pistón desgastados o sellos de válvulas defectuosos.")]
    },
    {  # REGLA 045
        "si": [("nivel_aceite", "BAJO_CONSTANTEMENTE"), "y", ("fuga_aceite_visible", "si")],
        "entonces": [("diagnostico_final",
                      "Fuga de aceite activa. Causas comunes: junta del cárter, retén del cigüeñal o tapón de drenaje mal apretado.")]
    },
    {  # REGLA 046
        "si": [("aspecto_aceite_motor", "CAFE_CON_LECHE_GRUMOSO")],
        "entonces": [("diagnostico_final",
                      "Contaminación de aceite con anticongelante. Confirma una junta de culata dañada o una fisura interna. No conduzca el vehículo.")]
    },
    {  # REGLA 047
        "si": [("ruido_motor", "TAQUETES_TIC_TIC_TIC")],
        "entonces": [("diagnostico_final",
                      "Posible nivel bajo de aceite o aceite muy viscoso/sucio. Los buzos hidráulicos no se están cargando correctamente. Realice un cambio de aceite.")]
    },

    # --- MÓDULO 6: SISTEMA DE FRENOS ---
    {  # REGLA 048
        "si": [("ruido_frenos", "CHILLIDO_AGUDO_INTERMITENTE")],
        "entonces": [("diagnostico_final",
                      "Los indicadores de desgaste de las pastillas de freno están sonando. Es el aviso para reemplazarlas pronto.")]
    },
    {  # REGLA 049
        "si": [("ruido_frenos", "ROCE_METALICO_GRINDING")],
        "entonces": [("diagnostico_final",
                      "¡ATENCIÓN! Las pastillas de freno están completamente gastadas. El metal de la pastilla está rozando contra el disco, dañándolo. Se requiere reparación inmediata.")]
    },
    {  # REGLA 050
        "si": [("sensacion_pedal_freno", "ESPONJOSO_O_HASTA_EL_FONDO")],
        "entonces": [("diagnostico_final",
                      "Pérdida de presión en el sistema. Causa probable: aire en las líneas de freno, nivel bajo de líquido de frenos o una fuga en el sistema. El vehículo no es seguro para conducir.")]
    },
    {  # REGLA 051
        "si": [("comportamiento_vehiculo_frenar", "SE_DESVIA_HACIA_UN_LADO")],
        "entonces": [("diagnostico_final",
                      "Frenado desigual. Causa probable: un cáliper de freno atascado, una manguera de freno obstruida o pastillas de freno contaminadas en un lado.")]
    },
    {  # REGLA 052
        "si": [("sensacion_pedal_freno", "VIBRA_O_PULSA_ALTA_VELOCIDAD")],
        "entonces": [("diagnostico_final",
                      "Discos de freno (rotores) alabeados o deformados. Se requiere rectificación o reemplazo de los discos.")]
    },
    {  # REGLA 053
        "si": [("luz_advertencia_frenos", "ENCENDIDA"), "o", ("luz_advertencia_abs", "ENCENDIDA")],
        "entonces": [("diagnostico_final",
                      "El sistema ha detectado una falla en el sistema de frenos antibloqueo (ABS) o en el nivel de líquido. Aunque los frenos básicos pueden funcionar, el ABS no lo hará. Se recomienda escaneo.")]
    },
    {  # REGLA 054
        "si": [("sensacion_pedal_freno", "MUY_DURO")],
        "entonces": [("diagnostico_final",
                      "Falla en el servofreno (booster). Posible fuga de vacío en el sistema que asiste al frenado.")]
    },

    # --- MÓDULO 7: SISTEMA ELÉCTRICO (BATERÍA Y ALTERNADOR) ---
    {  # REGLA 055
        "si": [("estado_arranque", "NO_HAY_LUCES_NI_SONIDO"), "o", ("estado_arranque", "SOLO_UN_CLIC")],
        "entonces": [("diagnostico_final",
                      "Batería completamente descargada o una mala conexión en los terminales. Revise si los postes de la batería están limpios y apretados.")]
    },
    {  # REGLA 056
        "si": [("estado_arranque", "MOTOR_GIRA_LENTO")],
        "entonces": [("diagnostico_final",
                      "Batería débil o con poca carga. Es posible que no tenga suficiente fuerza para arrancar el motor.")]
    },
    {  # REGLA 057
        "si": [("luz_bateria", "ENCENDIDA_MIENTRAS_CONDUCE")],
        "entonces": [("diagnostico_final",
                      "El sistema de carga está fallando. El alternador no está recargando la batería. Conduzca a un taller cercano antes de que el coche se apague.")]
    },
    {  # REGLA 058
        "si": [("comportamiento_luces", "BAJAN_INTENSIDAD_EN_RALENTI")],
        "entonces": [("diagnostico_final",
                      "Síntoma clásico de un alternador que está empezando a fallar y no genera suficiente corriente a bajas RPM.")]
    },
    {  # REGLA 059
        "si": [("edad_bateria", "MAS_DE_4_AÑOS"), "y", ("arranque_en_frio", "TARDA_EN_ARRANCAR")],
        "entonces": [("diagnostico_final",
                      "La batería ha llegado al final de su vida útil. Probablemente necesita ser reemplazada.")]
    },
    {  # REGLA 060
        "si": [("terminales_bateria", "CORROSION_BLANCA_O_VERDOSA")],
        "entonces": [("diagnostico_final",
                      "Conexión deficiente debido a la sulfatación. Limpiar los terminales con un cepillo y una mezcla de bicarbonato y agua puede restaurar la conexión.")]
    },
    {  # REGLA 061
        "si": [("comportamiento_post_arranque_puente", "SE_APAGA_AL_DESCONECTAR_CABLES")],
        "entonces": [("diagnostico_final",
                      "El alternador está completamente dañado. El motor solo funcionaba con la energía del otro vehículo.")]
    },

    # --- MÓDULO 8: SUSPENSIÓN, DIRECCIÓN Y NEUMÁTICOS ---
    {  # REGLA 062
        "si": [("ruido_suspension", "GOLPETEO_SECO_CLUNK_EN_BACHES")],
        "entonces": [("diagnostico_final",
                      "Ruido característico de componentes de suspensión desgastados. Sospechosos principales: bieletas de la barra estabilizadora, bujes o rótulas.")]
    },
    {  # REGLA 063
        "si": [("comportamiento_vehiculo", "REBOTA_EXCESIVAMENTE_EN_BACHES")],
        "entonces": [("diagnostico_final",
                      "Amortiguadores o struts desgastados. Han perdido su capacidad de controlar el movimiento del resorte.")]
    },
    {  # REGLA 064
        "si": [("sensacion_volante", "VIBRA_A_CIERTAS_VELOCIDADES")],
        "entonces": [("diagnostico_final",
                      "La causa más probable es un desbalanceo en las llantas delanteras. Requiere balanceo en un taller.")]
    },
    {  # REGLA 065
        "si": [("comportamiento_vehiculo", "SE_DESVIA_HACIA_UN_LADO_EN_RECTA")],
        "entonces": [("diagnostico_final",
                      "Problema de alineación de las ruedas. También puede ser causado por presión de aire desigual en las llantas.")]
    },
    {  # REGLA 066
        "si": [("ruido_vehiculo", "ZUMBIDO_O_RUGIDO_AUMENTA_CON_VELOCIDAD")],
        "entonces": [("diagnostico_final",
                      "Ruido típico de un balero (rodamiento) de rueda dañado. El ruido puede cambiar al dar vueltas.")]
    },
    {  # REGLA 067
        "si": [("ruido_direccion", "CHASQUIDO_AL_GIRAR_POR_COMPLETO")],
        "entonces": [("diagnostico_final",
                      "Síntoma clásico de una junta homocinética (CV joint) dañada, especialmente en vehículos de tracción delantera.")]
    },
    {  # REGLA 068
        "si": [("desgaste_llantas", "IRREGULAR_INTERIOR_O_EXTERIOR")],
        "entonces": [("diagnostico_final",
                      "Desgaste anormal causado por mala alineación. Un desgaste en el centro indica sobreinflado; en los bordes, bajo inflado.")]
    },
    {  # REGLA 069
        "si": [("ruido_direccion", "GEMIDO_O_ZUMBIDO_AL_GIRAR_VOLANTE")],
        "entonces": [
            ("diagnostico_final", "Nivel bajo de líquido en la dirección hidráulica o bomba de dirección fallando.")]
    },

    # --- MÓDULO 9: SISTEMA DE ESCAPE ---
    {  # REGLA 070
        "si": [("ruido_escape", "MUCHO_MAS_RUIDOSO_TIPO_TRACTOR")],
        "entonces": [
            ("diagnostico_final", "Fuga en el sistema de escape. Causa probable: silenciador o tubería picada o rota.")]
    },
    {  # REGLA 071
        "si": [("ruido_escape", "CASCABEL_METALICO_DEBAJO_DEL_COCHE")],
        "entonces": [
            ("diagnostico_final", "El interior del catalizador o de un silenciador se ha desprendido y está suelto.")]
    },
    {  # REGLA 072
        "si": [("olor_cabina", "GASES_DE_ESCAPE")],
        "entonces": [("diagnostico_final",
                      "PELIGROSO. Indica una fuga de escape cerca de la parte delantera del vehículo. Estos gases contienen monóxido de carbono. Ventile la cabina y repare de inmediato.")]
    },
    {  # REGLA 073
        "si": [("rendimiento_motor", "PERDIDA_POTENCIA_NOTABLE"), "y", ("ruido_escape", "SONIDO_TAPADO")],
        "entonces": [("diagnostico_final",
                      "Obstrucción en el sistema de escape, probablemente un catalizador tapado. Impide que los gases salgan libremente.")]
    },

    # --- MÓDULO 10: TRANSMISIÓN (BÁSICO) ---
    {  # REGLA 074
        "si": [("tipo_transmision", "AUTOMATICA"), "y", ("cambio_marcha", "GOLPE_FUERTE_AL_CAMBIAR_P_D_R")],
        "entonces": [("diagnostico_final",
                      "Puede indicar soportes de motor/transmisión dañados o un problema interno. Revise el nivel y estado del fluido de transmisión.")]
    },
    {  # REGLA 075
        "si": [("tipo_transmision", "AUTOMATICA"), "y",
               ("comportamiento_transmision", "MOTOR_ACELERA_PERO_COCHE_NO_AVANZA")],
        "entonces": [("diagnostico_final",
                      "Nivel bajo de fluido de transmisión o desgaste interno severo. Es un síntoma grave.")]
    },
    {  # REGLA 076
        "si": [("tipo_transmision", "MANUAL"), "y", ("sensacion_clutch", "ESPONJOSO_O_HASTA_EL_FONDO")],
        "entonces": [("diagnostico_final", "Falla en el sistema hidráulico del clutch (bomba o collarín).")]
    },
    {  # REGLA 077
        "si": [("tipo_transmision", "MANUAL"), "y",
               ("comportamiento_transmision", "MOTOR_REVOLUCIONA_PERO_VELOCIDAD_NO_AUMENTA")],
        "entonces": [
            ("diagnostico_final", "El clutch (embrague) está patinando debido al desgaste. Necesita ser reemplazado.")]
    },

    # --- MÓDULO 11: PROFUNDIZACIÓN EN FALLAS DE SENSORES ---

    # Sensor de Temperatura de Refrigerante (ECT)
    {  # REGLA 078
        "si": [
            ("arranque_en_frio", "TARDA_EN_ARRANCAR"), "y",
            ("humo_escape", "NEGRO_AL_ARRANCAR"), "y",
            ("consumo_combustible", "ELEVADO")
        ],
        "entonces": [("diagnostico_final",
                      "Falla probable del Sensor de Temperatura del Refrigerante (ECT), que está 'atascado' en una lectura caliente. La computadora inyecta menos combustible del necesario para un arranque en frío.")]
    },
    {  # REGLA 079
        "si": [("ventilador_radiador", "SE_ENCIENDE_INMEDIATAMENTE_EN_FRIO"), "o",
               ("ventilador_radiador", "NO_SE_APAGA_NUNCA")],
        "entonces": [("diagnostico_final",
                      "El Sensor de Temperatura del Refrigerante (ECT) probablemente está enviando una señal errónea de sobrecalentamiento constante. La computadora activa el ventilador como medida de protección.")]
    },
    {  # REGLA 080
        "si": [
            ("condicion", "SE_SOBRECALIENTA"), "y",
            ("ventilador_radiador", "NO_SE_ACTIVA"), "y",
            ("luz_check_engine", "ENCENDIDA")
        ],
        "entonces": [("diagnostico_final",
                      "Posible falla del Sensor de Temperatura del Refrigerante (ECT). Si el sensor no informa a la computadora que el motor está caliente, esta nunca activará los ventiladores.")]
    },
    {  # REGLA 081
        "si": [
            ("rendimiento_combustible", "POBRE"), "y",
            ("rendimiento_motor", "PEREZOSO"), "y",
            ("ralenti_motor", "LIGERAMENTE_ALTO")
        ],
        "entonces": [("diagnostico_final",
                      "Síntomas consistentes con un Sensor ECT 'atascado' en una lectura fría. La computadora mantiene una mezcla de combustible rica permanentemente, como si el motor nunca alcanzara su temperatura óptima.")]
    },

    # Sensor de Presión de Aceite (OPS)
    {  # REGLA 082
        "si": [
            ("luz_presion_aceite", "PARPADEA_O_SE_ENCIENDE_INTERMITENTE"), "y",
            ("ruido_motor", "NORMAL")
        ],
        "entonces": [("diagnostico_final",
                      "Probable falla del Sensor de Presión de Aceite (OPS) o su cableado. Un sensor defectuoso puede dar lecturas falsas a bajas RPM. Sin embargo, por precaución, verifique el nivel de aceite inmediatamente.")]
    },
    {  # REGLA 083
        "si": [
            ("luz_presion_aceite", "PERMANECE_ENCENDIDA"), "y",
            ("nivel_aceite", "CORRECTO"), "y",
            ("ruido_motor", "NORMAL")
        ],
        "entonces": [("diagnostico_final",
                      "Alta probabilidad de que el Sensor de Presión de Aceite (OPS) esté defectuoso y necesite ser reemplazado. Es una falla común y es el primer paso antes de sospechar de problemas mecánicos graves.")]
    },
    {  # REGLA 084
        "si": [("indicador_presion_aceite", "MARCA_CERO_O_MAXIMO_IRREAL")],
        "entonces": [("diagnostico_final",
                      "Falla eléctrica del Sensor de Presión de Aceite (OPS) o del indicador en el tablero. El sensor no está enviando una señal coherente.")]
    },

    # Sensor de Posición del Acelerador (TPS)
    {  # REGLA 085
        "si": [("rendimiento_motor", "ACELERA_ERRATICAMENTE_O_DA_TIRONES")],
        "entonces": [("diagnostico_final",
                      "El Sensor de Posición del Acelerador (TPS) puede tener 'puntos muertos' o zonas donde la señal se corta, causando una aceleración no deseada o vacilante.")]
    },
    {  # REGLA 086
        "si": [("tipo_transmision", "AUTOMATICA"), "y", ("cambio_marcha", "CAMBIOS_BRUSCOS_O_A_DESTIEMPO")],
        "entonces": [("diagnostico_final",
                      "Un Sensor TPS defectuoso envía información incorrecta a la computadora de la transmisión, que no sabe cuándo realizar los cambios de marcha de manera suave. Es una causa común de problemas de cambio.")]
    },
    {  # REGLA 087
        "si": [("rendimiento_motor", "NO_ACELERA_O_RESPONDE_LENTO")],
        "entonces": [("diagnostico_final",
                      "Falla grave en el Sensor de Posición del Acelerador (TPS). La computadora no está recibiendo la señal de cuánto está pisando el conductor el acelerador y, por seguridad, limita la respuesta del motor.")]
    },
    {  # REGLA 088
        "si": [("ralenti_motor", "MUY_ALTO_Y_NO_BAJA")],
        "entonces": [("diagnostico_final",
                      "El Sensor TPS podría estar atascado enviando una señal de que el acelerador está parcialmente presionado, aunque no lo esté. Esto provoca que la computadora mantenga el motor acelerado.")]
    },
    {  # REGLA 089
        "si": [
            ("luz_check_engine", "ENCENDIDA"), "y",
            ("problemas_conduccion", "ACELERACION_Y_CAMBIOS_DE_MARCHA_ERRATICOS")
        ],
        "entonces": [("diagnostico_final",
                      "El conjunto de síntomas apunta fuertemente a una falla del Sensor TPS. Se recomienda un escaneo para confirmar el código de falla correspondiente (ej. P0120 a P0124).")]
    },
    {  # REGLA 090
        "si": [("rendimiento_motor", "PIERDE_Y_RECUPERA_POTENCIA_REPENTINAMENTE")],
        "entonces": [("diagnostico_final",
                      "Intermitencia en la señal del Sensor TPS. El cableado o el propio sensor pueden estar fallando, causando que la computadora reciba y pierda la señal de la posición del acelerador momentáneamente.")]
    },

    # --- MÓDULO 12: DIAGNÓSTICO BASADO EN CÓDIGOS DE FALLA (DTCS) ---

    # Misfire (P0300-P0308)
    {  # REGLA 091
        "si": [("codigo_falla", "P0300")],
        "entonces": [("diagnostico_final",
                      "Falla de encendido en cilindros aleatorios (P0300). El problema afecta al motor de forma general. Causas comunes: presión de combustible baja, fuga de vacío masiva, o un sensor de cigüeñal (CKP) defectuoso.")]
    },
    {  # REGLA 092
        "si": [("codigo_falla", "P030X")],
        "entonces": [("diagnostico_parcial", "FALLA_CILINDRO_ESPECIFICO"), ("cilindro_afectado", "X")]
    },
    {  # REGLA 093
        "si": [("diagnostico_parcial", "FALLA_CILINDRO_ESPECIFICO")],
        "entonces": [("diagnostico_final",
                      "Falla de encendido detectada en el cilindro [X]. El problema está aislado. Sospechosos principales: bujía, cable de bujía, bobina de encendido o inyector de combustible de ese cilindro.")]
    },
    {  # REGLA 094
        "si": [("diagnostico_parcial", "FALLA_CILINDRO_ESPECIFICO")],
        "entonces": [("accion_recomendada",
                      "Intercambie la bobina de encendido del cilindro [X] con la de un cilindro vecino. Borre los códigos y conduzca. Si la falla se mueve al nuevo cilindro (ej. P0303), ha confirmado que la bobina está defectuosa.")]
    },
    {  # REGLA 095
        "si": [("diagnostico_parcial", "FALLA_CILINDRO_ESPECIFICO"), "y", ("diagnostico_bobina", "BUEN_ESTADO")],
        "entonces": [("accion_recomendada",
                      "El siguiente paso es revisar o reemplazar la bujía del cilindro [X]. Si el problema persiste, el inyector de combustible de ese cilindro podría estar obstruido o defectuoso.")]
    },

    # Catalizador (P0420)
    {  # REGLA 096
        "si": [("codigo_falla", "P0420")],
        "entonces": [("diagnostico_parcial", "P0420_DETECTADO")]
    },
    {  # REGLA 097
        "si": [("diagnostico_parcial", "P0420_DETECTADO"), "y", ("existen_otros_codigos_falla", "si")],
        "entonces": [("diagnostico_final",
                      "El código P0420 es probablemente una consecuencia de otro problema. Solucione primero las fallas de encendido ('misfires') o de mezcla de combustible, ya que estas pueden dañar el catalizador.")]
    },
    {  # REGLA 098
        "si": [("diagnostico_parcial", "P0420_DETECTADO"), "y", ("existen_otros_codigos_falla", "no")],
        "entonces": [("diagnostico_final",
                      "Posibles causas del P0420: un sensor de oxígeno (O2) defectuoso (el posterior al catalizador), una fuga en el sistema de escape, o finalmente, el propio catalizador dañado.")]
    },
    {  # REGLA 099
        "si": [("diagnostico_parcial", "P0420_DETECTADO")],
        "entonces": [("accion_recomendada",
                      "Inspeccione visualmente el sistema de escape en busca de fugas entre los dos sensores de oxígeno. Si no hay fugas, considere reemplazar el sensor de oxígeno trasero antes de cambiar el costoso convertidor catalítico.")]
    },

    # Mezcla de Combustible (P0171, P0172)
    {  # REGLA 100
        "si": [("codigo_falla", "P0171")],
        "entonces": [("diagnostico_parcial", "MEZCLA_POBRE_P0171")]
    },
    {  # REGLA 101
        "si": [("diagnostico_parcial", "MEZCLA_POBRE_P0171"), "y", ("ruido_motor", "SILBIDO_EN_COMPARTIMENTO")],
        "entonces": [("diagnostico_final",
                      "Alta probabilidad de una fuga de vacío (P0171). Revise todas las mangueras de vacío conectadas al múltiple de admisión en busca de grietas o desconexiones.")]
    },
    {  # REGLA 102
        "si": [("diagnostico_parcial", "MEZCLA_POBRE_P0171"), "y", ("fuga_vacio_aparente", "no")],
        "entonces": [("diagnostico_final",
                      "Otras causas comunes de P0171 (Mezcla Pobre) son un sensor de flujo de aire (MAF) sucio, una bomba de combustible débil o inyectores de combustible obstruidos.")]
    },
    {  # REGLA 103
        "si": [("codigo_falla", "P0172")],
        "entonces": [("diagnostico_parcial", "MEZCLA_RICA_P0172")]
    },
    {  # REGLA 104
        "si": [("diagnostico_parcial", "MEZCLA_RICA_P0172"), "y", ("olor_escape", "FUERTE_A_GASOLINA")],
        "entonces": [("diagnostico_final",
                      "Causas probables de P0172 (Mezcla Rica): un inyector de combustible atascado en posición abierta ('chorreando'), un regulador de presión de combustible defectuoso, o un sensor de oxígeno (O2) fallando.")]
    },
    {  # REGLA 105
        "si": [("codigo_falla", "P0171"), "o", ("codigo_falla", "P0172")],
        "entonces": [("accion_recomendada",
                      "Limpiar el sensor de flujo de aire (MAF) con un limpiador especializado es un primer paso de mantenimiento sencillo y de bajo costo que puede solucionar problemas de mezcla de combustible.")]
    },

    # --- MÓDULO 13: SISTEMA DE AIRE ACONDICIONADO (A/C) ---

    # A/C no enfría
    {  # REGLA 106
        "si": [("ac_estado", "ENCENDIDO"), "y", ("ac_aire", "NO_ES_FRIO"), "y", ("ac_compresor", "NO_SE_ACTIVA")],
        "entonces": [("diagnostico_final",
                      "El compresor del A/C no está enganchando. Causa más probable: nivel de refrigerante muy bajo (el presostato lo protege), fusible del A/C quemado, o un relevador (relay) defectuoso.")]
    },
    {  # REGLA 107
        "si": [("ac_aire", "ENFRIA_DEBILMENTE"), "y", ("ac_rendimiento", "MEJORA_AL_ACELERAR")],
        "entonces": [("diagnostico_final",
                      "Síntoma clásico de una carga de refrigerante baja. El sistema aún tiene algo de gas, pero no lo suficiente para enfriar eficientemente en ralentí.")]
    },
    {  # REGLA 108
        "si": [("ac_rendimiento", "ENFRIA_BIEN_EN_CARRETERA"), "y", ("ac_rendimiento", "DEJA_DE_ENFRIAR_EN_TRAFICO")],
        "entonces": [("diagnostico_final",
                      "El problema está en el flujo de aire a través del condensador. Verifique que el motoventilador del radiador se active cuando enciende el A/C. Si no lo hace, la falla está en el sistema del ventilador.")]
    },
    {  # REGLA 109
        "si": [("ac_estado", "ENCENDIDO"), "y", ("ac_compresor", "CICLOS_MUY_RAPIDOS")],
        "entonces": [("diagnostico_final",
                      "Esto usualmente indica una carga de refrigerante baja. El presostato detecta baja presión y apaga el compresor para protegerlo, luego la presión se estabiliza y vuelve a encender, repitiendo el ciclo.")]
    },
    {  # REGLA 110
        "si": [("ac_aire", "CALIENTE"), "y", ("ac_linea_aluminio", "CONGELADA")],
        "entonces": [("diagnostico_final",
                      "Posible obstrucción en el sistema de A/C, como en la válvula de expansión o el filtro deshidratador. El refrigerante no circula correctamente.")]
    },
    {  # REGLA 111
        "si": [("ac_aire", "NO_ENFRIA"), "y", ("ac_flujo_aire_ventilas", "DEBIL")],
        "entonces": [("diagnostico_final",
                      "El problema no es el sistema de A/C en sí, sino el flujo de aire. Causa más probable: un filtro de aire de cabina extremadamente sucio y obstruido.")]
    },
    {  # REGLA 112
        "si": [("ac_aire", "FRIO_POR_UN_LADO_CALIENTE_POR_OTRO")],
        "entonces": [("diagnostico_final",
                      "Falla en el sistema de control de clima, probablemente una compuerta de mezcla (blend door) atascada o su actuador defectuoso. También puede indicar una carga de refrigerante muy baja en algunos sistemas.")]
    },

    # Ruidos y Fugas A/C
    {  # REGLA 113
        "si": [("ac_ruido", "ROZAMIENTO_O_ZUMBIDO_FUERTE_CON_AC_ENCENDIDO")],
        "entonces": [("diagnostico_final",
                      "El compresor del A/C tiene un daño interno. El ruido es el mecanismo fallando. Se recomienda apagar el A/C para evitar una falla mayor.")]
    },
    {  # REGLA 114
        "si": [("ac_ruido", "BALERO_O_CHILLIDO_CONSTANTE_CON_AC_APAGADO")],
        "entonces": [("diagnostico_final",
                      "El balero (rodamiento) de la polea del clutch del compresor está dañado. La polea gira siempre con la banda del motor, aunque el A/C esté apagado.")]
    },
    {  # REGLA 115
        "si": [("ac_ruido", "GOLPETEO_METALICO_AL_ENCENDER_AC")],
        "entonces": [("diagnostico_final",
                      "El clutch del compresor está fallando. El ruido es el electroimán intentando enganchar el plato, pero este patina o está dañado.")]
    },
    {  # REGLA 116
        "si": [("ac_rendimiento", "DEJO_DE_ENFRIAR_PROGRESIVAMENTE")],
        "entonces": [("diagnostico_final",
                      "Existe una fuga lenta de refrigerante en el sistema. Es la causa más común de pérdida de rendimiento del A/C.")]
    },
    {  # REGLA 117
        "si": [("ac_fuga_visible", "MANCHAS_ACEITE_VERDOSO_AMARILLENTO")],
        "entonces": [("diagnostico_final",
                      "Se ha detectado el punto de fuga de refrigerante. El gas refrigerante contiene un aceite lubricante con un tinte UV para facilitar la detección de fugas.")]
    },
    {  # REGLA 118
        "si": [("olor_cabina", "QUIMICO_DULZON_CON_AC")],
        "entonces": [("diagnostico_final",
                      "Posible fuga de refrigerante en el evaporador, que se encuentra dentro del tablero. Es una reparación compleja.")]
    },

    # A/C Eléctrico
    {  # REGLA 119
        "si": [("ac_control", "BOTON_AC_NO_ILUMINA_O_NO_RESPONDE")],
        "entonces": [("diagnostico_final",
                      "Falla en el panel de control de clima o en su fusible. El sistema no está recibiendo la orden de encendido.")]
    },
    {  # REGLA 120
        "si": [("ac_ventilador_interior", "SOLO_FUNCIONA_EN_VELOCIDAD_ALTA")],
        "entonces": [("diagnostico_final",
                      "La resistencia del motor soplador está quemada. Es una falla eléctrica común que impide que el ventilador funcione a velocidades bajas o medias.")]
    },

    # --- MÓDULO 14: SISTEMA DE EMISIONES (EGR Y EVAP) ---

    # Válvula EGR
    {  # REGLA 121
        "si": [("ralenti_motor", "MUY_INESTABLE_O_SE_APAGA"), "y", ("rendimiento_motor", "MEJORA_AL_ACELERAR")],
        "entonces": [("diagnostico_final",
                      "Síntomas clásicos de una válvula EGR atascada en posición abierta. Está permitiendo que los gases de escape entren al motor en ralentí, cuando no debería, ahogando la combustión.")]
    },
    {  # REGLA 122
        "si": [("ruido_motor", "CASCABELEO_O_PINGING_AL_ACELERAR"), "y",
               ("rendimiento_motor", "NORMAL_EN_OTRAS_CONDICIONES")],
        "entonces": [("diagnostico_final",
                      "Posible válvula EGR atascada en posición cerrada. No está recirculando los gases para enfriar la combustión, lo que provoca detonaciones (pinging) bajo carga.")]
    },
    {  # REGLA 123
        "si": [("codigo_falla", "P0401")],
        "entonces": [("diagnostico_final",
                      "Código P0401 (Flujo EGR Insuficiente). Causa más común: los conductos de la válvula EGR o el múltiple están obstruidos por carbón, o la propia válvula está atascada cerrada.")]
    },
    {  # REGLA 124
        "si": [("codigo_falla", "P0404")],
        "entonces": [("diagnostico_final",
                      "Código P0404 (Rango/Rendimiento Circuito EGR). Indica un problema con el sensor de posición de la válvula EGR o el circuito eléctrico. La computadora no puede determinar si la válvula está abierta o cerrada correctamente.")]
    },

    # Sistema EVAP
    {  # REGLA 125
        "si": [("luz_check_engine", "ENCENDIDA"), "y", ("sintomas_conduccion", "no")],
        "entonces": [("diagnostico_final",
                      "Una falla en el sistema EVAP es una causa muy probable. La primera y más simple verificación es asegurarse de que el tapón del tanque de combustible esté bien apretado.")]
    },
    {  # REGLA 126
        "si": [("codigo_falla", "P0442")],
        "entonces": [("diagnostico_final",
                      "Código P0442 (Fuga Pequeña EVAP). Revise el sello de goma del tapón de combustible en busca de grietas. Si está bien, inspeccione visualmente las mangueras de vacío del sistema EVAP en busca de pequeñas fisuras.")]
    },
    {  # REGLA 127
        "si": [("codigo_falla", "P0455")],
        "entonces": [("diagnostico_final",
                      "Código P0455 (Fuga Grande EVAP). Causa más probable: el tapón del combustible no está puesto o está completamente suelto, o una manguera principal del sistema EVAP está desconectada.")]
    },
    {  # REGLA 128
        "si": [("olor_vehiculo", "COMBUSTIBLE_ALREDEDOR_DEL_COCHE")],
        "entonces": [("diagnostico_final",
                      "Indica una fuga de vapores de combustible. Puede ser una manguera del sistema EVAP rota, el cánister agrietado, o un sello defectuoso en la bomba de combustible.")]
    },
    {  # REGLA 129
        "si": [("ralenti_motor", "INESTABLE_JUSTO_DESPUES_DE_CARGAR_COMBUSTIBLE")],
        "entonces": [("diagnostico_final",
                      "Posible válvula de purga del cánister (Purge Solenoid) atascada en posición abierta. Está permitiendo que los vapores de combustible entren al motor de forma incontrolada.")]
    },
    {  # REGLA 130
        "si": [("problema_carga_combustible", "PISTOLA_SE_BOTA_CONSTANTEMENTE")],
        "entonces": [("diagnostico_final",
                      "Obstrucción en el sistema de ventilación del tanque. Causa común: una válvula de ventilación (Vent Solenoid) atascada en posición cerrada o el cánister de carbón saturado.")]
    },
    {  # REGLA 131
        "si": [("codigo_falla", "P0443")],
        "entonces": [("diagnostico_final",
                      "Código P0443 (Circuito Válvula de Purga EVAP). Falla eléctrica en el circuito de la válvula de purga. El problema no es una fuga, sino la propia válvula o su cableado.")]
    },
    {  # REGLA 132
        "si": [("estado_arranque", "DIFICULTAD_PARA_ARRANCAR_DESPUES_DE_CARGAR_COMBUSTIBLE")],
        "entonces": [("diagnostico_final",
                      "Síntoma clásico de un cánister de carbón saturado de combustible líquido. Esto ocurre cuando la válvula de purga falla o se sobrellena el tanque repetidamente, enviando gasolina cruda al cánister que fue diseñado solo para vapores.")]
    },
    {  # REGLA 133
        "si": [("hallazgo_inspeccion", "GRANULOS_NEGROS_EN_MANGUERAS_EVAP")],
        "entonces": [("diagnostico_final",
                      "El cánister de carbón se ha roto internamente. Estos gránulos pueden viajar por las líneas y dañar las válvulas solenoide. El cánister necesita ser reemplazado.")]
    },
    {  # REGLA 134
        "si": [("codigo_falla", "P0456")],
        "entonces": [("diagnostico_final",
                      "Código P0456 (Fuga Muy Pequeña EVAP). Estas son las más difíciles de encontrar y pueden ser causadas por una fisura minúscula en una manguera o un sello de O-ring resecado.")]
    },
    {  # REGLA 135
        "si": [("resultado_verificacion", "FALLA_PRUEBA_EMISIONES"), "y", ("codigo_falla_evap", "si")],
        "entonces": [("diagnostico_final",
                      "El sistema EVAP es un componente clave del control de emisiones. Cualquier código de falla activo (P0442, P0455, etc.) causará una falla automática en la prueba de emisiones.")]
    },

    # --- MÓDULO 15: PROBLEMAS DE CARROCERÍA Y ELÉCTRICOS MENORES ---

    # Luces
    {  # REGLA 136
        "si": [("falla_luz", "UNA_SOLA_LUZ_EXTERIOR_NO_ENCIENDE")],
        "entonces": [("diagnostico_final",
                      "La causa más probable es un foco o bombilla fundido. Es un reemplazo sencillo y el primer paso a realizar.")]
    },
    {  # REGLA 137
        "si": [("falla_luz", "AMBAS_LUCES_BAJAS_NO_ENCIENDEN_PERO_ALTAS_SI")],
        "entonces": [("diagnostico_final",
                      "Poco probable que ambos focos se fundan a la vez. Revise el fusible correspondiente a las luces bajas. También podría ser el relevador (relay) o el interruptor del volante.")]
    },
    {  # REGLA 138
        "si": [("falla_luz", "GRUPO_DE_LUCES_NO_ENCIENDEN")],
        "entonces": [("diagnostico_final",
                      "Indica un problema en un circuito compartido. Revise el fusible que alimenta ese circuito. Si está bien, podría ser un problema de conexión a tierra (ground) para ese grupo de luces.")]
    },
    {  # REGLA 139
        "si": [("falla_luz", "DIRECCIONAL_PARPADEA_MUY_RAPIDO")],
        "entonces": [("diagnostico_final",
                      "Esto indica que uno de los focos de ese lado (delantero o trasero) está fundido. El parpadeo rápido es una advertencia del sistema.")]
    },
    {  # REGLA 140
        "si": [("falla_luz", "LUZ_INTERIOR_NO_ENCIENDE_CON_UNA_PUERTA")],
        "entonces": [("diagnostico_final",
                      "El problema probablemente está en el interruptor o sensor de esa puerta, que no está detectando que se ha abierto.")]
    },

    # Fusibles
    {  # REGLA 141
        "si": [("falla_electrica", "COMPONENTE_DEJA_DE_FUNCIONAR_REPENTINAMENTE")],
        "entonces": [("diagnostico_final",
                      "El primer paso es revisar la caja de fusibles y localizar el fusible correspondiente a ese componente. Probablemente esté quemado.")]
    },
    {  # REGLA 142
        "si": [("falla_electrica", "FUSIBLE_SE_QUEMA_INMEDIATAMENTE_AL_REEMPLAZAR")],
        "entonces": [("diagnostico_final",
                      "¡ADVERTENCIA! No instale un fusible de mayor amperaje. Esto indica un cortocircuito en ese circuito. El cable positivo está tocando tierra en algún punto, o el componente mismo (ej. motor de la ventana) está dañado.")]
    },
    {  # REGLA 143
        "si": [("falla_electrica", "FUSIBLE_SE_QUEMA_REPETIDAMENTE")],
        "entonces": [("accion_recomendada",
                      "Desconecte el componente principal de ese circuito (ej. desconecte la radio). Si el fusible ya no se quema, el problema está en el componente. Si se sigue quemando, el cortocircuito está en el cableado.")]
    },

    # Ventanas y Seguros
    {  # REGLA 144
        "si": [("falla_electrica", "UNA_SOLA_VENTANA_NO_FUNCIONA_DESDE_NINGUN_INTERRUPTOR")],
        "entonces": [("diagnostico_final",
                      "El problema está aislado a esa puerta. Causas probables: el motor de la ventana está dañado o el regulador (mecanismo de tijera) está roto.")]
    },
    {  # REGLA 145
        "si": [("falla_electrica", "VENTANA_SOLO_FUNCIONA_DESDE_CONTROL_MAESTRO")],
        "entonces": [("diagnostico_final",
                      "El motor y el cableado principal están bien. El interruptor de esa puerta específica está defectuoso.")]
    },
    {  # REGLA 146
        "si": [("falla_electrica", "TODAS_LAS_VENTANAS_NO_FUNCIONAN")],
        "entonces": [("diagnostico_final",
                      "Problema general. Revise el fusible principal o el disyuntor (circuit breaker) de las ventanas. También podría ser una falla en el interruptor maestro del lado del conductor.")]
    },
    {  # REGLA 147
        "si": [("falla_electrica", "LUCES_BAJAN_INTENSIDAD_AL_USAR_VENTANA")],
        "entonces": [("diagnostico_final",
                      "El motor de la ventana está recibiendo corriente pero está atascado o quemado. Está consumiendo mucha energía sin poder moverse.")]
    },
    {  # REGLA 148
        "si": [("falla_electrica", "UN_SEGURO_ELECTRICO_NO_FUNCIONA")],
        "entonces": [("diagnostico_final",
                      "El problema casi siempre es el actuador del seguro dentro de esa puerta, que es el pequeño motor que mueve el mecanismo.")]
    },

    # Ruidos y Filtraciones
    {  # REGLA 149
        "si": [("ruido_carroceria", "SILBIDO_O_RUIDO_VIENTO_DESDE_PUERTA")],
        "entonces": [("diagnostico_final",
                      "El sello o empaque de goma de la puerta está desgastado, aplanado o mal ajustado. No está sellando correctamente contra el marco.")]
    },
    {  # REGLA 150
        "si": [("ruido_carroceria", "RUIDO_VIENTO_DESDE_PARABRISAS")],
        "entonces": [("diagnostico_final",
                      "La moldura exterior del parabrisas puede estar suelta o desprendida, permitiendo que el aire entre y cause el ruido.")]
    },
    {  # REGLA 151
        "si": [("filtracion_agua", "HUMEDAD_EN_ALFOMBRA_DESPUES_DE_LLOVER")],
        "entonces": [("diagnostico_final",
                      "Filtración de agua. Causas comunes: drenajes del quemacocos o del área del limpiaparabrisas obstruidos, o un sello de puerta defectuoso.")]
    },
    {  # REGLA 152
        "si": [("ruido_carroceria", "RUIDO_AGUA_MOVIENDOSE_DENTRO_DE_PUERTA")],
        "entonces": [("diagnostico_final",
                      "Los orificios de drenaje en la parte inferior de la puerta están obstruidos con tierra u hojas. El agua de lluvia se ha acumulado en el interior de la puerta y necesita ser drenada.")]
    }
]