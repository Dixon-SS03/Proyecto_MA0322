
async function calcularInterseccion() {
    ocultarElemento('resultados');
    ocultarElemento('error');

    const ecuacion1 = document.getElementById('ecuacion1').value.trim();
    const ecuacion2 = document.getElementById('ecuacion2').value.trim();

    if (!ecuacion1 || !ecuacion2) {
        mostrarError('Por favor, ingresa ambas ecuaciones de los planos.');
        return;
    }

    let plano1, plano2;
    
    try {
        plano1 = parsearEcuacion(ecuacion1);
    } catch (error) {
        mostrarError(`Error en la ecuación del Plano 1: ${error.message}`);
        return;
    }

    try {
        plano2 = parsearEcuacion(ecuacion2);
    } catch (error) {
        mostrarError(`Error en la ecuación del Plano 2: ${error.message}`);
        return;
    }

    if (!validarEntrada(plano1, plano2)) {
        return;
    }

    mostrarCargando();

    try {
        const response = await fetch('/api/calcular-interseccion', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                plano1: plano1,
                plano2: plano2
            })
        });

        const resultado = await response.json();

        if (resultado.exito) {
            mostrarResultados(resultado);
        } else {
            mostrarError(resultado.error || 'Error desconocido', resultado.detalles);
        }

    } catch (error) {
        mostrarError('Error de conexión con el servidor: ' + error.message);
    }
}

function parsearEcuacion(ecuacionStr) {
    let ecuacion = ecuacionStr.replace(/\s+/g, '');
    
    if (!ecuacion.includes('=')) {
        throw new Error('La ecuación debe contener el símbolo "="');
    }
    
    const partes = ecuacion.split('=');
    if (partes.length !== 2) {
        throw new Error('La ecuación debe tener exactamente un signo "="');
    }
    
    const izquierda = partes[0];
    const derecha = partes[1];
    
    const coeficientes = { a: 0, b: 0, c: 0, d: 0 };
    
    function parsearLado(texto, multiplicador) {
        const patronVar = /([+-]?)(\d*\.?\d*)([xyz])/gi;
        let match;
        
        patronVar.lastIndex = 0;
        
        while ((match = patronVar.exec(texto)) !== null) {
            const signo = match[1] === '-' ? -1 : 1;
            let coef = match[2];
            const variable = match[3].toLowerCase();
            
            if (coef === '' || coef === '.') {
                coef = 1;
            } else {
                coef = parseFloat(coef);
            }
            
            if (variable === 'x') {
                coeficientes.a += signo * coef * multiplicador;
            } else if (variable === 'y') {
                coeficientes.b += signo * coef * multiplicador;
            } else if (variable === 'z') {
                coeficientes.c += signo * coef * multiplicador;
            }
        }
        
        let textoSinVars = texto.replace(/[+-]?\d*\.?\d*[xyz]/gi, '');
        
        if (textoSinVars) {
            if (textoSinVars[0] !== '+' && textoSinVars[0] !== '-') {
                textoSinVars = '+' + textoSinVars;
            }
            
            const patronNum = /([+-]\d+\.?\d*)/g;
            let matchNum;
            
            while ((matchNum = patronNum.exec(textoSinVars)) !== null) {
                const num = parseFloat(matchNum[1]);
                coeficientes.d += num * multiplicador;
            }
        }
    }
    
    parsearLado(izquierda, 1);
    
    parsearLado(derecha, -1);
    
    if (coeficientes.a === 0 && coeficientes.b === 0 && coeficientes.c === 0) {
        throw new Error('La ecuación debe contener al menos una variable (x, y, o z) con coeficiente no nulo');
    }
    
    coeficientes.d = -coeficientes.d;
    
    return coeficientes;
}


