
# 🌍 Sistema de Recomendaciones Turísticas (MongoDB + Neo4j)

Este proyecto implementa un sistema de recomendación de lugares turísticos personalizado, combinando datos de turistas almacenados en **MongoDB** con una red de lugares turísticos conectados en **Neo4j**. La recomendación se basa en intereses, accesibilidad y cercanía geográfica.

---

## 🛠 Tecnologías utilizadas

- MongoDB (NoSQL, documentos JSON)
- Neo4j (Base de datos orientada a grafos)
- Python 3
- Pandas
- PyMongo
- Neo4j Python Driver

---

## 🚀 Requisitos

- Docker (para levantar Neo4j localmente)
- MongoDB corriendo localmente con los datos importados del CSV
- Python 3.8 o superior
- Dependencias instaladas:

```bash
pip install pymongo neo4j pandas
````

---

## 🐳 Iniciar Neo4j con Docker

Para iniciar Neo4j localmente, ejecuta:

```bash
docker run -d --name neo4j-container -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/strongpass neo4j:latest
```

Esto levantará Neo4j en `http://localhost:7474` con:

* Usuario: `neo4j`
* Contraseña: `strongpass`

---

## 📁 Estructura del repositorio

```
/RecomendacionesTur/
│
├── mongo_consultas.py              # Consultas simples a MongoDB
├── neo4j_consultas.py              # Consultas simples a Neo4j
├── cruce_recomendaciones.py        # Script principal de integración MongoDB–Neo4j
├── esquemaNeo4J.py                 # Carga todos los .txt con comandos Cypher en Neo4j
├── recomendaciones_con_distancia.csv  # Resultado del cruce
└── /txt_cypher/                    # Archivos Cypher para poblar Neo4j
    ├── Neo4j.txt
    ├── Neo4j2.txt
    ├── Neo4j3.txt
    └── Neo4j4.txt
```

---

## 🧪 Cómo ejecutar

### 1. Poblar Neo4j

Ejecuta el script `esquemaNeo4J.py` para cargar todos los archivos `.txt` de Cypher al grafo:

```bash
python esquemaNeo4J.py
```

> Asegúrate de haber iniciado el contenedor Docker antes de ejecutar esto.

### 2. Consultas individuales

```bash
python mongo_consultas.py      # Consulta en MongoDB
python neo4j_consultas.py      # Consulta en Neo4j
```

### 3. Generar recomendaciones cruzadas

```bash
python cruce_recomendaciones.py
```

Esto generará un archivo: `recomendaciones_con_distancia.csv` con los resultados finales.

---

## 📈 Ejemplo de salida

| Tourist ID | Interés      | Desde              | Lugar Recomendado         | Ciudad | País  | Rating |
| ---------- | ------------ | ------------------ | ------------------------- | ------ | ----- | ------ |
| 5          | Architecture | Taj Mahal          | Tumba de Itimad-ud-Daulah | Agra   | India | 4.1    |
| 9          | Cultural     | Gran Muralla China | Ciudad Prohibida          | Pekín  | China | 4.5    |

---

## 👥Integrantes

-Antonia Paredes

-Danko Torres

-Leandro Matamoros
