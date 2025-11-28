from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json

from utils.determinantes_service import resolverDeterminante


class Main(BaseHTTPRequestHandler):

    
    def do_GET(self):

        # Si es la raíz, mandar index
        if self.path == "/":
            self.path = "/static/views/index.html"

        file_path = "." + self.path  # ruta relativa al proyecto

        try:
            with open(file_path, "rb") as file:
                content = file.read()

            # Detectar tipo MIME
            mime = self.detectar_mime(file_path)

            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.end_headers()
            self.wfile.write(content)

        except FileNotFoundError:
            self.send_error(404, "Archivo no encontrado")

    
    def do_POST(self):

        if self.path == "/determinantes":

            try:
                content_length = int(self.headers["Content-Length"])
                datos_bytes = self.rfile.read(content_length)
                datos_str = datos_bytes.decode("utf-8")

                datos = json.loads(datos_str)

            except Exception:
                self.send_error(400, "JSON inválido o corrupto")
                return

            # Resolver el determinante llamando a calculateDeterminante.py
            resultado, pasos, error = resolverDeterminante(datos)

            respuesta = {
                "resultado": resultado,
                "pasos": pasos,
                "error": error
            }

            # Enviar JSON al frontend
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps(respuesta).encode("utf-8"))
            return

        # Ruta no válida
        self.send_error(404, "Ruta POST no encontrada")

    
    def detectar_mime(self, file_path):
        """Determina el tipo MIME según la extensión del archivo."""

        if file_path.endswith(".html"):
            return "text/html"
        if file_path.endswith(".css"):
            return "text/css"
        if file_path.endswith(".js"):
            return "application/javascript"
        if file_path.endswith(".png"):
            return "image/png"
        if file_path.endswith(".jpg") or file_path.endswith(".jpeg"):
            return "image/jpeg"

        return "application/octet-stream"



if __name__ == "__main__":
    print("\nServidor corriendo en http://localhost:8000")
    servidor = HTTPServer(("localhost", 8000), Main)
    servidor.serve_forever()
