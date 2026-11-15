# UT2-A2 - Realidad Aumentada para la identificación de componentes de hardware

## 1. Resultado de aprendizaje, contenido y criterios de evaluación

### Resultado de aprendizaje

RA2. Caracteriza las tecnologías habilitadoras digitales necesarias para la adecuación/transformación de las empresas a entornos digitales describiendo sus características y aplicaciones. 

### Contenido

1.- Tecnologías Habilitadoras Digitales (THD)
2.- Las THD en el desarrollo de productos y servicios.

### Criterios de evaluación

a) Se han identificado las principales tecnologías habilitadoras digitales.
b) Se han relacionado las THD con el desarrollo de productos y servicios.
g) Se ha elaborado un informe que relacione, las tecnologías con sus características y áreas de aplicación.


## 2. Agrupamiento

Parejas (grupos de 2 personas). 
La fase de escaneo por fotogrametría requiere que una persona sujete el objeto o gire alrededor de él mientras la otra maneja el dispositivo de captura; el resto de fases (edición, programación, publicación) se recomienda realizarlas conjuntamente para que ambos miembros comprendan el proceso completo.

## 3. Contexto

Esta actividad forma parte del proyecto **Realidad Aumentada de Motherboards**, cuyo objetivo final es construir una herramienta que permita a cualquier persona, apuntando la cámara del móvil a una placa base real, identificar sus componentes (CPU, RAM, chipset, conectores...) mediante etiquetas en Realidad Aumentada.

## 4. Objetivo de la actividad

Al finalizar la actividad, cada pareja debe tener **publicada en internet** una página web que muestre su objeto escaneado en 3D, con varios puntos etiquetados, y que pueda visualizarse en Realidad Aumentada desde un móvil Android compatible.

## 5. Enunciado de la actividad

### Paso 1 — Escanear el objeto

