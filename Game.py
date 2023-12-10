import tensorflow as tf
import Deck
import Player
import Hand
import random
import pygad
import time
import pygad.gann
import pygad.nn
import pickle

class HumanGame:
    def __init__(self):
        self.players = [Player.Player(0), Player.Player(1)]
        self.bigBlind = 0 if random.randint(0,1) == 0 else 1

    def run(self):
        while self.players[0].chips.getTotal() > 0 and self.players[1].chips.getTotal() > 0:
            self.deck = Deck.Deck()
            self.deck.shuffle()
            currentHand = Hand.Hand(self.players, self.deck, self.bigBlind)
            currentHand.startHand()
            self.bigBlind = int(not self.bigBlind)

class AIvsRandomGame():
    def __init__(self):
        self.bigBlind = 0 if random.randint(0,1) == 0 else 1
        num_inputs = 7
        output_size = 3  # Three actions: check, bet, fold
        hidden_layer_size = 10
        num_solutions = 10

        deck = Deck.Deck()
        hasht = {}
        i = 0
        for card in deck.cards:
            hasht[str(card)] = i
            i += 1
        hasht['Empty'] = i

        self.players = [Player.randomPlayer(0), Player.AIPlayer(1, hasht)]

        GANN_instance = pygad.gann.GANN(num_solutions=num_solutions,
                                        num_neurons_input=num_inputs,
                                        num_neurons_hidden_layers=[hidden_layer_size],
                                        num_neurons_output=output_size,
                                        hidden_activations=["relu"],
                                        output_activation="softmax")

        def fitness_func(ga_instance, solution, solution_idx):
            print("FITNESS FUNCTION")
            numOfHands = 0
            
            while (self.players[0].game_over == False and self.players[1].game_over == False and numOfHands < 200):
                self.deck = Deck.Deck()
                self.deck.shuffle()
                self.players[1].passParams(GANN_instance, solution_idx)
                currentHand = Hand.Hand(self.players, self.deck, self.bigBlind)
                currentHand.startHand()
                numOfHands += 1
                self.bigBlind = int(not self.bigBlind)
            print("This fitness function run has finished, player 1 finished w/ ",self.players[1].chips.getTotal())
            # I think we need to reset each players chips 
            fitness = self.players[1].chips.getTotal()
            self.players[0].resetChipsTo2000()
            self.players[1].resetChipsTo2000()
            return fitness
        
        def callback_generation(ga_instance):
            print("CALLBACK FUNCTION")
            population_matrices = pygad.gann.population_as_matrices(population_networks=GANN_instance.population_networks, population_vectors=ga_instance.population)
            GANN_instance.update_population_trained_weights(population_trained_weights=population_matrices)

            print(f"Generation = {ga_instance.generations_completed}")
            print(f"Fitness    = {ga_instance.best_solution()[1]}")


        population_vectors = pygad.gann.population_as_vectors(population_networks=GANN_instance.population_networks)

        initial_population = population_vectors.copy()

        num_parents_mating = 4

        num_generations = 2

        mutation_percent_genes = 35

        parent_selection_type = "sss"

        crossover_type = "single_point"

        mutation_type = "random"

        keep_parents = 1

        init_range_low = -1
        init_range_high = 1

        ga_instance = pygad.GA(num_generations=num_generations,
                            num_parents_mating=num_parents_mating,
                            initial_population=initial_population,
                            fitness_func=fitness_func,
                            mutation_percent_genes=mutation_percent_genes,
                            init_range_low=init_range_low,
                            init_range_high=init_range_high,
                            parent_selection_type=parent_selection_type,
                            crossover_type=crossover_type,
                            mutation_type=mutation_type,
                            keep_parents=keep_parents,
                            on_generation=callback_generation)

        ga_instance.run()
        #ga_instance.save('savedModel')
        print('done training')


