#!/usr/bin/env python3
"""
Script para corregir problemas de indentación en archivos Python
"""
import os
import glob

def fix_python_file(filepath):
    """Corregir espacios al inicio de archivos Python"""
    try:
        # Leer el archivo
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar si tiene espacios al inicio
        if content and (content[0] == ' ' or content[0] == '\t'):
            # Eliminar espacios/tabs al inicio
            original_len = len(content)
            content = content.lstrip()
            removed_chars = original_len - len(content)
            
            # Escribir el archivo corregido
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✓ Corregido: {filepath} (eliminados {removed_chars} caracteres)")
            return True
        else:
            print(f"  OK: {filepath}")
            return False
            
    except Exception as e:
        print(f"✗ Error en {filepath}: {e}")
        return False

def main():
    """Buscar y corregir todos los archivos Python"""
    print("=" * 50)
    print("Buscando archivos Python con problemas...")
    print("=" * 50)
    
    # Patrones de archivos a buscar
    patterns = [
        "*.py",
        "services/*.py",
        "models/*.py",
        "utils/*.py",
        "static/js/*.js",  # También revisar JavaScript
    ]
    
    all_files = []
    for pattern in patterns:
        all_files.extend(glob.glob(pattern, recursive=True))
    
    # Eliminar duplicados
    all_files = list(set(all_files))
    
    print(f"\nEncontrados {len(all_files)} archivos para revisar\n")
    
    fixed_count = 0
    for filepath in sorted(all_files):
        if os.path.isfile(filepath):
            if fix_python_file(filepath):
                fixed_count += 1
    
    print("\n" + "=" * 50)
    print(f"Resumen: {fixed_count} archivos corregidos")
    print("=" * 50)
    
    if fixed_count > 0:
        print("\n⚠️  IMPORTANTE: Ahora debes reconstruir los contenedores:")
        print("  1. docker-compose down")
        print("  2. docker-compose build --no-cache")
        print("  3. docker-compose up -d")

if __name__ == "__main__":
    main()