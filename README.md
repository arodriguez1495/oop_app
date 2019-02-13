# oop_app

Para utilizar esta aplicacion deben tener instalado Python 3 o superior.  

Clonar el repositorio mediante terminal (linux y mac) utilizando el comando:  
$ git clone https://github.com/arodriguez1495/oop_app.git

Para el caso de windows debes instalar git (https://github.com/arodriguez1495/oop_app.git) y utilizar el mismo comando.  

Luego entrar a la carpeta:  
$ cd oop_app/  

Despues instalar las librerias de python necesarias para que la app funcione:  
$ pip install -r requirements.txt  

Finalmente para inicializar el app utilizar el comando:  
$ python3 app.py  


Estos son los archivos necesarios para el funcionamiento de la aplicacion:  
1. app.py : aplicacion principal
2. teacher.py: Clase de profesor
3. admin.py: Clase de administrador (herencia de profesor)
4. school.db: Base de datos de la escuela

En el archivo "sqlite.py" se encuentra el script utilizado para crear la bd "school.db" (tabla, conexiones y generar datos ficticios).

