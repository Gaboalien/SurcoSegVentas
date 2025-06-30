import os
import django
import pandas as pd
from datetime import datetime

from datetime import datetime

def parse_fecha(valor):
    if not valor:
        return None
    if isinstance(valor, datetime):
        return valor.date()
    str_val = str(valor).strip()
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(str_val, fmt).date()
        except ValueError:
            continue
    return None

def valor_surco(celda):
    if not celda:
        return "No"
    valor = str(celda).strip().lower()
    if valor in ["", "0", "nan", "none"]:
        return "No"
    return "Sí"

# CONFIGURAR PROYECTO
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Prueba1.settings')  # CAMBIAR por el nombre real del proyecto
django.setup()

from App.models import Cliente  # CAMBIAR si tu app se llama diferente

# Mapeo de asesor a ID de usuario
asesor_id_map = {
    'Catherine': 3,
    'Yhennifer': 4,
    'Yazmin': 5,
    'Nancy': 6,
}

# Leer el archivo Excel (hoja específica)
df = pd.read_excel('Base ventas hasta 03.06.2025.xlsx', sheet_name='SIN VIDA Y SIN HOGAR ', dtype=str)

# Usar solo las primeras 5 filas
df = df.head(5)

# Insertar cada fila
for _, row in df.iterrows():
    asesor_nombre = row.get('Asesor', '').strip()
    usuario_id = asesor_id_map.get(asesor_nombre)

    if not usuario_id:
        print(f"⚠️ Asesor no reconocido: {asesor_nombre}, omitiendo fila.")
        continue

    Cliente.objects.create(
    cliced_a=row.get('CLICED_A'),
    rescierre=row.get('RESCIERRE'),
    resvto=row.get('RESVTO'),
    cliente_desde=parse_fecha(row.get('CLIENTE_DESDE')),
    tarven=row.get('TARVEN'),
    cliapeuno=row.get('CLIAPEUNO'),
    cliapedos=row.get('CLIAPEDOS'),
    clinomuno=row.get('CLINOMUNO'),
    clinomdos=row.get('CLINOMDOS'),
    edad=int(row['EDAD']) if row.get('EDAD') and str(row['EDAD']).isdigit() else None,
    clifecnac=parse_fecha(row.get('CLIFECNAC')),
    loc=row.get('LOC'),
    dpto=row.get('DPTO'),
    clical=row.get('CLICAL'),
    clindp=row.get('CLINDP'),
    clibis=row.get('CLIBIS'),
    clirut=row.get('CLIRUT'),
    clikms=row.get('CLIKMS'),
    clipas=row.get('CLIPAS'),
    cliblo=row.get('CLIBLO'),
    clitor=row.get('CLITOR'),
    cliapt=row.get('CLIAPT'),
    climan=row.get('CLIMAN'),
    telp=row.get('TELP'),
    telt=row.get('TELT'),
    cel1=row.get('CEL1'),
    cel2=row.get('CEL2'),
    telbau=row.get('TELBAU'),
    telweb=row.get('TELWEB'),
    celweb=row.get('CELWEB'),
    surco_vida=valor_surco(row.get('SURCO_VIDA')),
    surco_hogar=valor_surco(row.get('SURCO_HOGAR')),
    hasta=parse_fecha(row.get('HASTA')),
    usuario_id=usuario_id,
    fecha_carga=datetime.today().date(),
    email=row.get('EMAIL') or '',
    genero=row.get('GENERO') or ''
)

print("✅ Importación de las primeras 5 filas completada.")
