from flask import Flask, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app) 

WEBHOOK_URL = "https://discord.com/api/webhooks/1389844080741060678/uaV4LqiNV6cTZrHl_LsN87M76_C6Ml2vU0J9trt0WD_o_GpMnKVXUIjmD8pJVNgnIkja"
CLAVE_SECRETA = "baSLsVSrMMfxlfAdleg6Lqey9N5G"


PING_ID = {
    "AUTO_BONOS": {
        "ID": "1390085681803427971"
    },

}


def mensaje(placeNb, Name_user, script, Informacion):

#? ╭───────────────────────────╮
#? │        🛠 HOOKS 🛠        │
#? ╰───────────────────────────╯
    GENERAL = PING_ID[placeNb]
    ID = GENERAL["ID"]
#? ╭───────────────────────────╮
#? │      🛠 MENSAJE 🛠        │
#? ╰───────────────────────────╯
    EMBEB = {
        "content": f"<@{Name_user}>",
        "embeds": [
            {
            "description": f"""```ansi
[2;35m[1;35mHoliiiii...!

Vengo a avisarte por parte del script(\"{script}\") para decirte que:[0m[2;35m[0m
```
```ansi
[2;34------>
{Informacion}
------>[0m
```

```ansi
[2;35m[2;35m[1;35m¡Bueno, todo eso te tenía comunicar así que bye! A y no te olvidas de recordarnos con tus amigos shiiii~[0m[2;35m[0m[2;35m[0m
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
    clave = request.args.get("clave", "")
    _placeNb_ = request.args.get("placeNb", "")
    _Name_user_ = request.args.get("Name_user", "")
    _script_ = request.args.get("script", "")
    _Informacion_ = request.args.get("Informacion", "")
    
    if clave != CLAVE_SECRETA:
        return "❌ Clave incorrecta. No autorizado.", 403

    if not all([_placeNb_, _Name_user_, _script_, _Informacion_]):
        return "⚠️ Faltan parámetros obligatorios.", 400

    return mensaje(_placeNb_, _Name_user_, _script_, _Informacion_)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