Con una app de escaneo 3D por fotogrametría (por ejemplo, [**Kiri Engine**](https://www.kiriengine.app/)), disponible para Android e iOS), capturad fotos del objeto elegido desde todos los ángulos posibles, siguiendo las indicaciones de la propia app. Al terminar el procesado, exportad el resultado en formato **OBJ**.

Nombra el fichero como: *modelo-\<NOMBRE DE LA PLACA\>.obj*

Este formato genera siempre **tres ficheros que deben mantenerse juntos**, en la misma carpeta y con los nombres exactos que se referencian entre ellos:

- `modelo-<NOMBRE DE LA PLACA>.obj` — la geometría (vértices, caras y coordenadas de textura)
- `modelo-<NOMBRE DE LA PLACA>.mtl` — el material, que referencia la textura por su nombre de fichero (`map_Kd modelo.jpg`)
- `modelo-<NOMBRE DE LA PLACA>.jpg` — la textura (el color del objeto, ya "horneado" sobre la malla)

> ⚠️ Linux distingue mayúsculas de minúsculas en los nombres de fichero. Si el `.mtl` dice `map_Kd modelo.jpg` y el fichero real se llama `Modelo.JPG`, no se enlazará.

### Paso 2 — Limpiar el modelo en Blender

1. **File > Import > Wavefront (.obj)**. Si los tres ficheros están en la misma carpeta, Blender enlaza la textura automáticamente.
2. Eliminad el cubo que Blender añade por defecto en toda escena nueva (seleccionadlo y pulsad `X` → *Delete*).
3. **Object > Set Origin > Origin to Geometry** — centra el punto de pivote del objeto en su propia geometría (si no queda centrado a la vista, repetid la operación y cambiad *Median Point* por *Bounds Center* en el panel inferior izquierdo, `F9`).
4. **`Alt + G`** — mueve el objeto al centro de la escena, ahora que su origen coincide con su centro visual.
5. **`Ctrl + A` > *All Transforms*** — aplica cualquier rotación o escala pendiente, para que no cause sorpresas al exportar.

### Paso 3 — Exportar a glTF Binario (.glb)

**File > Export > glTF 2.0**, formato **"glTF Binary (.glb)"**, con materiales y texturas incluidos. El resultado es un único fichero que contiene geometría y textura juntas.

### Paso 4 — Optimizar el modelo para móvil

Un escaneo por fotogrametría trae muchísimo más detalle del necesario para verlo fluido en un móvil. Se optimiza con la herramienta de línea de comandos **gltf-transform** (necesita Node.js instalado):

```bash
npx @gltf-transform/cli optimize modelo-<NOMBRE DE LA PLACA>.glb modelomodelo-<NOMBRE DE LA PLACA>_optimizado.glb \
  --compress quantize \
  --simplify-ratio 0.35 --simplify-error 0.001 \
  --texture-compress webp --texture-size 2048
```

Qué hace cada parte de este comando:

- `--compress quantize`: reduce la precisión numérica de las coordenadas del modelo (de decimales de alta precisión a enteros de 16 bits). No necesita ningún componente adicional para poder leerse después, a diferencia de otros métodos de compresión como Draco.
- `--simplify-ratio 0.35`: intenta reducir la malla a aproximadamente un 35% de sus triángulos originales (el resultado real depende de cuántas "costuras" de textura tenga el modelo, que limitan cuánto se puede simplificar).
- `--texture-compress webp --texture-size 2048`: convierte la textura de JPEG a WebP (más ligera a igual calidad visual) y limita su tamaño a 2048×2048 píxeles.

En el objeto de prueba de este proyecto, este paso redujo el fichero de **8,94 MB a 3,87 MB**.

### Paso 5 — Colocar los puntos de interés (*hotspots*)

En el siguiente enlace [**modelviewer**](https://modelviewer.dev/editor/), cargad vuestro `.glb` optimizado. 

Ve a Editar (icono lápiz) --> Animations\Hotspots --> Botón "Add Hotspot"

Con la herramienta de *hotspots* del propio editor, haced clic directamente sobre cada punto del modelo que queráis etiquetar. 

El editor calcula automáticamente los valores `data-position` y `data-normal` (la posición 3D y la orientación de la superficie en ese punto) y os da el código ya listo para copiar.

En cada *hotspots* indica qué es y qué hace, por ejemplo: *Disipador. Elemento para radiar el calor y evitar sobrecalentamiento del microprocesador*.

Coloca *hotspots* en:

 - **Zona del procesador**
	- Zócalo/socket de CPU
	- Disipador/ventilador de CPU (si viene integrado o sujeto a la placa)
	- Conectores de alimentación de CPU (4-pin o 8-pin EPS, cerca del zócalo)

- **Memoria**
	- Ranuras/slots de RAM (DIMM)
	- Clips de sujeción de la RAM

- **Chipset**
	- Puente Norte (Northbridge) 🕰️ — en placas modernas esta función está integrada en la CPU
	- Puente Sur (Southbridge) 🕰️ — en placas modernas pasa a llamarse simplemente “chipset” (PCH)
	- Chipset/PCH (Platform Controller Hub) — la placa moderna equivalente, normalmente con su propio disipador
	- Disipador del chipset (si lo tiene)

- **Alimentación**
	- Conector ATX principal (24 pines)
	- Fases de alimentación (VRM) de la CPU
	- Disipadores de las VRM (si los tiene)
	- Condensadores (electrolíticos o de estado sólido)

	- **Expansión**
	- Ranuras PCIe x16 (gráfica)
	- Ranuras PCIe x1 / x4
	- Ranuras PCI 🕰️ (en placas muy antiguas)
	- Ranura AGP 🕰️ (anterior a PCIe, en placas muy antiguas)

- **Almacenamiento**
	- Conectores SATA
	- Ranura M.2
	- Conector IDE/PATA 🕰️ (el conector ancho de cinta plana)
	- Conector de disquetera (FDD) 🕰️

- **Red y E/S integrada**
	- Chip de red (Ethernet) integrado
	- Chip de audio integrado (codec)
	- Puertos USB (los conectores de placa, no los del panel trasero)
	- Header USB para el panel frontal de la torre

- **Panel trasero (I/O shield)**
	- Puertos USB traseros
	- Salida de vídeo integrada (HDMI/DisplayPort/VGA/DVI si tiene gráfica integrada)
	- Conectores de audio traseros
	- Puerto Ethernet trasero
	- Puerto PS/2 🕰️ (teclado/ratón, en placas más antiguas)
	- Puerto serie/paralelo 🕰️ (muy antiguas)

- **Otros puntos**
	- Batería de la BIOS/CMOS (la pila redonda)
	- Chip de la BIOS/UEFI
	- Pines del panel frontal (power switch, reset, LEDs)
	- Conectores de ventiladores (fan headers)
	- Jumpers de configuración 🕰️ (muy presentes en placas antiguas para configurar voltajes/frecuencias a mano)


### Paso 6 — Montar la página web

Necesitáis tres ficheros en la misma carpeta: `index.html`, `style.css`, y vuestro `.glb` optimizado. Usad como base el siguiente código, sustituyendo el nombre del fichero `.glb`, los `data-position`/`data-normal` de vuestros propios *hotspots*, y el texto de cada etiqueta:

**`index.html`**

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Mi objeto — Realidad Aumentada</title>
<link rel="stylesheet" href="style.css">
<script type="module" src="https://cdn.jsdelivr.net/npm/@google/model-viewer@4.1.0/dist/model-viewer.min.js"></script>
</head>
<body>

<model-viewer
    id="viewer"
    src="modelo-<NOMBRE DE LA PLACA>_optimizado.glb"
    ar
    ar-modes="webxr scene-viewer quick-look"
    camera-controls
    tone-mapping="neutral"
    shadow-intensity="1">

  <button class="Hotspot" slot="hotspot-1"
      data-position="0 0 0m"
      data-normal="0 1 0m"
      data-visibility-attribute="visible">
    <div class="HotspotAnnotation">Texto de la etiqueta 1</div>
  </button>

  <!-- Repetid este bloque <button> por cada hotspot, cambiando el número de slot -->

  <div class="progress-bar hide" slot="progress-bar">
    <div class="update-bar"></div>
  </div>

  <button slot="ar-button" id="ar-button">Ver en tu espacio</button>

</model-viewer>

<script>
  // Mostrar/ocultar la etiqueta al PULSAR el hotspot (no al pasar el ratón,
  // que no funciona en pantalla táctil). Solo una etiqueta abierta a la vez.
  document.querySelectorAll('.Hotspot').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var wasOpen = btn.classList.contains('is-open');
      document.querySelectorAll('.Hotspot').forEach(function (b) {
        b.classList.remove('is-open');
      });
      if (!wasOpen) btn.classList.add('is-open');
    });
  });

  // Barra de progreso mientras carga el modelo 3D
  var viewer = document.querySelector('#viewer');
  viewer.addEventListener('progress', function (event) {
    var bar = viewer.querySelector('.update-bar');
    var progressBar = viewer.querySelector('.progress-bar');
    var pct = event.detail.totalProgress * 100;
    bar.style.width = pct + '%';
    if (pct === 100) {
      progressBar.classList.add('hide');
    } else {
      progressBar.classList.remove('hide');
    }
  });
