from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json
from controllers.planos_controller import calcular_interseccion_planos
from utils.triangulos_service import resolver_triangulo
from utils.determinantes_service import resolverDeterminante

class Main(BaseHTTPRequestHandler):

    def do_GET(self):
        # Si el usuario entra al dominio principal:
        if self.path == "/":
            # Ruta del archivo por defecto
            self.path = "/static/views/index.html"
        
        # Rutas especiales para las páginas HTML (sin extensión)
        elif self.path == "/determinantes" or self.path == "/determinantes/":
            self.path = "/static/views/determinantes.html"
        elif self.path == "/triangulos" or self.path == "/triangulos/":
            self.path = "/static/views/triangulos.html"
        elif self.path == "/planos" or self.path == "/planos/":
            self.path = "/static/views/index.html"
        
        # Redirecciones para errores tipográficos comunes
        elif self.path == "/determiantes" or self.path == "/determiantes/":
            self.path = "/static/views/determinantes.html"

        try:
            file_path = "." + self.path  # añade el "." para ruta local
            
            # Si no tiene extensión y es una ruta de views, intentar agregar .html
            if not os.path.splitext(file_path)[1] and "/static/views/" in file_path:
                file_path += ".html"

            with open(file_path, "rb") as file:
                content = file.read()

                # Detectar MIME
                mime = self.detectar_mime(file_path)

                self.send_response(200)
                self.send_header("Content-Type", mime)
                self.end_headers()
                self.wfile.write(content)

        except FileNotFoundError:
            self.send_error(404, "Archivo no encontrado")

    def do_POST(self):
        # Manejo de la ruta API para intersección de planos
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
            except (ValueError, TypeError):
                content_len = 0
            
            body_bytes = self.rfile.read(content_len) if content_len > 0 else b"{}"
            body_str = body_bytes.decode("utf-8") if body_bytes else "{}"

            try:
                datos = json.loads(body_str)
            except json.JSONDecodeError as e:
                print("Error parseando JSON:", e)
                self.send_error(400, "JSON inválido")
                return

            # Resolver el triángulo
            resultado = resolver_triangulo(datos)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(resultado, ensure_ascii=False).encode("utf-8"))
        
        # ------------------- DETERMINANTES ----------------------
        elif self.path == "/determinantes":
            try:
                content_len = int(self.headers.get('Content-Length', 0))
            except (ValueError, TypeError):
                content_len = 0
            
            body_bytes = self.rfile.read(content_len) if content_len > 0 else b"{}"
            body_str = body_bytes.decode("utf-8") if body_bytes else "{}"

            try:
                datos = json.loads(body_str)
            except json.JSONDecodeError as e:
                print("Error parseando JSON determinantes:", e)
                self.send_error(400, "JSON inválido")
                return

            # Resolver el determinante
            resultado, pasos, error = resolverDeterminante(datos)
            respuesta = {
                "resultado": resultado,
                "pasos": pasos,
                "error": error
            }
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(respuesta, ensure_ascii=False).encode("utf-8"))
        
        else:
            self.send_error(404, "Endpoint no encontrado")

    def do_OPTIONS(self):
        # Manejo de preflight requests para CORS
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    
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
        if file_path.endswith(".svg"):
            return "image/svg+xml"
        if file_path.endswith(".json"):
            return "application/json"
        return "application/octet-stream"

# Servidor iniciado
# Para correr el servidor: python service.py
if __name__ == "__main__":
    print("Servidor corriendo en http://localhost:8000")
    print("Endpoints disponibles:")
    print("  - GET  /                          -> Página principal")
    print("  - POST /api/calcular-interseccion -> Intersección de planos")
    print("  - POST /triangulos                -> Análisis de triángulos")
    print("  - POST /determinantes             -> Cálculo de determinantes")
    print("\nPresiona Ctrl+C para detener el servidor")
    try:
        HTTPServer(("localhost", 8000), Main).serve_forever()
    except KeyboardInterrupt:
        print("\n\nServidor detenido.")
