import customtkinter as ctk
import pyodbc
from threading import Thread

# --- CONFIGURACIÓN VISUAL ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class AdamGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.title("A.D.A.M. - Sistema Experto Automotriz")
        self.geometry("900x700")
        self.resizable(False, False)

        # Variables del Motor
        # --- ¡RECUERDA VERIFICAR TU SERVIDOR AQUÍ! ---
        self.CONNECTION_STRING = (
            r"DRIVER={ODBC Driver 17 for SQL Server};"
            r"SERVER=.;"
            r"DATABASE=ADAM_DB;"
            r"Trusted_Connection=yes;"
        )

        self.reglas_todas = []  # Todas las reglas cargadas de la DB
        self.reglas_activas = []  # Subconjunto de reglas que usaremos (filtradas o todas)
        self.hechos = {}
        self.modulos_disponibles = []  # Lista de nombres de módulos únicos

        self.variable_actual = None
        self.valor_esperado_actual = None

        # Mapa de Preguntas (Se mantiene igual, resumido aquí para brevedad pero funcional)
        self.mapa_preguntas = {
            # ... (PEGA AQUÍ TU DICCIONARIO COMPLETO mapa_preguntas DE ANTES) ...
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
            "arranque_en_frio_normal": "¿El arranque en frío es 'NORMAL'?",

            # Módulo 3: Encendido
            "ralenti_motor": "¿El motor en ralentí (detenido) está 'INESTABLE_O_TEMBLOROSO'?",
            "mantenimiento_bujias": "¿El mantenimiento de las bujías es 'ANTIGUO_O_DESCONOCIDO'?",
            "estado_cables_bobinas": "¿Los cables de bujía o las bobinas se ven 'AGRIETADOS_O_DAÑADOS'?",
            "revoluciones_ralenti": "¿Las revoluciones en ralentí 'OSCILAN_SOLAS' (suben y bajan)?",
            "revoluciones_ralenti_estables": "¿Las revoluciones son 'ESTABLES_PERO_EL_MOTOR_TIEMBLA'?",
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
            "ruido_motor_normal": "¿El motor 'SUENA_NORMAL', sin ruidos metálicos?",
            "nivel_aceite_correcto": "¿Verificó el nivel de aceite y está 'CORRECTO'?",

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
            "codigo_falla": "¿Ha escaneado el vehículo? ¿Tiene un código de falla?",
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

        # --- INICIALIZAR FRAMES ---
        self.frame_home = None
        self.frame_modulos = None
        self.frame_diagnostico = None

        self.crear_pantalla_home()

        # Cargar datos al inicio
        self.after(500, self.cargar_reglas)

    # --- PANTALLAS ---

    def crear_pantalla_home(self):
        # Limpiar
        self.limpiar_pantalla()

        self.frame_home = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_home.pack(fill="both", expand=True, padx=40, pady=40)

        lbl_titulo = ctk.CTkLabel(self.frame_home, text="A.D.A.M.", font=("Roboto Medium", 48))
        lbl_titulo.pack(pady=(40, 10))

        lbl_sub = ctk.CTkLabel(self.frame_home, text="Seleccione el modo de operación", font=("Roboto", 18))
        lbl_sub.pack(pady=(0, 50))

        btn_basico = ctk.CTkButton(self.frame_home, text="Diagnóstico Básico\n(Guiado paso a paso)",
                                   command=self.iniciar_basico, width=300, height=80, font=("Roboto", 18),
                                   fg_color="#3B8ED0", hover_color="#36719F")
        btn_basico.pack(pady=20)

        btn_avanzado = ctk.CTkButton(self.frame_home, text="Diagnóstico Avanzado\n(Seleccionar Módulo)",
                                     command=self.iniciar_avanzado, width=300, height=80, font=("Roboto", 18),
                                     fg_color="#2CC985", hover_color="#229A66")
        btn_avanzado.pack(pady=20)

        self.lbl_status = ctk.CTkLabel(self.frame_home, text="Conectando a base de datos...", text_color="gray")
        self.lbl_status.pack(side="bottom", pady=20)

    def crear_pantalla_modulos(self):
        self.limpiar_pantalla()

        self.frame_modulos = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_modulos.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        header = ctk.CTkFrame(self.frame_modulos, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))

        btn_volver = ctk.CTkButton(header, text="< Volver", width=80, command=self.crear_pantalla_home,
                                   fg_color="transparent", border_width=1)
        btn_volver.pack(side="left")

        lbl_titulo = ctk.CTkLabel(header, text="Seleccione un Módulo", font=("Roboto Medium", 24))
        lbl_titulo.pack(side="left", padx=20)

        # Grid de botones
        grid_frame = ctk.CTkScrollableFrame(self.frame_modulos)
        grid_frame.pack(fill="both", expand=True)

        # Crear botones dinámicamente basados en los módulos cargados
        col = 0
        row = 0
        for modulo in self.modulos_disponibles:
            btn = ctk.CTkButton(grid_frame, text=modulo, width=180, height=60, font=("Roboto", 14),
                                command=lambda m=modulo: self.iniciar_diagnostico_modulo(m))
            btn.grid(row=row, column=col, padx=10, pady=10)

            col += 1
            if col > 2:  # 3 columnas
                col = 0
                row += 1

    def crear_pantalla_diagnostico(self, titulo_modo):
        self.limpiar_pantalla()

        self.frame_diagnostico = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_diagnostico.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        header = ctk.CTkFrame(self.frame_diagnostico, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))

        btn_volver = ctk.CTkButton(header, text="< Menú", width=80, command=self.crear_pantalla_home,
                                   fg_color="transparent", border_width=1)
        btn_volver.pack(side="left")

        lbl_titulo = ctk.CTkLabel(header, text=titulo_modo, font=("Roboto Medium", 20))
        lbl_titulo.pack(side="left", padx=20)

        # Área de pregunta
        self.lbl_pregunta = ctk.CTkLabel(self.frame_diagnostico, text="Iniciando...", font=("Roboto", 24),
                                         wraplength=500, justify="center")
        self.lbl_pregunta.place(relx=0.5, rely=0.4, anchor="center")

        # Botones de respuesta
        self.frame_botones = ctk.CTkFrame(self.frame_diagnostico, fg_color="transparent")

        self.btn_si = ctk.CTkButton(self.frame_botones, text="SÍ", command=lambda: self.procesar_respuesta("si"),
                                    width=120, height=45, fg_color="#2CC985", hover_color="#229A66")
        self.btn_no = ctk.CTkButton(self.frame_botones, text="NO", command=lambda: self.procesar_respuesta("no"),
                                    width=120, height=45, fg_color="#C92C2C", hover_color="#9A2222")
        self.btn_nose = ctk.CTkButton(self.frame_botones, text="No sé / Otro",
                                      command=lambda: self.procesar_respuesta("nose"),
                                      width=120, height=45, fg_color="#3B8ED0", hover_color="#36719F")

        # Área de Resultado
        self.frame_resultado = ctk.CTkScrollableFrame(self.frame_diagnostico, label_text="Diagnóstico Final")
        self.lbl_resultado = ctk.CTkLabel(self.frame_resultado, text="", font=("Roboto", 16), justify="left",
                                          wraplength=500)
        self.lbl_resultado.pack(pady=10, padx=10)

        self.btn_nuevo = ctk.CTkButton(self.frame_diagnostico, text="Nuevo Diagnóstico",
                                       command=self.crear_pantalla_home)

    def limpiar_pantalla(self):
        for widget in self.winfo_children():
            widget.pack_forget()

    # --- LÓGICA DE DATOS ---

    def cargar_reglas(self):
        try:
            conn = pyodbc.connect(self.CONNECTION_STRING)
            cursor = conn.cursor()
            # Ahora traemos también el Módulo
            cursor.execute("SELECT ID_Regla, Modulo FROM Reglas ORDER BY ID_Regla")
            filas_reglas = cursor.fetchall()

            nuevas_reglas = []
            modulos_set = set()

            for row in filas_reglas:
                id_regla = row.ID_Regla
                modulo = row.Modulo or "General"
                modulos_set.add(modulo)

                # Condiciones
                cursor.execute(
                    "SELECT Variable, Valor, Operador_Siguiente FROM Condiciones WHERE ID_Regla = ? ORDER BY Orden",
                    (id_regla,))
                conds = cursor.fetchall()
                si_lista = []
                for c in conds:
                    si_lista.append((c.Variable, c.Valor))
                    if c.Operador_Siguiente: si_lista.append(c.Operador_Siguiente)

                # Consecuencias
                cursor.execute("SELECT Variable, Valor FROM Consecuencias WHERE ID_Regla = ?", (id_regla,))
                cons = cursor.fetchall()
                entonces_lista = [(c.Variable, c.Valor) for c in cons]

                nuevas_reglas.append({
                    "id": id_regla,
                    "modulo": modulo,
                    "si": si_lista,
                    "entonces": entonces_lista
                })

            conn.close()
            self.reglas_todas = nuevas_reglas
            self.modulos_disponibles = sorted(list(modulos_set))
            self.lbl_status.configure(text=f"Conectado: {len(self.reglas_todas)} reglas cargadas.")

        except Exception as e:
            self.lbl_status.configure(text=f"Error SQL: {e}", text_color="red")

    # --- FLUJO DE TRABAJO ---

    def iniciar_basico(self):
        # En básico usamos TODAS las reglas
        self.reglas_activas = self.reglas_todas
        self.hechos = {}
        self.crear_pantalla_diagnostico("Diagnóstico Básico")
        self.siguiente_paso()

    def iniciar_avanzado(self):
        self.crear_pantalla_modulos()

    def iniciar_diagnostico_modulo(self, modulo_nombre):
        # Filtramos solo las reglas de ese módulo
        self.reglas_activas = [r for r in self.reglas_todas if r["modulo"] == modulo_nombre]
        self.hechos = {}
        self.crear_pantalla_diagnostico(f"Módulo: {modulo_nombre}")
        self.siguiente_paso()

    def siguiente_paso(self):
        # 1. Verificar si ya tenemos un diagnóstico final
        if "diagnostico_final" in self.hechos:
            self.mostrar_resultado(self.hechos["diagnostico_final"])
            return

        variables_internas = {"condicion", "diagnostico_parcial", "diagnostico_final"}
        pregunta_encontrada = False

        # Iteramos sobre REGLAS ACTIVAS (filtradas o no)
        for regla in self.reglas_activas:
            if self.regla_es_util(regla):
                for item in regla["si"]:
                    if isinstance(item, tuple):
                        variable, valor_esperado = item
                        if variable not in self.hechos and variable not in variables_internas:
                            self.lanzar_pregunta(variable, valor_esperado)
                            pregunta_encontrada = True
                            return

        if not pregunta_encontrada:
            self.ejecutar_inferencias()
            if "diagnostico_final" in self.hechos:
                self.mostrar_resultado(self.hechos["diagnostico_final"])
            else:
                self.mostrar_resultado("No se encontró un diagnóstico exacto en este módulo con la información dada.")

    def regla_es_util(self, regla):
        condiciones = regla["si"]
        if "o" in condiciones: return True
        for item in condiciones:
            if isinstance(item, tuple):
                var, val = item
                if var in self.hechos and self.hechos[var] != val:
                    return False
        return True

    def lanzar_pregunta(self, variable, valor_esperado):
        self.variable_actual = variable
        self.valor_esperado_actual = valor_esperado

        texto_pregunta = self.mapa_preguntas.get(variable, f"¿{variable} es {valor_esperado}?")
        self.lbl_pregunta.configure(text=texto_pregunta)

        self.btn_si.pack(side="left", padx=10)
        self.btn_no.pack(side="left", padx=10)

        if "codigo" in variable:
            self.btn_nose.configure(text="Ingresar Código")
            self.btn_nose.pack(side="left", padx=10)
        else:
            self.btn_nose.pack_forget()

        self.frame_botones.place(relx=0.5, rely=0.7, anchor="center")

    def procesar_respuesta(self, respuesta):
        var = self.variable_actual
        val_esp = self.valor_esperado_actual

        for widget in self.frame_botones.winfo_children():
            widget.pack_forget()
        self.frame_botones.place_forget()

        if respuesta == "si":
            self.hechos[var] = val_esp
        elif respuesta == "no":
            self.hechos[var] = "no"
        elif respuesta == "nose":
            if "codigo" in var:
                dialog = ctk.CTkInputDialog(text="Ingrese el código DTC (ej. P0300):", title="Código de Falla")
                cod = dialog.get_input()
                if cod:
                    self.hechos[var] = cod.strip().upper()
                else:
                    self.hechos[var] = "no_se"
            else:
                self.hechos[var] = "no_se"

        self.ejecutar_inferencias()
        self.siguiente_paso()

    def ejecutar_inferencias(self):
        cambios = True
        while cambios:
            cambios = False
            # Importante: Inferir sobre TODAS las reglas cargadas, no solo las activas,
            # para aprovechar conocimiento cruzado si es necesario, aunque en modo avanzado
            # nos enfocamos en el subconjunto. Por seguridad usamos activas.
            for regla in self.reglas_activas:
                if self.evaluar_regla(regla):
                    for var, val in regla["entonces"]:
                        if var not in self.hechos:
                            self.hechos[var] = val
                            cambios = True

    def evaluar_regla(self, regla):
        condiciones = regla["si"]
        if "o" in condiciones:
            for item in condiciones:
                if item == "o": continue
                var, val = item
                if var in self.hechos and self.hechos[var] == val: return True
            return False
        else:
            for item in condiciones:
                if item == "y": continue
                var, val = item
                if var not in self.hechos or self.hechos[var] != val: return False
            return True

    def mostrar_resultado(self, texto):
        self.lbl_pregunta.place_forget()
        self.frame_botones.place_forget()
        self.lbl_resultado.configure(text=texto)
        self.frame_resultado.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.5)
        self.btn_nuevo.place(relx=0.5, rely=0.9, anchor="center")


if __name__ == "__main__":
    app = AdamGUI()
    app.mainloop()