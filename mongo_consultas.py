from pymongo import MongoClient
import ast
from collections import Counter

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
collection = client["Hoteles"]["Hoteles"]

print("\n📌 Turistas con satisfacción mayor a 3:")
for doc in collection.find({"Satisfaction": {"$gt": 3}}, {"Tourist ID": 1, "Satisfaction": 1.0, "_id": 0}):
    print(doc)

print("\n📌 Total de turistas con accesibilidad activada:")
total = collection.count_documents({"Accessibility": True})
print("Accesibilidad:", total)

print("\n📌 Intereses más comunes entre los turistas:")
intereses = []
for doc in collection.find():
    try:
        intereses += ast.literal_eval(doc.get("Interests", "[]"))
    except:
        continue

conteo = Counter(intereses)
for interes, count in conteo.most_common():
    print(f"{interes}: {count}")
