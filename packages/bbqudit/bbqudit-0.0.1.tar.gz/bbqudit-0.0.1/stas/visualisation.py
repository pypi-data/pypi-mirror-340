import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.gridspec as gridspec

from qudit_toric_code import QuditToricCode
# from bp_decoder import BeliefPropagationDecoder
from dosd import dijkstra_osd


def generate_random_errors(code, error_rate):
    """
    Generate random X errors on qudits of the toric code.
    
    Args:
        code: QuditToricCode instance
        error_rate: Probability of each qudit having an error
        
    Returns:
        Array of error values (0 = no error)
    """
    n_qudits = code.n_qudits
    d = code.d
    
    # Generate errors with specified probability
    errors = np.zeros(n_qudits, dtype=int)
    error_mask = np.random.rand(n_qudits) < error_rate
    
    # For qudits with errors, assign a random non-zero value
    for i in np.where(error_mask)[0]:
        errors[i] = np.random.randint(1, d)
    
    return errors


def compute_syndrome(code, error):
    """
    Compute the Z syndrome for X errors.
    
    Args:
        code: QuditToricCode instance
        error: Array of X error values
        
    Returns:
        Array of Z syndrome values
    """
    # For X errors, compute Z syndromes (plaquette operators)
    H = code.H_Z
    
    # Compute syndrome: H * error (mod d)
    syndrome = (H.dot(error)) % code.d
    
    return syndrome


def visualize_toric_code(code, errors=None, syndrome=None, decoded_errors=None, 
                        title="Toric Code Visualization", debug_errors = [], debug_labels = {}):
    print(debug_labels)
    """
    Visualize the toric code with errors and syndromes shown as numbered circles.
    
    Args:
        code: QuditToricCode instance
        errors: Original error values (optional)
        syndrome: Syndrome values (optional)
        decoded_errors: Decoded error values (optional)
        title: Plot title
    """
    L = code.L
    d = code.d

    assert set(debug_errors) == set(debug_labels.keys())
    
    # Create figure with subplots
    if decoded_errors is not None:
        fig = plt.figure(figsize=(18, 6))
        gs = gridspec.GridSpec(1, 3, width_ratios=[1, 1, 1])
        ax1 = plt.subplot(gs[0])
        ax2 = plt.subplot(gs[1])
        ax3 = plt.subplot(gs[2])
        axes = [ax1, ax2, ax3]
        titles = ["Original X Errors", "Z Syndrome", "Decoded X Errors"]
    else:
        fig = plt.figure(figsize=(12, 6))
        gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1])
        ax1 = plt.subplot(gs[0])
        ax2 = plt.subplot(gs[1])
        axes = [ax1, ax2]
        titles = ["Original X Errors", "Z Syndrome"]
    
    # Draw all subplots
    for i, ax in enumerate(axes):
        # Draw the grid
        for j in range(L+1):
            ax.plot([0, L], [j, j], 'k-', alpha=0.3)
            ax.plot([j, j], [0, L], 'k-', alpha=0.3)
        
        # Draw vertices as small black dots
        for r in range(L):
            for c in range(L):
                ax.plot(c, r, 'ko', markersize=3)
        
        # Set plot limits and title
        ax.set_xlim(-0.5, L+0.5)
        ax.set_ylim(-0.5, L+0.5)
        ax.set_aspect('equal')
        ax.set_title(titles[i])
        
        # Remove axis labels
        ax.set_xticks([])
        ax.set_yticks([])
    
    # Draw original errors (on first subplot)
    if errors is not None:
        # Horizontal edges
        for r in range(L):
            for c in range(L):
                qudit_idx = r * L + c
                if errors[qudit_idx] > 0:
                    circle = Circle((c+0.5, r), 0.15, color='blue', alpha=0.8)
                    ax1.add_patch(circle)
                    ax1.text(c+0.5, r, str(errors[qudit_idx]), 
                            ha='center', va='center', color='white', fontsize=8)
        
        # Vertical edges
        for r in range(L):
            for c in range(L):
                qudit_idx = L**2 + r * L + c
                if errors[qudit_idx] > 0:
                    circle = Circle((c, r+0.5), 0.15, color='blue', alpha=0.8)
                    ax1.add_patch(circle)
                    ax1.text(c, r+0.5, str(errors[qudit_idx]), 
                            ha='center', va='center', color='white', fontsize=8)
    
    # Draw syndrome (on second subplot)
    if syndrome is not None:
        for r in range(L):
            for c in range(L):
                syndrome_idx = r * L + c
                if syndrome[syndrome_idx] > 0:
                    circle = Circle((c+0.5, r+0.5), 0.15, color='red', alpha=0.8)
                    ax2.add_patch(circle)
                    ax2.text(c+0.5, r+0.5, str(syndrome[syndrome_idx]), 
                            ha='center', va='center', color='white', fontsize=8)
    
    # Draw decoded errors (on third subplot, if present)
    if decoded_errors is not None:
        # Horizontal edges
        for r in range(L):
            for c in range(L):
                qudit_idx = r * L + c
                if qudit_idx in debug_errors:
                    circle = Circle((c+0.5, r), 0.2, color='grey', alpha=0.3)
                    ax3.add_patch(circle)
                    ax3.text(c+0.5, r, str(debug_labels[qudit_idx]), 
                            ha='center', va='center', color='black', fontsize=8)

                if decoded_errors[qudit_idx] > 0:
                    circle = Circle((c+0.5, r), 0.15, color='green', alpha=0.8)
                    ax3.add_patch(circle)
                    ax3.text(c+0.5, r, str(decoded_errors[qudit_idx]), 
                            ha='center', va='center', color='white', fontsize=8)

        
        # Vertical edges
        for r in range(L):
            for c in range(L):
                qudit_idx = L**2 + r * L + c
                if qudit_idx in debug_errors:
                    circle = Circle((c, r+0.5), 0.2, color='grey', alpha=0.3)
                    ax3.add_patch(circle)
                    ax3.text(c, r+0.5, str(debug_labels[qudit_idx]), 
                            ha='center', va='center', color='black', fontsize=8)
                if decoded_errors[qudit_idx] > 0:
                    circle = Circle((c, r+0.5), 0.15, color='green', alpha=0.8)
                    ax3.add_patch(circle)
                    ax3.text(c, r+0.5, str(decoded_errors[qudit_idx]), 
                            ha='center', va='center', color='white', fontsize=8)
    
    # Add legend
    legend_elements = []
    if errors is not None:
        legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', 
                               markerfacecolor='blue', markersize=10, label='X Error'))
    if syndrome is not None:
        legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', 
                               markerfacecolor='red', markersize=10, label='Z Syndrome'))
    if decoded_errors is not None:
        legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', 
                               markerfacecolor='green', markersize=10, label='Decoded Error'))
    
    # Place the legend on the first subplot
    ax1.legend(handles=legend_elements, loc='upper right')
    
    plt.suptitle(title, fontsize=16)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    return fig


