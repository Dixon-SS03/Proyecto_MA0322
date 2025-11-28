from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json
from controllers.planos_controller import calcular_interseccion_planos
from utils.triangulos_service import resolver_triangulo

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

    def do_POST(self):
        # Manejo de la ruta API
        if self.path == "/api/calcular-interseccion":
            try:
                # Leer el contenido del POST
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                # Parsear JSON
                data = json.loads(post_data.decode('utf-8'))
                
                # Procesar la solicitud
                resultado = calcular_interseccion_planos(data)
                
                # Enviar respuesta JSON
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                
                response = json.dumps(resultado, ensure_ascii=False)
                self.wfile.write(response.encode('utf-8'))
                
            except json.JSONDecodeError:
                self.send_error(400, "JSON inválido")
            except Exception as e:
                # Error interno
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                
                error_response = json.dumps({
                    'exito': False,
                    'error': f'Error del servidor: {str(e)}'
                }, ensure_ascii=False)
                self.wfile.write(error_response.encode('utf-8'))
        
        # ------------------- TRIÁNGULOS ----------------------
        elif self.path == "/triangulos":
            try:
                content_len = int(self.headers.get('Content-Length', 0))
            except:
                content_len = 0
            body_bytes = self.rfile.read(content_len) if content_len > 0 else b"{}"
            body_str = body_bytes.decode("utf-8") if body_bytes else "{}"

            try:
                datos = json.loads(body_str)
            except Exception as e:
                print("Error parseando JSON:", e)
                self.send_error(400, "JSON inválido")
                return

            # Necesitas importar esta función o implementarla
            # from controllers.triangulos_controller import resolver_triangulo
            resultado = resolver_triangulo(datos)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(resultado).encode("utf-8"))
        else:
            self.send_error(404, "Endpoint no encontrado")

    def do_OPTIONS(self):
        # Manejo de preflight requests para CORS
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

# Servidor iniciado
#Para correr el servidor, python service.py
print("Servidor corriendo en http://localhost:8000")
HTTPServer(("localhost", 8000), Main).serve_forever()