def init_menu_and_show_menu(opciones, titulo=None, texto_salida="Salir", menu_raiz=False):
    """
    Muestra un menú interactivo y devuelve el índice elegido.
    Cada opción puede ser:
    - ("Texto", función)
    - ("Texto", función, valor)
    - "Texto simple"
    
    Retorna:
    - 0 si se seleccionó la opción de salida
    - Índice (1-based) de la opción elegida
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
                return 0
            elif 1 <= eleccion <= len(opciones):
                item = opciones[eleccion - 1]
                if isinstance(item, tuple):
                    if len(item) == 3:
                        _, funcion, valor = item
                        funcion(valor)
                    elif len(item) == 2:
                        _, funcion = item
                        funcion()
                else:
                    print(f"Has seleccionado: {item}")
                return eleccion
            else:
                print("Opción inválida. Intenta de nuevo.")
        except ValueError:
            print("Entrada inválida. Ingresa un número.")