def main():
    """Función principal para el CLI"""
    from .metodos_lineales import eliminacion_gauss
    import numpy as np
    
    A = np.array([[2.0, 1.0], [1.0, 3.0]])
    b = np.array([4.0, 5.0])
    print("Solución:", eliminacion_gauss(A, b))
    
if __name__ == "__main__":
    main()