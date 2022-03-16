"""
Base para desarrollo de modulos externos.
Para obtener el modulo/Funcion que se esta llamando:
     GetParams("module")

Para obtener las variables enviadas desde formulario/comando Rocketbot:
    var = GetParams(variable)
    Las "variable" se define en forms del archivo package.json

Para modificar la variable de Rocketbot:
    SetVar(Variable_Rocketbot, "dato")

Para obtener una variable de Rocketbot:
    var = GetVar(Variable_Rocketbot)

Para obtener la Opcion seleccionada:
    opcion = GetParams("option")


Para instalar librerias se debe ingresar por terminal a la carpeta "libs"
    
    pip install <package> -t .

"""

import json
import requests
import uuid
base_path = tmp_global_obj["basepath"]
cur_path = base_path + "modules" + os.sep + "radar" + os.sep + "libs" + os.sep

if cur_path not in sys.path:
    sys.path.append(cur_path)


global mod_radar_sessions

SESSION_DEFAULT = "default"
try:
    if not mod_radar_sessions:
        mod_radar_sessions = {SESSION_DEFAULT: {}}
except NameError:
    mod_radar_sessions = {SESSION_DEFAULT: {}}


module = GetParams("module")

try:

    if module == "connect":

        var_ = GetParams("var_")
        email = GetParams("email")
        apitoken = GetParams("apitoken")
        name_session = GetParams("session")

        json_data = {"email": email, "apiToken": apitoken}
        header = {'Content-Type': 'application/json'}
        response = requests.post(
            'https://api.somosradar.com/v1/loginToken', json=json_data, headers=header)

        if response.status_code == 200:
            if name_session is None:
                name_session = "default"
            if name_session == "":
                name_session = "default"

            SetVar(var_, True)
            token = response.json()
            token = token["access_token_jwt"]
            mod_radar_sessions[name_session] = token

        else:
            raise Exception("Email o Token incorrectos")
            SetVar(var_, False)

    if module == "getBalance":

        name_session = GetParams("session")
        var_ = GetParams("var_")

        if name_session is None:
            name_session = "default"
        if name_session == "":
            name_session = "default"

        header = {'Content-Type': 'application/json',
                  "Authorization": f"Bearer {mod_radar_sessions[name_session]}"}
        response = requests.get(
            'https://api.somosradar.com/v1/payout/balance', headers=header)

        SetVar(var_, response.json())

    if module == "createTransaction":

        rut = GetParams("rut")
        name = GetParams("name")
        email = GetParams("email")
        sbifNumber = GetParams("sbif")
        accountNumber = GetParams("accountNumber")
        messageToAdressee = GetParams("messageToAdressee")
        amount = GetParams("amount")
        var_ = GetParams("var_")
        name_session = GetParams("session")
        id_client = str(uuid.uuid4())
        
        indice1 = email.index('@')
        indice2 = email.index('.')
        dominio = email[indice1 + 1:indice2]
        id_client = dominio + "-" + id_client
        if name_session is None or "":
            name_session = "default"

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json', 'Authorization': f'Bearer {mod_radar_sessions[name_session]}'}

        json_data = {
            'tef': {
                'recipientData': {
                    'rut': rut,
                    'name': name,
                    'email': email,
                },
                'id': id_client,
                'messageToAddressee': messageToAdressee,
                'amount': amount,
                'bankData': {
                    'bankSBIFNumber': sbifNumber,
                    'bankAccount': accountNumber,
                },
            },
            'callbackUrl': 'https://webhook.site/callbackResponse',
        }
        response = requests.post(
            'https://api.somosradar.com/v1/payout/tef', headers=headers, json=json_data)
        print(id_client)
        SetVar(var_, response.json())
except Exception as e:
    print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
    PrintException()
    SetVar(var_, False)
    raise e
