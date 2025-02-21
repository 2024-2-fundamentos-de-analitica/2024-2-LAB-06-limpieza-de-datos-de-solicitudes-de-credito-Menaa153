"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""
import os
import pandas as pd

def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    def cargar_data(ruta_archivo):
        return pd.read_csv(ruta_archivo, sep=';')

    def limpiar_columnas(df):
        df.drop(['Unnamed: 0'], axis=1, inplace=True)
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)
        return df

    def normalizar_fechas(df):
        df[['día', 'mes', 'año']] = df['fecha_de_beneficio'].str.split('/', expand=True)
        df.loc[df['año'].str.len() < 4, ['día', 'año']] = df.loc[df['año'].str.len() < 4, ['año', 'día']].values
        df['fecha_de_beneficio'] = df['año'] + '-' + df['mes'] + '-' + df['día']
        df.drop(['día', 'mes', 'año'], axis=1, inplace=True)
        return df

    def normalizar_texto(df):
        columnas_texto = ['sexo', 'tipo_de_emprendimiento', 'idea_negocio', 'línea_credito']
        df[columnas_texto] = df[columnas_texto].apply(lambda x: x.str.lower().replace(['-', '_'], ' ', regex=True).str.strip())
        df['barrio'] = df['barrio'].str.lower().replace(['-', '_'], ' ', regex=True)
        return df

    def limpiar_montos(df):
        df['monto_del_credito'] = df['monto_del_credito'].str.replace("[$, ]", "", regex=True).str.strip()
        df['monto_del_credito'] = pd.to_numeric(df['monto_del_credito'], errors='coerce')
        df['monto_del_credito'] = df['monto_del_credito'].fillna(0).astype(int)
        df['monto_del_credito'] = df['monto_del_credito'].astype(str).str.replace('.00', '')
        return df

    def guardar_data(df, ruta_salida):
        directorio_salida = os.path.dirname(ruta_salida)
        os.makedirs(directorio_salida, exist_ok=True)
        df.to_csv(ruta_salida, sep=';', index=False)

    ruta_archivo = 'files/input/solicitudes_de_credito.csv'
    ruta_salida = 'files/output/solicitudes_de_credito.csv'

    data = cargar_data(ruta_archivo)
    data = limpiar_columnas(data)
    data = normalizar_fechas(data)
    data = normalizar_texto(data)
    data = limpiar_montos(data)
    data.drop_duplicates(inplace=True)

    guardar_data(data, ruta_salida)
    print(f"Archivo limpio guardado en {ruta_salida}")


if __name__ == '__main__':
    print(pregunta_01())