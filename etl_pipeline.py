import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import boto3
import io

def pipeline_etl_completo():
    print("=== 1. FASE DE EXTRACCION (Extract) ===")
    raw_data = {
        "cliente": ["Cliente_A", "Cliente_B", "Cliente_C", "Cliente_D", "Cliente_E"],
        "edad": [20, 40, 60, 30, 22],
        "monto_compras": [1200.0, 50000.0, 30000.0, 15000.0, 8000.0]
    }
    df_raw = pd.DataFrame(raw_data)
    print("Dataset Raw Extraido:")
    print(df_raw)

    print("\n=== 2. FASE DE TRANSFORMACION (Transform) ===")
    # Discretizacion (Binning)
    df_raw["categoria_edad"] = pd.cut(
        df_raw["edad"],
        bins=[0, 25, 50, 100],
        labels=["Joven", "Adulto", "Senior"]
    )

    # Normalizacion Min-Max
    scaler = MinMaxScaler()
    df_raw["monto_normalizado"] = scaler.fit_transform(df_raw[["monto_compras"]])

    # Feature Engineering
    df_raw["score_promocional"] = df_raw["monto_normalizado"] * 100

    print("Dataset Transformado:")
    print(df_raw)

    print("\n=== 3. FASE DE CARGA (Load) ===")
    # Serializacion a Parquet en memoria
    buffer = io.BytesIO()
    df_raw.to_parquet(buffer, index=False, engine="pyarrow", compression="snappy")
    buffer.seek(0)

    # Si vas a subir a S3, reemplaza "tu-bucket-destino" por el nombre de tu bucket de AWS
    BUCKET_NAME = "tu-bucket-destino"
    KEY_S3 = "processed/etl_output.parquet"

    # Si tienes credenciales activas, descomenta la linea de subida a S3:
    # s3_client = boto3.client("s3", region_name="us-east-1")
    # s3_client.put_object(Bucket=BUCKET_NAME, Key=KEY_S3, Body=buffer.getvalue())

    # Para prueba local guardamos una copia del archivo parquet:
    with open("etl_output.parquet", "wb") as f:
        f.write(buffer.getvalue())

    print(f"-> Exito: Archivo Parquet generado correctamente ({KEY_S3}).")

if __name__ == "__main__":
    pipeline_etl_completo()
