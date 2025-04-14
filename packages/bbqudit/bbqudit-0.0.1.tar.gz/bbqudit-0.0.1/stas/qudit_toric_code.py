import numpy as np
from scipy import sparse
import matplotlib.pyplot as plt

class QuditToricCode:
    def __init__(self, L, d):
        """
        Initialize a qudit toric code with:
        L x L lattice size (L must be >= 2)
        d-dimensional qudits (d must be prime)
        
        The toric code has:
        - 2 * L^2 qudits (placed on edges)
        - 2 * L^2 stabilizer generators (L^2 vertex + L^2 plaquette)
        - Encodes 2 logical qudits
        """
        if L < 2:
            raise ValueError("Lattice size L must be at least 2")
        
        self.L = L
        self.d = d
        
        # Number of qudits (edges)
        self.n_qudits = 2 * L * L
        
        # Number of stabilizers
        self.n_vertices = L * L
        self.n_plaquettes = L * L
        self.n_stabilizers = self.n_vertices + self.n_plaquettes
        
        # Create the parity check matrices
        self._construct_parity_check_matrix()
        
        # Create the logical operator matrices
        self._construct_logical_operators()

    def get_logical_effect(self, X_error, Z_error):
        return np.array([np.dot(self.Z_logical_1, X_error) % self.d, np.dot(self.Z_logical_2, X_error) % self.d, \
            np.dot(self.X_logical_1, Z_error) % self.d, np.dot(self.X_logical_2, Z_error) % self.d])
            
    
    def _construct_parity_check_matrix(self):
        """
        Construct the parity check matrix for the qudit toric code.
        H_X: X-type stabilizers (vertex operators)
        H_Z: Z-type stabilizers (plaquette operators)
        """
        L = self.L
        n_qudits = self.n_qudits
        n_vertices = self.n_vertices
        n_plaquettes = self.n_plaquettes
        
        # Initialize sparse matrices
        self.H_X = sparse.lil_matrix((n_vertices, n_qudits), dtype=int)
        self.H_Z = sparse.lil_matrix((n_plaquettes, n_qudits), dtype=int)
        
        # Label qudits:
        # - Horizontal edges: 0 to LÂ²-1
        # - Vertical edges: LÂ² to 2LÂ²-1
        
        # Construct vertex operators (X-type stabilizers)
        for v in range(n_vertices):
            # Get vertex coordinates
            row = v // L
            col = v % L
            # print(f"vertex {v} at {row} {col}")
            
            # Get incident edges (considering periodic boundary conditions)
            # Each vertex has 4 incident edges
            
            # Right edge (horizontal)
            h_edge_right = row * L + col
            # Left edge (horizontal) - periodic boundary
            h_edge_left = row * L + ((col - 1) % L)
            # Up edge (vertical)
            v_edge_up = L**2 + row * L + col
            # Down edge (vertical) - periodic boundary
            v_edge_down = L**2 + ((row - 1) % L) * L + col
            # print(v_edge_up, h_edge_right, v_edge_down, h_edge_left)
            
            # Set entries to 1 or -1 mod d
            self.H_X[v, h_edge_right] = 1
            self.H_X[v, h_edge_left] = self.d - 1
            self.H_X[v, v_edge_down] = self.d - 1
            self.H_X[v, v_edge_up] = 1
        
        # Construct plaquette operators (Z-type stabilizers)
        for p in range(n_plaquettes):
            # Get plaquette coordinates (top-left vertex)
            row = p // L
            col = p % L
            # print(f"plaquette {p} at {row} {col}")
            
            # Get edges forming the plaquette (considering periodic boundaries)
            
            # Top edge (horizontal)
            h_edge_top = ((row + 1)%L) * L + col
            # Bottom edge (horizontal) - periodic boundary
            h_edge_bottom = row * L + col
            # Left edge (vertical)
            v_edge_left = L**2 + row * L + col
            # Right edge (vertical) - periodic boundary
            v_edge_right = L**2 + row * L + ((col + 1) % L)
            # print(h_edge_top, v_edge_right, h_edge_bottom, v_edge_left)
            
            # Set entries with appropriate powers
            # For Z-type operators, we need to set proper orientations
            self.H_Z[p, h_edge_top] = 1
            self.H_Z[p, h_edge_bottom] = self.d - 1  # Equivalent to -1 mod d
            self.H_Z[p, v_edge_left] =  1  # Equivalent to -1 mod d
            self.H_Z[p, v_edge_right] = self.d - 1
    
    def _construct_logical_operators(self):
        """
        Construct the logical operator matrices for the qudit toric code.
        - Logical X operators: non-contractible loops on the dual lattice
        - Logical Z operators: non-contractible loops on the primal lattice
        """
        L = self.L
        n_qudits = self.n_qudits
        
        # Initialize logical operator matrices
        # We have 2 logical qudits, each with d-1 logical operators (X, X^2, ..., X^(d-1))
        # and d-1 logical operators (Z, Z^2, ..., Z^(d-1))
        
        # First, we'll create the basic logical operators (X_1, X_2, Z_1, Z_2)
        
        # Logical Z_1: vertical non-contractible loop on the primal lattice
        self.Z_logical_1 = np.zeros(n_qudits, dtype=int)
        for i in range(L):
            # Use the first column of vertical edges
            self.Z_logical_1[L**2 + i * L] = 1
        
        # Logical Z_2: horizontal non-contractible loop on the primal lattice
        self.Z_logical_2 = np.zeros(n_qudits, dtype=int)
        for i in range(L):
            # Use the first row of horizontal edges
            self.Z_logical_2[i] = 1
        
        # Logical X_1: horizontal non-contractible loop on the dual lattice
        self.X_logical_1 = np.zeros(n_qudits, dtype=int)
        for i in range(L):
            # Use the first row of vertical edges
            self.X_logical_1[L**2 + i] = 1
        
        # Logical Z_2: vertical non-contractible loop on the dual lattice
        self.X_logical_2 = np.zeros(n_qudits, dtype=int)
        for i in range(L):
            # Use the first column of horizontal edges
            self.X_logical_2[i * L] = 1
            
    def verify_commutation_relations(self):
        """
        Verify the commutation relations between stabilizers and logical operators.
        For the qudit case, we verify the omega-commutation relations.
        
        Returns a dictionary with the verification results
        """
        L = self.L
        d = self.d
        
        results = {
            "X_stab_Z_stab": True,
            "X_stab_X_log": True,
            "Z_stab_Z_log": True,
            "X_log_Z_log": True
        }
        
        # Convert to numpy arrays for easier calculation
        H_X = self.H_X.toarray()
        H_Z = self.H_Z.toarray()
        
        # 1. Verify that X_stabilizers commute with Z_stabilizers
        for i in range(self.n_vertices):
            for j in range(self.n_plaquettes):
                # Inner product mod d should be 0 for commutation
                inner_prod = sum(H_X[i, k] * H_Z[j, k] for k in range(self.n_qudits)) % d
                if inner_prod != 0:
                    results["X_stab_Z_stab"] = False
                    print(f"X-stabilizer {i} and Z-stabilizer {j} don't commute!")
        
        # 2. Verify that X_stabilizers commute with Z_logical operators
        for i in range(self.n_vertices):
            # Z_logical_1
            inner_prod = sum(H_X[i, k] * self.Z_logical_1[k] for k in range(self.n_qudits)) % d
            if inner_prod != 0:
                results["X_stab_Z_log"] = False
                print(f"X-stabilizer {i} and Z-logical-1 don't commute!")
            
            # Z_logical_2
            inner_prod = sum(H_X[i, k] * self.Z_logical_2[k] for k in range(self.n_qudits)) % d
            if inner_prod != 0:
                results["X_stab_Z_log"] = False
                print(f"X-stabilizer {i} and Z-logical-2 don't commute!")
        
        # 3. Verify that Z_stabilizers commute with X_logical operators
        for i in range(self.n_plaquettes):
            # X_logical_1
            inner_prod = sum(H_Z[i, k] * self.X_logical_1[k] for k in range(self.n_qudits)) % d
            if inner_prod != 0:
                results["Z_stab_X_log"] = False
                print(f"Z-stabilizer {i} and Z-logical-1 don't commute!")
            
            # X_logical_2
            inner_prod = sum(H_Z[i, k] * self.X_logical_2[k] for k in range(self.n_qudits)) % d
            if inner_prod != 0:
                results["Z_stab_X_log"] = False
                print(f"Z-stabilizer {i} and X-logical-2 don't commute!")
        
        # 4. Verify that X_logical_i and Z_logical_j have the omega-commutation relation
        X1_Z1_inner = sum(self.X_logical_1[k] * self.Z_logical_1[k] for k in range(self.n_qudits)) % d
        X2_Z2_inner = sum(self.X_logical_2[k] * self.Z_logical_2[k] for k in range(self.n_qudits)) % d
        X1_Z2_inner = sum(self.X_logical_1[k] * self.Z_logical_2[k] for k in range(self.n_qudits)) % d
        X2_Z1_inner = sum(self.X_logical_2[k] * self.Z_logical_1[k] for k in range(self.n_qudits)) % d
        
        # XÌ„â‚ and ZÌ„â‚ should omega-commute (inner product = 1 mod d)
        if X1_Z1_inner != 1:
            results["X_log_Z_log"] = False
            print(f"X-logical-1 and Z-logical-1 don't properly omega-commute! Inner product: {X1_Z1_inner}")
        
        # XÌ„â‚‚ and ZÌ„â‚‚ should omega-commute (inner product = 1 mod d)
        if X2_Z2_inner != 1:
            results["X_log_Z_log"] = False
            print(f"X-logical-2 and Z-logical-2 don't properly omega-commute! Inner product: {X2_Z2_inner}")
        
        # XÌ„â‚ and ZÌ„â‚‚ should commute (inner product = 0 mod d)
        if X1_Z2_inner != 0:
            results["X_log_Z_log"] = False
            print(f"X-logical-1 and Z-logical-2 don't commute! Inner product: {X1_Z2_inner}")
        
        # XÌ„â‚‚ and ZÌ„â‚ should commute (inner product = 0 mod d)
        if X2_Z1_inner != 0:
            results["X_log_Z_log"] = False
            print(f"X-logical-2 and Z-logical-1 don't commute! Inner product: {X2_Z1_inner}")
        
        return results
        
    def visualize_code(self, show_logical=True):
        """
        Visualize the qudit toric code structure
        """
        L = self.L
        
        plt.figure(figsize=(10, 10))
        
        # Plot vertices
        for i in range(L):
            for j in range(L):
                plt.plot(j, i, 'ko', markersize=8)
        
        # Plot horizontal edges
        for i in range(L):
            for j in range(L):
                plt.plot([j, (j+1)%L], [i, i], 'b-', linewidth=2)
        
        # Plot vertical edges
        for i in range(L):
            for j in range(L):
                plt.plot([j, j], [i, (i+1)%L], 'g-', linewidth=2)
        
        # Show logical operators if requested
        if show_logical:
            # Highlight X_logical_1 (vertical path)
            for i in range(L):
                plt.plot([0, 0], [i, (i+1)%L], 'r-', linewidth=4)
            
            # Highlight X_logical_2 (horizontal path)
            for j in range(L):
                plt.plot([j, (j+1)%L], [0, 0], 'r-', linewidth=4)
            
            # Highlight Z_logical_1 (horizontal path)
            for j in range(L):
                plt.plot([j, (j+1)%L], [L//2, L//2], 'm-', linewidth=4)
            
            # Highlight Z_logical_2 (vertical path)
            for i in range(L):
                plt.plot([L//2, L//2], [i, (i+1)%L], 'm-', linewidth=4)
        
        plt.grid(True)
        plt.xlim(-0.5, L-0.5)
        plt.ylim(-0.5, L-0.5)
        plt.title(f"Qudit Toric Code (L={L}, d={self.d})")
        
        # Add legend
        plt.plot([], [], 'b-', linewidth=2, label='Horizontal Edges')
        plt.plot([], [], 'g-', linewidth=2, label='Vertical Edges')
        plt.plot([], [], 'ko', markersize=8, label='Vertices')
        
        if show_logical:
            plt.plot([], [], 'r-', linewidth=4, label='X Logical Operators')
            plt.plot([], [], 'm-', linewidth=4, label='Z Logical Operators')
        
        plt.legend()
        plt.show()
    
    def get_code_parameters(self):
        """
        Return the code parameters [n, k, d]_q where:
        n = number of physical qudits
        k = number of logical qudits
        d = code distance
        q = dimension of each qudit
        """
        n = self.n_qudits
        k = 2  # Toric code encodes 2 logical qudits
        code_distance = self.L  # Distance of the toric code is L
        q = self.d
        
        return {
            "n": n,
            "k": k,
            "code_distance": code_distance,
            "q": q,
            "parameters": f"[[{n}, {k}, {code_distance}]]_{q}"
        }

# Example usage
if __name__ == "__main__":
    # Create a qudit toric code with L=3, d=5
    code = QuditToricCode(L=5, d=5)
    
    # Print code parameters
    params = code.get_code_parameters()
    print(f"Qudit Toric Code Parameters: {params['parameters']}")
    print(f"Number of qudits: {params['n']}")
    print(f"Number of logical qudits: {params['k']}")
    print(f"Code distance: {params['code_distance']}")
    print(f"Qudit dimension: {params['q']}")
    
    # Verify that the code satisfies the necessary commutation relations
    results = code.verify_commutation_relations()
    print("\nCommutation relation verification:", "PASSED" if all(results.values()) else "FAILED")
    
    # Visualize the code
    code.visualize_code()
    
    # Optional: Print the parity check matrices
    print("\nX Stabilizer Matrix (H_X) shape:", code.H_X.shape)
    print("Z Stabilizer Matrix (H_Z) shape:", code.H_Z.shape)
    
    # To get dense matrices, use .toarray()
    # H_X_dense = code.H_X.toarray()
    # H_Z_dense = code.H_Z.toarray()