function validarEntrada(plano1, plano2) {
    const valores1 = [plano1.a, plano1.b, plano1.c, plano1.d];
    const valores2 = [plano2.a, plano2.b, plano2.c, plano2.d];

    for (let val of [...valores1, ...valores2]) {
        if (isNaN(val)) {
            mostrarError('Por favor, ingresa valores numéricos válidos en todos los campos.');
            return false;
        }
    }

    if (plano1.a === 0 && plano1.b === 0 && plano1.c === 0) {
        mostrarError('El Plano 1 no es válido: los coeficientes a, b y c no pueden ser todos cero.');
        return false;
    }

    if (plano2.a === 0 && plano2.b === 0 && plano2.c === 0) {
        mostrarError('El Plano 2 no es válido: los coeficientes a, b y c no pueden ser todos cero.');
        return false;
    }

    return true;
}


function mostrarResultados(resultado) {
    const contenedor = document.getElementById('contenidoResultados');
    let html = '';

    html += '<div class="info-planos">';
    html += `<div class="info-plano">
        <h4>${resultado.plano1.nombre}</h4>
        <p><strong>Ecuación:</strong> ${resultado.plano1.ecuacion}</p>
    </div>`;
    html += `<div class="info-plano">
        <h4>${resultado.plano2.nombre}</h4>
        <p><strong>Ecuación:</strong> ${resultado.plano2.ecuacion}</p>
    </div>`;
    html += '</div>';

    const tipoClase = resultado.tipo_interseccion;
    html += `<div class="tipo-interseccion ${tipoClase}">
        <h3>${resultado.descripcion}</h3>
        <p>${resultado.mensaje}</p>
    </div>`;

    if (resultado.justificacion) {
        html += `<div class="justificacion">
            <h4>📝 Justificación:</h4>
            <p>${resultado.justificacion}</p>
        </div>`;
    }

    if (resultado.tipo_interseccion === 'recta' && resultado.gauss_jordan) {
        html += generarPasosGaussJordan(resultado.gauss_jordan);
        
        if (resultado.ecuacion_parametrica) {
            html += generarEcuacionParametrica(resultado.ecuacion_parametrica);
        }
    }

    contenedor.innerHTML = html;
    mostrarElemento('resultados');
}


function generarPasosGaussJordan(gaussJordan) {
    let html = '<div class="pasos-gauss">';
    html += '<h3>Método de Gauss-Jordan</h3>';
    html += '<p><strong>Matriz aumentada del sistema:</strong></p>';

    for (let paso of gaussJordan.pasos) {
        html += '<div class="paso">';
        html += `<div class="paso-descripcion">${paso.descripcion}</div>`;
        html += generarMatriz(paso.matriz);
        html += '</div>';
    }

    html += '</div>';
    return html;
}


function generarMatriz(matriz) {
    let html = '<div class="matriz">';
    
    for (let fila of matriz) {
        html += '<div class="matriz-fila">';
        for (let elemento of fila) {
            const valorFormateado = formatearNumero(elemento);
            html += `<span class="matriz-elemento">${valorFormateado}</span>`;
        }
        html += '</div>';
    }
    
    html += '</div>';
    return html;
}


function generarEcuacionParametrica(ecuacion) {
    let html = '<div class="ecuacion-parametrica">';
    html += '<h4>Ecuación Paramétrica de la Recta de Intersección:</h4>';
    html += `<p><strong>x</strong> = ${ecuacion.x}</p>`;
    html += `<p><strong>y</strong> = ${ecuacion.y}</p>`;
    html += `<p><strong>z</strong> = ${ecuacion.z}</p>`;
    html += '<br>';
    html += `<p><strong>Punto en la recta:</strong> (${formatearNumero(ecuacion.punto[0])}, ${formatearNumero(ecuacion.punto[1])}, ${formatearNumero(ecuacion.punto[2])})</p>`;
    html += `<p><strong>Vector dirección:</strong> (${formatearNumero(ecuacion.vector_direccion[0])}, ${formatearNumero(ecuacion.vector_direccion[1])}, ${formatearNumero(ecuacion.vector_direccion[2])})</p>`;
    html += '</div>';
    return html;
}


