
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ------------------------------------------------------------
# CONFIGURACIÓN GENERAL
# ------------------------------------------------------------

st.set_page_config(
    page_title="DSS Integridad y Mantenimiento",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------
# ESTILO
# ------------------------------------------------------------

st.markdown("""
<style>

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

[data-testid="stMetric"] {
    background-color: #ffffff;
    border: 1px solid #d9e2ec;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.06);
}

h1, h2, h3 {
    color: #0b2d4d;
}

.dashboard-title {
    background: linear-gradient(90deg,#082b49,#135b7d);
    padding: 20px;
    border-radius: 14px;
    color: white;
    margin-bottom: 20px;
}

.dashboard-subtitle {
    font-size: 16px;
    color: #d9edf7;
}

.alert-critical {
    background-color: #ffe5e5;
    border-left: 6px solid #d62728;
    padding: 12px;
    border-radius: 8px;
}

.alert-high {
    background-color: #fff3e0;
    border-left: 6px solid #ff7f0e;
    padding: 12px;
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# CARGA DE DATOS
# ------------------------------------------------------------

ARCHIVO = "/content/Reporte_Ejecutivo_DSS_Mantenimiento.xlsx"

@st.cache_data
def cargar_datos():

    resumen = pd.read_excel(
        ARCHIVO,
        sheet_name="00_RESUMEN_EJECUTIVO"
    )

    riesgo = pd.read_excel(
        ARCHIVO,
        sheet_name="01_RIESGO_DRBI"
    )

    cartera = pd.read_excel(
        ARCHIVO,
        sheet_name="02_CARTERA_MTTO"
    )

    programa = pd.read_excel(
        ARCHIVO,
        sheet_name="03_PROGRAMA_MILP"
    )

    finanzas = pd.read_excel(
        ARCHIVO,
        sheet_name="04_FINANZAS"
    )

    presupuesto = pd.read_excel(
        ARCHIVO,
        sheet_name="05_PRESUPUESTO_MENSUAL"
    )

    recursos = pd.read_excel(
        ARCHIVO,
        sheet_name="06_RECURSOS"
    )

    rolling = pd.read_excel(
        ARCHIVO,
        sheet_name="07_ROLLING_HORIZON"
    )

    return (
        resumen,
        riesgo,
        cartera,
        programa,
        finanzas,
        presupuesto,
        recursos,
        rolling
    )


(
    resumen,
    riesgo,
    cartera,
    programa,
    finanzas,
    presupuesto,
    recursos,
    rolling
) = cargar_datos()


# ------------------------------------------------------------
# ENCABEZADO
# ------------------------------------------------------------

st.markdown("""
<div class="dashboard-title">

<h1 style="color:white; margin:0;">
DSS de Integridad y Mantenimiento
</h1>

<div class="dashboard-subtitle">
Modelo integrado DRBI – IOWs – Bayes – MDP-RVO – MILP
</div>

</div>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------

st.sidebar.title("DSS Refinería")

st.sidebar.markdown(
    "### Filtros de análisis"
)

tramos_disponibles = sorted(
    riesgo["ID_tramo"]
    .dropna()
    .unique()
)

tramos_seleccionados = st.sidebar.multiselect(
    "Tramos",
    tramos_disponibles,
    default=tramos_disponibles
)

niveles_disponibles = [
    "BAJO",
    "MEDIO",
    "ALTO",
    "CRITICO"
]

niveles_seleccionados = st.sidebar.multiselect(
    "Nivel de riesgo",
    niveles_disponibles,
    default=niveles_disponibles
)

st.sidebar.markdown("---")

st.sidebar.info(
    "Prototipo académico del Sistema de Apoyo a Decisiones "
    "para integridad y mantenimiento de tuberías."
)


# ------------------------------------------------------------
# FILTROS
# ------------------------------------------------------------

riesgo_f = riesgo[
    riesgo["ID_tramo"]
    .isin(tramos_seleccionados)
].copy()

riesgo_f = riesgo_f[
    riesgo_f["NIVEL_RIESGO"]
    .isin(niveles_seleccionados)
]

programa_f = programa[
    programa["ID_TRAMO"]
    .isin(tramos_seleccionados)
].copy()

finanzas_f = finanzas[
    finanzas["ID_tramo"]
    .isin(tramos_seleccionados)
].copy()


# ------------------------------------------------------------
# TABS
# ------------------------------------------------------------

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([

    "📊 Resumen Ejecutivo",

    "🛡️ Integridad",

    "🔧 Mantenimiento",

    "💰 Finanzas",

    "👷 Recursos",

    "🔄 Rolling Horizon"

])


# ============================================================
# TAB 1 - RESUMEN EJECUTIVO
# ============================================================

with tab1:

    st.subheader(
        "Resumen Ejecutivo"
    )

    total_tramos = riesgo_f["ID_tramo"].nunique()

    criticos = (
        riesgo_f["NIVEL_RIESGO"]
        .eq("CRITICO")
        .sum()
    )

    altos = (
        riesgo_f["NIVEL_RIESGO"]
        .eq("ALTO")
        .sum()
    )

    programadas = (
        programa_f["ESTADO_PROGRAMACION"]
        .eq("PROGRAMADO")
        .sum()
    )

    presupuesto_total = (
        finanzas_f[
            "PRESUPUESTO_MANTENIMIENTO_S"
        ]
        .sum()
    )

    impacto_total = (
        finanzas_f[
            "IMPACTO_OPERATIVO_S"
        ]
        .sum()
    )

    hh_total = (
        finanzas_f[
            "HH_TOTAL"
        ]
        .sum()
    )

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    c1.metric(
        "Tramos evaluados",
        total_tramos
    )

    c2.metric(
        "Riesgo crítico",
        criticos
    )

    c3.metric(
        "Riesgo alto",
        altos
    )

    c4.metric(
        "Programados",
        programadas
    )

    c5.metric(
        "Presupuesto",
        f"S/ {presupuesto_total:,.0f}"
    )

    c6.metric(
        "HH totales",
        f"{hh_total:,.0f}"
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        dist_riesgo = (
            riesgo_f["NIVEL_RIESGO"]
            .value_counts()
            .reset_index()
        )

        dist_riesgo.columns = [
            "Nivel",
            "Cantidad"
        ]

        fig = px.bar(
            dist_riesgo,
            x="Nivel",
            y="Cantidad",
            title="Distribución del riesgo DRBI",
            text="Cantidad"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with col2:

        costo_tramo = (
            finanzas_f[
                [
                    "ID_tramo",
                    "COSTO_ECONOMICO_TOTAL_S"
                ]
            ]
            .sort_values(
                "COSTO_ECONOMICO_TOTAL_S",
                ascending=True
            )
        )

        fig = px.bar(
            costo_tramo,
            x="COSTO_ECONOMICO_TOTAL_S",
            y="ID_tramo",
            orientation="h",
            title="Costo económico total por tramo"
        )

        fig.update_xaxes(
            title="Costo económico total (S/)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    st.subheader(
        "Activos prioritarios"
    )

    prioritarios = programa_f[
        programa_f["NIVEL_RIESGO"]
        .isin(["ALTO", "CRITICO"])
    ]

    st.dataframe(
        prioritarios[
            [
                "ID_TRAMO",
                "SERVICIO",
                "NIVEL_RIESGO",
                "PRIORIDAD",
                "ESTRATEGIA",
                "FECHA_PROGRAMADA",
                "PRESUPUESTO_MTTO_S"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# TAB 2 - INTEGRIDAD
# ============================================================

with tab2:

    st.subheader(
        "Integridad y Riesgo Dinámico"
    )

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            riesgo_f.sort_values(
                "Riesgo_DRBI",
                ascending=False
            ),
            x="ID_tramo",
            y="Riesgo_DRBI",
            color="NIVEL_RIESGO",
            title="Riesgo DRBI por tramo"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with col2:

        fig = px.scatter(
            riesgo_f,
            x="PoF_posterior",
            y="CoF_valor",
            size="Riesgo_DRBI",
            color="NIVEL_RIESGO",
            hover_name="ID_tramo",
            title="Matriz PoF – CoF"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    st.subheader(
        "Detalle de condición"
    )

    st.dataframe(
        riesgo_f[
            [
                "ID_tramo",
                "E_t",
                "PoF_prior",
                "PoF_posterior",
                "CoF_valor",
                "Riesgo_DRBI",
                "NIVEL_RIESGO"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# TAB 3 - MANTENIMIENTO
# ============================================================

with tab3:

    st.subheader(
        "Plan de Mantenimiento"
    )

    st.dataframe(
        programa_f[
            [
                "ID_SOLICITUD",
                "ID_TRAMO",
                "SERVICIO",
                "NIVEL_RIESGO",
                "PRIORIDAD",
                "ESTRATEGIA",
                "SEMANA_PROGRAMADA",
                "FECHA_PROGRAMADA",
                "HORAS_INTERVENCION",
                "HH_TOTAL",
                "PRESUPUESTO_MTTO_S",
                "ESTADO_PROGRAMACION"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.subheader(
        "Horas de intervención por tramo"
    )

    fig = px.bar(
        programa_f.sort_values(
            "HORAS_INTERVENCION",
            ascending=False
        ),
        x="ID_TRAMO",
        y="HORAS_INTERVENCION",
        color="NIVEL_RIESGO"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# TAB 4 - FINANZAS
# ============================================================

with tab4:

    st.subheader(
        "Gestión Económica y Presupuestal"
    )

    presupuesto_mtto = (
        finanzas_f[
            "PRESUPUESTO_MANTENIMIENTO_S"
        ]
        .sum()
    )

    impacto_operativo = (
        finanzas_f[
            "IMPACTO_OPERATIVO_S"
        ]
        .sum()
    )

    costo_economico = (
        finanzas_f[
            "COSTO_ECONOMICO_TOTAL_S"
        ]
        .sum()
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Presupuesto mantenimiento",
        f"S/ {presupuesto_mtto:,.0f}"
    )

    c2.metric(
        "Impacto operativo",
        f"S/ {impacto_operativo:,.0f}"
    )

    c3.metric(
        "Exposición económica",
        f"S/ {costo_economico:,.0f}"
    )


    fig = px.bar(
        finanzas_f,
        x="ID_tramo",
        y=[
            "COSTO_MANO_OBRA_S",
            "COSTO_MATERIALES_S",
            "COSTO_EQUIPOS_S",
            "COSTO_SERVICIOS_TERCEROS_S"
        ],
        title="Composición del costo por tramo",
        barmode="stack"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    if len(presupuesto) > 0:

        fig = go.Figure()

        fig.add_bar(
            x=presupuesto["MES"],
            y=presupuesto[
                "Presupuesto_programado"
            ],
            name="Programado"
        )

        fig.add_bar(
            x=presupuesto["MES"],
            y=presupuesto[
                "Presupuesto_disponible"
            ],
            name="Disponible"
        )

        fig.update_layout(
            title="Control presupuestal mensual",
            barmode="group"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# TAB 5 - RECURSOS
# ============================================================

with tab5:

    st.subheader(
        "Utilización de Recursos"
    )

    if len(recursos) > 0:

        fig = go.Figure()

        columnas_recursos = [

            "HH_Mecanico",

            "HH_Soldador",

            "HH_Inspector",

            "HH_Corrosion",

            "HH_Planificacion",

            "HH_Operaciones"

        ]

        for col in columnas_recursos:

            fig.add_trace(

                go.Scatter(

                    x=recursos[
                        "SEMANA_PROGRAMADA"
                    ],

                    y=recursos[col],

                    mode="lines+markers",

                    name=col

                )

            )

        fig.update_layout(
            title="Carga semanal por especialidad",
            xaxis_title="Semana",
            yaxis_title="Horas-hombre"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(
            recursos,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# TAB 6 - ROLLING HORIZON
# ============================================================

with tab6:

    st.subheader(
        "Rolling Horizon y Reoptimización"
    )

    st.dataframe(
        rolling[
            [
                "ID_SOLICITUD",
                "ID_TRAMO",
                "SERVICIO",
                "NIVEL_RIESGO",
                "NIVEL_RIESGO_ACTUAL",
                "RIESGO_ACTUAL",
                "DELTA_RIESGO",
                "SEMANA_PROGRAMADA",
                "FECHA_PROGRAMADA",
                "ESTADO_HORIZONTE",
                "DECISION_ROLLING_HORIZON",
                "ACCION_PLANIFICACION"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


    decisiones = (
        rolling[
            "DECISION_ROLLING_HORIZON"
        ]
        .value_counts()
        .reset_index()
    )

    decisiones.columns = [
        "Decisión",
        "Cantidad"
    ]

    fig = px.bar(
        decisiones,
        x="Cantidad",
        y="Decisión",
        orientation="h",
        title="Decisiones del Rolling Horizon"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ------------------------------------------------------------
# PIE
# ------------------------------------------------------------

st.markdown("---")

st.caption(
    "DSS de Integridad y Mantenimiento | "
    "DRBI – IOWs – actualización bayesiana – MDP-RVO – MILP"
)

