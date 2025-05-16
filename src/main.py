from kung import kung_max, kung_min
import matplotlib.pyplot as plt
import numpy as np
            
if __name__ == "__main__":
    while True:
        print("\n--- Menú Principal ---")
        print("1. Probar el algoritmo de Kung para calcular el conjunto de soluciones no dominadas")
        print("2. Probar el algoritmo NSGAII sobre el conjunto WFG")
        print("3. Salir")

        opcion = input("Ingrese la opción deseada: ")

        if opcion == "1":
            n_samples = 1000
            n_obj = 2

            P = [tuple(np.random.rand(n_obj) * 100) for _ in range(n_samples)]
            
            # para maximizar ordenamos P de forma DESCENDENTE de acuerdo al primer valor de cada tupla (la primera función objetivo)
            P_descendente = sorted(P, key=lambda x: x[0], reverse=True)

            # para minimizar se ordena P de forma ASCENDENTE de acuerdo al primer valor de cada tupla (la primera función objetivo)
            # P_ascendente = sorted(P, key=lambda x: x[0])
            
            pareto_front_max = kung_max(P_descendente)
            # pareto_front_min = kung_min(P_ascendente)
    
            print(f"\nFrente de Pareto encontrado con el algoritmo de Kung:")
            for p in pareto_front_max:
                print(p)
            # for p in pareto_front_min:
            #     print(p)

            P_arr = np.array(P)
            pf_arr = np.array(pareto_front_max)
            # pf_arr = np.array(pareto_front_min)

            plt.scatter(pf_arr[:, 0], pf_arr[:, 1], color='green', label="Frente de pareto", s=50)    
            plt.scatter(P_arr[:, 0], P_arr[:, 1], label="Puntos que no se encuentran en el frente de pareto", alpha=0.5)
            plt.xlabel("Objetivo 1")
            plt.ylabel("Objetivo 2")
            plt.title("Frente de Pareto")
            plt.legend()
            plt.grid(True)
            plt.show()
                
        elif opcion == "2":
            print("hola mundo")
            
        elif opcion == "3":
            print("Saliendo del programa ...")
            break

        else:
            print("No se reconoció la opción, ingresa una opción válida.")
