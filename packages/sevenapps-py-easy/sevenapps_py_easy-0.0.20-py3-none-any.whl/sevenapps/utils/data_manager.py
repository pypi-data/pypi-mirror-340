def filtrar_objetos_por_condicion(arreglo, condicion):
    """
    Filtra un arreglo de objetos, devolviendo solo aquellos que cumplen con la condición dada.

    Ejemplo de condición:
        lambda x: x['edad'] > 18

    Argumentos:
        arreglo (list): Lista de objetos (diccionarios) a filtrar.
        condicion (función): Una función que recibe un objeto y devuelve True si cumple con la condición, False de lo contrario.

    Retorna:
        list: Lista de objetos que cumplen con la condición dada.
    """

    return list(filter(condicion, arreglo))

