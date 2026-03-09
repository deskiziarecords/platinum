#  INAS (Intelligent Neural Abstraction System) 
#  Author: José Roberto Jiménez Cordero  - tijuanapaint@gmail.com  - @hipotermiah
#  Synth-fuse Labs (c) 2026 

import random
import math
from collections import defaultdict

class INAS:
    def __init__(self, eta=0.1, alpha=0.5, curiosity_thresh=0.5, mutation_window=10):
        """
        Initialize the INAS system state.
        
        Args:
            eta (float): Learning rate for weight updates.
            alpha (float): EMA decay factor for curiosity.
            curiosity_thresh (float): Threshold to switch between Explore/Compress.
            mutation_window (int): Steps to look back for stagnation detection.
        """
        # I. Core State Definition
        self.K = {}           # Concept weight map: {concept: weight}
        self.H = defaultdict(float) # Hypothesis strength map: {(c1, c2): strength}
        self.Phi = (set(), defaultdict(float)) # Concept Graph: (Vertices V, Edges E)
        self.G = "explore"    # Active research goal
        self.C = 1.0          # Curiosity scalar
        self.J = 0.0          # Performance functional
        self.t = 0            # Time step

        # Internal parameters
        self.eta = eta
        self.alpha = alpha
        self.curiosity_thresh = curiosity_thresh
        
        # For mutation tracking
        self.mutation_window = mutation_window
        self.J_history = [] 

    # ---------------------------------------------------------
    # II. High-Level Control Loop
    # ---------------------------------------------------------
    def step(self, idea):
        """
        Algorithm 0: INAS Main Loop
        """
        # 1. Ingest and Update Concepts
        self.K = self.update_concept_weights(self.K, idea)

        # 2. Generate Hypotheses (Relational structures)
        self.H = self.generate_hypotheses(self.K)

        # 3. Update the Concept Graph
        self.Phi = self.update_graph(self.Phi, self.H)

        # 4. Evolve Goal (Explore vs Compress)
        self.G = self.evolve_goal(self.K, self.Phi, self.C)

        # 5. Evaluate Performance
        self.J = self.evaluate_structure(self.K, self.H, self.Phi)
        self.J_history.append(self.J)
        if len(self.J_history) > self.mutation_window:
            self.J_history.pop(0)

        # 6. Learn (Refine hypotheses)
        self.H = self.learn(self.H)

        # 7. Structural Mutation (If stagnating)
        if self.mutation_condition():
            self.Phi, self.K = self.structural_mutation(self.Phi, self.K)

        # 8. Update Curiosity
        self.C = self.update_curiosity(self.C, idea)

        self.t += 1
        return self.get_state()

    # ---------------------------------------------------------
    # III. Knowledge Ingestion Algorithm
    # ---------------------------------------------------------
    def update_concept_weights(self, K, idea):
        """
        Algorithm 1: UpdateConceptWeights
        Reinforcement accumulation mechanism.
        K_{t+1}(c) = K_t(c) + eta * 1_{c=idea}
        """
        if idea not in K:
            K[idea] = random.uniform(0.01, 0.1) # Small random init
        else:
            K[idea] += self.eta
        
        # Optional: Normalize to prevent unbounded growth
        total_weight = sum(K.values())
        if total_weight > 0:
            for k in K:
                K[k] /= total_weight
                
        return K

    # ---------------------------------------------------------
    # IV. Hypothesis Generation Algorithm
    # ---------------------------------------------------------
    def generate_hypotheses(self, K):
        """
        Algorithm 2: GenerateHypotheses
        Proposes relational structures.
        H_ij = (K_i + K_j) / 2
        """
        concepts = list(K.keys())
        new_hypotheses = defaultdict(float)
        
        # Optimization: Don't sample O(n^2) if large, but for demo 
        # we sample a subset to simulate "combinatorial relation generator"
        # If n is small, we can do all pairs.
        n = len(concepts)
        sample_size = min(n * (n - 1) // 2, 50) # Cap at 50 pairs per step for efficiency
        
        pairs = []
        if n >= 2:
            # Generate pairs
            for i in range(n):
                for j in range(i + 1, n):
                    pairs.append((concepts[i], concepts[j]))
            
            # Sample if too many
            if len(pairs) > sample_size:
                pairs = random.sample(pairs, sample_size)

        for c_i, c_j in pairs:
            # Calculate strength based on weights
            strength = (K[c_i] + K[j]) / 2.0
            
            # Update persistent H map (or add to buffer)
            # Here we update the persistent H directly for simplicity
            key = tuple(sorted((c_i, c_j)))
            new_hypotheses[key] = strength
            
        # Merge new hypotheses into existing H (persistence)
        for k, v in new_hypotheses.items():
            self.H[k] = v 

        return self.H

    # ---------------------------------------------------------
    # V. Graph Update Algorithm
    # ---------------------------------------------------------
    def update_graph(self, Phi, H):
        """
        Algorithm 3: UpdateGraph
        Maintain evolving concept network.
        """
        V, E = Phi
        
        # Ensure all nodes in hypotheses are in graph
        for (c1, c2) in H:
            V.add(c1)
            V.add(c2)
            
            # Update or Add edge
            # We take the strength from H as the edge weight
            if (c1, c2) in E or (c2, c1) in E:
                # Update logic (simple moving average or replace)
                # Here we replace with latest hypothesis strength
                E[(c1, c2)] = H[(c1, c2)]
            else:
                E[(c1, c2)] = H[(c1, c2)]
                
        return (V, E)

    # ---------------------------------------------------------
    # VI. Goal Field Evolution
    # ---------------------------------------------------------
    def evolve_goal(self, K, Phi, C):
        """
        Algorithm 4: EvolveGoal
        Decide epistemic strategy based on Curiosity.
        """
        if C > self.curiosity_thresh:
            return "explore"
        else:
            return "compress"

    # ---------------------------------------------------------
    # VII. Evaluation Functional
    # ---------------------------------------------------------
    def evaluate_structure(self, K, H, Phi):
        """
        Algorithm 5: EvaluateStructure
        Measures epistemic performance.
        """
        V, E = Phi
        
        # Compression Score: Cs = 1 / (1 + |E|)
        # Encourages parsimony (fewer edges)
        Cs = 1.0 / (1.0 + len(E))
        
        # Predictive Coherence: Ps = Sum(H_ij) / (1 + |H|)
        # Encourages rich, strong relationships
        sum_h = sum(H.values())
        Ps = sum_h / (1.0 + len(H))
        
        # Total Performance
        J = Cs + Ps
        return J

    # ---------------------------------------------------------
    # VIII. Learning Algorithm
    # ---------------------------------------------------------
    def learn(self, H):
        """
        Algorithm 6: Learn
        Refine hypothesis strengths with noise/gradient.
        """
        keys = list(H.keys())
        for k in keys:
            # Add Gaussian noise simulated by random uniform for simplicity 
            # or small gradient step. Here: noise as per prompt.
            noise = random.uniform(-0.01, 0.01)
            H[k] += self.eta * noise
            
            # Keep strictly positive
            if H[k] < 0: H[k] = 0
            
        return H

    # ---------------------------------------------------------
    # IX. Structural Mutation Algorithm
    # ---------------------------------------------------------
    def mutation_condition(self):
        """
        Check if performance J is stagnating.
        """
        if len(self.J_history) < self.mutation_window:
            return False
        
        # Simple check: if standard deviation is very low
        arr = self.J_history
        mean_j = sum(arr) / len(arr)
        variance = sum((x - mean_j) ** 2 for x in arr) / len(arr)
        
        # Threshold for stagnation
        return variance < 0.001

    def structural_mutation(self, Phi, K):
        """
        Algorithm 7: StructuralMutation
        Hierarchical abstraction.
        """
        V, E = Phi
        
        # Create new meta-concept
        meta_name = f"Meta_{self.t}"
        K[meta_name] = 0.5 # Assign initial weight
        V.add(meta_name)
        
        # Identify high-strength clusters (Top 3 nodes by weight)
        sorted_concepts = sorted(K.items(), key=lambda x: x[1], reverse=True)
        top_nodes = [c[0] for c in sorted_concepts[:3]]
        
        # Connect meta-concept to cluster nodes
        for node in top_nodes:
            if node != meta_name:
                E[(meta_name, node)] = 0.5 # Strong initial connection
        
        # Increase complexity counter (implied by adding nodes)
        print(f"[Mutation] Created abstraction: {meta_name}")
        
        return (V, K)

    # ---------------------------------------------------------
    # X. Curiosity Update
    # ---------------------------------------------------------
    def update_curiosity(self, C, idea):
        """
        Algorithm 8: UpdateCuriosity
        C_{t+1} = alpha * C_t + (1-alpha) * Novelty
        """
        # Novelty defined as 1 if new concept, 0 otherwise
        novelty = 0.0 if idea in self.K else 1.0
        
        new_C = (self.alpha * C) + ((1 - self.alpha) * novelty)
        return new_C

    # ---------------------------------------------------------
    # Utilities
    # ---------------------------------------------------------
    def get_state(self):
        V, E = self.Phi
        return {
            "time": self.t,
            "concepts": len(self.K),
            "hypotheses": len(self.H),
            "edges": len(E),
            "goal": self.G,
            "curiosity": round(self.C, 3),
            "performance": round(self.J, 3)
        }

# ==========================================
# Simulation Driver
# ==========================================

if __name__ == "__main__":
    # Initialize System
    inas = INAS(eta=0.05, alpha=0.9, curiosity_thresh=0.3)
    
    # Simulate a stream of ideas/concepts
    # 'A', 'B' are common, 'Z' is rare, 'New' appears late
    data_stream = [
        "apple", "banana", "apple", "banana", "cherry", 
        "apple", "banana", "date", "elderberry", "fig",
        "apple", "banana", "apple", "banana", "new_concept",
        "new_concept", "new_concept", "apple", "banana", "grape"
    ] * 5 # Repeat to allow mutation to trigger

    print(f"{'T':<4} | {'Concepts':<8} | {'Edges':<5} | {'Goal':<10} | {'Cur':<5} | {'Perf (J)':<8}")
    print("-" * 55)

    for idea in data_stream:
        state = inas.step(idea)
        
        # Print status every 5 steps or on mutation
        if state['time'] % 5 == 0:
            print(f"{state['time']:<4} | {state['concepts']:<8} | {state['edges']:<5} | "
                  f"{state['goal']:<10} | {state['curiosity']:<5} | {state['performance']:<8}")

    print("\nFinal Graph Sample (Nodes & Edge Weights):")
    V, E = inas.Phi
    print(f"Total Nodes: {len(V)}")
    # Show some edges
    for i, (u, v) in enumerate(list(E.keys())[:5]):
        print(f"  {u} -- {v} : {E[(u,v)]:.3f}")
