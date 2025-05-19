from kung import kung_max, kung_min
from nsgaii import random_population, crossover, mutation, local_search, evaluation, crowding_calculation, remove_using_crowding, pareto_front_finding, selection
from pymoo.problems import get_problem
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
            
if __name__ == "__main__":
    while True:
        print("\n--- Menú Principal ---")
        print("1. Probar el algoritmo de Kung para calcular el conjunto de soluciones no dominadas")
        print("2. Probar el algoritmo NSGAII")
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
            while True:
                print("\n--- Conjuntos de pruebas ---")
                print("1. ZDT")
                print("2. DTLZ")
                print("3. WFG")
                print("4. Regresar al menú principal")
                
                opcion = input("Ingrese la opción deseada: ")

                if opcion == "1":
                    while True:                    
                        print("\n--- Problemas del conjunto ZDT ---")
                        print("1. ZDT1")
                        print("2. ZDT2")
                        print("3. ZDT3")
                        print("4. ZDT4")
                        print("5. ZDT5")
                        print("6. ZDT6")

                        opcion = input("Ingrese la opción deseada: ")

                        if opcion == "1":
                            problem = get_problem("zdt1")
                        elif opcion == "2":
                            problem = get_problem("zdt2")
                        elif opcion == "3":
                            problem = get_problem("zdt3")
                        elif opcion == "4":
                            problem = get_problem("zdt4")
                        elif opcion == "5":
                            problem = get_problem("zdt5")
                        elif opcion == "6":
                            problem = get_problem("zdt6")
                        else:
                            print("Opción inválida.")
                            continue
                            
                        # Parámetros
                        nv = problem.n_var
                        lb = problem.xl
                        ub = problem.xu
                        pop_size = 100
                        rate_crossover = 30
                        rate_mutation = 20
                        rate_local_search = 30
                        step_size = 0.1
                        pop = random_population(nv,pop_size,lb,ub)

                        for i in range(150):
                            offspring_from_crossover = crossover(pop,rate_crossover)
                            offspring_from_mutation = mutation(pop,rate_mutation)
                            offspring_from_local_search = local_search(pop, rate_local_search, step_size, problem)
                            combined = np.vstack((pop, offspring_from_crossover, offspring_from_mutation, offspring_from_local_search))
                            combined_fitness = evaluation(combined, problem)
                            pop, _ = selection(combined, combined_fitness, pop_size)
                    
                        fitness_values     = evaluation(pop, problem)
                        pareto_mask        = pareto_front_finding(fitness_values, np.arange(pop.shape[0]))
                        pop_optimal        = pop[pareto_mask, :]
                        fitness_optimal    = fitness_values[pareto_mask]

                        print("_________________")
                        print("Optimal solutions:")
                        print("  " + "    ".join([f"x{i+1}" for i in range(nv)]))
                        for sol in pop_optimal:
                            print(sol)
                        print("______________")
                        print("Fitness values:")
                        print("objective 1  objective 2")
                        print(fitness_optimal)

                        plt.scatter(fitness_optimal[:, 0], fitness_optimal[:, 1])
                        plt.xlabel('Objective 1')
                        plt.ylabel('Objective 2')
                        plt.show()
                    
                        break
                        
                elif opcion == "2":
                    while True:                    
                        print("\n--- Problemas del conjunto DTLZ ---")
                        print("1. DTLZ1")
                        print("2. DTLZ2")
                        print("3. DTLZ3")
                        print("4. DTLZ4")
                        print("5. DTLZ5")
                        print("6. DTLZ6")
                        print("7. DTLZ7")

                        opcion = input("Ingrese la opción deseada: ")
                
                        if opcion == "1":
                            problem = get_problem("dtlz1", n_var=7, n_obj=3)
                        elif opcion == "2":
                            problem = get_problem("dtlz2", n_var=12, n_obj=3)
                        elif opcion == "3":
                            problem = get_problem("dtlz3", n_var=12, n_obj=3)
                        elif opcion == "4":
                            problem = get_problem("dtlz4", n_var=12, n_obj=3)
                        elif opcion == "5":
                            problem = get_problem("dtlz5", n_var=12, n_obj=3)
                        elif opcion == "6":
                            problem = get_problem("dtlz6", n_var=12, n_obj=3)
                        elif opcion == "7":
                            problem = get_problem("dtlz7", n_var=22, n_obj=3)
                        else:
                            print("Opción inválida.")
                            continue                                

                        nv = problem.n_var
                        lb = problem.xl
                        ub = problem.xu
                        pop_size = 100
                        rate_crossover = 30
                        rate_mutation = 20
                        rate_local_search = 30
                        step_size = 0.1
                        pop = random_population(nv, pop_size, lb, ub)

                        for i in range(150):
                            offspring_from_crossover = crossover(pop, rate_crossover)
                            offspring_from_mutation = mutation(pop, rate_mutation)
                            offspring_from_local_search = local_search(pop, rate_local_search, step_size, problem)
                            combined = np.vstack((pop, offspring_from_crossover, offspring_from_mutation, offspring_from_local_search))
                            combined_fitness = evaluation(combined, problem)
                            pop, _ = selection(combined, combined_fitness, pop_size)

                        fitness_values = evaluation(pop, problem)
                        pareto_mask = pareto_front_finding(fitness_values, np.arange(pop.shape[0]))
                        pop_optimal = pop[pareto_mask, :]
                        fitness_optimal = fitness_values[pareto_mask]

                        print("_________________")
                        print("Optimal solutions:")
                        print("  " + "    ".join([f"x{i+1}" for i in range(nv)]))
                        for sol in pop_optimal:
                            print(sol)
                        print("______________")
                        print("Fitness values:")
                        print("  " + "    ".join([f"objective {i+1}" for i in range(problem.n_obj)]))
                        print(fitness_optimal)

                        # Gráfica: sólo funciona bien si son 2 o 3 objetivos
                        if problem.n_obj == 2:
                            plt.scatter(fitness_optimal[:, 0], fitness_optimal[:, 1])
                            plt.xlabel('Objective 1')
                            plt.ylabel('Objective 2')
                            plt.show()
                        elif problem.n_obj == 3:
                            fig = plt.figure()
                            ax = fig.add_subplot(111, projection='3d')
                            ax.scatter(fitness_optimal[:, 0], fitness_optimal[:, 1], fitness_optimal[:, 2])
                            ax.set_xlabel('Objective 1')
                            ax.set_ylabel('Objective 2')
                            ax.set_zlabel('Objective 3')
                            plt.show()
                            
                        break

                elif opcion == "3":
                    while True:
                        print("\n--- Problemas del conjunto WFG ---")
                        print("1. WFG1")
                        print("2. WFG2")
                        print("3. WFG3")
                        print("4. WFG4")
                        print("5. WFG5")
                        print("6. WFG6")
                        print("7. WFG7")
                        print("8. WFG8")
                        print("9. WFG9")

                        opcion = input("Ingrese la opción deseada: ")

                        if opcion == "1":
                            problem = get_problem("wfg1", n_var=10, n_obj=3)
                        elif opcion == "2":
                            problem = get_problem("wfg2", n_var=24, n_obj=3)
                        elif opcion == "3":
                            problem = get_problem("wfg3", n_var=24, n_obj=3)
                        elif opcion == "4":
                            problem = get_problem("wfg4", n_var=24, n_obj=3)
                        elif opcion == "5":
                            problem = get_problem("wfg5", n_var=24, n_obj=3)
                        elif opcion == "6":
                            problem = get_problem("wfg6", n_var=24, n_obj=3)
                        elif opcion == "7":
                            problem = get_problem("wfg7", n_var=24, n_obj=3)
                        elif opcion == "8":
                            problem = get_problem("wfg8", n_var=24, n_obj=3)
                        elif opcion == "9":
                            problem = get_problem("wfg9", n_var=24, n_obj=3)
                        else:
                            print("Opción inválida.")
                            continue                                
                
                        nv = problem.n_var
                        lb = problem.xl
                        ub = problem.xu
                        pop_size = 100
                        rate_crossover = 30
                        rate_mutation = 20
                        rate_local_search = 30
                        step_size = 0.1
                        pop = random_population(nv, pop_size, lb, ub)

                        for i in range(150):
                            offspring_from_crossover = crossover(pop, rate_crossover)
                            offspring_from_mutation = mutation(pop, rate_mutation)
                            offspring_from_local_search = local_search(pop, rate_local_search, step_size, problem)
                            combined = np.vstack((pop, offspring_from_crossover, offspring_from_mutation, offspring_from_local_search))
                            combined_fitness = evaluation(combined, problem)
                            pop, _ = selection(combined, combined_fitness, pop_size)

                        fitness_values = evaluation(pop, problem)
                        pareto_mask = pareto_front_finding(fitness_values, np.arange(pop.shape[0]))
                        pop_optimal = pop[pareto_mask, :]
                        fitness_optimal = fitness_values[pareto_mask]

                        print("_________________")
                        print("Optimal solutions:")
                        print("  " + "    ".join([f"x{i+1}" for i in range(nv)]))
                        for sol in pop_optimal:
                            print(sol)
                        print("______________")
                        print("Fitness values:")
                        print("  " + "    ".join([f"objective {i+1}" for i in range(problem.n_obj)]))
                        print(fitness_optimal)

                        if problem.n_obj == 2:
                            plt.scatter(fitness_optimal[:, 0], fitness_optimal[:, 1])
                            plt.xlabel('Objective 1')
                            plt.ylabel('Objective 2')
                            plt.show()
                        elif problem.n_obj == 3:
                            fig = plt.figure()
                            ax = fig.add_subplot(111, projection='3d')
                            ax.scatter(fitness_optimal[:, 0], fitness_optimal[:, 1], fitness_optimal[:, 2])
                            ax.set_xlabel('Objective 1')
                            ax.set_ylabel('Objective 2')
                            ax.set_zlabel('Objective 3')
                            plt.show()
                            
                            break
                        else:
                            print("Opción inválida.")
                    
                elif opcion == "4":
                    print("Regresando el menú principal ...")
                    break        
                else:
                    print("No se reconoció la opción, ingresa una opción válida.")            
                        
        elif opcion == "3":
            print("Saliendo del programa ...")
            break

        else:
            print("No se reconoció la opción, ingresa una opción válida.")