function formatearNumero(num) {
    if (typeof num === 'string') {
        return num;
    }
    
    if (typeof num === 'number') {
        if (Math.abs(num) < 0.0001 && num !== 0) {
            return num.toExponential(4);
        }
        
        const redondeado = Math.round(num * 10000) / 10000;
        
        if (Math.abs(redondeado) < 0.0001) {
            return '0';
        }
        
        if (Number.isInteger(redondeado)) {
            return redondeado.toString();
        }
        
        return redondeado.toString();
    }
    
    return String(num);
}


function mostrarError(mensaje, detalles = null) {
    const errorDiv = document.getElementById('error');
    const mensajeP = document.getElementById('mensajeError');
    
    let textoError = mensaje;
    
    if (detalles) {
        textoError += '<br><br><strong>Detalles:</strong><br>';
        if (typeof detalles === 'object') {
            textoError += '<ul>';
            for (let key in detalles) {
                textoError += `<li><strong>${key}:</strong> ${detalles[key].join(', ')}</li>`;
            }
            textoError += '</ul>';
        } else {
            textoError += detalles;
        }
    }
    
    mensajeP.innerHTML = textoError;
    mostrarElemento('error');
}


function mostrarCargando() {
    const contenedor = document.getElementById('contenidoResultados');
    contenedor.innerHTML = '<div class="cargando">Calculando...</div>';
    mostrarElemento('resultados');
}


function mostrarElemento(id) {
    document.getElementById(id).classList.remove('oculto');
}

function ocultarElemento(id) {
    document.getElementById(id).classList.add('oculto');
}


function cargarEjemplo(tipo) {
    switch(tipo) {
        case 'interseccion':
            document.getElementById('ecuacion1').value = 'x + 2y + 3z = 6';
            document.getElementById('ecuacion2').value = '2x + y - z = 4';
            break;
            
        case 'paralelos':
            document.getElementById('ecuacion1').value = '3z + 2y + x = 6';
            document.getElementById('ecuacion2').value = '6z + 4y + 2x = 18';
            break;
            
        case 'coincidentes':
            document.getElementById('ecuacion1').value = '2y + 3z + x = 6';
            document.getElementById('ecuacion2').value = '4y + 6z + 2x = 12';
            break;
            
        case 'ordenAleatorio':
            document.getElementById('ecuacion1').value = '-3y + 2z = 10 + 3 - x';
            document.getElementById('ecuacion2').value = '5 = 2x + y - z';
            break;
    }
    
    mostrarMensajeInfo(tipo);
}


function mostrarMensajeInfo(tipo) {
    const mensajes = {
        'interseccion': 'Planos que se intersecan en una recta',
        'paralelos': 'Planos paralelos ',
        'coincidentes': 'Planos coincidentes',
        'ordenAleatorio': 'Variables en ambos lados'
    };
    
    let mensajeDiv = document.getElementById('mensajeEjemplo');
    if (!mensajeDiv) {
        mensajeDiv = document.createElement('div');
        mensajeDiv.id = 'mensajeEjemplo';
        mensajeDiv.style.cssText = `
            background: #e7f3ff;
            border-left: 4px solid #2196F3;
            padding: 12px 20px;
            margin: 15px 0;
            border-radius: 4px;
            color: #1565C0;
            font-weight: 500;
            text-align: center;
        `;
        const formulario = document.getElementById('formularioPlanos');
        formulario.parentNode.insertBefore(mensajeDiv, formulario.nextSibling);
    }
    
    mensajeDiv.textContent = mensajes[tipo] || 'Ejemplo cargado';
    mensajeDiv.style.display = 'block';
    
    setTimeout(() => {
        if (mensajeDiv) {
            mensajeDiv.style.opacity = '0';
            mensajeDiv.style.transition = 'opacity 0.5s';
            setTimeout(() => {
                mensajeDiv.style.display = 'none';
                mensajeDiv.style.opacity = '1';
            }, 500);
        }
    }, 3000);
}
