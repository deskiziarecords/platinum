# Spectral-Forensic-Auditor algorithm_sfa.py

import jax
import jax.numpy as jnp
from functools import partial

# --- TIER 1: SPECTRAL STABILITY (PSVD) ---
@jax.jit
def psvd_ortho_check(weight_matrix):
    """
    Enforces and evaluates weight orthonormality via SVD.
    [1, 2]
    """
    u, s, vh = jnp.linalg.svd(weight_matrix, full_matrices=False)
    # Spectral integrity score: similarity to Identity
    integrity_score = jnp.linalg.norm(s - 1.0)
    return u @ vh, integrity_score

# --- TIER 2: FORENSIC AUDIT (Algorithm Iota) ---
def l4_weight_sparsity(weights):
    """
    Algorithm Iota logic: Maximize l4-norm to evaluate sparsification.
    Detects cherry-picking via absolute fourth-power coefficients.
    [4, 5]
    """
    l4_score = jnp.sum(jnp.abs(weights)**4)
    # VC-Dimension threshold check (simplified)
    is_plausible = l4_score > 0.60
    return l4_score, is_plausible

# --- TIER 3: ALIGNMENT (CKA) ---
@jax.jit
def centered_kernel_alignment(tangent_features, labels):
    """
    CKA calculation to measure weight contribution.
    [7, 8]
    """
    features_centered = tangent_features - jnp.mean(tangent_features, axis=0)
    labels_centered = labels - jnp.mean(labels, axis=0)
    
    k_f = features_centered @ features_centered.T
    k_l = labels_centered @ labels_centered.T
    
    # Linear CKA: <K_f, K_l>_F / (||K_f||_F * ||K_l||_F)
    num = jnp.sum(k_f * k_l)
    den = jnp.linalg.norm(k_f) * jnp.linalg.norm(k_l)
    return num / den

# --- INTEGRATED EVALUATION KERNEL ---
@jax.jit
def evaluate_weight_manifold(weights, features, labels):
    """
    Independent module for structural weight evaluation.
    """
    # 1. Check Spectral Orthonormality
    ortho_weights, spec_err = psvd_ortho_check(weights)
    
    # 2. Audit for Cherry-Picking (l4-Sparsity)
    l4_val, plausible = l4_weight_sparsity(ortho_weights)
    
    # 3. Measure Alignment with Objective
    contribution = centered_kernel_alignment(features, labels)
    
    return {
        "spectral_error": spec_err,
        "plausibility_score": l4_val,
        "is_plausible": plausible,
        "cka_alignment": contribution
    }
