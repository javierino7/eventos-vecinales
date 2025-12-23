\# Eventos Vecinales



Plataforma web para publicar y gestionar eventos comunitarios, con control de estados, cupos e inscripción de asistentes. Incluye validaciones como restricción +18 cuando corresponde.



\## Requisitos

\- Python 3.x

\- Git

\- MySQL (Azure Database for MySQL) o MySQL local

\- Pip



\## Instalación y ejecución (entorno local)

1\. Clonar repositorio:

&nbsp;  git clone https://github.com/javierino7/eventos-vecinales.git

2\. Entrar al proyecto:

&nbsp;  cd eventos\_vecinales

3\. Crear y activar entorno virtual:

&nbsp;  python -m venv venv

&nbsp;  .\\venv\\Scripts\\activate

4\. Instalar dependencias:

&nbsp;  pip install -r requirements.txt

5\. Configurar base de datos en settings.py (Azure Database for MySQL):

&nbsp;  - HOST: ev-mysql-vecinal.mysql.database.azure.com

&nbsp;  - PORT: 3306

&nbsp;  - SSL requerido

6\. Migraciones:

&nbsp;  python manage.py makemigrations

&nbsp;  python manage.py migrate

7\. Ejecutar:

&nbsp;  python manage.py runserver

8\. Acceso:

&nbsp;  http://127.0.0.1:8000/



\## Nota de seguridad

No incluir credenciales ni llaves en el repositorio. La configuración sensible debe manejarse con variables de entorno cuando corresponda.



