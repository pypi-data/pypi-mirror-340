def init_menu_and_show_menu(opciones, titulo=None, texto_salida="Salir", menu_raiz=False):
    """
    Muestra un menú interactivo con funciones asociadas.
    La opción 0 es siempre una acción especial ('Salir' o 'Volver').

    :param opciones: Lista de tuplas (texto, función) o strings (sin función).
    :param titulo: Título del menú.
    :param texto_salida: Texto para la opción 0 (por ejemplo, 'Salir' o 'Volver').
    :param menu_raiz: Si es el menú principal (True), al salir puede cerrar la app.
    """
    while True:
        print("\n" + "=" * 40)
        if titulo:
            print(f"{titulo}")
            print("-" * len(titulo))
        print(f"0. {texto_salida}")
        
        for i, item in enumerate(opciones, 1):
            texto = item[0] if isinstance(item, tuple) else str(item)
            print(f"{i}. {texto}")

        try:
            eleccion = int(input("Opción: "))
            if eleccion == 0:
                if menu_raiz:
                    print("Saliendo del programa. ¡Hasta luego!")
                else:
                    print(f"{texto_salida} al menú anterior...")
                break
            elif 1 <= eleccion <= len(opciones):
                item = opciones[eleccion - 1]
                if isinstance(item, tuple) and callable(item[1]):
                    item[1]() 
                else:
                    print(f"Has seleccionado: {item}")
            else:
                print("Opción inválida. Intenta de nuevo.")
        except ValueError:
            print("Entrada inválida. Ingresa un número.")