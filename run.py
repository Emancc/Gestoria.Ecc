#!/usr/bin/env python3
"""
Script de inicio para la aplicación Documentación Vehicular
"""

import os
from app import app, db, check_db_connection

def create_app():
    """Crear y configurar la aplicación Flask"""
    # Configurar variables de entorno
    os.environ.setdefault('FLASK_ENV', 'development')
    
    # Verificar conexión a la base de datos
    if not check_db_connection():
        print("\n❌ No se pudo conectar a la base de datos")
        print("💡 Ejecuta los siguientes comandos para configurar las migraciones:")
        print("   1. flask db init")
        print("   2. flask db migrate")
        print("   3. flask db upgrade")
        return None
    
    print("✅ Conexión a MySQL exitosa")
    print("🗄️  Base de datos: gestoria")
    print("👤 Usuario: root (sin contraseña)")
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    if app is None:
        print("\n❌ No se pudo inicializar la aplicación")
        print("\n🔧 Pasos para configurar la base de datos:")
        print("1. Asegúrate de que MySQL esté ejecutándose")
        print("2. Verifica que la base de datos 'gestoria' exista")
        print("3. Ejecuta: flask db init")
        print("4. Ejecuta: flask db migrate")
        print("5. Ejecuta: flask db upgrade")
        exit(1)
    
    print("\n🚗 Iniciando Documentación Vehicular...")
    print("📱 Abre tu navegador en: http://localhost:5000")
    print("⏹️  Presiona Ctrl+C para detener la aplicación")
    print("=" * 50)
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\n👋 Aplicación detenida por el usuario")
    except Exception as e:
        print(f"\n❌ Error al iniciar la aplicación: {e}")
