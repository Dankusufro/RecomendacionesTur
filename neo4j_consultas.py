from neo4j import GraphDatabase

# Conexión a Neo4j
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "strongpass"))

with driver.session() as session:

    print("\n📌 Categorías de lugares turísticos:")
    result = session.run("MATCH (c:Categoria) RETURN c.nombre AS categoria")
    for r in result:
        print("-", r["categoria"])

    print("\n📌 Lugares con promedio > 4.5:")
    result = session.run("""
        MATCH (l:LugarTuristico)
        WHERE l.promedio_general > 4.5
        RETURN l.nombre AS nombre, l.ciudad AS ciudad, l.pais AS pais, l.promedio_general AS rating
        ORDER BY rating DESC
    """)
    for r in result:
        print(f"{r['nombre']} ({r['ciudad']}, {r['pais']}) → Rating: {r['rating']}")

    print("\n📌 Conteo de lugares por país:")
    result = session.run("""
        MATCH (l:LugarTuristico)
        RETURN l.pais AS pais, COUNT(*) AS total
        ORDER BY total DESC
    """)
    for r in result:
        print(f"{r['pais']}: {r['total']} lugares")

driver.close()
