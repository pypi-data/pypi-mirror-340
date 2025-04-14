import math
#-----------------------------BISECCION/BISECTION-------------------------------------------------------------------
def bisection(f, a, b, tol=0.01, max_iter=1000):
    """
    Encuentra una raíz de la ecuación f(x) = 0 en el intervalo [a, b] usando el método de bisección.

    El método requiere que f(a) y f(b) tengan signos opuestos, garantizando la existencia de al menos una raíz
    en el intervalo dado. La aproximación se mejora iterativamente hasta que el error estimado es menor a la 
    tolerancia especificada o se alcanza el número máximo de iteraciones.

    Args:
        f (function): Función continua f(x) a evaluar.
        a (float): Extremo izquierdo del intervalo.
        b (float): Extremo derecho del intervalo.
        tol (float, optional): Tolerancia aceptada para el error relativo. Default es 0.01.
        max_iter (int, optional): Máximo número de iteraciones permitidas. Default es 1000.

    Returns:
        tuple:
            float: Raíz aproximada de f(x) = 0.
            int: Número de iteraciones realizadas.

    Raises:
        ValueError: Si f(a) y f(b) no tienen signos opuestos (no garantizan cambio de signo).
    """
    
    if(f(a)*f(b)) >= 0:
        raise ValueError("Error, la funcion no cambia de signo en [a,b]")
    iteraciones = 0
    while (b-a)/2 > tol and iteraciones < max_iter:  #calcula el error y verifica que sea mayor a la tolernacia y que no supere el maximo de iteraciones
        c = (a + b) / 2  #punto medio
        if (f(c) == 0):
            return c, iteraciones
        elif f(a) * f(c) < 0:
            b = c #la raiz se encuentra entre a y c
        else:
            a = c #la raiz se encuentra entre c y b
        iteraciones += 1

    return (a + b) / 2, iteraciones
