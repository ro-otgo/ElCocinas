# import os
# import json

# contenido = os.listdir('D:/UEM/main/ElCocinas/transcript')

# for i in len(contenido):


# # test cases for jsonStringA and jsonStringB according to your data input
# jsonStringA = '{"error_1395946244342":"valueA","error_1395952003":"valueB"}'
# jsonStringB = '{"error_%d":"Error Occured on machine %s in datacenter %s on the %s of process %s"}' % (timestamp_number, host_info, local_dc, step, c)

# # now we have two json STRINGS

# dictA = json.loads(jsonStringA)
# dictB = json.loads(jsonStringB)

# merged_dict = {key: value for (key, value) in (dictA.items() + dictB.items())}

# # string dump of the merged dict
# jsonString_merged = json.dumps(merged_dict)


import json
import os
 
# Obtenemos una lista de todos los archivos en la carpeta
archivos = os.listdir('transcript')
 
# Iteramos a través de cada archivo en la carpeta
for nombre_archivo in archivos:
 # Si el archivo tiene la extensión .json, lo abrimos y filtramos
    if nombre_archivo.endswith('.json'):
        with open(nombre_archivo, 'r') as f:
            datos = json.load(f)
 
 # Creamos una lista para almacenar los elementos que cumplen con las condiciones
    filtrados = []
 
 # Iteramos a través de cada elemento en el archivo
    for elemento in datos:
 # Si el campo "texto" del elemento cumple con ciertas condiciones, lo agregamos a la lista
        if elemento['text'] == 'algo':
            filtrados.append(elemento)
 
# Creamos un nuevo archivo y escribimos la lista de elementos filtrados en él
with open('filtrados.json', 'w') as f:
 json.dump(filtrados, f)