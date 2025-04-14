import numpy as np
from itertools import product, combinations
import galois
# from bp_decoder import BeliefPropagationDecoder



def dijkstra_osd(H, syndrome, p, q=2, debug = False):
    """
    D+OSD decoder for quantum qudit codes over GF(q).
    
    Parameters:
        H: parity check matrix (numpy array)
        syndrome: syndrome measurement (numpy array)
        p: physical error rate
        q: dimension of the qudit system (prime number)
        combination_sweep_depth: parameter λ for the combination sweep strategy
    
    Returns:
        error_estimate: estimated error pattern
        success: whether the decoding was successful
    """


    m,n  = H.shape
    
    prior_probabilities = np.zeros((n, q))
    
    # For each qudit, set probability of no error (value 0) to 1-p
    # and distribute p among other error types
    prior_probabilities[:, 0] = 1 - p
    for i in range(1, q):
        prior_probabilities[:, i] = p / (q - 1)

    # Mini-Dijkstra
    check_distances = np.ones(m)*n
    error_distances = np.ones(n)*n

    for c in syndrome.nonzero()[0]:
        check_distances[c] = 0

    update_made = True
    while(update_made):
        update_made = False
        for c in range(m):
            current_distance = check_distances[c]
            for e in np.nonzero(H[c])[0]:
                if current_distance + 1 < error_distances[e]:
                    error_distances[e] = current_distance + 1
                    update_made = True
            
        for e in range(n):
            current_distance = error_distances[e]
            for c in np.nonzero(H[:,e])[0]:
                if current_distance + 1 < check_distances[c]:
                    check_distances[c] = current_distance + 1
                    update_made = True

    certainties = error_distances
    
    # Sort qudits by how certain we are of their values (most to least certain)
    
    col_rank_perm = np.argsort(certainties)
    col_rank_inv_perm = np.empty_like(col_rank_perm)
    col_rank_inv_perm[col_rank_perm] = np.arange(len(col_rank_perm))
    
    # Create Galois field elements
    GF = galois.GF(q)
    
    # Convert H and syndrome to Galois field arrays
    H_gf = GF(H.copy())
    syndrome_gf = GF(syndrome.copy())
    
    # Order the columns of H according to the ranking
    H_ordered_gf = H_gf[:, col_rank_perm]
    
    # Find the reduced row echelon form (RREF) and identify pivot columns
    H_rref_gf, syndrome_rref_gf, pivot_cols = rref_with_pivots(H_ordered_gf, syndrome_gf)
    m_ind = H_rref_gf.shape[0]
    non_pivot_cols = [i for i in range(n) if i not in pivot_cols]
    
    # Select the first rank(H) linearly independent columns as basis set
    P = H_rref_gf[:, pivot_cols]
    assert P.shape == (m_ind, m_ind)
    B = H_rref_gf[:, non_pivot_cols]

    priors_perm = prior_probabilities[col_rank_perm]

    def sln_from(g):
        assert g.shape == (n - m_ind,)
        remainder =  syndrome_rref_gf - B @ g
        fix = np.linalg.solve(P, remainder)
        assert (P @ fix + B @ g == syndrome_rref_gf).all()

        score = 0
        sln = GF.Zeros(n)
        # Find prob of basis set
        for i in range(m_ind):
            p = priors_perm[pivot_cols[i],fix[i]]
            sln[pivot_cols[i]] = fix[i]
            if p > 0:
                score += np.log(p)
            else:
                p += -1000
        
        for i in range(n - m_ind):
            p = priors_perm[non_pivot_cols[i], g[i]]
            sln[non_pivot_cols[i]] = g[i]
            if p > 0:
                score += np.log(p)
            else:
                p += -1000
        
        assert (H_rref_gf @ sln == syndrome_rref_gf).all()
        assert (H_gf @ sln[col_rank_inv_perm] == syndrome_gf).all()
    
        return np.array(sln[col_rank_inv_perm]), score
    

    # OSD_0 solution
    best_solution, best_score = sln_from(GF.Zeros(n - m_ind))
    pivot_col_labels = {col_rank_perm[c]: int(error_distances[col_rank_perm[c]]) for c in pivot_cols}
    if debug:
        return best_solution, True, [col_rank_perm[i] for i in pivot_cols], pivot_col_labels
    else:
        return best_solution