class AIvsAIGame():
    def __init__(self):
        self.bigBlind = 0 if random.randint(0,1) == 0 else 1
        num_inputs = 7
        output_size = 3  # Three actions: check, bet, fold
        hidden_layer_size = 10
        num_solutions = 10
        self.num_solutions = num_solutions

        deck = Deck.Deck()
        hasht = {}
        i = 0
        for card in deck.cards:
            hasht[str(card)] = i
            i += 1
        hasht['Empty'] = i
        self.hasht = hasht

        self.players = [Player.AIPlayer(1, hasht), Player.AIPlayer(1, hasht)]

        GANN_instance = pygad.gann.GANN(num_solutions=num_solutions,
                                        num_neurons_input=num_inputs,
                                        num_neurons_hidden_layers=[hidden_layer_size],
                                        num_neurons_output=output_size,
                                        hidden_activations=["relu"],
                                        output_activation="softmax")
        
        self.GANN_instance = GANN_instance

        self.dictToStoreBattleScores={}
              

        population_vectors = pygad.gann.population_as_vectors(population_networks=GANN_instance.population_networks)

        initial_population = population_vectors.copy()

        num_parents_mating = 4

        num_generations = 20

        mutation_percent_genes = 35

        parent_selection_type = "sss"

        crossover_type = "single_point"

        mutation_type = "random"

        keep_parents = 1

        init_range_low = -1
        init_range_high = 1

        self.ga_instance = pygad.GA(num_generations=num_generations,
                            num_parents_mating=num_parents_mating,
                            initial_population=initial_population,
                            fitness_func=self.fitness_func,
                            mutation_percent_genes=mutation_percent_genes,
                            init_range_low=init_range_low,
                            init_range_high=init_range_high,
                            parent_selection_type=parent_selection_type,
                            crossover_type=crossover_type,
                            mutation_type=mutation_type,
                            keep_parents=keep_parents,
                            on_generation=self.callback_generation)
        
    def loadGAInstance(self, fileName):
        self.ga_instance = pygad.GA.load(filename=fileName)
    
    def train(self):

        self.ga_instance.run()

        

    def fitness_func(self, ga_instance, solution, solution_idx):
        #print("FITNESS FUNCTION")
        
        num_solutions = self.num_solutions
        GANN_instance = self.GANN_instance
        
        sumOfChipsPlayer1 =0
        
        for i in range(num_solutions):

            if i != solution_idx:
                
                if (solution_idx, i) in self.dictToStoreBattleScores:
                    sumOfChipsPlayer1 += self.dictToStoreBattleScores[(solution_idx,i)]
                    #print("saving work")

                else:
                   # print("doing work")
                    numOfHands=0
                    while (self.players[0].game_over == False and self.players[1].game_over == False and numOfHands < 200):
                        self.deck = Deck.Deck()
                        self.deck.shuffle()
                        self.players[0].passParams(GANN_instance, i)#pass i as the solution id to make it play the other individuals
                        self.players[1].passParams(GANN_instance, solution_idx)
                        currentHand = Hand.Hand(self.players, self.deck, self.bigBlind)
                        currentHand.startHand()
                        numOfHands += 1
                        self.bigBlind = int(not self.bigBlind)


                    sumOfChipsPlayer1 += self.players[1].chips.getTotal()
                    self.dictToStoreBattleScores[(solution_idx,i)]=sumOfChipsPlayer1
                    self.dictToStoreBattleScores[(i,solution_idx)]=self.players[0].chips.getTotal()

                    self.players[0].resetChipsTo2000()
                    self.players[1].resetChipsTo2000()
        
        return (sumOfChipsPlayer1/(num_solutions-1))
    

        
    def callback_generation(self,ga_instance):
        #("CALLBACK FUNCTION")

        GANN_instance = self.GANN_instance

        self.dictToStoreBattleScores.clear()
        population_matrices = pygad.gann.population_as_matrices(population_networks=GANN_instance.population_networks, population_vectors=ga_instance.population)
        GANN_instance.update_population_trained_weights(population_trained_weights=population_matrices)

        ga_instance.save('savedModel')
        print(f"Generation = {ga_instance.generations_completed}")
        #print(f"Fitness    = {ga_instance.best_solution()[1]}")

    def playVsRandom(self):
        self.players = [Player.randomPlayer(0), Player.AIPlayer(1, self.hasht)]

        for solution_idx in range(self.num_solutions):
            numOfHands =0
            while (self.players[0].game_over == False and self.players[1].game_over == False and numOfHands < 200):
                self.deck = Deck.Deck()
                self.deck.shuffle()
                self.players[1].passParams(self.GANN_instance, solution_idx)
                currentHand = Hand.Hand(self.players, self.deck, self.bigBlind)
                currentHand.startHand()
                numOfHands += 1
                self.bigBlind = int(not self.bigBlind)

            print("This test against the random player has finshed, AI player finished w/ ",self.players[1].chips.getTotal())









hi = AIvsAIGame()
hi.train()
hi.playVsRandom()
# hi = HumanGame()
# hi.run()
