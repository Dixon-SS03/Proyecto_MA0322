// static/js/triangulos.js
// Plano R^2 con etiquetas, zoom y conexión al endpoint /triangulos

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

const coordsList = document.getElementById("coordsList");
const scaleLabel = document.getElementById("scaleLabel");
const summary = document.getElementById("summary");
const measurements = document.getElementById("measurements");
const stepsPre = document.getElementById("steps");

const zoomPlus = document.getElementById("zoomPlus");
const zoomMinus = document.getElementById("zoomMinus");
const clearBtn = document.getElementById("clearBtn");
const resetViewBtn = document.getElementById("resetView");

// Tamaño y escala
let scale = 10;      // ±scale en ejes (mínimo 10)
const minScale = 10;

// Datos de puntos en coordenadas reales {x, y}
let puntos = [];     // A, B, C en orden de clic

scaleLabel.innerText = `Escala: ±${scale}`;

// ----------------------
// Utilities de conversión
// ----------------------
function pxPerUnit() {
  // suponemos canvas cuadrado (width == height)
  return canvas.width / (scale * 2);
}

function screenToMath(sx, sy) {
  const ppu = pxPerUnit();
  const mx = (sx - canvas.width / 2) / ppu;
  const my = (canvas.height / 2 - sy) / ppu;

  // 🔥 Convertimos a enteros exactos
  return { x: Math.round(mx), y: Math.round(my) };
}


function mathToScreen(mx, my) {
  const ppu = pxPerUnit();
  const sx = canvas.width / 2 + mx * ppu;
  const sy = canvas.height / 2 - my * ppu;
  return { x: sx, y: sy };
}

// ----------------------
// Dibujado de grid con números
// ----------------------
function drawGrid() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const ppu = pxPerUnit();

  // líneas ligeras
  ctx.lineWidth = 1;
  ctx.strokeStyle = "#e6e6e6";

  for (let i = -scale; i <= scale; i++) {
    const x = canvas.width / 2 + i * ppu;
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, canvas.height);
    ctx.stroke();
  }

  for (let j = -scale; j <= scale; j++) {
    const y = canvas.height / 2 - j * ppu;
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(canvas.width, y);
    ctx.stroke();
  }

  // ejes destacados
  ctx.strokeStyle = "#333";
  ctx.lineWidth = 1.4;
  // eje X
  ctx.beginPath();
  ctx.moveTo(0, canvas.height / 2);
  ctx.lineTo(canvas.width, canvas.height / 2);
  ctx.stroke();
  // eje Y
  ctx.beginPath();
  ctx.moveTo(canvas.width / 2, 0);
  ctx.lineTo(canvas.width / 2, canvas.height);
  ctx.stroke();

  // Etiquetas numéricas en ticks
  ctx.fillStyle = "#111";
  ctx.font = "12px Arial";
  ctx.textAlign = "center";
  ctx.textBaseline = "top";

  // Números en eje X (debajo del eje horizontal)
  for (let i = -scale; i <= scale; i++) {
    const x = canvas.width / 2 + i * ppu;
    const y = canvas.height / 2 + 4; // ligeramente debajo
    // No etiquetamos demasiado juntos (si ppu muy pequeño, saltamos)
    ctx.fillText(i.toString(), x, y);
  }

  // Números en eje Y (a la izquierda del eje vertical)
  ctx.textAlign = "right";
  ctx.textBaseline = "middle";
  for (let j = -scale; j <= scale; j++) {
    const x = canvas.width / 2 - 6;
    const y = canvas.height / 2 - j * ppu;
    ctx.fillText(j.toString(), x, y);
  }
}

