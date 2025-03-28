import pandas as pd
import random
import csv
import os

# Archivo de datos
pokemon_file = "pokemon.csv"
ranking_file = "ranking.csv"

# Cargar datos desde el archivo CSV si existe
if os.path.exists(pokemon_file):
    df = pd.read_csv(pokemon_file)
    df.columns = df.columns.str.strip().str.lower()
    pokemon_list = df.to_dict(orient="records")
else:
    pokemon_list = []

# Cargar o crear tabla de clasificación
if os.path.exists(ranking_file):
    ranking_df = pd.read_csv(ranking_file)
    ranking = {row["name"]: row["wins"] for _, row in ranking_df.iterrows()}
else:
    ranking = {}

# Guardar la lista de Pokémon en CSV
def guardar_pokemon():
    df = pd.DataFrame(pokemon_list)
    df.to_csv(pokemon_file, index=False)

# Guardar el ranking en CSV
def guardar_ranking():
    with open(ranking_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "wins"])
        for name, wins in ranking.items():
            writer.writerow([name, wins])

# Función para mostrar Pokémon disponibles
def mostrar_pokemon():
    if not pokemon_list:
        print("\n❌ No hay Pokémon disponibles.")
        return
    print("\n📋 Lista de Pokémon:")
    for i, p in enumerate(pokemon_list):
        print(f"{i + 1}. {p['name']} ({p['type_1']}) - ATK: {p['attack']}, DEF: {p['defense']}, HP: {p['hp']}")

# Función para mostrar tabla de clasificación (solo Pokémon que han peleado)
def mostrar_ranking():
    print("\n🏆 Tabla de Clasificación (Solo Pokémon que han peleado):")
    ranking_filtrado = {name: wins for name, wins in ranking.items() if wins > 0}

    if not ranking_filtrado:
        print("❌ Aún no hay Pokémon con victorias.")
        return

    ranking_ordenado = sorted(ranking_filtrado.items(), key=lambda x: x[1], reverse=True)
    for i, (name, wins) in enumerate(ranking_ordenado):
        print(f"{i + 1}. {name} - {wins} victorias")

# Función para agregar un nuevo Pokémon
def agregar_pokemon():
    name = input("🆕 Nombre del Pokémon: ")
    type_1 = input("🌱 Tipo del Pokémon: ")
    attack = input("⚔ Ataque: ")
    defense = input("🛡 Defensa: ")
    hp = input("❤️ HP: ")

    new_pokemon = {"name": name, "type_1": type_1, "attack": attack, "defense": defense, "hp": hp}
    pokemon_list.append(new_pokemon)
    guardar_pokemon()

    print(f"\n✅ Pokémon {name} agregado con éxito!")

# Función para eliminar un Pokémon
def eliminar_pokemon():
    if not pokemon_list:
        print("\n❌ No hay Pokémon para eliminar.")
        return

    mostrar_pokemon()
    
    try:
        index = int(input("\n🗑 Escribe el número del Pokémon a eliminar: ")) - 1
        if 0 <= index < len(pokemon_list):
            eliminado = pokemon_list.pop(index)
            guardar_pokemon()
            print(f"\n✅ Pokémon {eliminado['name']} eliminado con éxito!")
        else:
            print("❌ Número inválido.")
    except ValueError:
        print("❌ Entrada no válida.")

# Función para escoger Pokémon y simular batalla
def batalla():
    if len(pokemon_list) < 2:
        print("\n❌ No hay suficientes Pokémon para una batalla.")
        return

    mostrar_pokemon()
    
    try:
        p1 = int(input("\n🎮 Escribe el número del primer Pokémon: ")) - 1
        p2 = int(input("🎮 Escribe el número del segundo Pokémon: ")) - 1

        if p1 == p2:
            print("\n❌ No puedes elegir el mismo Pokémon.")
            return

        if 0 <= p1 < len(pokemon_list) and 0 <= p2 < len(pokemon_list):
            pokemon1 = pokemon_list[p1]
            pokemon2 = pokemon_list[p2]

            score1 = int(pokemon1["attack"]) + int(pokemon1["defense"]) + int(pokemon1["hp"]) + random.randint(0, 10)
            score2 = int(pokemon2["attack"]) + int(pokemon2["defense"]) + int(pokemon2["hp"]) + random.randint(0, 10)

            print(f"\n⚔ Batalla entre {pokemon1['name']} y {pokemon2['name']}!")
            print(f"{pokemon1['name']} (Puntos: {score1}) 🆚 {pokemon2['name']} (Puntos: {score2})")

            if score1 > score2:
                print(f"\n🏆 ¡{pokemon1['name']} gana la batalla!")
                ranking[pokemon1["name"]] = ranking.get(pokemon1["name"], 0) + 1
            elif score1 < score2:
                print(f"\n💀 ¡{pokemon2['name']} gana la batalla!")
                ranking[pokemon2["name"]] = ranking.get(pokemon2["name"], 0) + 1
            else:
                print("\n🤝 ¡Es un empate!")

            guardar_ranking()
        else:
            print("❌ Uno de los números es inválido.")
    except ValueError:
        print("❌ Entrada no válida.")

# Menú principal
while True:
    print("\n🌟 MENÚ DE POKÉMON 🌟")
    print("1️⃣ Ver Pokémon disponibles")
    print("2️⃣ Crear un nuevo Pokémon")
    print("3️⃣ Eliminar un Pokémon")
    print("4️⃣ Iniciar una batalla")
    print("5️⃣ Ver tabla de clasificación")
    print("6️⃣ Salir")

    opcion = input("🔹 Escoge una opción: ")

    if opcion == "1":
        mostrar_pokemon()
    elif opcion == "2":
        agregar_pokemon()
    elif opcion == "3":
        eliminar_pokemon()
    elif opcion == "4":
        batalla()
    elif opcion == "5":
        mostrar_ranking()
    elif opcion == "6":
        print("\n👋 ¡Hasta la próxima!")
        break
    else:
        print("❌ Opción no válida. Intenta otra vez.")

