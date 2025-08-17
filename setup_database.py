#!/usr/bin/env python3
"""
Script para configurar y verificar la conexión a MySQL
"""

import pymysql
import sys
import getpass

def test_mysql_connection(host, user, password, database=None):
    """Probar conexión a MySQL"""
    try:
        if database:
            connection = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
        else:
            connection = pymysql.connect(
                host=host,
                user=user,
                password=password
            )
        
        print(f"✅ Conexión exitosa a MySQL en {host}")
        print(f"👤 Usuario: {user}")
        
        if database:
            print(f"🗄️  Base de datos: {database}")
        
        # Probar consulta simple
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"📊 Versión de MySQL: {version[0]}")
        
        connection.close()
        return True
        
    except pymysql.Error as e:
        print(f"❌ Error de conexión: {e}")
        return False

def create_database(host, user, password, database_name):
    """Crear base de datos si no existe"""
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password
        )
        
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
            print(f"✅ Base de datos '{database_name}' creada/verificada")
            
            # Verificar permisos
            cursor.execute(f"SHOW GRANTS FOR '{user}'@'{host}'")
            grants = cursor.fetchall()
            print(f"🔑 Permisos del usuario {user}:")
            for grant in grants:
                print(f"   {grant[0]}")
        
        connection.close()
        return True
        
    except pymysql.Error as e:
        print(f"❌ Error al crear base de datos: {e}")
        return False

def interactive_setup():
    """Configuración interactiva de MySQL"""
    print("🔧 Configuración de MySQL para Documentación Vehicular")
    print("=" * 50)
    
    # Obtener credenciales del usuario
    host = input("Host de MySQL (default: localhost): ").strip() or "localhost"
    user = input("Usuario de MySQL (default: root): ").strip() or "root"
    password = getpass.getpass("Contraseña de MySQL: ")
    database = input("Nombre de la base de datos (default: gestoria): ").strip() or "gestoria"
    
    print(f"\n📋 Configuración ingresada:")
    print(f"   Host: {host}")
    print(f"   Usuario: {user}")
    print(f"   Base de datos: {database}")
    
    # Probar conexión sin base de datos
    print(f"\n🔍 Probando conexión a MySQL...")
    if not test_mysql_connection(host, user, password):
        print("❌ No se pudo conectar a MySQL")
        print("💡 Verifica que:")
        print("   - MySQL esté ejecutándose")
        print("   - El usuario y contraseña sean correctos")
        print("   - El usuario tenga permisos para conectarse desde localhost")
        return None
    
    # Crear base de datos
    print(f"\n🗄️  Creando base de datos...")
    if not create_database(host, user, password, database):
        print("❌ No se pudo crear la base de datos")
        return None
    
    # Probar conexión con base de datos
    print(f"\n🔍 Probando conexión a la base de datos...")
    if not test_mysql_connection(host, user, password, database):
        print("❌ No se pudo conectar a la base de datos")
        return None
    
    # Generar configuración
    config = {
        'host': host,
        'user': user,
        'password': password,
        'database': database
    }
    
    print(f"\n✅ Configuración completada exitosamente!")
    return config

def generate_env_file(config):
    """Generar archivo .env con la configuración"""
    env_content = f"""# Configuración de MySQL generada automáticamente
MYSQL_USER={config['user']}
MYSQL_PASSWORD={config['password']}
MYSQL_HOST={config['host']}
MYSQL_DATABASE={config['database']}

# Configuración de Flask
FLASK_ENV=development
SECRET_KEY=mi_clave_secreta_super_segura_2025
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("📁 Archivo .env creado con la configuración")
        return True
    except Exception as e:
        print(f"❌ Error al crear archivo .env: {e}")
        return False

def update_config_py(config):
    """Actualizar config.py con las credenciales"""
    try:
        with open('config.py', 'r') as f:
            content = f.read()
        
        # Reemplazar las credenciales por defecto
        content = content.replace("MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or '123456'", 
                                f"MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or '{config['password']}'")
        
        with open('config.py', 'w') as f:
            f.write(content)
        
        print("📝 Archivo config.py actualizado")
        return True
    except Exception as e:
        print(f"❌ Error al actualizar config.py: {e}")
        return False

def main():
    """Función principal"""
    print("🚗 Configuración de MySQL para Documentación Vehicular")
    print("=" * 60)
    
    # Configuración interactiva
    config = interactive_setup()
    if not config:
        print("\n❌ La configuración falló. Intenta nuevamente.")
        sys.exit(1)
    
    # Generar archivos de configuración
    print(f"\n📁 Generando archivos de configuración...")
    
    if generate_env_file(config):
        print("✅ Archivo .env creado")
    else:
        print("⚠️  No se pudo crear .env, pero puedes crearlo manualmente")
    
    if update_config_py(config):
        print("✅ Archivo config.py actualizado")
    else:
        print("⚠️  No se pudo actualizar config.py")
    
    print(f"\n🎉 Configuración completada!")
    print(f"\n📋 Próximos pasos:")
    print(f"1. Ejecuta: flask db init")
    print(f"2. Ejecuta: flask db migrate")
    print(f"3. Ejecuta: flask db upgrade")
    print(f"4. Ejecuta: python run.py")
    
    print(f"\n🔧 Si prefieres usar variables de entorno:")
    print(f"   export MYSQL_USER={config['user']}")
    print(f"   export MYSQL_PASSWORD={config['password']}")
    print(f"   export MYSQL_HOST={config['host']}")
    print(f"   export MYSQL_DATABASE={config['database']}")

if __name__ == '__main__':
    main()
