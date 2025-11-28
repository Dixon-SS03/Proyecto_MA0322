from http.server import BaseHTTPRequestHandler, HTTPServer
import os

class Main(BaseHTTPRequestHandler):

    def do_GET(self):
        # Si el usuario entra al dominio principal:
        if self.path == "/":
            # Ruta del archivo por defecto
            self.path = "/static/views/index.html"

        try:
            file_path = "." + self.path  # añade el "." para ruta local

            with open(file_path, "rb") as file:
                content = file.read()

                # Detectar MIME
                if file_path.endswith(".html"):
                    mime = "text/html"
                elif file_path.endswith(".css"):
                    mime = "text/css"
                elif file_path.endswith(".js"):
                    mime = "application/javascript"
                else:
                    mime = "application/octet-stream"

                self.send_response(200)
                self.send_header("Content-Type", mime)
                self.end_headers()
                self.wfile.write(content)

        except FileNotFoundError:
            self.send_error(404, "Archivo no encontrado")

# Servidor iniciado
#Para correr el servidor, python service.py
print("Servidor corriendo en http://localhost:8000")
HTTPServer(("localhost", 8000), Main).serve_forever()