// ----------------------
// Dibuja puntos, triángulo, etiquetas de lados y ángulos
// ----------------------
function drawAll(lastServerResult = null) {
  drawGrid();

  // Dibuja puntos
  ctx.fillStyle = "red";
  puntos.forEach((p, idx) => {
    const s = mathToScreen(p.x, p.y);
    ctx.beginPath();
    ctx.arc(s.x, s.y, 5, 0, Math.PI * 2);
    ctx.fill();

    // Etiqueta A, B, C
    ctx.fillStyle = "#000";
    ctx.font = "bold 13px Arial";
    ctx.textAlign = "left";
    ctx.textBaseline = "bottom";
    ctx.fillText(["A", "B", "C"][idx] || "?", s.x + 6, s.y - 6);
    ctx.fillStyle = "red";
  });

  // Si tenemos 3 puntos, dibujamos triángulo y etiquetas numéricas
  if (puntos.length === 3) {
    const A = puntos[0], B = puntos[1], C = puntos[2];
    const sA = mathToScreen(A.x, A.y);
    const sB = mathToScreen(B.x, B.y);
    const sC = mathToScreen(C.x, C.y);

    ctx.strokeStyle = "blue";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(sA.x, sA.y);
    ctx.lineTo(sB.x, sB.y);
    ctx.lineTo(sC.x, sC.y);
    ctx.closePath();
    ctx.stroke();

    // Si el servidor retornó medidas, las usamos para etiquetar
    if (lastServerResult && lastServerResult.lados && lastServerResult.angulos) {
      // Lados: a = BC, b = AC, c = AB  (según modelo)
      const lados = lastServerResult.lados; // objeto {a:..., b:..., c:...}
      const angulos = lastServerResult.angulos; // objeto {A:.., B:.., C:..}

      // Etiqueta side a (entre B y C) - colocar en punto medio
      const midBC = { x: (B.x + C.x) / 2, y: (B.y + C.y) / 2 };
      const sMidBC = mathToScreen(midBC.x, midBC.y);
      ctx.fillStyle = "#0a3";
      ctx.font = "13px Arial";
      ctx.textAlign = "center";
      ctx.textBaseline = "bottom";
      ctx.fillText(`a=${Number(lados.a).toFixed(3)}`, sMidBC.x, sMidBC.y - 4);

      // side b (entre A y C)
      const midAC = { x: (A.x + C.x) / 2, y: (A.y + C.y) / 2 };
      const sMidAC = mathToScreen(midAC.x, midAC.y);
      ctx.fillText(`b=${Number(lados.b).toFixed(3)}`, sMidAC.x, sMidAC.y - 4);

      // side c (entre A y B)
      const midAB = { x: (A.x + B.x) / 2, y: (A.y + B.y) / 2 };
      const sMidAB = mathToScreen(midAB.x, midAB.y);
      ctx.fillText(`c=${Number(lados.c).toFixed(3)}`, sMidAB.x, sMidAB.y - 4);

      // Ángulos en cada vértice (mostrar grados)
      ctx.fillStyle = "#b00";
      ctx.font = "12px Arial";
      ctx.textAlign = "left";
      ctx.textBaseline = "top";
      ctx.fillText(`${Number(angulos.A).toFixed(2)}°`, sA.x + 6, sA.y + 6);
      ctx.fillText(`${Number(angulos.B).toFixed(2)}°`, sB.x + 6, sB.y + 6);
      ctx.fillText(`${Number(angulos.C).toFixed(2)}°`, sC.x + 6, sC.y + 6);
    }
  }
}

// ----------------------
// Eventos canvas (clics)
// ----------------------
canvas.addEventListener("click", (ev) => {
  if (puntos.length >= 3) return;
  const rect = canvas.getBoundingClientRect();
  const sx = ev.clientX - rect.left;
  const sy = ev.clientY - rect.top;

  const p = screenToMath(sx, sy);
  puntos.push(p);
  updateCoordsList();
  drawAll();

  if (puntos.length === 3) {
    // Llamar al servidor
    enviarAlServidor();
  } else {
    // Actualizar estado
    summary.innerHTML = `<p><strong>Estado:</strong> ${puntos.length} punto(s) seleccionados. Falta(n) ${3 - puntos.length}.</p>`;
  }
});

// Mostrar coordenadas seleccionadas en listado
function updateCoordsList() {
  coordsList.innerHTML = puntos.map((p, i) => {
    return `<span>${["A","B","C"][i] || "?"}: (${p.x}, ${p.y})</span>`;
  }).join(" • ");
}

// ----------------------
// Zoom + / -
// ----------------------
zoomPlus.addEventListener("click", () => {
  scale += 1;
  scaleLabel.innerText = `Escala: ±${scale}`;
  drawAll();
});

zoomMinus.addEventListener("click", () => {
  if (scale > minScale) {
    scale -= 1;
    scaleLabel.innerText = `Escala: ±${scale}`;
    drawAll();
  } else {
    alert(`La escala mínima es ±${minScale}`);
  }
});

// ----------------------
// Limpiar / Reset
// ----------------------
clearBtn.addEventListener("click", () => {
  puntos = [];
  updateCoordsList();
  summary.innerHTML = `<p><strong>Estado:</strong> Esperando 3 clics...</p>`;
  measurements.innerHTML = "";
  stepsPre.textContent = "Aquí aparecerán los pasos detallados devueltos por el modelo.";
  drawAll();
});

