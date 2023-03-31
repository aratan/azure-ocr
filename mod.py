#Librerias
import json
import os

import jsonlint
from dotenv import load_dotenv
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient, BlobClient



# Carga las variables de entorno desde el archivo .env
load_dotenv()

endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")
model_id = "model_1"
formUrl = "https://github.com/aratan/Azure-OCR/blob/adfe9d0db7be28cda624e9ea1370d84a67779627/parte_amistoso_0.jpg?raw=true"

document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# Make sure your document's type is included in the list of document types the custom model can analyze
poller = document_analysis_client.begin_analyze_document_from_url(model_id, formUrl)
result = poller.result()

for idx, document in enumerate(result.documents):
    #print("--------Analyzing document #{}--------".format(idx + 1))
    #print("Document has type {}".format(document.doc_type))
    #print("Document has confidence {}".format(document.confidence))
    #print("Document was analyzed by model with ID {}".format(result.model_id))
    for name, field in document.fields.items():
        field_value = field.value if field.value else field.content
        print("......found field of type '{}' with value '{}' and with confidence {}".format(field.value_type,
                                                                                                field_value,
                                                                                                 field.confidence))


    # iterate over tables, lines, and selection marks on each page
    for page in result.pages:
        print("\nLines found on page {}".format(page.page_number))
        '''
        for line in page.lines:
            print("...Line '{}'".format(line.content.encode('utf-8')))
        
        for word in page.words:
            print(
                "...Word '{}' has a confidence of {}".format(
                    word.content.encode('utf-8'), word.confidence
                )
            )
        '''
        '''
        for selection_mark in page.selection_marks:
            print(
                "...Selection mark is '{}' and has a confidence of {}".format(
                    selection_mark.state, selection_mark.confidence
                )
            )
        '''
'''
    for i, table in enumerate(result.tables):
        print("\nTable {} can be found on page:".format(i + 1))
        for region in table.bounding_regions:
            print("...{}".format(i + 1, region.page_number))
        for cell in table.cells:
            print(
                "...Cell[{}][{}] has content '{}'".format(
                    cell.row_index, cell.column_index, cell.content.encode('utf-8')
                )
            )
    
    print("-----------------------------------")
    '''


n = 0;
diccionario = {}

for word in page.words:
    n = n + 1
    # print(len(page.words))
    # print(f"{n} '{word.content}' ,fiabilidad {word.confidence} * Lee todo *")
    diccionario[n] = word.content

    
try:
    data = jsonlint.ValidationError(diccionario)
    print("\n El JSON es válido/reparado:", data)
    
except json.JSONDecodeError as err:
    print("\n El JSON no es válido:", err)

    # print(data)

print("----------------------------------------")


# lo más facil del mundo, componer.
# Buscamos los datos que queremos de cada asegurado/cliente

# Datos del asegurado A
nombre_a = diccionario[645]
fecha_a = diccionario[676]
danos_a = "Daños apreciado vehiculo B " + diccionario[705] + diccionario[706] + diccionario[707]

# Datos de asegurado B
nombre_b = diccionario[645]
fecha_b = diccionario[676]
danos_b = "Daños apreciado vehiculo B " + diccionario[705] + diccionario[706] + " " + diccionario[707]

# los pintamos para ver si estan bien
# print('Vehicle Data:', nombre_b)
# print('Accident Date:', fecha_b)
# print('Daños', danos_b)

# Componemos el json con los datos de cada cliente
cliente_a = {
    "nombre": nombre_a,
    "Fecha_Acidente": fecha_a,
    "Daños": danos_a
}

cliente_b = {
    "nombre": nombre_b,
    "Fecha_Acidente": fecha_b,
    "Daños": danos_b
}

# fusion de los datos para que cada cual tenga sus cosas y no este mezclado
clientes = {"cliente1": cliente_a, "cliente2": cliente_b}

# lo pintamos para ver si esta bien
print(clientes)

# Salvamos el json personalizado con los datos que nos piden
# tambien para la descarga

with open("personalizado.json", "w") as archivo:
    # Escribe el objeto JSON en el archivo usando la función dump()
    json.dump(clientes, archivo)
