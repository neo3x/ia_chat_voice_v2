#!/usr/bin/env python3
import requests

print("Probando conexión con Ollama...")

# Test 1: Verificar que Ollama responde
try:
    resp = requests.get('http://localhost:11434/api/tags')
    print(f"Ollama status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print("Modelos disponibles:")
        for model in data.get('models', []):
            print(f"  - {model['name']}")
except Exception as e:
    print(f"Error conectando con Ollama: {e}")

# Test 2: Probar chat directamente con Ollama
print("\nProbando chat con Ollama...")
try:
    payload = {
        "model": "llama2:7b",
        "messages": [
            {"role": "system", "content": "Responde en español."},
            {"role": "user", "content": "Hola"}
        ],
        "stream": False
    }
    resp = requests.post('http://localhost:11434/api/chat', json=payload, timeout=30)
    print(f"Chat status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print(f"Respuesta: {data.get('message', {}).get('content', 'SIN CONTENIDO')}")
    else:
        print(f"Error: {resp.text}")
except Exception as e:
    print(f"Error en chat: {e}")