def run_and_visualize_decoding(code, error_rate=0.1,verbose=True):
    """
    Generate random errors, compute syndromes, decode, and visualize the results.
    
    Args:
        code: QuditToricCode instance
        error_rate: Probability of each qudit having an error
        verbose: Whether to print detailed information
        
    Returns:
        Dictionary with results and figure
    """
    # Generate random errors
    original_errors = generate_random_errors(code, error_rate)
    error_count = np.sum(original_errors > 0)
    
    if verbose:
        print(f"Generated {error_count} errors (rate: {error_rate:.2f})")
    
    # Compute the syndrome
    syndrome = compute_syndrome(code, original_errors)
    syndrome_count = np.sum(syndrome > 0)
    
    if verbose:
        print(f"Syndrome has {syndrome_count} non-zero elements")
    
    # Run the D+OSD decoder
    decoded_errors, success, pivot_cols, pivot_col_labels = dijkstra_osd(
        code.H_Z.toarray(), syndrome, error_rate, q=code.d, debug=True
    )

    if verbose:
        # Check if the syndrome is satisfied
        decoded_syndrome = compute_syndrome(code, decoded_errors)
        syndrome_satisfied = np.array_equal(syndrome, decoded_syndrome)
        
        # Check for logical errors (error after correction)
        error_difference = (original_errors - decoded_errors) % code.d
        logical_effect = code.get_logical_effect(error_difference, np.zeros_like(error_difference))
        logical_error = np.any(logical_effect != 0)
        
        print(f"Decoding successful: {success}")
        print(f"Syndrome satisfied: {syndrome_satisfied}")
        print(f"Logical error: {logical_error}")
        if logical_error:
            print(f"Logical effect: {logical_effect}")
    
    # Visualize the results
    fig = visualize_toric_code(
        code, 
        errors=original_errors,
        syndrome=syndrome,
        decoded_errors=decoded_errors,
        title=f"Toric Code Decoding (L={code.L}, d={code.d})",
        debug_errors = pivot_cols,
        debug_labels = pivot_col_labels
    )
    
    # Return results
    results = {
        "code": code,
        "original_errors": original_errors,
        "syndrome": syndrome,
        "decoded_errors": decoded_errors,
        "decoding_success": success,
        "figure": fig
    }
    
    return results

if __name__ == "__main__":
    # Parameters
    L = 9  # Lattice size
    d = 5  # Qudit dimension (must be prime)
    error_rate = 0.03
    max_iterations = 100
    
    print(f"Creating qudit toric code with L={L}, d={d}")
    code = QuditToricCode(L, d)
    
    # Run basic decoding and visualization
    print("\n--- Running BP+OSD decoder ---")
    results = run_and_visualize_decoding(code, error_rate, max_iterations)
    plt.show()


    # Try with a different qudit dimension
    if d != 5:  # Only run if we haven't already used d=5
        print("\n--- Running with d=5 ---")
        code_d5 = QuditToricCode(L, 5)
        d5_results = run_and_visualize_decoding(code_d5, error_rate, max_iterations)
        plt.show()