resetViewBtn.addEventListener("click", () => {
  scale = minScale;
  scaleLabel.innerText = `Escala: ±${scale}`;
  drawAll();
});

// ----------------------
// Llamada POST al servidor con A,B,C
// ----------------------
function enviarAlServidor() {
  summary.innerHTML = `<p><strong>Estado:</strong> Enviando puntos al servidor...</p>`;

  // Construir payload con arrays [x,y] (compatible con tu service)
  const payload = {
    A: [puntos[0].x, puntos[0].y],
    B: [puntos[1].x, puntos[1].y],
    C: [puntos[2].x, puntos[2].y]
  };

  fetch("http://localhost:8000/triangulos", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
  .then(async (res) => {
    // Si el servidor devuelve HTML en vez de JSON, mostramos error
    const txt = await res.text();
    try {
      const data = JSON.parse(txt);
      return data;
    } catch (e) {
      throw new Error("Respuesta no es JSON. Respuesta del servidor:\n" + txt);
    }
  })
  .then((data) => {
    // data es el diccionario que devuelve resolver_triangulo
    // Esperamos claves: lados (obj), angulos (obj), clasificacion_lados, clasificacion_angulos, pasos (array), colineal (bool), mensaje opcional
    renderResultados(data);
    drawAll(data); // re-dibujar con etiquetas usando medidas
    
    // 🔥 GUARDAR EN HISTORIAL AQUÍ
    if (!data.colineal && data.lados) {
      // Calcular área y perímetro desde los lados
      const a = Number(data.lados.a || 0);
      const b = Number(data.lados.b || 0);
      const c = Number(data.lados.c || 0);
      const perimetro = a + b + c;
      
      // Área usando fórmula de Herón
      const s = perimetro / 2;
      const area = Math.sqrt(s * (s - a) * (s - b) * (s - c));
      
      saveToHistory({
        A: `(${puntos[0].x}, ${puntos[0].y})`,
        B: `(${puntos[1].x}, ${puntos[1].y})`,
        C: `(${puntos[2].x}, ${puntos[2].y})`
      }, {
        area: area,
        perimetro: perimetro,
        steps: data.pasos ? data.pasos.join('\n') : 'Sin pasos disponibles'
      });
    }
  })
  .catch((err) => {
    summary.innerHTML = `<p style="color:darkred"><strong>Error:</strong> ${err.message}</p>`;
    stepsPre.textContent = `Error al recibir respuesta del servidor:\n${err.stack || err.message}`;
  });
}

// ----------------------
// Renderizar resultados detallados y pasos
// ----------------------
function renderResultados(data) {
  if (!data) {
    summary.innerHTML = `<p style="color:darkred">Respuesta vacía del servidor.</p>`;
    return;
  }

  // Si el modelo devolvió 'mensaje' en colinealidad
  if (data.colineal || data.mensaje) {
    let msg = data.mensaje ? data.mensaje : (data.colineal ? "Los puntos son colineales." : "");
    summary.innerHTML = `<p><strong>Resultado:</strong> ${msg}</p>`;
  } else {
    summary.innerHTML = `<p><strong>Resultado:</strong> Triángulo válido.</p>`;
  }

  // Mostrar longitudes
  if (data.lados) {
    // data.lados puede venir como objeto con a,b,c
    const a = Number(data.lados.a || data.lados["a"] || 0);
    const b = Number(data.lados.b || data.lados["b"] || 0);
    const c = Number(data.lados.c || data.lados["c"] || 0);

    measurements.innerHTML = `
      <p><strong>Longitudes (a=BC, b=AC, c=AB):</strong></p>
      <ul>
        <li>a = ${a.toFixed(6)}</li>
        <li>b = ${b.toFixed(6)}</li>
        <li>c = ${c.toFixed(6)}</li>
      </ul>
    `;
  } else {
    measurements.innerHTML = ``;
  }

  // Ángulos y clasificaciones
  if (data.angulos) {
    const A = Number(data.angulos.A || 0);
    const B = Number(data.angulos.B || 0);
    const C = Number(data.angulos.C || 0);
    const clasL = data.clasificacion_lados ? (data.clasificacion_lados.tipo || data.clasificacion_lados) : (data.clasificacion_lados || "");
    const clasA = data.clasificacion_angulos ? (data.clasificacion_angulos.tipo || data.clasificacion_angulos) : (data.clasificacion_angulos || "");

    measurements.innerHTML += `
      <p><strong>Ángulos internos (°):</strong> A=${A.toFixed(4)}, B=${B.toFixed(4)}, C=${C.toFixed(4)}</p>
      <p><strong>Clasificación por lados:</strong> ${clasL}</p>
      <p><strong>Clasificación por ángulos:</strong> ${clasA}</p>
    `;
  }

    // Pasos - arreglo de strings
  if (Array.isArray(data.pasos)) {
    stepsPre.textContent = data.pasos.join("\n");
  } else {
    stepsPre.textContent = "El servidor no devolvió pasos detallados.";
  }
}

// ============== FUNCIONES DE HISTORIAL ==============

// Guardar triángulo en localStorage
function saveToHistory(vertices, resultado) {
    const historyKey = 'triangulos_history';
    let history = JSON.parse(localStorage.getItem(historyKey) || '[]');
    
    const newEntry = {
        id: Date.now(),
        fecha: new Date().toLocaleString('es-ES'),
        vertices: vertices,
        area: resultado.area,
        perimetro: resultado.perimetro,
        steps: resultado.steps
    };
    
    history.unshift(newEntry); // Agregar al inicio
    
    // Limitar a 10 triángulos
    if (history.length > 10) {
        history = history.slice(0, 10);
    }
    
    localStorage.setItem(historyKey, JSON.stringify(history));
    renderHistory();
}

// Renderizar historial
function renderHistory() {
    const historyList = document.getElementById('historyList');
    const historyKey = 'triangulos_history';
    const history = JSON.parse(localStorage.getItem(historyKey) || '[]');
    
    if (history.length === 0) {
        historyList.innerHTML = '<div class="history-empty">No hay triángulos guardados aún</div>';
        return;
    }
    
    historyList.innerHTML = history.map((item, index) => `
        <div class="history-item" data-index="${index}">
            <div class="history-item-content">
                <strong>A${item.vertices.A}, B${item.vertices.B}, C${item.vertices.C}</strong>
                <div class="history-item-date">${item.fecha} • Área: ${item.area.toFixed(2)}</div>
            </div>
            <button class="history-item-delete" data-id="${item.id}">✕</button>
        </div>
    `).join('');
    
    // Agregar eventos
    document.querySelectorAll('.history-item').forEach(item => {
        item.addEventListener('click', (e) => {
            if (!e.target.classList.contains('history-item-delete')) {
                const index = parseInt(item.dataset.index);
                loadFromHistory(index);
            }
        });
    });
    
    document.querySelectorAll('.history-item-delete').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const id = parseInt(btn.dataset.id);
            deleteFromHistory(id);
        });
    });
}

