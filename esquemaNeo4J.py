import os
from neo4j import GraphDatabase

# ==============================
# CONFIGURACIÓN
# ==============================
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "strongpass"

# Ruta local donde tienes guardados los archivos .txt de Neo4j
# Asegúrate de reemplazar esta ruta con la real en tu sistema
CARPETA_TXT = "txtfiles"  # <-- AJUSTA ESTA RUTA

# ==============================
# FUNCIONES PRINCIPALES
# ==============================

def ejecutar_cypher_desde_txt(driver, carpeta):
    with driver.session() as session:
        archivos = sorted([f for f in os.listdir(carpeta) if f.endswith(".txt")])
        for archivo in archivos:
            ruta = os.path.join(carpeta, archivo)
            print(f"📂 Procesando: {archivo}")

            with open(ruta, "r", encoding="utf-8") as f:
                cypher_completo = f.read()

            # Dividir múltiples comandos Cypher por ";"
            comandos = [c.strip() for c in cypher_completo.split(";") if c.strip()]
            for comando in comandos:
                try:
                    session.run(comando)
                except Exception as e:
                    print(f"❌ Error en {archivo}:\n→ {e}\n→ Fragmento: {comando[:100]}...\n")

    print("✅ Todos los archivos fueron ejecutados correctamente.")

# ==============================
# EJECUCIÓN
# ==============================

if __name__ == "__main__":
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    ejecutar_cypher_desde_txt(driver, CARPETA_TXT)
    driver.close()
