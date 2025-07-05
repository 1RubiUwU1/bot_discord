from flask import Flask, request
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app) 

WEBHOOK_URL = os.getenv("LINK")
CLAVE_SECRETA = "baSLsVSrMMfxlfAdleg6Lqey9N5G"


PING_ID = {
    "DEAD_RIELS": {
        "ID": "1390085681803427971",
        "SCRIPT": "AUTO BONOS"
    },
}

# https://botdiscord-api.up.railway.app/enviar?clave=CLAVE_SECRETA&placeNb=VALOR&Name_user=VALOR&script=VALOR&Informacion=VALOR

def mensaje(placeNb, Name_user, Informacion):

#? ╭───────────────────────────╮
#? │        🛠 HOOKS 🛠        │
#? ╰───────────────────────────╯
    GENERAL = PING_ID[placeNb]
    ID = GENERAL["ID"]
    ST = GENERAL["SCRIPT"]
#> ╭───────────────────────────╮
#> │      🛠 MENSAJE 🛠        │
#> ╰───────────────────────────╯
    EMBEB = {
        "content": f"# Holiiiii...! <@{Name_user}>",
        "allowed_mentions": {"users": [Name_user]},
        "embeds": [
            {
            "title": "Holiiiii...!",
            "description": f"""```ansi
[2;35m[1;35m[1;35m[1;35mVengo a avisarte por parte del script(\"{ST}\") para decirte que:[0m[1;35m[0m[1;35m[0m[2;35m[0m
``````ansi
[2;35m[1;35m[1;35m[1;35m[0m[1;35m[0m[1;35m[0m[2;35m[0m[2;34m[1;34m[1;40m----------->

{Informacion}

----------->[0m[1;34m[0m[2;34m[0m
``````ansi
[2;35m[1;35m¡Bueno, eso era todo, bye! No olvides de recomendarnos con tus amigos shiii~[0m[2;35m[0m

```""",
            "color": 16121600,
            "image": {
                "url": "https://firebasestorage.googleapis.com/v0/b/fotos-b8a54.appspot.com/o/9f0db6ff6c059e1d14b1f37b69f55c21%201.png?alt=media&token=76744d86-5e4a-4676-8461-ea5095916b4e"
            }
            }
        ],
    }

    try:
        resp = requests.post(WEBHOOK_URL, json=EMBEB, params={"thread_id": ID})

        if resp.status_code in (200, 204):
            return "✅ Mensaje enviado al hilo de Discord", 200
        else:
            return f"❌ Error al enviar mensaje: {resp.status_code}\n{resp.text}", 500
    except Exception as e:
        return f"❌ Error en el servidor: {str(e)}", 500    
    



@app.route("/enviar", methods=["GET"])
def enviar():
    clave = request.args.get("Nkart", "")
    _placeNb_ = request.args.get("IPFUEOPjd", "")
    _Name_user_ = request.args.get("davvgfrF", "")
    _Informacion_ = request.args.get("OIHDoihio", "")

    if clave != CLAVE_SECRETA:
        return "❌ Clave incorrecta. No autorizado.", 403


    if _placeNb_ not in PING_ID:
        return f"❌ Lugar '{_placeNb_}' no registrado.", 400

    return mensaje(_placeNb_, _Name_user_, _Informacion_)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