def rref_with_pivots(A, v, x = None):
    """
    Perform Gaussian elimination to find the reduced row echelon form (RREF).
    Also identifies the pivot columns.
    Also reduces a vector to keep a linear system invariant.
    
    Parameters:
        A: Galois field matrix to row reduce
        
    Returns:
        A_rref: row-reduced form of A
        pivots: indices of pivot columns
    """
    # Get a copy to avoid modifying the original
    A_rref = A.copy()
    v_rref = v.copy()
    m, n = A_rref.shape
    assert v.shape == (m,)
    # assert (A_rref @ x == v_rref).all()
    
    # Track the pivot positions
    pivot_cols = []
    pivot_rows = []
    
    # Iterate through columns
    for c in range(n):
        # Find pivot in column c
        for r in range(m):
            if A_rref[r, c] != 0 and r not in pivot_rows:
                break
        else:
            continue

        # Record this column as a pivot column
        pivot_cols.append(c)
        pivot_rows.append(r)
        
        # Scale the pivot row to make the pivot element 1
        pivot = A_rref[r, c]
        A_rref[r] = A_rref[r] / pivot
        v_rref[r] = v_rref[r]/pivot
        
        # Eliminate other elements in the pivot column
        for i in range(m):
            if i != r and A_rref[i, c] != 0:
                v_rref[i] = v_rref[i] - A_rref[i,c] * v_rref[r]
                A_rref[i] = A_rref[i] - A_rref[i, c] * A_rref[r]
        
        # If we've exhausted all rows, we're done
        if len(pivot_rows) == m:
            break
    
    if len(pivot_rows) < A.shape[0]:
        print("Matrix is not full rank.")

    return A_rref[sorted(pivot_rows)], v_rref[sorted(pivot_rows)], pivot_cols


# Example usage:
if __name__ == "__main__":

    GF = galois.GF(5)
    A = GF(np.random.randint(0,5,500).reshape((10,50)))
    x = GF(np.random.randint(0,5,50))
    s = A @ x
    print(x,s, x.shape)
    assert (A @ x == s).all()
    A_ref, s_ref, cols = rref_with_pivots(A, s, x)
    assert (A_ref @ x == s_ref).all()
    
    # Small example for a ternary (q=3) code
    q = 3
    H = np.array([
        [1, 1, 2, 0, 1],
        [2, 0, 1, 1, 0]
    ])
    
    # Random syndrome
    syndrome = np.array([1, 2])
    
    # Error rate
    p = 0.1
    
    # Run BP+OSD decoder with the BeliefPropagationDecoder adapter
    error_estimate = dijkstra_osd(H, syndrome, p, q=q)
    
    print("Estimated error:", error_estimate)
    
    # Verify using galois
    GF = galois.GF(q)
    H_gf = GF(H)
    syndrome_gf = GF(syndrome)
    error_gf = GF(error_estimate)
    
    print("Syndrome check:", np.array_equal((H_gf @ error_gf), syndrome))
    
    # Compare with standard BP decoding alone
    bp_decoder = BeliefPropagationDecoder(H, d=q, max_iterations=100)
    
    # Create prior probabilities
    n = H.shape[1]
    prior_probabilities = np.zeros((n, q))
    prior_probabilities[:, 0] = 1 - p
    for i in range(1, q):
        prior_probabilities[:, i] = p / (q - 1)
    
    bp_estimate = bp_decoder.decode(syndrome, prior_probabilities)
    bp_success = bp_decoder.verify_decoder(syndrome, bp_estimate)
    
    print("\nStandard BP Decoding:")
    print("Estimated error:", bp_estimate)
    print("Decoding successful:", bp_success)
    print("Syndrome check:", np.array_equal((H_gf @ GF(bp_estimate)), syndrome))