</script>

</body>
</html>
```

**`style.css`**

```css
:root{
  --bg:#f2ede6;
  --fg:#1c1a17;
  --surface:#ffffff;
  --accent:#b5452f;
  --accent-fg:#ffffff;
  color-scheme: light dark;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#17140f;
    --fg:#f2ede6;
    --surface:#2a251f;
  }
}

*{ box-sizing:border-box; }

html,body{
  height:100%;
  margin:0;
  background:var(--bg);
  color:var(--fg);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
}

model-viewer{
  width:100%;
  height:100vh;
  background:var(--bg);
}

/* Punto pulsable sobre el modelo */
.Hotspot{
  width:28px; height:28px;
  border-radius:50%;
  background:var(--accent);
  border:2px solid var(--accent-fg);
  box-shadow:0 2px 6px rgba(0,0,0,.35);
  padding:0;
  cursor:pointer;
}

/* Etiqueta con la descripción: oculta hasta que se pulsa el hotspot */
.HotspotAnnotation{
  position:absolute;
  left:50%; bottom:140%;
  transform:translateX(-50%);
  background:var(--surface);
  color:var(--fg);
  padding:6px 12px;
  border-radius:8px;
  white-space:nowrap;
  box-shadow:0 2px 10px rgba(0,0,0,.3);
  font-size:14px;
  opacity:0;
  pointer-events:none;
  transition:opacity .15s ease;
}
.Hotspot.is-open .HotspotAnnotation{ opacity:1; }

/* Botón de Realidad Aumentada */
#ar-button{
  position:absolute;
  bottom:16px; right:16px;
  background:var(--accent);
  color:var(--accent-fg);
  border:none;
  padding:10px 18px;
  border-radius:24px;
  font-size:14px;
  font-weight:600;
  cursor:pointer;
}

