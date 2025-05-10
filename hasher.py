import hashlib
import os
import sys
import requests
from pathlib import Path
from typing import Set, Tuple

# Salt fijo para el proceso de hash
SALT_FIJO = "123qwesd"

def descargar_diccionario() -> Set[str]:
    """Descarga y genera un diccionario extenso de passwords"""
    print("\n🌍 Descargando diccionario de passwords...")
    
    # Diccionario base por si falla la descarga
    passwords = {
        '123456', 'password', 'admin', '12345678', 'qwerty',
        'abc123', '123456789', 'password1', '1234567', '12345',
        'admin123', 'test', 'root', '1234', '1q2w3e4r'
    }

    # Intenta descargar diccionario online
    url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000.txt"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            nuevas = set(response.text.splitlines())
            print(f"✅ Añadidas {len(nuevas)} passwords del diccionario online")
            passwords.update(nuevas)
    except Exception as e:
        print(f"⚠️ Usando diccionario local: {e}")

    # Genera variaciones comunes
    variations = set()
    for pwd in passwords:
        variations.update([
            pwd.lower(), pwd.upper(),
            f"{pwd}123", f"{pwd}!", f"{pwd}#",
            pwd[::-1],  # Reverso
            pwd + pwd,  # Duplicado
            *[f"{pwd}{i}" for i in range(10)]  # Números al final
        ])

    passwords.update(variations)
    print(f"🔐 Diccionario total: {len(passwords)} passwords")
    return passwords

# Inicializa el diccionario al cargar el script
PASSWORDS = descargar_diccionario()

def mostrar_menu() -> int:
    """Menú principal con estilo 😎"""
    print("\n🔐 Hasheitor de Terminator - ¡Donde los hashes vienen a morir! 🔐")
    print("╔═══════════════════════════════════════════════╗")
    print("║ 🔄 1. MD5 → Texto plano (modo detective)      ║")
    print("║ 🔒 2. Texto → SHA256 con salt fijo            ║")
    print("║ 🔐 3. Texto → SHA256 con salt fijo+variable   ║")
    print("║ 🔓 4. SHA256 → Texto plano                    ║")
    print("║ 🚪 5. Salir (huida estratégica)              ║")
    print("╚═══════════════════════════════════════════════╝")
    return int(input("\n😎 Elige tu aventura (1-5): "))

def md5_a_plano(hash_md5: str) -> str:
    """Convierte hash MD5 a texto usando múltiples técnicas"""
    try:
        hash_md5 = hash_md5.strip().lower()
        if not hash_md5:
            return ''

        # 1. Busca en el diccionario principal
        for password in PASSWORDS:
            if hashlib.md5(str(password).encode()).hexdigest() == hash_md5:
                return str(password)

        # 2. Prueba números secuenciales
        for i in range(10000):
            if hashlib.md5(str(i).encode()).hexdigest() == hash_md5:
                return str(i)

        # 3. Patrones de teclado comunes
        for pattern in ['qwerty', 'asdfgh', '123qwe', 'zxcvbn', '1q2w3e']:
            if hashlib.md5(pattern.encode()).hexdigest() == hash_md5:
                return pattern

        return ''
    except:
        return ''

def get_input_file() -> str:
    """Maneja la entrada del archivo (arrastrado o ruta)"""
    if len(sys.argv) > 1:
        path = Path(sys.argv[1].strip("'\""))
        if path.exists() and path.suffix == '.txt':
            return str(path)
    
    while True:
        print("\n[❌] Escribe 'exit' para volver al menú")
        ruta = input("📂 Arrastra o escribe la ruta del archivo .txt: ").strip().strip("'\"")
        
        if ruta.lower() == 'exit':
            return ''
            
        path = Path(ruta)
        if path.exists() and path.suffix == '.txt':
            return str(path)
        print("❌ Archivo no válido o no encontrado")

def get_output_file(input_path: str, suffix: str) -> str:
    """Genera nombre para archivo de salida"""
    path = Path(input_path)
    salida = input(f"\n📝 Nombre del archivo de salida [{path.stem}_{suffix}.txt]: ").strip()
    if not salida:
        salida = f"{path.stem}_{suffix}.txt"
    return str(path.parent / salida)

def plano_a_sha256(texto: str, salt: str = "") -> str:
    """Genera hash SHA256 con salt opcional"""
    try:
        texto = texto.strip()
        return hashlib.sha256(f"{salt}{texto}".encode()).hexdigest() if texto else ''
    except:
        return ''

def parse_line(line: str) -> Tuple[str, str]:
    """Parsea una línea en formato email:password"""
    parts = line.strip().split(':')
    return (parts[0], parts[1]) if len(parts) == 2 else ('', line.strip())

def procesar_archivo(funcion_conversion, suffix: str):
    """Procesa el archivo aplicando la conversión seleccionada"""
    try:
        entrada = get_input_file()
        if not entrada:
            return
            
        salida = get_output_file(entrada, suffix)
        
        print(f"\n🚀 Procesando: {entrada}")
        print(f"📝 Guardando en: {salida}")
        
        if input("\n¿Comenzamos? (s/n): ").lower() != 's':
            print("\n⏪ Volviendo al menú...")
            return
        
        total = convertidos = 0
        
        with open(entrada, 'r') as f_in, open(salida, 'w') as f_out:
            for linea in f_in:
                if suffix == "sha256_var":
                    email, password = parse_line(linea)
                    hash_result = plano_a_sha256(password, f"{SALT_FIJO}{email}")
                    resultado = f"{email}:{hash_result}\n" if email else f"{hash_result}\n"
                else:
                    resultado = f"{funcion_conversion(linea.strip())}\n"
                
                f_out.write(resultado)
                total += 1
                if resultado.strip():
                    convertidos += 1
                
                if total % 50 == 0:
                    print(f"⚡ {total} hashes procesados...")
        
        print(f"\n✨ ¡Misión cumplida!")
        print(f"📊 Resultados:")
        print(f"   • Total: {total}")
        print(f"   • Convertidos: {convertidos}")
        print(f"   • Fallidos: {total - convertidos}")
        
    except FileNotFoundError:
        print("\n💥 ¡El archivo se ha escondido muy bien!")
    except Exception as e:
        print(f"\n💀 Error: {str(e)}")

def main():
    print("\n¡Bienvenido al laboratorio secreto de hashing! 🧪")
    print("💡 Tip: Puedes arrastrar archivos .txt al terminal")
    
    while True:
        try:
            opcion = mostrar_menu()
            
            if opcion == 1:
                procesar_archivo(md5_a_plano, "plain")
            elif opcion == 2:
                procesar_archivo(lambda x: plano_a_sha256(x, SALT_FIJO), "sha256")
            elif opcion == 3:
                procesar_archivo(lambda x: x, "sha256_var")
            elif opcion == 4:
                procesar_archivo(lambda x: plano_a_sha256(x, SALT_FIJO), "plain")
            elif opcion == 5:
                print("\n👋 ¡Hasta la próxima, crypto-warrior!")
                break
            else:
                print("\n🤦 ¡Esa opción no existe en este universo!")
                
        except ValueError:
            print("\n🚫 ¡Los números, por favor!")
        except KeyboardInterrupt:
            print("\n\n😱 ¡Interrupción detectada!")
            break
        except Exception as e:
            print(f"\n💣 ¡Ka-boom! Error: {str(e)}")

if __name__ == "__main__":
    main()