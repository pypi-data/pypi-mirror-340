"""
File to manage the CMA-ES optimization process for the SVDC controller
"""

import cma, os, multiprocessing, time, csv
# This line is for managing the multi-threading in Mac. 
multiprocessing.set_start_method('spawn', force=True)
from SVDC.SVDC import SVDC
import numpy as np

def evaluate_solution(args):
    """
    Helper function for multiprocessing.
    It will call the fitness function with the given solution and the input.
    Args:
        args: A tuple (solution, SVDC_input, output_size, layer_count, fitness_function)
    Returns:
        (fitness, output) for the given solution.
    """
    solution, SVDC_input, output_size, layer_count, fitness_function = args
    controller = SVDC(solution,
                      output_size=output_size,
                      layer_count=layer_count,
                      sensor_input_sample=SVDC_input,
                      verbose=False)
    fitness = fitness_function(controller, SVDC_input)
    output = controller.forward(SVDC_input)
    return fitness, output

class SVDC_CMA:
    """
    High-level class that uses the CMA-ES algorithm to evolve weights for the SVDC controller.
    Enhanced logging: logs all candidate solutions per generation with their fitness.
    """
    def __init__(self,
                 starting_weights,
                 output_size,
                 SVDC_layers,
                 fitness_function,
                 generations,
                 log_folder,
                 sigma=0.5,
                 population_size=None,
                 verbose=False,
                 plot_solution = False,
                 log_fitness = True,
                 log_parameters = True):
        """Setup the CMA-ES optimizer for the SVDC controller."""
        self.starting_weights = np.array(starting_weights, dtype=np.float32)
        self.output_size = output_size
        self.SVDC_layer_count = SVDC_layers
        self.fitness_function = fitness_function
        self.generations = generations
        self.sigma = sigma
        self.verbose = verbose
        self.log_folder = log_folder
        self.plot_solution = plot_solution
        self.log_fitness = log_fitness
        self.log_parameter = log_parameters

        opts = {'verb_log': 0, 'popsize': population_size} if population_size else {'verb_log': 0}
        self.es = cma.CMAEvolutionStrategy(self.starting_weights, self.sigma, opts)
        
        if self.plot_solution or self.log_fitness or self.log_parameter:
            self._init_logging(self.log_folder)
    
    def log_parameters(self):
        """Log the parameters used in this run to a text file in the log directory."""
        param_file = os.path.join(self.log_folder, f"{self.timestamp}_RunParameters.txt")
        
        with open(param_file, "w") as file:
            file.write("SVDCCMAESOptimizer Run Parameters\n")
            file.write("="*40 + "\n")
            file.write(f"Output Size: {self.output_size}\n")
            file.write(f"SVDC Layer Count: {self.SVDC_layer_count}\n")
            file.write(f"Generations: {self.generations}\n")
            file.write(f"Sigma: {self.sigma}\n")
            file.write(f"Population Size: {self.es.popsize}\n")
            file.write(f"Weight Dimensions: {self.starting_weights.shape}\n")
            file.write(f"Fitness Function: {self.fitness_function.__name__}\n")

    def _init_logging(self, base_folder):
        """Setup the logging directory and files"""
        # Setup and create the base folder
        base_folder = os.path.abspath(base_folder)
        os.makedirs(base_folder, exist_ok=True)

        # This is the run-id of this specific run
        self.timestamp = os.path.basename(os.path.normpath(base_folder))

        if self.log_fitness:
            # .csv file for saving the scores
            self.log_file = os.path.join(base_folder, f"{self.timestamp}_FitnessScores.csv")
            with open(self.log_file, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Generation", "Solution_Index", "Positive_Fitness"])
        
        if self.log_parameter:
            self.log_parameters()

    def log_generation(self, generation, fitnesses):
        """
        Logs all candidate solutions for a generation.
        Each candidate's positive fitness (-fitness) is recorded.
        """
        with open(self.log_file, "a", newline="") as file:
            writer = csv.writer(file)
            for idx, fitness in enumerate(fitnesses):
                pos_fitness = -fitness  # Flip the fitness
                writer.writerow([generation, idx+1, pos_fitness])

    def save_best_individual(self, best_solution):
        """
        Saves the best solution to a .npy file in the specified directory.
        """
        os.makedirs(self.log_folder, exist_ok=True)
        file_path = os.path.join(self.log_folder, "best_individual.npy")
        np.save(file_path, best_solution)
        return file_path
    
    def train(self, SVDC_input):
        """Main training loop for the CMA-ES algorithm."""
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())  # Use all available CPU cores
        
        # For each generation
        for generation in range(1, self.generations + 1):
            # Evaluate the solutions
            solutions = self.es.ask()
            args_list = [(solution, SVDC_input, self.output_size, self.SVDC_layer_count, self.fitness_function)
                        for solution in solutions]
            results = pool.map(evaluate_solution, args_list)

            fitnesses = []
            for _, (fitness, _) in enumerate(results):
                fitnesses.append(fitness)

            self.es.tell(solutions, fitnesses)

            if self.log_fitness:
                self.log_generation(generation, fitnesses)

            if self.verbose:
                gen_best_fitness = min(fitnesses)
                print(f"Generation {generation}: Best fitness = {-gen_best_fitness:.2f}")

        pool.close()
        pool.join()

        result = self.es.result
        best_solution = result[0]
        best_fitness = result[1]

        print(f"Best fitness from CMA-ES: {-best_fitness:.4f}")

        best_path = self.save_best_individual(best_solution)
        print(f"Best individual saved at: {best_path}")

        return {
            "best_solution": best_solution,
            "best_fitness": best_fitness
        }