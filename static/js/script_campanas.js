let todasLasCampañas = []; // Para mantener una copia de todas las campañas originales

        window.onload = function() {
            cargarCampañasGuardadas();
            document.getElementById('limpiarCampañasBtn').addEventListener('click', confirmarLimpiarTodasLasCampañas);
            
            // ESTA ES LA LÍNEA CRÍTICA PARA EL BOTÓN REGRESAR:
            // Se asigna la función 'regresar' como manejador del evento 'click', SIN ejecutarla inmediatamente.
            document.getElementById('btnRegresar').addEventListener('click', regresar); 
            
            document.getElementById('btnAplicarFiltros').addEventListener('click', aplicarFiltros);
            document.getElementById('btnLimpiarFiltros').addEventListener('click', limpiarCamposDeFiltro);

            // Opcional: aplicar filtros al presionar Enter en los campos de texto o cambiar select/date
            const filterInputs = document.querySelectorAll('.filter-grid input[type="text"], .filter-grid input[type="date"], .filter-grid select');
            filterInputs.forEach(input => {
                input.addEventListener('keypress', function(event) {
                    if (event.key === 'Enter') {
                        aplicarFiltros();
                    }
                });
                if (input.tagName === 'SELECT' || input.type === 'date') {
                     input.addEventListener('change', aplicarFiltros);
                }
            });
        };

        function regresar() {
            console.log("Botón Regresar presionado. Redirigiendo..."); // Para depuración
            // Cambia 'index.html' por el nombre real de tu página principal de generación de GUIs si es diferente.
            window.location.href = 'index.html'; 
        }

        function parseGuiString(guiString) {
            if (!guiString || typeof guiString !== 'string') return null;
            const parts = guiString.split('-');
            // Se espera una estructura específica. Ajustar el mínimo si es necesario.
            // Pais-PlatCont-Tipo-Fecha-NombreReloj(puede tener guiones)-IdReloj-Persona-NoImport
            // Por lo tanto, al menos 8 partes si el nombre del reloj es una sola palabra.
            if (parts.length < 8) { 
                console.warn("Cadena GUI no tiene suficientes partes para parsear:", guiString);
                return null;
            }

            const pais = parts[0];
            const plataformaContador = parts[1];
            const plataforma = plataformaContador ? plataformaContador.charAt(0) : '';
            // const contador = plataformaContador ? plataformaContador.substring(1) : ''; // No se usa directamente en filtros
            const tipoCampana = parts[2];
            const fecha = parts[3]; // Se espera YYYY-MM-DD

            // Los últimos 3 segmentos son fijos: IdReloj, Persona, NoImport
            const numImportacion = parts[parts.length - 1];
            const persona = parts[parts.length - 2];
            const idReloj = parts[parts.length - 3];
            
            // Nombre del reloj es lo que está entre la fecha (índice 3) y los últimos 3 segmentos.
            // El slice va desde el índice 4 hasta (longitud total - 3)
            const nombreReloj = parts.slice(4, parts.length - 3).join('-');

            return {
                raw: guiString,
                pais,
                plataforma,
                // contador, // Descomentar si necesitas filtrar por contador
                tipoCampana,
                fecha,
                nombreReloj,
                idReloj,
                persona,
                numImportacion
            };
        }

        function cargarCampañasGuardadas() {
            const campañasGuardadasRaw = JSON.parse(localStorage.getItem('campañasGuardadas') || '[]');
            todasLasCampañas = campañasGuardadasRaw.map(parseGuiString).filter(Boolean); // Parsear y quitar nulos
            renderCampañas(todasLasCampañas);
        }

        function renderCampañas(campañas) {
            const listaUl = document.getElementById('listaCampañasGuardadas');
            listaUl.innerHTML = ''; 

            if (campañas.length === 0) {
                const pInfo = document.createElement('p');
                pInfo.className = 'no-campaigns';
                pInfo.textContent = 'No hay campañas que coincidan con los filtros o no hay campañas guardadas.';
                listaUl.appendChild(pInfo);
            } else {
                campañas.forEach(campañaObj => {
                    if (!campañaObj || !campañaObj.raw) return; // Chequeo de seguridad
                    const li = document.createElement('li');
                    li.textContent = campañaObj.raw;
                    listaUl.appendChild(li);
                });
            }
        }
        
        function aplicarFiltros() {
            const filtroPaisVal = document.getElementById('filtroPais').value.trim().toLowerCase();
            const filtroPlataformaVal = document.getElementById('filtroPlataforma').value; // Ya es 'F' o 'T'
            const filtroTipoCampanaVal = document.getElementById('filtroTipoCampana').value.trim().toLowerCase();
            const filtroFechaVal = document.getElementById('filtroFecha').value; // Formato YYYY-MM-DD
            const filtroNombreRelojVal = document.getElementById('filtroNombreReloj').value.trim().toLowerCase();
            const filtroIdRelojVal = document.getElementById('filtroIdReloj').value.trim().toLowerCase();
            const filtroPersonaVal = document.getElementById('filtroPersona').value.trim().toLowerCase();
            const filtroNumImportacionVal = document.getElementById('filtroNumImportacion').value.trim().toLowerCase();

            const campañasFiltradas = todasLasCampañas.filter(campaña => {
                if (!campaña) return false; // Seguridad

                const paisMatch = !filtroPaisVal || (campaña.pais && campaña.pais.toLowerCase().includes(filtroPaisVal));
                const plataformaMatch = !filtroPlataformaVal || (campaña.plataforma && campaña.plataforma === filtroPlataformaVal);
                const tipoCampanaMatch = !filtroTipoCampanaVal || (campaña.tipoCampana && campaña.tipoCampana.toLowerCase().includes(filtroTipoCampanaVal));
                const fechaMatch = !filtroFechaVal || (campaña.fecha && campaña.fecha === filtroFechaVal);
                const nombreRelojMatch = !filtroNombreRelojVal || (campaña.nombreReloj && campaña.nombreReloj.toLowerCase().includes(filtroNombreRelojVal));
                const idRelojMatch = !filtroIdRelojVal || (campaña.idReloj && campaña.idReloj.toLowerCase().includes(filtroIdRelojVal));
                const personaMatch = !filtroPersonaVal || (campaña.persona && campaña.persona.toLowerCase().includes(filtroPersonaVal));
                const numImportacionMatch = !filtroNumImportacionVal || (campaña.numImportacion && campaña.numImportacion.toLowerCase().includes(filtroNumImportacionVal));
                
                return paisMatch && plataformaMatch && tipoCampanaMatch && fechaMatch && nombreRelojMatch && idRelojMatch && personaMatch && numImportacionMatch;
            });

            renderCampañas(campañasFiltradas);
        }

        function limpiarCamposDeFiltro() {
            document.getElementById('filtroPais').value = '';
            document.getElementById('filtroPlataforma').value = '';
            document.getElementById('filtroTipoCampana').value = '';
            document.getElementById('filtroFecha').value = '';
            document.getElementById('filtroNombreReloj').value = '';
            document.getElementById('filtroIdReloj').value = '';
            document.getElementById('filtroPersona').value = '';
            document.getElementById('filtroNumImportacion').value = '';
            
            renderCampañas(todasLasCampañas); // Mostrar todas las campañas de nuevo
        }

        function confirmarLimpiarTodasLasCampañas() {
            if (confirm("¿Estás seguro de que quieres borrar TODAS las campañas guardadas? Esta acción no se puede deshacer.")) {
                localStorage.removeItem('campañasGuardadas');
                todasLasCampañas = []; // Limpiar la copia en memoria también
                renderCampañas([]); // Recargar la lista (que ahora estará vacía)
                alert("Todas las campañas guardadas han sido eliminadas.");
            }
        }