// Cargar triángulo desde historial
function loadFromHistory(index) {
    const historyKey = 'triangulos_history';
    const history = JSON.parse(localStorage.getItem(historyKey) || '[]');
    const item = history[index];
    
    if (!item) return;
    
    // Convertir coordenadas de string a objeto {x, y}
    const parseCoord = (str) => {
        const nums = str.replace(/[()]/g, '').split(',').map(Number);
        return { x: nums[0], y: nums[1] };
    };
    
    const A = parseCoord(item.vertices.A);
    const B = parseCoord(item.vertices.B);
    const C = parseCoord(item.vertices.C);
    
    // Actualizar puntos actuales
    puntos = [A, B, C];
    
    // Redibujar
    drawAll();
    
    // Actualizar coordenadas
    updateCoordsList();
    
    // Mostrar resultados guardados
    summary.innerHTML = `
        <p><strong>Triángulo cargado del historial</strong></p>
        <p>A = ${item.vertices.A}, B = ${item.vertices.B}, C = ${item.vertices.C}</p>
    `;
    
    measurements.innerHTML = `
        <h4>Medidas:</h4>
        <p><strong>Área:</strong> ${item.area.toFixed(4)} unidades²</p>
        <p><strong>Perímetro:</strong> ${item.perimetro.toFixed(4)} unidades</p>
    `;
    
    stepsPre.textContent = item.steps || 'Sin pasos guardados';
}

// Eliminar un triángulo del historial
function deleteFromHistory(id) {
    const historyKey = 'triangulos_history';
    let history = JSON.parse(localStorage.getItem(historyKey) || '[]');
    history = history.filter(item => item.id !== id);
    localStorage.setItem(historyKey, JSON.stringify(history));
    renderHistory();
}

// Limpiar todo el historial
document.getElementById('clearHistory').addEventListener('click', () => {
    if (confirm('¿Estás seguro de eliminar todo el historial?')) {
        localStorage.removeItem('triangulos_history');
        renderHistory();
    }
});

// Cargar historial al iniciar
document.addEventListener('DOMContentLoaded', () => {
    renderHistory();
});

// Inicializar dibujo
drawAll();
