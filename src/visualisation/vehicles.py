import sqlite3
import os
import requests
import json

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(CURRENT_DIR, 'vehicles.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            marque TEXT NOT NULL,
            modele TEXT NOT NULL,
            consommation REAL NOT NULL,  -- L/100km
            type_carburant TEXT NOT NULL,  -- 'essence' or 'diesel'
            co2_g_per_km REAL NOT NULL
        )
    ''')
    
    # Insérer les véhicules courants
    vehicles_data = [
        ('Peugeot', '208', 5.5, 'essence', 125),
        ('Volkswagen', 'Passat', 6.2, 'diesel', 145),
        ('Kia', 'Venga', 5.8, 'essence', 135),
        ('Renault', 'Clio', 5.2, 'essence', 120),
        ('Renault', 'Clio 4', 5.0, 'essence', 115),
        ('Renault', 'Scénic', 6.5, 'diesel', 150),
        ('Peugeot', '308', 5.8, 'diesel', 130),
        ('Citroën', 'C3', 5.0, 'essence', 110),
        ('Ford', 'Fiesta', 5.3, 'essence', 120),
        ('Toyota', 'Yaris', 4.8, 'essence', 105),
        ('Nissan', 'Qashqai', 6.0, 'diesel', 140),
        ('Volkswagen', 'Golf', 5.5, 'essence', 125),
        ('Peugeot', '3008', 6.2, 'diesel', 145),
        ('Renault', 'Captur', 5.8, 'essence', 135),
        ('Dacia', 'Sandero', 5.5, 'essence', 125),
        ('Opel', 'Corsa', 5.2, 'essence', 118),
        ('Fiat', '500', 5.0, 'essence', 115),
        ('Hyundai', 'i20', 5.1, 'essence', 117),
        ('Kia', 'Rio', 5.3, 'essence', 122),
        ('Seat', 'Ibiza', 5.4, 'essence', 124),
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO vehicles (marque, modele, consommation, type_carburant, co2_g_per_km)
        VALUES (?, ?, ?, ?, ?)
    ''', vehicles_data)
    
    conn.commit()
    conn.close()

def get_all_vehicles():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, marque, modele, consommation, type_carburant, co2_g_per_km FROM vehicles ORDER BY marque, modele')
    vehicles = cursor.fetchall()
    conn.close()
    return [{'id': v[0], 'marque': v[1], 'modele': v[2], 'consommation': v[3], 'type_carburant': v[4], 'co2_g_per_km': v[5]} for v in vehicles]

def get_vehicle_by_id(vehicle_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, marque, modele, consommation, type_carburant, co2_g_per_km FROM vehicles WHERE id = ?', (vehicle_id,))
    vehicle = cursor.fetchone()
    conn.close()
    if vehicle:
        return {'id': vehicle[0], 'marque': vehicle[1], 'modele': vehicle[2], 'consommation': vehicle[3], 'type_carburant': vehicle[4], 'co2_g_per_km': vehicle[5]}
    return None

def get_fuel_prices():
    try:
        url = "https://www.prix-carburants.gouv.fr/rn/1.0/somme"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        essence_price = data.get('SP95', {}).get('prix_moyen', 1.70)
        diesel_price = data.get('Gazole', {}).get('prix_moyen', 1.60)
        
        return {
            'essence': round(essence_price / 1000, 3),
            'diesel': round(diesel_price / 1000, 3)
        }
    except Exception as e:
        print(f"Erreur récupération prix carburant depuis API: {e}")
        try:
            return {
                'essence': 1.75,
                'diesel': 1.65
            }
        except:
            return {
                'essence': 1.60,
                'diesel': 1.50
            }

init_db()