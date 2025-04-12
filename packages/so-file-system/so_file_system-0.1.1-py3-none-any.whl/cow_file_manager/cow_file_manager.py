import os
import json
import zlib
import base64
from datetime import datetime
from colorama import Fore, Style
import time
import concurrent.futures
import io
from tqdm import tqdm

"""
    Gestor de archivos versionados utilizando bloques de 4KB y compresión de datos.

    Permite crear, abrir, leer, escribir versiones de archivos, manejar el uso de memoria,
    y realizar operaciones de recolección de bloques huérfanos.

    Atributos:
        ruta_archivo (str): Ruta del archivo a gestionar.
        nombre_archivo (str): Nombre del archivo.
        directorio_base (str): Carpeta base para almacenar datos.
        directorio_archivos (str): Carpeta para archivos originales.
        directorio_versiones_base (str): Carpeta base para versiones de archivos.
        directorio_inodos (str): Carpeta para metadatos de archivos (inodos).
        directorio_logs (str): Carpeta para registros de cambios.
        inodo (dict): Estructura que guarda la información de versiones y bloques.
        current_version (int): Índice de la versión actual activa.
    """
class GestorArchivos:


    """
        Inicializa el gestor de archivos versionados.

        Args:
            ruta_archivo (str): Ruta del archivo que se va a gestionar.

        Crea la estructura base de carpetas y archivos relacionados,
        pero no crea el archivo físico hasta llamar a `create()`.
        """
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo
        self.nombre_archivo = os.path.basename(ruta_archivo)
        self.directorio_base = "lavacamu_data"
        self.directorio_archivos = os.path.join(self.directorio_base, "archivos")
        self.directorio_versiones_base = os.path.join(self.directorio_base, "versiones")
        self.directorio_inodos = os.path.join(self.directorio_base, "inodos")
        self.directorio_logs = os.path.join(self.directorio_base, "logs")

        self.inodo_path = os.path.join(self.directorio_inodos, f"{self.nombre_archivo}.json")
        self.versiones_dir = os.path.join(self.directorio_versiones_base, self.nombre_archivo)
        self.log_path = os.path.join(self.directorio_logs, f"{self.nombre_archivo}.log")

        self.BLOQUE_TAM_MAX = 4096  # 4KB por bloque

        self.inodo = None
        self.current_version = -1

    """
        Crea las carpetas necesarias para operar si no existen:
        - Base
        - Archivos
        - Versiones
        - Inodos
        - Logs
        """
    def _asegurar_estructura(self):
        for d in [self.directorio_base, self.directorio_archivos,
                  self.directorio_versiones_base, self.directorio_inodos,
                  self.directorio_logs, self.versiones_dir]:
            os.makedirs(d, exist_ok=True)

    """
        Carga la información de versiones (inodo) desde disco.
        Si no existe, crea un inodo inicial vacío para el archivo.
        """
    def _cargar_o_crear_inodo(self):
        if os.path.exists(self.inodo_path):
            with open(self.inodo_path, "r", encoding="utf-8") as f:
                self.inodo = json.load(f)
        else:
            self.inodo = {
                "nombre": self.nombre_archivo,
                "primer_bloque": "",
                "fat": {},
                "versiones": [],
                "current_version": -1
            }
            self._guardar_inodo()

    """
       Guarda la estructura de inodo (versiones, bloques, etc.) en disco.
       """
    def _guardar_inodo(self):
        with open(self.inodo_path, "w", encoding="utf-8") as f:
            json.dump(self.inodo, f, indent=4)

    """
        Registra un mensaje en el log de cambios del archivo.

        Args:
            mensaje (str): Texto a registrar en el archivo de logs.
        """
    def _registrar_log(self, mensaje):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {mensaje}\n")

    def _ruta_bloque(self, nombre_bloque):
        return os.path.join(self.versiones_dir, nombre_bloque)

    """
       Crea un nuevo bloque JSON vacío para almacenar fragmentos de datos.

       El nombre del bloque es incremental ('block_XXXX.json') dentro de la carpeta de versiones.

       Returns:
           str: Nombre del nuevo bloque creado.
       """
    def _crear_nuevo_bloque(self):
        bloques_existentes = [f for f in os.listdir(self.versiones_dir) if f.startswith("block_") and f.endswith(".json")]
        if not bloques_existentes:
            nuevo_nombre = "block_0001.json"
        else:
            bloques_existentes.sort()
            ultimo = bloques_existentes[-1]
            numero = int(ultimo.replace("block_", "").replace(".json", ""))
            nuevo_nombre = f"block_{numero+1:04d}.json"

        bloque = {"nombre": nuevo_nombre, "contenido": "", "usado": 0, "max": self.BLOQUE_TAM_MAX, "paginas": []}
        self._guardar_bloque(bloque)
        self.inodo["fat"][nuevo_nombre] = {"next": None, "usado": 0}
        self._guardar_inodo()
        return nuevo_nombre

    """
    Guarda en disco el contenido actualizado de un bloque.

    Args:
        bloque (dict): Estructura del bloque a persistir.
    """
    def _guardar_bloque(self, bloque):
        with open(self._ruta_bloque(bloque["nombre"]), "w", encoding="utf-8") as f:
            json.dump(bloque, f, indent=4)

    """
        Carga desde disco el contenido de un bloque específico.

        Args:
            nombre (str): Nombre del bloque a cargar.

        Returns:
            dict or None: Estructura del bloque, o None si no existe.
        """
    def _obtener_bloque(self, nombre):
        ruta = self._ruta_bloque(nombre)
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    """
       Crea un archivo vacío en modo binario y prepara su estructura de versionado.

       Si el archivo ya existe, no lo sobrescribe.
       """
    def create(self):
        if self.inodo is not None:
            print("⚠️ Ya tienes un archivo abierto. Debes cerrarlo primero antes de crear uno nuevo.")
            return
        self._asegurar_estructura()
        if not os.path.exists(self.ruta_archivo):
            with open(self.ruta_archivo, "wb") as f:
                pass
            print(f"✅ Archivo '{self.nombre_archivo}' creado exitosamente y preparado para versionado.")
            self._cargar_o_crear_inodo()
            self._registrar_log("Archivo creado")
        else:
            print(f"⚠️ El archivo '{self.nombre_archivo}' ya existe.")

    """
        Abre un archivo existente, cargando su información de versiones e inodo.

        Si el archivo no existe, sugiere crear uno nuevo.
        """

    def open(self):
        """Abre el archivo existente y asegura que haya al menos una versión inicial."""
        if self.inodo is not None:
            print("⚠️ Ya tienes un archivo abierto. Cierra el actual antes de abrir otro.")
            return

        self._asegurar_estructura()

        if os.path.exists(self.ruta_archivo):
            self._cargar_o_crear_inodo()

            if not self.inodo["versiones"]:
                print("📦 No se encontraron versiones. Creando versión inicial (v0)...")
                self._crear_version_inicial()

            self.current_version = self.inodo["current_version"]
            print(f"✅ Archivo '{self.nombre_archivo}' abierto exitosamente.")
        else:
            print(f"❌ Archivo '{self.nombre_archivo}' no encontrado. Usa 'create()' primero.")

    def _crear_version_inicial(self):
        """Crea automáticamente la versión inicial (v0) a partir del archivo físico."""
        try:
            with open(self.ruta_archivo, "rb") as f:
                contenido = f.read()

            if contenido:
                self.write(contenido)
                print("🎯 Versión inicial (v0) creada correctamente.")
            else:
                print("⚠️ El archivo estaba vacío. No se creó versión inicial.")
        except Exception as e:
            print(f"❌ Error creando versión inicial: {e}")

    """
        Lee y reconstruye el contenido de la última versión guardada del archivo.

        Recupera el contenido binario original a partir de los bloques almacenados.
        Muestra el tamaño del contenido reconstruido.

        Raises:
            Exception: Si ocurre algún error en la descompresión o reconstrucción.
        """
    def read(self):
        if self.inodo is None:
            print("⚠️ No hay archivo abierto. Usa 'open()' o 'create()' primero.")
            return
        if self.current_version == -1:
            print("⚠️ No existen versiones aún para leer. Debes crear una primero escribiendo contenido.")
            return
        if self.current_version == -1:
            print("⚠️ No hay versiones disponibles para leer.")
            return

        version = self.inodo["versiones"][self.current_version]
        contenido_total = ""

        for bloque_info in version["bloques"]:
            bloque = self._obtener_bloque(bloque_info["bloque"])
            if bloque:
                inicio = bloque_info["offset_inicio"]
                fin = bloque_info["offset_fin"]
                contenido_total += bloque["contenido"][inicio:fin]

        try:
            contenido_comprimido = base64.b64decode(contenido_total.encode("utf-8"))
            contenido_base64 = zlib.decompress(contenido_comprimido)
            binario = base64.b64decode(contenido_base64)
            print(f"📖 Contenido de la última versión (tamaño {len(binario)} bytes) recuperado exitosamente.")
        except Exception as e:
            print(f"❌ Error leyendo la versión: {e}")

    """
        Escribe nuevos datos como una nueva versión del archivo.

        Fragmenta y comprime los datos usando zlib y base64, almacena en bloques de 4KB, 
        y registra una nueva versión.

        Args:
            data (str or bytes): Contenido a escribir.
            level (int, optional): Nivel de compresión (1 a 9). Default = 9.

        Raises:
            Exception: Si ocurre error en la escritura o fragmentación de bloques.
        """

    def write(self, data, level=9):
        """
        Guarda datos en una nueva versión:
        - Si `data` es un texto, lo guarda como texto.
        - Si `data` es una ruta válida a un archivo, lo guarda como binario.
        """
        inicio = time.time()

        if self.inodo is None:
            print("⚠️ No hay archivo abierto. Usa 'open()' o 'create()' primero.")
            return

        if not isinstance(data, (str, bytes)):
            print("❌ El contenido debe ser tipo string, bytes, o ruta de archivo válida.")
            return

        # Auto detectar si es ruta de archivo
        if isinstance(data, str) and os.path.exists(data):
            print(f"📂 Detectado archivo: {data}")
            with open(data, "rb") as f:
                contenido = f.read()
        elif isinstance(data, str):
            contenido = data.encode("utf-8")
        else:
            contenido = data

        if len(contenido) == 0:
            print("⚠️ No se puede guardar contenido vacío.")
            return

        # Codificación y compresión
        buffer = io.BytesIO()
        base64_bytes = base64.b64encode(contenido)
        compressed_bytes = zlib.compress(base64_bytes, level=level)
        buffer.write(base64.b64encode(compressed_bytes))
        buffer.seek(0)
        contenido_final = buffer.read().decode('utf-8')

        longitud_total = len(contenido_final)
        offset_inicio = 0

        bloques_existentes = {
            nombre: self._obtener_bloque(nombre)
            for nombre in os.listdir(self.versiones_dir)
            if nombre.startswith("block_")
        }
        bloques_utilizados = []
        acciones = []

        def guardar_bloque(bloque, fragmento, offset_bloque, bytes_a_escribir):
            bloque["contenido"] += fragmento
            bloque["usado"] += bytes_a_escribir
            bloque["paginas"].append({
                "version_id": f"v{len(self.inodo['versiones'])}",
                "offset": offset_bloque,
                "longitud": bytes_a_escribir
            })
            self._guardar_bloque(bloque)

        with concurrent.futures.ThreadPoolExecutor() as executor, tqdm(total=longitud_total, desc="Guardando bloques",
                                                                       unit="B", unit_scale=True) as barra:
            while offset_inicio < longitud_total:
                bloque_usado = next(
                    (b for b in bloques_existentes.values() if b and (b["max"] - b["usado"] > 0)),
                    None
                )

                if not bloque_usado:
                    nuevo_nombre = self._crear_nuevo_bloque()
                    bloque_usado = self._obtener_bloque(nuevo_nombre)
                    bloques_existentes[nuevo_nombre] = bloque_usado

                espacio_disponible = bloque_usado["max"] - bloque_usado["usado"]
                bytes_a_escribir = min(espacio_disponible, longitud_total - offset_inicio)
                fragmento = contenido_final[offset_inicio: offset_inicio + bytes_a_escribir]
                offset_bloque = bloque_usado["usado"]

                acciones.append(executor.submit(
                    guardar_bloque,
                    bloque_usado,
                    fragmento,
                    offset_bloque,
                    bytes_a_escribir
                ))

                bloques_utilizados.append({
                    "bloque": bloque_usado["nombre"],
                    "offset_inicio": offset_bloque,
                    "offset_fin": offset_bloque + bytes_a_escribir
                })

                barra.update(bytes_a_escribir)
                offset_inicio += bytes_a_escribir

            concurrent.futures.wait(acciones)

        version_metadata = {
            "id": f"v{len(self.inodo['versiones'])}",
            "bloques": bloques_utilizados,
            "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S")
        }

        self.inodo["versiones"].append(version_metadata)
        self._actualizar_current_version(len(self.inodo["versiones"]) - 1)
        self._guardar_inodo()
        self._registrar_log(f"Nueva versión creada: {version_metadata['id']}")

        fin = time.time()
        print("\n🛠️ Nueva versión", version_metadata['id'], "guardada exitosamente.")
        print(f"⏱️ Tiempo total: {fin - inicio:.2f} segundos.")

    """
        Actualiza el índice de la versión actual en el inodo.

        Args:
            new_index (int): Índice de la nueva versión actual activa.
        """
    def _actualizar_current_version(self, new_index):
        self.inodo["current_version"] = new_index
        self.current_version = new_index
        self._guardar_inodo()

    """
        Cierra el archivo actual, limpiando las referencias en memoria.

        Registra el evento de cierre en el log de cambios.
        """
    def close(self):
        if self.ruta_archivo is None:
            print("⚠️ No hay archivo abierto actualmente.")
            return
        if self.ruta_archivo:
            print(f"🔒 Archivo '{self.nombre_archivo}' cerrado correctamente.")
            self._registrar_log("Archivo cerrado")
        self.ruta_archivo = None
        self.nombre_archivo = None
        self.inodo = None
        self.current_version = -1

    """
        Lista todas las versiones disponibles del archivo, mostrando:
        - ID de la versión
        - Tamaño en bytes
        - Número de bloques utilizados
        - Timestamp de creación

        Si no hay versiones, muestra advertencia.
        """

    def listar_versiones(self):
        """
        Lista todas las versiones disponibles del archivo, mostrando tamaño en disco y tamaño real estimado.
        """
        if not self.inodo or not self.inodo["versiones"]:
            print("⚠️ No hay versiones registradas.")
            return

        print(f"📜 Versiones disponibles para '{self.nombre_archivo}':\n")

        for i, version in enumerate(self.inodo["versiones"]):
            vid = version.get("id", "Sin ID")
            timestamp = version.get("timestamp", "Sin fecha")
            bloques = len(version.get("bloques", []))
            tamano_en_disco = sum(b["offset_fin"] - b["offset_inicio"] for b in version.get("bloques", []))

            # Reconstruir contenido para estimar tamaño real
            contenido_total = ""
            for bloque_info in version["bloques"]:
                bloque = self._obtener_bloque(bloque_info["bloque"])
                if bloque:
                    inicio = bloque_info["offset_inicio"]
                    fin = bloque_info["offset_fin"]
                    contenido_total += bloque["contenido"][inicio:fin]

            tamano_real = None

            if i == 0:
                # v0: es archivo puro, no codificado
                tamano_real = tamano_en_disco
            else:
                try:
                    contenido_comprimido = base64.b64decode(contenido_total.encode("utf-8"))
                    contenido_base64 = zlib.decompress(contenido_comprimido)
                    binario = base64.b64decode(contenido_base64)
                    tamano_real = len(binario)
                except Exception:
                    tamano_real = "❓"

            print(
                f"🔹 {i + 1}. ID: {vid} | Tamaño en disco: {tamano_en_disco} bytes | Estimado real: {tamano_real} bytes | Bloques: {bloques} | Creado: {timestamp}")

        print(f"\n🔄 Versión actual activa: {self.current_version}")

    """
        Muestra estadísticas de uso de memoria:
        - Bytes usados vs. capacidad máxima de cada bloque.
        - Porcentaje de ocupación por bloque.
        - Espacio total usado y libre.

        Útil para diagnosticar eficiencia de almacenamiento.
        """
    def mostrar_uso_memoria(self):
        """
        Muestra estadísticas de uso de memoria en los bloques del archivo.
        """
        if not self.inodo or not self.inodo["fat"]:
            print("⚠️ No hay bloques asignados.")
            return

        total_usado = 0
        total_max = 0

        print(f"📊 Uso de memoria para el archivo '{self.nombre_archivo}':\n")

        for bloque_nombre, fat_entry in self.inodo["fat"].items():
            bloque = self._obtener_bloque(bloque_nombre)
            if bloque:
                usados = bloque["usado"]
                maximo = bloque["max"]
                porcentaje = (usados / maximo) * 100 if maximo else 0
                total_usado += usados
                total_max += maximo
                print(f"🔹 {bloque_nombre}: {usados} / {maximo} bytes usados ({porcentaje:.2f}%)")

        print(f"\n📦 Total de bloques: {len(self.inodo['fat'])}")
        print(f"✅ Espacio total usado: {total_usado} bytes")
        print(f"💡 Espacio libre disponible: {total_max - total_usado} bytes")

    """
        Identifica y elimina bloques huérfanos no asociados a ninguna versión.

        Libera espacio de almacenamiento eliminando archivos de bloques
        no referenciados en las versiones activas.
        """
    def recolectar_bloques_huerfanos(self):
        """
        Elimina los bloques que no están referenciados por ninguna versión activa.
        """
        if not self.inodo:
            print("⚠️ No hay información de inodo cargada.")
            return

        print(f"🧹 Iniciando recolección de bloques huérfanos para '{self.nombre_archivo}'...")

        bloques_usados = set()
        for version in self.inodo["versiones"]:
            for b in version["bloques"]:
                bloques_usados.add(b["bloque"])

        bloques_en_disco = [f for f in os.listdir(self.versiones_dir) if f.startswith("block_")]

        eliminados = 0

        for bloque in bloques_en_disco:
            if bloque not in bloques_usados:
                try:
                    os.remove(self._ruta_bloque(bloque))
                    if bloque in self.inodo["fat"]:
                        del self.inodo["fat"][bloque]
                    eliminados += 1
                    print(f"🗑️ Eliminado bloque huérfano: {bloque}")
                except Exception as e:
                    print(f"❌ Error al eliminar bloque {bloque}: {e}")

        if eliminados > 0:
            self._guardar_inodo()
            self._registrar_log(f"Se eliminaron {eliminados} bloques huérfanos")
            print(f"✅ {eliminados} bloques huérfanos eliminados exitosamente.")
        else:
            print("✅ No se encontraron bloques huérfanos.")

    def rollback_backward(self):
        """
        Retrocede a la versión anterior disponible si es posible.
        """
        if not self.inodo or not self.inodo["versiones"]:
            print("⚠️ No hay versiones disponibles.")
            return

        if self.current_version > 0:
            self.current_version -= 1
            self.inodo["current_version"] = self.current_version
            self._guardar_inodo()
            print(f"⬅️ Retrocediste a la versión {self.inodo['versiones'][self.current_version]['id']}.")
        else:
            print("⚠️ Ya estás en la primera versión, no puedes retroceder más.")

    def rollback_forward(self):
        """
        Avanza a la siguiente versión disponible si existe.
        """
        if not self.inodo or not self.inodo["versiones"]:
            print("⚠️ No hay versiones disponibles.")
            return

        if self.current_version < len(self.inodo["versiones"]) - 1:
            self.current_version += 1
            self.inodo["current_version"] = self.current_version
            self._guardar_inodo()
            print(f"➡️ Avanzaste a la versión {self.inodo['versiones'][self.current_version]['id']}.")
        else:
            print("⚠️ Ya estás en la última versión, no puedes avanzar más.")

    def cambiar_a_version(self, version_id):
        """
        Cambia directamente a una versión específica por su ID (ej: 'v2', 'v5').
        """
        if not self.inodo or not self.inodo["versiones"]:
            print("⚠️ No hay versiones disponibles.")
            return

        encontrado = False
        for idx, version in enumerate(self.inodo["versiones"]):
            if version["id"] == version_id:
                self.current_version = idx
                self.inodo["current_version"] = idx
                self._guardar_inodo()
                print(f"🔄 Cambiaste a la versión {version_id}.")
                encontrado = True
                break

        if not encontrado:
            print(f"❌ No se encontró la versión {version_id}.")