/* Barra de progreso de carga */
.progress-bar{
  position:absolute; left:15%; right:15%; top:50%;
  height:6px; border-radius:3px; overflow:hidden;
  background:rgba(0,0,0,.15);
}
.progress-bar.hide{ display:none; }
.update-bar{ height:100%; width:0%; background:var(--accent); transition:width .2s; }
```

**Dos detalles de este código que suelen fallar si no se respetan:**

- El `<script type="module" src="...model-viewer.min.js">` es **imprescindible**: sin él, el navegador no reconoce la etiqueta `<model-viewer>` y no se ve nada.
- Las clases CSS del HTML (`Hotspot`, `HotspotAnnotation`, con mayúscula) deben coincidir **exactamente** con las del `style.css`. En CSS, las mayúsculas y minúsculas son distintas: `Hotspot` y `hotspot` son dos clases diferentes.

### Paso 7 — Probar en local

Con la extensión **Live Server** (de VS Code, por ejemplo) o cualquier servidor local, abrid la página en Chrome de escritorio. Debéis ver el modelo y, al pulsar sobre cada punto de color, su etiqueta correspondiente.

> No sirve abrir el `index.html` con doble clic (como fichero `file://`): ni la carga del modelo ni el modo AR funcionan así, necesitan un servidor.
>
> Tampoco esperéis ver el botón de Realidad Aumentada en el PC: `model-viewer` solo lo muestra cuando detecta que el dispositivo puede activarla de verdad (un móvil compatible), nunca en un navegador de escritorio.

### Paso 8 — Publicar la página con HTTPS (GitHub Pages)

La Realidad Aumentada en el navegador exige que la página esté servida por **HTTPS**; no funciona en local ni por HTTP normal. La forma gratuita más sencilla es GitHub Pages:

1. Crear una cuenta en (**GitHub**)[https://github.com] (si no se tiene ya).
2. Icono **"+"** (arriba a la derecha) → **"New repository"**. Nombre sencillo, marcado como **Public** (imprescindible para GitHub Pages gratuito), sin añadir README.
3. Dentro del repositorio recién creado: **"Add file" > "Upload files"**. Arrastrar los tres ficheros (`index.html`, `style.css`, el `.glb`). Confirmar con **"Commit changes"**.
4. **Pestaña "Settings" > "Pages"** (menú lateral). En *Source*, elegir **"Deploy from a branch"**, rama **main**, carpeta **/ (root)**, y **Save**.
5. Esperar 1–2 minutos y recargar esa misma página de *Settings > Pages*: aparecerá la URL final, con esta forma: `https://tu-usuario.github.io/nombre-repositorio/`.

### Paso 9 — Verificar la Realidad Aumentada en el móvil

Abrir esa URL en **Chrome para Android** (no en el navegador interno de otra app) y pulsar el botón de AR.

> ⚠️ **El botón de AR puede no aparecer aunque todo el código esté bien.** Esto no es necesariamente un error: el botón solo se muestra si el propio sistema Android considera el dispositivo compatible con **Google Play Services for AR** (antes llamado ARCore). No todos los móviles están certificados — los modelos de gama de entrada o las variantes "Lite" de algunas marcas suelen quedar fuera de esa lista aunque el resto del modelo sí esté soportado.
>
> Para comprobarlo: abrid la **Play Store** y buscad manualmente **"Google Play Services for AR"**. Si no se puede instalar o aparece como incompatible con vuestro modelo, es una limitación del propio dispositivo, no de vuestro trabajo — documentadlo así en la entrega.
>
> Lista oficial de dispositivos certificados: **https://developers.google.com/ar/devices**

### Problemas típicos y cómo resolverlos

| Síntoma | Causa probable | Solución |
|---|---|---|
| Pantalla en negro, no se ve nada | Falta el `<script>` que carga `model-viewer`, o las clases CSS no coinciden con las del HTML | Comprobar que el script del CDN está presente y que los nombres de clase son idénticos, mayúsculas incluidas |
| Las etiquetas están siempre visibles y no reaccionan al pulsar | Falta el JavaScript que escucha el evento `click` sobre los hotspots | Añadir el bloque de `addEventListener('click', ...)` del Paso 6 |
| El modelo tarda muchísimo en cargar (varios segundos o más) | El `.glb` es demasiado pesado sin optimizar | Aplicar el Paso 4 (optimización con `gltf-transform`) |
| Tras corregir los ficheros, la página sigue mostrando el fallo antiguo | Los ficheros corregidos están guardados en otra carpeta y no se han copiado a la que sirve el servidor local o a la subida a GitHub | Copiar/subir los ficheros corregidos sobre los antiguos y recargar forzando caché (`Ctrl + Shift + R`) |
| No aparece el botón de AR en el móvil | El dispositivo no está certificado para Google Play Services for AR | Ver el aviso del Paso 9. No es un fallo del código |

## 6. Material proporcionado al alumnado

- Esta guía (`guia-motherboard-ra.md`).
- Plantilla base de `index.html` y `style.css` (Paso 6 de esta guía).
- Enlace al editor visual de *hotspots*: https://modelviewer.dev/editor/
- Enlace a la lista oficial de dispositivos compatibles con ARCore: https://developers.google.com/ar/devices
- Acceso a una cuenta de GitHub (de centro o personal) para la publicación.

## 7. Entrega

Formato del documento: pdf.
Nombre del fichero: `tuNombre_Apellido1_Apellido2_UT1-A1.pdf`

## 8. Rúbrica

| Apartado de la Actividad | Criterio Relacionado | Mal | Regular | Bien | Muy Bien | Excelente |
|---|---|---|---|---|---|---|
| **Modelo 3D y Optimización** | CE a) Identificar las principales THD. | No entrega modelo o es irreconocible. (0 pts) | Escanea el modelo pero no lo limpia (mantiene el cubo por defecto, origen descentrado). (0.5 pts) | Modelo limpio y centrado, pero omite el paso de compresión y optimización del peso. (1 pto) | Modelo limpio y optimizado correctamente con `gltf-transform`. (1.5 pts) | Modelo impecable, optimizado y documentando de forma precisa la reducción de tamaño conseguida. (2 pts) |
| **Identificación de Componentes Hardware** | Transversal: Reconocimiento de arquitectura física. | No hay hotspots o la información técnica es totalmente errónea. (0 pts) | Etiqueta 2-3 componentes básicos pero con descripciones vagas o genéricas. (0.5 pts) | Identifica varios componentes clave (CPU, RAM, Puertos) con descripciones correctas. (1.5 pts) | Etiqueta abundantes zonas (incluyendo chipset, alimentación o almacenamiento) con buena precisión técnica. (2 pts) | Etiquetado exhaustivo y profesional de zonas complejas (VRM, PCIe, headers) con descripciones técnicas ricas. (2.5 pts) |
| **Integración Web e Interfaz** | CE b) Relacionar THD con productos. | La página no carga el modelo o los archivos están mal enlazados. (0 pts) | Carga el modelo pero la interfaz tiene fallos visuales o los hotspots están siempre abiertos. (0.5 pts) | Página funcional donde el modelo es visible y los botones interactúan correctamente. (1 pto) | Interfaz muy cuidada, CSS limpio y el comportamiento de las etiquetas (cerrar al abrir otra) es perfecto. (1.5 pts) | Interfaz pulida y responsive, barra de progreso funcional y adaptación a modo claro/oscuro fluida. (2 pts) |
| **Despliegue y Pruebas AR** | CE b) Relacionar THD con servicios. | No publicado o enlace roto (error 404). (0 pts) | Publicado pero fallan rutas relativas (HTTP mixto) o no funciona en móvil. (0.25 pts) | Publicado en GitHub Pages (HTTPS) y accesible desde cualquier navegador. (0.75 pts) | Publicado con éxito, probado en móvil y documentando si aparece el botón AR. (1 pto) | Despliegue impecable en GitHub Pages. Testeo en varios dispositivos comparando compatibilidad de ARCore. (1.5 pts) |
| **Documentación e Informe** | CE g) Elaborar informe relacionando tecnologías. | No entrega PDF o es un simple volcado de texto sin estructura. (0 pts) | Documentación escasa, enumera pasos sin capturas ni justificación tecnológica. (0.5 pts) | Informe correcto que detalla el proceso seguido y relaciona la RA con el producto. (1 pto) | Informe bien estructurado que detalla pasos, capturas, incidencias y su resolución. (1.5 pts) | Informe profesional (reglas de oro), análisis profundo de las THD empleadas y resolución magistral de incidencias. (2 pts) |

<br>

|  | Se retrasa más de 5 días | Se retrasa entre 4 y 5 días | Se retrasa entre 2 y 3 días | Se retrasa 1 día. | Entrega en plazo |
|---|---|---|---|---|---|
| **Entrega tarea en plazo** | - 5 | - 3 | -2 | -1 | 0 |


