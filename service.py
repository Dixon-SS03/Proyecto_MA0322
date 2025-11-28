from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from fractions import Fraction


from controllers.planos_controller import calcular_interseccion_planos


class FractionEncoder(json.JSONEncoder):
    """Encoder personalizado para serializar Fractions como strings"""
    def default(self, obj):
        if isinstance(obj, Fraction):
            if obj.denominator == 1:
                return str(obj.numerator)
            else:
                return f"{obj.numerator}/{obj.denominator}"
        return super().default(obj)


class Main(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.path = "/static/views/index.html"
        
        if self.path == "/api/calcular-interseccion":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            response = json.dumps({
                'exito': False,
                'error': 'Este endpoint requiere método POST',
                'mensaje': 'Para calcular la intersección de planos, envía una petición POST con los datos de los planos en formato JSON.'
            }, ensure_ascii=False)
            self.wfile.write(response.encode('utf-8'))
            return

        try:
            file_path = "." + self.path 

            with open(file_path, "rb") as file:
                content = file.read()

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
        """Maneja peticiones POST para la API"""
        
        if self.path == "/api/calcular-interseccion":
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                data = json.loads(post_data.decode('utf-8'))
                
                resultado = calcular_interseccion_planos(data)
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                
                response = json.dumps(resultado, ensure_ascii=False, cls=FractionEncoder)
                self.wfile.write(response.encode('utf-8'))
                
            except json.JSONDecodeError:
                self.send_error(400, "JSON inválido")
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                error_response = json.dumps({
                    'exito': False,
                    'error': f'Error del servidor: {str(e)}'
                }, ensure_ascii=False)
                self.wfile.write(error_response.encode('utf-8'))
        else:
            self.send_error(404, "Endpoint no encontrado")
    
    def do_OPTIONS(self):
        """Maneja peticiones OPTIONS para CORS"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

print("Servidor corriendo en http://localhost:8000")
print("API disponible en http://localhost:8000/api/calcular-interseccion")
HTTPServer(("localhost", 8000), Main).serve_forever()
