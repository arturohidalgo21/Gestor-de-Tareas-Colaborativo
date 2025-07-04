# 📦 Archivo `requirements.txt` del Proyecto

Este archivo contiene todas las dependencias necesarias para ejecutar correctamente el **Sistema de Gestión de Tareas Colaborativo**.  
Es importante instalar cada una para asegurar la compatibilidad y el correcto funcionamiento del backend.

---

## 🔧 Requisitos del entorno

> Asegúrate de tener instalada la versión recomendada de Python:

```bash
Python 3.13.5
```

Puedes verificar tu versión con:

```bash
python --version
```

---

## 📋 Contenido de `requirements.txt`

```txt
Flask==2.3.2
Flask-Login==0.6.2
Flask-SQLAlchemy==3.0.3
SQLAlchemy==2.0.19
```

---

## 📖 Explicación de cada paquete

| Paquete           | Versión   | Descripción                                                                 |
|-------------------|-----------|-----------------------------------------------------------------------------|
| **Flask**         | 2.3.2     | Microframework web para Python. Facilita la creación de rutas, vistas y APIs. |
| **Flask-Login**   | 0.6.2     | Manejo sencillo de autenticación, sesiones, login/logout y protección de rutas. |
| **Flask-SQLAlchemy** | 3.0.3 | Extensión que une Flask con SQLAlchemy, simplificando consultas SQL y modelos. |
| **SQLAlchemy**    | 2.0.19    | ORM robusto y flexible para trabajar con bases de datos relacionales en Python. |

---

## ⚙️ Instalación de dependencias

Ejecuta este comando dentro del entorno virtual:

```bash
pip install -r requirements.txt
```

Esto descargará e instalará todas las librerías con las versiones exactas necesarias para correr el sistema.

---

## 🧠 Recomendación

Mantener las versiones fijas ayuda a prevenir errores por incompatibilidades entre versiones más nuevas o cambios de API.  
En proyectos colaborativos o de despliegue, ¡esto es fundamental!

---