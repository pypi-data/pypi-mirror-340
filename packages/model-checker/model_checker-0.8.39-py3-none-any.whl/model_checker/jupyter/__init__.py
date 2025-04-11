"""
ModelChecker Jupyter integration package.

This package provides tools for using ModelChecker in Jupyter notebooks
with interactive visualizations and simplified interfaces.

Basic usage:
    from model_checker.jupyter import check_formula
    check_formula("p → q", premises=["p"])
    
Interactive usage:
    from model_checker.jupyter import ModelExplorer
    explorer = ModelExplorer()
    explorer.display()
"""

# Check for required dependencies
import importlib.util
import warnings

# Track available features
HAS_JUPYTER_DEPS = True

# Check for ipywidgets
if importlib.util.find_spec("ipywidgets") is None:
    HAS_JUPYTER_DEPS = False
    warnings.warn(
        "ipywidgets not found. Install with 'pip install model-checker[jupyter]' "
        "to enable interactive features."
    )

# Check for matplotlib
if importlib.util.find_spec("matplotlib") is None:
    HAS_JUPYTER_DEPS = False
    warnings.warn(
        "matplotlib not found. Install with 'pip install model-checker[jupyter]' "
        "to enable visualization features."
    )

# Check for networkx
if importlib.util.find_spec("networkx") is None:
    HAS_JUPYTER_DEPS = False
    warnings.warn(
        "networkx not found. Install with 'pip install model-checker[jupyter]' "
        "to enable graph visualization features."
    )

# Define core utilities (these don't require optional dependencies)
from .unicode import unicode_to_latex, latex_to_unicode
from .environment import setup_environment, get_available_theories
from .utils import load_examples

# Define the minimal public API
__all__ = [
    # Utilities (always available)
    "unicode_to_latex",
    "latex_to_unicode",
    "setup_environment",
    "get_available_theories",
    "load_examples",
    "HAS_JUPYTER_DEPS",
]

# Add interactive features if dependencies are available
if HAS_JUPYTER_DEPS:
    try:
        # First import display functions
        from .display import (
            display_model, 
            display_formula_check, 
            display_countermodel
        )
        
        # Then import interactive components (which may use display functions)
        from .interactive import (
            ModelExplorer, 
            check_formula, 
            find_countermodel, 
            explore_formula
        )
        
        # Try to import FormulaChecker if it exists
        try:
            from .interactive import FormulaChecker
            has_formula_checker = True
        except ImportError:
            has_formula_checker = False
        
        # Add to public API
        __all__.extend([
            # High-level functions
            "check_formula",
            "find_countermodel",
            "explore_formula",
            
            # UI Components
            "ModelExplorer",
            
            # Display Functions
            "display_model",
            "display_formula_check",
            "display_countermodel",
        ])
        
        # Add FormulaChecker if available
        if has_formula_checker:
            __all__.append("FormulaChecker")
            
    except ImportError as e:
        warnings.warn(
            f"Some Jupyter features couldn't be imported: {e}. "
            "Install with 'pip install model-checker[jupyter]' to enable all features."
        )

# Define stub functions for when dependencies aren't available
if not HAS_JUPYTER_DEPS:
    def missing_dependencies_error(feature_name):
        """Raise error for missing dependencies."""
        raise ImportError(
            f"{feature_name} requires additional dependencies. "
            "Install with 'pip install model-checker[jupyter]' to enable this feature."
        )
        
    def check_formula(*args, **kwargs):
        """Stub for check_formula when dependencies are missing."""
        missing_dependencies_error("check_formula")
        
    def find_countermodel(*args, **kwargs):
        """Stub for find_countermodel when dependencies are missing."""
        missing_dependencies_error("find_countermodel")
        
    def explore_formula(*args, **kwargs):
        """Stub for explore_formula when dependencies are missing."""
        missing_dependencies_error("explore_formula")
        
    # Add these to __all__ to ensure consistent API
    __all__.extend(["check_formula", "find_countermodel", "explore_formula"])
