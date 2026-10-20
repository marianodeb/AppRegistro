import sqlite3
import streamlit as st


def main():
  st.title("Control de cosecha")

  # Diccionario para convertir el nombre del mes al número correspondiente (ej: Enero -> 01)
  # Necesario para que coincida con el formato de fecha guardado en la base de datos (YYYY-MM-DD)
  meses_dict = {
      "Enero": "01",
      "Febrero": "02",
      "Marzo": "03",
      "Abril": "04",
      "Mayo": "05",
      "Junio": "06",
      "Julio": "07",
      "Agosto": "08",
      "Septiembre": "09",
      "Octubre": "10",
      "Noviembre": "11",
      "Diciembre": "12",
  }

  # Creación del formulario en Streamlit
  with st.form(key="mi_formulario"):
    hortalizaelegida = st.selectbox(
        "Selecciona la hortaliza",
        [
            "Acelga",
            "Ajo",
            "Apio",
            "Arveja",
            "Batata",
            "Berenjena",
            "Brócoli",
            "Calabacín",
            "Cebolla",
            "Cebolla de verdeo",
            "Espinaca",
            "Frutilla",
            "Lechuga",
            "Maíz",
            "Papa",
            "Pepino",
            "Pimiento",
            "Rabanito",
            "Remolacha",
            "Repollo",
            "Tomate",
            "Zanahoria",
            "Zapallo kokena",
            "Zapallo veronez",
        ],
    )

    anio = st.selectbox(
        "Seleccione el año: ", ["2024", "2025", "2026", "2027", "2028"]
    )

    mes = st.selectbox("Seleccione el mes: ", list(meses_dict.keys()))

    # Botón de envío obligatorio dentro de st.form
    submit_button = st.form_submit_button(label="Enviar")

  # Las consultas y resultados se ejecutan SOLAMENTE cuando se presiona el botón
  if submit_button:
    # Conexión a la base de datos SQLite
    conn = sqlite3.connect("cosechas.db")
    kursor = conn.cursor()

    # Variables armadas previamente para evitar errores con el operador LIKE de SQL
    busqueda_anio = f"{anio}%"
    busqueda_mes = f"{anio}-{meses_dict[mes]}%"

    # 1. Primera consulta: suma total para el año seleccionado
    kursor.execute(
        """
        SELECT SUM(gramos) FROM cosecha
        WHERE hortaliza = ? AND fecha LIKE ?
        """,
        (hortalizaelegida, busqueda_anio),
    )
    resultado_anio = kursor.fetchone()[0]
    total_anio = resultado_anio if resultado_anio is not None else 0.0

    # 2. Segunda consulta: suma total para el mes y año seleccionados
    kursor.execute(
        """
        SELECT SUM(gramos) FROM cosecha
        WHERE hortaliza = ? AND fecha LIKE ?
        """,
        (hortalizaelegida, busqueda_mes),
    )
    resultado_mes = kursor.fetchone()[0]
    total_mes = resultado_mes if resultado_mes is not None else 0.0

    # 3. Tercera consulta: suma histórica total de la hortaliza seleccionada
    kursor.execute(
        """
        SELECT SUM(gramos) FROM cosecha
        WHERE hortaliza = ?
        """,
        (hortalizaelegida,),
    )
    resultado_historico = kursor.fetchone()[0]
    total_historico = (
        resultado_historico if resultado_historico is not None else 0.0
    )

    # Cierre de la conexión a la base de datos
    conn.close()

    # Mostrar resultados en pantalla dentro del condicional
    st.success(f"Ingreso: {hortalizaelegida}, {mes}, {anio}")
    st.write(f"año: {anio} : {int(total_anio) / 1000} Kg")
    st.write(f"mes: {mes} : {int(total_mes) / 1000} Kg")
    st.write(f"Total registrado: {int(total_historico) / 1000} Kg")


if __name__ == "__main__":
  main()
