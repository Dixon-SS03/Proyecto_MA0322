from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json

# Importamos el servicio que llamará al modelo matemático
from utils.determinantes_service import resolver_determinante


class Main(BaseHTTPRequestHandler):

    # -------------------------------------------------------
    #                     PETICIONES GET
    # -------------------------------------------------------
    def do_GET(self):
        # Ruta principal -> index.html
        if self.path == "/":
            self.path = "/static/views/index.html"

        try:
            file_path = "." + self.path  # ruta relativa

            with open(file_path, "rb") as file:
                content = file.read()

                # Detectar MIME
                if file_path.endswith(".html"):
                    mime = "text/html"
                elif file_path.endswith(".css"):
                    mime = "text/css"
                elif file_path.endswith(".js"):
                    mime = "application/javascript"
                elif file_path.endswith(".png") or file_path.endswith(".jpg"):
                    mime = "image/png"
                else:
                    mime = "application/octet-stream"

                self.send_response(200)
                self.send_header("Content-Type", mime)
                self.end_headers()
                self.wfile.write(content)

        except FileNotFoundError:
            self.send_error(404, "Archivo no encontrado")


    # -------------------------------------------------------
    def do_POST(self):

        # ----------- RUTA PARA DETERMINANTES ----------------
        if self.path == "/determinantes":

            content_length = int(self.headers['Content-Length'])
            datos_bytes = self.rfile.read(content_length)
            datos_str = datos_bytes.decode("utf-8")

            try:
                datos = json.loads(datos_str)
            except:
                self.send_error(400, "JSON inválido")
                return

            resultado, pasos, error = resolver_determinante(datos)

            respuesta = {
                "resultado": resultado,
                "pasos": pasos,
                "error": error
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps(respuesta).encode("utf-8"))
            return
        # -----------------------------------------------------

        # Si llega aquí, la ruta no existe
        self.send_error(404, "Ruta POST no encontrada")



# -------------------------------------------------------
# priebnas
if __name__ == "__main__":
    from models.determinantes_model import validar_matriz

    print("\n--- PRUEBA VALIDAR MATRIZ ---")

    matriz_prueba = [
        ["5", "1.2", "-3"],
        ["0", "4", "7"],
        ["8", "9.5", "10"]
    ]

    ok, err = validar_matriz(matriz_prueba)

    print("Resultado de validación:", ok)
    print("Mensaje de error:", err)



    print("\n--- PRUEBA SARRUS (3x3) ---")

    from models.determinantes_model import determinante_3x3_sarrus

    matriz_sarrus = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]

    det, pasos = determinante_3x3_sarrus(matriz_sarrus)

    print("Determinante:", det)
    print("\nPasos:")
    for p in pasos:
        print("-", p)
    

    
    print("\n--- PRUEBA COFACTORES (3x3) ---")

    from models.determinantes_model import determinante_3x3_cofactores

    matriz_cof = [
        [1, 2, 3],
        [0, 1, 4],
        [5, 6, 0]
    ]

    det2, pasos2 = determinante_3x3_cofactores(matriz_cof)

    print("Determinante:", det2)
    print("\nPasos:")
    for p in pasos2:
        print("-", p)

    print("\n--- PRUEBA DETERMINANTE 4x4 ---")



    from models.determinantes_model import determinante_4x4

    matriz_4x4 = [
        [1, 2, 3, 4],
        [0, 1, 4, 5],
        [2, 3, 1, 0],
        [1, 0, 2, 1]
    ]

    # "fila" o "columna"
    modo = "fila"      
    indice = 1          

    # 3x3: "sarrus" o "cofactores"
    metodo_3x3 = "cofactores"

    det4, pasos4 = determinante_4x4(matriz_4x4, metodo_3x3, modo, indice)

    print("Determinante 4x4:", det4)
    print("\nPasos:")
    for p in pasos4:
        print("-", p)


    print("\nServidor corriendo en http://localhost:8000")
    HTTPServer(("localhost", 8000), Main).serve_forever()