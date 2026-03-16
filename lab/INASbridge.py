# INASbridge.py       -Connecting INAS MODULES-


import math
from collections import defaultdict

import sys
import os

# Add the parent directory to sys.path to import inas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from inas import INAS
except ImportError:
    print("Error: 'inas.py' not found in the parent directory.")
    sys.exit(1)

class INASBridge:
    """
    INAS Bridge: Facilitates communication, synchronization, and consensus
    between two INAS instances.
    """

    def __init__(self, agent_A, agent_B, learning_rate=0.1):
        """
        Initialize the bridge between two agents.
        
        Args:
            agent_A (INAS): The first INAS instance.
            agent_B (INAS): The second INAS instance.
            learning_rate (float): How fast they converge to each other's state (0.0 to 1.0).
        """
        self.A = agent_A
        self.B = agent_B
        self.eta_bridge = learning_rate

    def get_total_mass(self, agent):
        """Helper: Calculate total knowledge mass of an agent for weighting."""
        return sum(agent.K.values()) if agent.K else 1.0

    def cross_pollinate(self):
        """
        Algorithm 1: Cross-Pollination
        Agents exchange their 'strongest' concept (highest weight in K) 
        to broaden the other's horizon.
        """
        # A -> B
        if self.A.K:
            best_concept_A = max(self.A.K, key=self.A.K.get)
            # B ingests A's best idea
            self.B.K = self.B.update_concept_weights(self.B.K, best_concept_A)

        # B -> A
        if self.B.K:
            best_concept_B = max(self.B.K, key=self.B.K.get)
            # A ingests B's best idea
            self.A.K = self.A.update_concept_weights(self.A.K, best_concept_B)
            
        print(f"  [Bridge] Cross-pollinated top concepts.")

    def synchronize_weights(self, source, target):
        """
        Algorithm 2: Weighted Consensus Merge
        Merges Concept Weights (K) and Hypotheses (H) based on knowledge mass.
        The agent with more knowledge (higher total mass) has more influence.
        """
        mass_s = self.get_total_mass(source)
        mass_t = self.get_total_mass(target)
        total_mass = mass_s + mass_t

        # 1. Merge Concept Weights (K)
        all_keys = set(source.K.keys()) | set(target.K.keys())
        for k in all_keys:
            val_s = source.K.get(k, 0.0)
            val_t = target.K.get(k, 0.0)
            
            # Weighted Average
            new_val = (val_s * mass_s + val_t * mass_t) / total_mass
            
            target.K[k] = new_val

        # 2. Merge Hypotheses (H)
        all_keys = set(source.H.keys()) | set(target.H.keys())
        for k in all_keys:
            val_s = source.H.get(k, 0.0)
            val_t = target.H.get(k, 0.0)
            
            new_val = (val_s * mass_s + val_t * mass_t) / total_mass
            target.H[k] = new_val

    def synchronize_graph(self, source, target):
        """
        Algorithm 3: Graph Union
        Merges the concept graph Topology (Phi).
        """
        V_s, E_s = source.Phi
        V_t, E_t = target.Phi

        # Union of Vertices
        new_V = V_s | V_t

        # Union of Edges
        all_edges = set(E_s.keys()) | set(E_t.keys())
        new_E = defaultdict(float)

        for edge in all_edges:
            w_s = E_s.get(edge, 0.0)
            w_t = E_t.get(edge, 0.0)
            # Average the edge weights
            new_E[edge] = (w_s + w_t) / 2.0

        target.Phi = (new_V, new_E)

    def align_internal_state(self):
        """
        Algorithm 4: Epistemic Alignment
        Aligns scalar values (Curiosity C, Performance J) to prevent 
        one agent from getting stuck in a local loop while the other explores.
        """
        # Align Curiosity (C)
        avg_C = (self.A.C + self.B.C) / 2.0
        self.A.C = avg_C
        self.B.C = avg_C

        # Align Goals (G) - If they disagree, default to Explore
        if self.A.G != self.B.G:
            self.A.G = "explore"
            self.B.G = "explore"

    def bridge_cycle(self):
        """
        Main Bridge Loop:
        1. Cross-Pollinate (Ideas)
        2. Synchronize Knowledge (Weights & Graphs)
        3. Align Internal State (Scalars)
        """
        print(f"--- BRIDGE CONNECTED (Step {self.A.t}) ---")
        
        # 1. Share Top Concepts
        self.cross_pollinate()

        # 2. Bidirectional Knowledge Synchronization
        # A learns from B
        self.synchronize_weights(self.B, self.A)
        self.synchronize_graph(self.B, self.A)
        
        # B learns from A
        self.synchronize_weights(self.A, self.B)
        self.synchronize_graph(self.A, self.B)

        # 3. Align Internal Parameters
        self.align_internal_state()
        
        print("  [Bridge] Synchronization Complete.")

# ==========================================
# Simulation Driver
# ==========================================

if __name__ == "__main__":
    # 1. Initialize two separate INAS instances
    # Agent A will learn about 'Fruits'
    # Agent B will learn about 'Tech'
    
    print("Initializing Agent A (Fruit Expert) and Agent B (Tech Expert)...")
    agent_A = INAS(eta=0.1, alpha=0.9)
    agent_B = INAS(eta=0.1, alpha=0.9)

    # 2. Create the Bridge
    bridge = INASBridge(agent_A, agent_B)

    # 3. Separate Training Phase (No Bridge)
    print("\n--- PHASE 1: ISOLATED LEARNING ---")
    fruit_data = ["apple", "banana", "apple", "cherry"] * 3
    tech_data = ["server", "python", "server", "code"] * 3

    for idea in fruit_data:
        agent_A.step(idea)
    for idea in tech_data:
        agent_B.step(idea)

    print(f"Agent A Concepts: {list(agent_A.K.keys())}")
    print(f"Agent B Concepts: {list(agent_B.K.keys())}")

    # 4. Bridge Interaction Phase
    print("\n--- PHASE 2: BRIDGING ---")
    # Run one bridge cycle to merge knowledge
    bridge.bridge_cycle()

    print(f"\nPost-Bridge Agent A Concepts: {list(agent_A.K.keys())}")
    print(f"Post-Bridge Agent B Concepts: {list(agent_B.K.keys())}")

    # 5. Joint Training Phase (Bridge active every step)
    print("\n--- PHASE 3: JOINT EVOLUTION ---")
    mixed_data = [
        ("apple", "server"), 
        ("banana", "code"), 
        ("cherry", "python")
    ]

    for idea_a, idea_b in mixed_data:
        agent_A.step(idea_a)
        agent_B.step(idea_b)
        
        # Connect them every step
        if agent_A.t % 1 == 0:
            bridge.bridge_cycle()

    print("\nFinal State:")
    print(f"Agent A Knowledge Size: {len(agent_A.K)} | Perf: {agent_A.J:.3f}")
    print(f"Agent B Knowledge Size: {len(agent_B.K)} | Perf: {agent_B.J:.3f}")
    
    # Verify Graph Merge
    Va, Ea = agent_A.Phi
    Vb, Eb = agent_B.Phi
    print(f"Shared Graph Nodes A: {len(Va)}")
    print(f"Shared Graph Nodes B: {len(Vb)}")
