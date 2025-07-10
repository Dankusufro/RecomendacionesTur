from pymongo import MongoClient
from neo4j import GraphDatabase
import ast
import pandas as pd

# === Conexiones ===
mongo = MongoClient("mongodb://localhost:27017/")["Hoteles"]["Hoteles"]
neo4j = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "strongpass"))

# === Mapeo de intereses de MongoDB a categorías de Neo4j ===
interes_mapeo = {
    "Art": "Arte",
    "Architecture": "Arquitectura",
    "History": "Historico",
    "Cultural": "Cultural",
    "Nature": "Naturaleza"
}

# === Mapeo de lugares MongoDB -> Neo4j ===
nombre_mapeo = {
    "Eiffel Tower": "Torre Eiffel",
    "Taj Mahal": "Taj Mahal",
    "Great Wall of China": "Gran Muralla China",
    "Machu Picchu": "Machu Picchu",
    "Colosseum": "Coliseo Romano",
    "Statue of Liberty": "Estatua de la Libertad",
    "Louvre Museum": "Museo del Louvre",
    "MoMA": "MoMA",
    "Empire State Building": "Empire State Building",
    "Central Park": "Central Park"
}

def recomendar_con_distancia():
    recomendaciones = []

    with neo4j.session() as session:
        for doc in mongo.find({"Satisfaction": {"$gte": 4.0}}):
            try:
                tid = int(doc["Tourist ID"])
                accessible = bool(doc.get("Accessibility", False))
                interests = ast.literal_eval(doc.get("Interests", "[]"))
                sitios_visitados = ast.literal_eval(doc.get("Sites Visited", "[]"))

                for interest in interests:
                    categoria_neo4j = interes_mapeo.get(interest)
                    if not categoria_neo4j:
                        continue  # ignorar intereses no relacionados

                    for sitio in sitios_visitados:
                        sitio_neo4j = nombre_mapeo.get(sitio)
                        if not sitio_neo4j:
                            continue  # ignorar lugares no mapeados

                        result = session.run("""
                            MATCH (v:LugarTuristico {nombre: $visitado})<-[:CERCA_DE]-(sugerido:LugarTuristico)-[:PERTENECE_A]->(c:Categoria)
                            WHERE sugerido.accesible = $accesible
                              AND c.nombre = $categoria
                              AND sugerido.nombre <> $visitado
                            RETURN sugerido.nombre AS lugar, sugerido.ciudad AS ciudad,
                                   sugerido.pais AS pais, sugerido.promedio_general AS rating,
                                   v.nombre AS desde
                            ORDER BY rating DESC
                            LIMIT 2
                        """, visitado=sitio_neo4j, accesible=accessible, categoria=categoria_neo4j)

                        for row in result:
                            recomendaciones.append({
                                "Tourist ID": tid,
                                "Interés": interest,
                                "Desde": row["desde"],
                                "Lugar Recomendado": row["lugar"],
                                "Ciudad": row["ciudad"],
                                "País": row["pais"],
                                "Rating": row["rating"]
                            })

            except Exception as e:
                print(f"❌ Error turista ID {doc.get('Tourist ID')}: {e}")

    return recomendaciones

# Ejecutar y guardar
recoms = recomendar_con_distancia()
df = pd.DataFrame(recoms)
df.to_csv("recomendaciones_con_distancia.csv", index=False)
print("✅ Archivo 'recomendaciones_con_distancia.csv' generado.")
