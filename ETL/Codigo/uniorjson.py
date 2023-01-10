import json
import os
 
# Obtenemos una lista de todos los archivos en la carpeta
archivos = os.listdir('./transcript')
 
if os.path.exists('./transcript'):
    print('La carpeta ./transcript existe')
else:
    print('La carpeta ./transcript no existe')
 
if os.access('./transcript', os.R_OK):
    print('Tienes permisos de lectura para la carpeta ./transcript')
else:
    print('No tienes permisos de lectura para la carpeta ./transcript')
    
filtrados = [] 
# Iteramos a través de cada archivo en la carpeta
for nombre_archivo in archivos:
 # Si el archivo tiene la extensión .json, lo abrimos y filtramos
    if nombre_archivo.endswith('.json'):
        os.path.exists(nombre_archivo)
 # Imprimimos la ruta completa del archivo
 #print(f'./transcript/{nombre_archivo}')
        print('El nombre del archivo es', nombre_archivo)
 
        with open(f'./transcript/{nombre_archivo}', 'r') as f:
            datos = json.load(f)
    #texto = f.read()
    
    # Creamos una lista para almacenar los elementos que cumplen con las condiciones
            
        #print('He creado una lista')
        
        # Iteramos a través de cada elemento en el archivo
            for elemento in datos:
        # Si el campo "texto" del elemento cumple con ciertas condiciones, lo agregamos a la lista
                filtrados.append(elemento['text'])
        
        # Creamos un nuevo archivo y escribimos la lista de elementos filtrados en él
                with open(f'filtrados.json', 'w') as f:
                    json.dump(filtrados, f)
                    print('He rellenado el archivo filtrados.json')