from cow_file_manager.cow_file_manager import GestorArchivos

gestor = None

def mostrar_menu():
    print("\n" + "=" * 60)
    print("🧠 Sistema de Archivos Versionado - Menú Principal")
    print("=" * 60)
    print("1. 📁 Crear archivo nuevo")
    print("2. 📂 Abrir archivo existente")
    print("3. 📖 Leer archivo (última versión)")
    print("4. ✏️  Escribir en archivo (nueva versión)")
    print("5. 📜 Listar versiones disponibles")
    print("6. 📀 Mostrar uso de memoria")
    print("7. 🛉 Recolectar bloques huérfanos")
    print("8. 🔙 Retroceder versión")
    print("9. 🔜 Avanzar versión")
    print("10. 🔁 Cambiar a versión específica")
    print("11. 🔒 Cerrar archivo")
    print("12. 🧹 Optimizar bloques manualmente")
    print("13. 🚪 Salir del sistema")
    print("14. 🧪 Mostrar File Descriptor actual")
    print("=" * 60)

while True:
    mostrar_menu()
    opcion = input("Seleccione una opción: ").strip()

    try:
        if opcion == "1":
            ruta = input("📁 Ingrese el nombre del nuevo archivo: ").strip()
            gestor = GestorArchivos(ruta)
            gestor.create()

        elif opcion == "2":
            ruta = input("📂 Ingrese el nombre del archivo existente: ").strip()
            gestor = GestorArchivos(ruta)
            fd = gestor.open()
            if fd is not None:
                print(f"🧪 File Descriptor abierto: {fd}")

        elif opcion == "3":
            if gestor:
                gestor.read()
            else:
                print("⚠️ No hay archivo abierto.")

        elif opcion == "4":
            if gestor:
                data = input("✏️ Ingrese el contenido a escribir: ")
                gestor.write(data)
            else:
                print("⚠️ No hay archivo abierto.")

        elif opcion == "5":
            if gestor:
                gestor.listar_versiones()
                gestor.mostrar_cadena_bloques()
            else:
                print("⚠️ No hay archivo abierto.")

        elif opcion == "6":
            if gestor:
                gestor.mostrar_uso_memoria()
            else:
                print("⚠️ No hay archivo abierto.")

        elif opcion == "7":
            if gestor:
                gestor.recolectar_bloques_huerfanos()
            else:
                print("⚠️ No hay archivo abierto.")

        elif opcion == "8":
            if gestor:
                gestor.rollback_backward()
            else:
                print("⚠️ No hay archivo abierto.")

        elif opcion == "9":
            if gestor:
                gestor.rollback_forward()
            else:
                print("⚠️ No hay archivo abierto.")

        elif opcion == "10":
            if gestor:
                version_id = input("🔁 Ingrese el ID de la versión a la que desea cambiar (ej: v0, v1, v2): ").strip()
                gestor.cambiar_a_version(version_id)
            else:
                print("⚠️ No hay archivo abierto.")

        elif opcion == "11":
            if gestor:
                gestor.close()
                gestor = None
            else:
                print("⚠️ No hay archivo abierto.")

        elif opcion == "12":
            if gestor:
                gestor.optimizar_bloques()
            else:
                print("⚠️ No hay archivo abierto.")

        elif opcion == "13":
            if gestor:
                gestor.close()
            print("👋 Saliendo del sistema. ¡Hasta luego!")
            break

        elif opcion == "14":
            if gestor and hasattr(gestor, 'fd'):
                if gestor.fd is not None:
                    print(f"🧪 File Descriptor activo: {gestor.fd}")
                else:
                    print("❗ No hay descriptor abierto actualmente.")
            else:
                print("⚠️ No hay archivo abierto.")

        else:
            print("❌ Opción no válida. Intente nuevamente.")

    except Exception as e:
        print(f"🚨 Error inesperado: {e}")
