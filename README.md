# 🔐 Hasher - Hasheitor de Terminator

> Herramienta para convertir hashes y contraseñas entre diferentes formatos, con soporte para salt fijo y variable.

## 📋 Características

- 🔄 Conversión MD5 → Texto plano (con diccionario online)
- 🔒 Conversión Texto → SHA256 con salt fijo
- 🔐 Conversión Texto → SHA256 con salt fijo + variable
- 🔓 Desencriptación de hashes SHA256 

## 🚀 Instalación

1. Crear entorno virtual:
```bash
# Instalar virtualenv si no lo tienes
sudo apt install python3-venv

# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate
```

2. Instalar dependencias:
```bash
pip install requests
```

## 💻 Uso

### Método 1: Arrastrar archivo
```bash
python hasher.py archivo.txt
```

### Método 2: Ejecutar y especificar ruta
```bash
python hasher.py
```

## 📁 Formatos de Archivo

### Para MD5 a texto plano
```plaintext
d8578edf8458ce06fbc5bb76a58c5ca4
69f1975c3dde3f6894affab807aa00a0
```

### Para SHA256 con salt variable
```plaintext
usuario1@ejemplo.com:password123
usuario2@ejemplo.com:admin123
```

## 🛠️ Cómo Funciona

1. **Diccionario de Passwords**
   - Descarga automática de SecLists
   - Backup local por si falla la descarga
   - Generación de variaciones (mayúsculas, números, etc)

2. **Conversión MD5 → Texto**
   - Búsqueda en diccionario online
   - Prueba números secuenciales
   - Patrones de teclado comunes

3. **SHA256 con Salt**
   - Salt fijo: `123qwesd`
   - Salt variable: `salt_fijo + email`
   - Formato: `SHA256(salt + password)`

## 🔍 Estructura del Código

```python
# Funciones principales
descargar_diccionario()  # Obtiene diccionario de passwords
md5_a_plano()           # Convierte MD5 a texto
plano_a_sha256()        # Genera hash SHA256 con salt
parse_line()            # Procesa formato email:password
procesar_archivo()      # Maneja la conversión de archivos
```

## 📊 Ejemplos de Uso

1. **Convertir hashes MD5**
```bash
# Input: pass.txt
d8578edf8458ce06fbc5bb76a58c5ca4

# Output: pass_plain.txt
qwerty
```

2. **Generar SHA256 con salt variable**
```bash
# Input: ejemplo.txt
usuario@test.com:password123

# Output: ejemplo_sha256_var.txt
usuario@test.com:a1b2c3... (hash SHA256)
```

## ⚙️ Requisitos

- Python 3.6+
- Sistema operativo: Linux/Unix
- Conexión a internet (opcional, para diccionario online)

## 🚨 Notas Importantes

- Los archivos deben ser .txt
- Un hash/password por línea
- Para salt variable usar formato email:password
- Salt fijo configurado: "123qwesd"

## 🔰 Tips

- Usa Ctrl+C para cancelar en cualquier momento
- Escribe 'exit' para volver al menú
- Arrastra archivos directamente al terminal
- Verifica los resultados en archivos _plain.txt o _sha256.txt

## 🎨 Personalización

Para modificar el salt fijo, edita la variable:
```python
SALT_FIJO = "123qwesd"  # Cambia por tu salt
```

## 👥 Autor

DogSoulDev
