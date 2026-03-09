## Explanation of the Code Structure (INAS)

   ### State Representation: 
-         K (Concepts): A dictionary mapping concept names to weights.
 -        H (Hypotheses): A dictionary mapping tuples of concept pairs to their calculated strength.
  -       Phi (Graph): A tuple containing a set of Vertices (V)   and a dictionary of Edges (E)  
  -       G, C, J: Scalar values for Goal, Curiosity, and Performance.
          

   ### The Main Loop (step method): 
         This orchestrates the 8 algorithms in sequence. It handles the flow of data from Ingestion → 
         Mutation.
          

    #### **Key Algorithms Implemented:**
    
         update_concept_weights: Implements the reinforcement rule. If a concept is seen, its weight increases. It normalizes to prevent explosion.
         generate_hypotheses: Samples pairs of concepts and calculates their average weight. It limits samples per step (to 50) to ensure the script runs efficiently, though the logic supports full combinatorial generation.
         evaluate_structure: Calculates J 
         using the specific formulas provided: Cs​=1+∣E∣1​ 
         and Ps​=1+∣H∣∑H​ 
        .
         structural_mutation: Monitors the variance of the performance score J 
        . If it drops below a threshold (stagnation), it generates a "Meta" node and connects it to the strongest existing concepts, creating hierarchical abstraction.
          

   #### Simulation: 
         The driver code feeds a repetitive list of strings. You will see Curiosity drop as "apple" and "banana" become frequent. Eventually, the system switches Goal from "explore" to "compress". If the performance stabilizes (stagnates), a mutation triggers, creating a Meta_X node.
          

      
