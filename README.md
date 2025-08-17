# Documentación Vehicular

Aplicación web desarrollada en Flask para la gestión de documentación vehicular, incluyendo vehículos, gestoría y entrega de papeles.

## Características

- **Gestión de Vehículos**: Registro de vehículos con información del cliente, modelo, lugar de compra, color y patente
- **Gestoría**: Control de papeles recibidos y observaciones por cliente y patente
- **Entrega de Papeles**: Seguimiento de documentación entregada con fechas
- **Base de Datos MySQL**: Almacenamiento persistente con SQLAlchemy y Flask-Migrate

## Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Base de Datos**: MySQL con SQLAlchemy
- **Migraciones**: Flask-Migrate con Alembic
- **Frontend**: Bootstrap 5 + Bootstrap Icons
- **Lenguaje**: Python 3.8+

## Requisitos Previos

- **Python 3.8+**
- **MySQL Server** ejecutándose en localhost
- **Base de datos 'gestoria'** creada en MySQL

## Instalación

1. **Clonar o descargar el proyecto**

2. **Crear un entorno virtual (recomendado):**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # En Windows
   # o
   source venv/bin/activate  # En Linux/Mac
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar MySQL:**
   ```bash
   # Ejecutar el script de configuración interactiva
   python setup_database.py
   ```

## Configuración de Migraciones

### **Primera vez (Inicialización):**
```bash
# 1. Inicializar el sistema de migraciones
flask db init

# 2. Crear la primera migración
flask db migrate

# 3. Aplicar la migración
flask db upgrade
```

### **Comandos de Migración Disponibles:**
```bash
# Inicializar sistema de migraciones
flask db init

# Crear migración automática
flask db migrate

# Crear migración con mensaje personalizado
flask db migrate -m "Agregar nueva columna"

# Aplicar migraciones pendientes
flask db upgrade

# Ver estado de migraciones
flask db current
flask db history
```

## Uso

1. **Ejecutar la aplicación:**
   ```bash
   python run.py
   # o
   python app.py
   ```

2. **Abrir en el navegador:**
   ```
   http://localhost:5000
   ```

## Estructura del Proyecto

```
Documentacion_Vehicular/
├── app.py                 # Aplicación principal Flask
├── config.py              # Configuración de la aplicación
├── run.py                 # Script de inicio
├── setup_database.py      # Script de configuración de MySQL
├── requirements.txt       # Dependencias del proyecto
├── README.md             # Este archivo
├── templates/            # Plantillas HTML
│   ├── base.html         # Plantilla base con Bootstrap
│   ├── vehiculos.html    # Página de gestión de vehículos
│   ├── gestoria.html     # Página de gestión de gestoría
│   └── entrega_papeles.html # Página de entrega de papeles
└── .gitignore            # Archivos a excluir del control de versiones
```

## Funcionalidades

### Vehículos
- Agregar nuevos vehículos
- Visualizar lista de vehículos
- Eliminar vehículos
- Validación de patente única

### Gestoría
- Registrar papeles recibidos
- Agregar observaciones
- Seguimiento por cliente y patente

### Entrega de Papeles
- Registrar entregas de documentación
- Fechas de entrega
- Descripción de documentación entregada

### Migraciones de Base de Datos
- Control de versiones de esquema
- Migraciones automáticas y manuales
- Rollback de cambios
- Historial de modificaciones

## Base de Datos

La aplicación utiliza **MySQL** con las siguientes tablas:
- `vehiculo`: Información de vehículos
- `gestoria`: Registros de gestoría
- `entrega_papeles`: Entregas de documentación

### Configuración de Base de Datos

```python
# Conexión por defecto
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost/gestoria'
```

**Parámetros:**
- **Usuario**: root
- **Contraseña**: 123456 (configurable)
- **Host**: localhost
- **Base de datos**: gestoria

## Flujo de Trabajo con Migraciones

### **Desarrollo:**
1. Modificar modelos en `app.py`
2. Crear migración: `flask db migrate`
3. Revisar migración generada en `migrations/versions/`
4. Aplicar migración: `flask db upgrade`

### **Producción:**
1. Copiar archivos de migración
2. Ejecutar: `flask db upgrade`
3. Verificar estado: `flask db current`

## Personalización

- Modificar colores y estilos en `templates/base.html`
- Agregar nuevas funcionalidades en `app.py`
- Personalizar formularios en las plantillas HTML
- Cambiar configuración de base de datos en `config.py`
- Modificar configuración de migraciones

## Ventajas de Flask-Migrate

- ✅ **Control de versiones** del esquema de base de datos
- ✅ **Migraciones automáticas** basadas en cambios en modelos
- ✅ **Rollback** de cambios no deseados
- ✅ **Colaboración en equipo** con historial de cambios
- ✅ **Despliegue seguro** en producción
- ✅ **Sincronización** entre entornos de desarrollo y producción

## Solución de Problemas

### Error de Conexión a MySQL
1. Verifica que MySQL esté ejecutándose
2. Verifica que la base de datos 'gestoria' exista
3. Verifica que el usuario 'root' tenga permisos
4. Verifica que la contraseña sea correcta

### Error en Migraciones
1. Verifica que el directorio 'migrations' exista
2. Ejecuta `flask db init` si es la primera vez
3. Verifica que la base de datos esté accesible
4. Revisa los logs de error en la consola

### Comandos Útiles de MySQL
```sql
-- Conectar a MySQL
mysql -u root -p

-- Crear base de datos
CREATE DATABASE IF NOT EXISTS gestoria;

-- Ver bases de datos
SHOW DATABASES;

-- Usar base de datos
USE gestoria;

-- Ver tablas
SHOW TABLES;

-- Ver estructura de tabla
DESCRIBE vehiculo;
```

## Soporte

Para reportar problemas o solicitar nuevas funcionalidades, contactar al desarrollador.

## Licencia

Este proyecto es de uso libre para fines educativos y comerciales.
