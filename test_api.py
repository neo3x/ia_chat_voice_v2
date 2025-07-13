#!/usr/bin/env python3
"""
Prueba directa de la API
"""
import requests
import json

print("Probando API...")

# Probar health
try:
    resp = requests.get('http://localhost:7860/health')
    print(f"Health check: {resp.status_code}")
    print(f"Respuesta: {resp.json()}")
except Exception as e:
    print(f"Error en health: {e}")

# Probar chat
try:
    resp = requests.post('http://localhost:7860/chat', 
                        json={'message': 'Hola'},
                        timeout=30)
    print(f"\nChat test: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print(f"Respuesta del bot: {data.get('response', 'SIN RESPUESTA')}")
    else:
        print(f"Error: {resp.text}")
except Exception as e:
    print(f"Error en chat: {e}")

# Probar modelos
try:
    resp = requests.get('http://localhost:7860/api/models')
    print(f"\nModels test: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print(f"Modelos: {data.get('models', [])}")
        print(f"Modelo actual: {data.get('current', 'NINGUNO')}")
except Exception as e:
    print(f"Error en models: {e}")
