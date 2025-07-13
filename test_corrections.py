#!/usr/bin/env python3
"""
Script de prueba para verificar las correcciones
"""
import requests
import json

def test_spanish_response():
    """Probar que las respuestas sean solo en español"""
    print("Probando respuestas en español...")
    
    test_messages = [
        "Hello, how are you?",
        "What's your name?",
        "Can you help me?",
        "Hola, ¿cómo estás?"
    ]
    
    for msg in test_messages:
        print(f"\nPregunta: {msg}")
        try:
            response = requests.post('http://localhost:7860/chat', 
                                   json={'message': msg},
                                   timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"Respuesta: {data.get('response', 'Sin respuesta')}")
                
                # Verificar que no haya palabras en inglés comunes
                english_words = ['I\'m', 'I am', 'AI', 'assistant', 'help', 'tasks', 'humans']
                response_text = data.get('response', '').lower()
                found_english = [w for w in english_words if w.lower() in response_text]
                
                if found_english:
                    print(f"  ⚠️  Encontradas palabras en inglés: {found_english}")
                else:
                    print("  ✓ Respuesta completamente en español")
                    
        except Exception as e:
            print(f"  ✗ Error: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("Pruebas de correcciones")
    print("=" * 50)
    test_spanish_response()
