# ModelChecker Guide for Agents

## Quick Start
This project creates a programmatic semantics framework for implementing and comparing logical theories, with a focus on modal, counterfactual, and hyperintensional logic. It provides tooling for defining semantic theories, testing logical principles, and finding countermodels.

### Key Search Paths
- Core implementations: `/home/benjamin/Documents/Philosophy/Projects/ModelChecker/Code/src/model_checker/`
- Theory definitions: `/home/benjamin/Documents/Philosophy/Projects/ModelChecker/Code/src/model_checker/theory_lib/`
- Jupyter integrations: `/home/benjamin/Documents/Philosophy/Projects/ModelChecker/Code/src/model_checker/jupyter/`

## Commands
- Run all tests: `pytest theory_lib/<theory_name>/test/`
- Run specific test: `pytest theory_lib/<theory_name>/test/test_<theory_name>.py -k "<test_name>"`
- Run with verbose output: `pytest -v theory_lib/<theory_name>/test/`
- Run main module: `python -m model_checker`
- Create a new theory: `python -m model_checker -l <theory_name>`
- Check an example file: `python -m model_checker <example_file.py>`
- Development CLI: `python dev_cli.py <example_file.py>`
- Run jupyter notebooks: `./run_jupyter.sh`

## Code Style
- **Imports**: Standard libraries first, then local imports
- **Spacing**: 4-space indentation
- **Naming**: 
  - Functions: `snake_case`
  - Classes: `PascalCase`
  - Modules: `lowercase`
- **Error handling**: Use descriptive exception messages
- **Documentation**: Triple-quoted docstrings for modules and functions
- **Architecture**: 
  - Maintain separation between semantic and syntactic components
  - Each theory in `theory_lib/` follows same structure (operators.py, semantic.py, examples.py)
  - New theories should match existing module patterns

## Design Philosophy
- **Fail Fast**: Let errors occur naturally with standard Python tracebacks rather than adding complex conditional logic to handle edge cases.
- **Deterministic Behavior**: Avoid default values, fallbacks, or implicit conversions that can mask errors or introduce non-deterministic behavior.
- **Required Parameters**: Parameters should be explicitly required with no implicit conversion between different types of values (e.g., world arrays vs. world IDs).
- **Clear Data Flow**: Keep a clear and consistent approach to passing data between components, making sure all required values are explicitly passed.
- **No Silent Failures**: Don't catch exceptions or provide defaults just to avoid errors. If a value is missing or of the wrong type, let the error happen clearly.
- **Explicit World References**: In bimodal logic, always use consistent world references. World IDs should be explicitly provided where needed rather than attempting conversions.

## Debugging Philosophy
- **Root Cause Analysis**: Always trace errors to their source rather than addressing symptoms. Fix the underlying issue instead of adding patches.
- **Error as Feedback**: View errors as valuable signals pointing to areas that need improvement in the codebase.
- **Structural Solutions**: When fixing bugs, consider if the issue reveals a deeper architectural problem that should be addressed.
- **Refactor Over Workaround**: Choose to refactor problematic code rather than adding conditional logic to work around issues.
- **Test-Driven Resolution**: Create regression tests that reproduce bugs before fixing them to ensure they don't return.
- **Documentation of Learnings**: Document significant bugs and their solutions to build institutional knowledge.
- **Simplification**: If a component generates frequent errors, consider simplifying its interface or responsibilities.
- **No Defensive Programming**: Avoid adding excessive validation or error handling that obscures the natural flow of the code.
- **Error Messages as Documentation**: Write clear, specific error messages that help future developers understand requirements.
- **Eliminate Error Classes**: Reduce similar errors by identifying patterns and making structural improvements.

## Documentation Reference

### Core Documentation
| Document Path | Description | When to Use |
|--------------|-------------|-------------|
| `/README.md` | Project overview, installation, usage | Start here for general overview |
| `/src/model_checker/README.md` | API architecture, components | Understanding architecture |
| `/src/model_checker/theory_lib/README.md` | Theory library overview | Adding/modifying theories |
| `/src/model_checker/jupyter/README.md` | Jupyter integration | Interactive usage |

### Theory Documentation
| Document Path | Description | When to Use |
|--------------|-------------|-------------|
| `/src/model_checker/theory_lib/default/README.md` | Default theory details | Working with hyperintensional logic |
| `/src/model_checker/theory_lib/bimodal/README.md` | Bimodal theory details | Working with temporal counterfactuals |
| `/src/model_checker/theory_lib/exclusion/README.md` | Exclusion theory details | Working with exclusion semantics |
| `/src/model_checker/theory_lib/imposition/README.md` | Imposition theory details | Working with imposition semantics |

### Jupyter and Troubleshooting
| Document Path | Description | When to Use |
|--------------|-------------|-------------|
| `/src/model_checker/jupyter/TROUBLESHOOTING.md` | Common issues and solutions | Fixing integration problems |
| `/src/model_checker/jupyter/NixOS_jupyter.md` | NixOS setup guide | Setting up on NixOS |
| `/src/model_checker/jupyter/debug/DEBUGGING.md` | Debugging workflow | Systematic troubleshooting |

### Interactive Notebooks
| Document Path | Description | When to Use |
|--------------|-------------|-------------|
| `/src/model_checker/jupyter/notebooks/basic_demo.ipynb` | Basic usage examples | Getting started with notebooks |
| `/src/model_checker/jupyter/notebooks/options_demo.ipynb` | Advanced options | Learning advanced features |
| `/src/model_checker/theory_lib/default/notebooks/default_demo.ipynb` | Default theory demo | Exploring hyperintensional logic |
| `/src/model_checker/theory_lib/exclusion/notebooks/exclusion_demo.ipynb` | Exclusion theory demo | Exploring exclusion semantics |

## Project Structure

The ModelChecker implements a modular framework for logical model checking with the following architecture:

### Core Components

1. **Builder System** (`builder.py`)
   - `BuildExample`: Creates and executes individual model checking examples
   - `BuildModule`: Manages multiple examples across different theories
   - `BuildProject`: Creates new theory implementations from templates

2. **Model System** (`model.py`)
   - `ModelConstraints`: Core constraint generation for model checking
   - `ModelDefaults`: Base implementation for model structures
   - `SemanticDefaults`: Fundamental semantic operations (fusion, part-hood, etc.)
   - `PropositionDefaults`: Base proposition class for formula evaluation

3. **Syntactic System** (`syntactic.py`)
   - `Syntax`: Parses formulas and builds logical structures
   - `Sentence`: Represents logical formulas with metadata
   - `Operator`: Base class for logical operators
   - `DefinedOperator`: Complex operators defined using primitives
   - `OperatorCollection`: Registry system for operator management

4. **Utilities** (`utils.py`)
   - Theory loading and registration
   - Example loading and execution
   - Common helper functions
   - Path management utilities

5. **Command-line Interface** (`__main__.py`, `cli.py`)
   - Command-line argument processing
   - Project initialization
   - Example execution
   - Error handling and output formatting

### Theory Library

The `theory_lib/` package contains implementations of specific semantic theories:

1. **Default Theory**: Standard bilateral truthmaker semantics
   - `semantic.py`: Core semantic model implementation
   - `operators.py`: Definition of logical operators
   - `examples.py`: Demonstration examples
   - `test/`: Unit tests for theory validation

2. **Exclusion Theory**: Unilateral semantics with exclusion relations
   - Same structure as default theory

3. **Imposition Theory**: Semantics with imposition relations
   - Same structure as default theory

4. **Bimodal Theory**: Bimodal semantics for counterfactuals (experimental)
   - Same structure as default theory

Each theory is registered in `theory_lib/__init__.py` for discovery and lazy loading.

### Jupyter Integration

The `jupyter/` package provides interactive notebook capabilities:

1. **Public API** (`__init__.py`)
   - High-level functions: `check_formula`, `find_countermodel`, etc.
   - UI Components: `ModelExplorer`, `FormulaChecker`
   - Display functions for visualization

2. **Component Modules**
   - `interactive.py`: Interactive UI components
   - `display.py`: Model visualization utilities
   - `unicode.py`: Unicode/LaTeX notation conversion
   - `adapters.py`: Theory-specific visualization adapters
   - `environment.py`: Environment setup and configuration
   - `utils.py`: Jupyter-specific utilities

3. **Debugging Tools** (`debug/`)
   - Diagnostic tools for troubleshooting
   - Error capture utilities
   - Testing notebooks

4. **Demo Notebooks** (`notebooks/`)
   - Basic usage examples
   - Advanced features demonstrations

### Development Tools

1. **Testing Tools** (`run_tests.py`)
   - Automatic test discovery and execution
   - Theory-specific test runners

2. **Package Management** (`run_update.py`)
   - Version management
   - Package building and deployment

3. **Development CLI** (`dev_cli.py`)
   - Local development interface
   - Path configuration for development mode

4. **NixOS Support** (`shell.nix`)
   - Development environment definition
   - Path management for NixOS systems

## Common Workflows

### Adding a New Theory
1. Create a new directory in `theory_lib/`: `mkdir theory_lib/new_theory_name`
2. Implement required files: `semantic.py`, `operators.py`, `examples.py`
3. Add theory to registry in `theory_lib/__init__.py`: Add 'new_theory_name' to AVAILABLE_THEORIES
4. Create tests in `theory_lib/new_theory_name/test/`
5. Verify with `pytest theory_lib/new_theory_name/test/`

### Adding a New Operator
1. In the relevant theory's `operators.py`:
   - For primitive operators: Create a subclass of `Operator`
   - For derived operators: Create a subclass of `DefinedOperator`
2. Define semantic clauses for the operator
3. Register the operator in the theory's operator collection
4. Add test cases in `examples.py` or test files

### Working with Jupyter Integration
1. Start the Jupyter server: `./run_jupyter.sh`
2. Use high-level functions: `check_formula()`, `find_countermodel()`
3. For interactive exploration: `ModelExplorer().display()`
4. For theory-specific demos: Navigate to theory-specific notebook directories

### Debugging Issues
1. Check logs and error messages for tracebacks
2. Use the debugging tools in `jupyter/debug/`
3. Review the debug logging in `__main__.py` and `cli.py`
4. Follow the systematic debugging approach in `jupyter/debug/DEBUGGING.md`

## Known Challenges

1. **Theory Compatibility**: Different theories may have incompatible operators or semantics. Use the theory adapter system for conversion.

2. **NixOS Path Issues**: On NixOS, PYTHONPATH management is critical. Use the provided scripts (`run_jupyter.sh`, `dev_cli.py`) instead of direct commands.

3. **Z3 Solver Limitations**: 
   - Complex models may hit solver timeouts (adjust the max_time setting)
   - Some logical structures may be undecidable or exceed bitvector capacity

4. **Jupyter Widget Display**: If widgets don't display properly, ensure ipywidgets is properly installed and nbextensions are enabled.

## Key API Examples

### Basic Model Checking
```python
from model_checker import BuildExample, get_theory

# Load a theory
theory = get_theory("default")

# Create a model
model = BuildExample("simple_modal", theory)

# Check a formula 
result = model.check_formula("\\Box p -> p")

# Analyze the result
print(f"Formula is {'valid' if result else 'invalid'}")
```

### Jupyter Integration
```python
# Simple formula checking
from model_checker import check_formula
result = check_formula("p → (q → p)")

# With premises
check_formula("q", premises=["p", "p → q"])

# Interactive exploration
from model_checker import ModelExplorer
explorer = ModelExplorer()
explorer.display()
```

### Creating a New Theory
```python
# In theory_lib/__init__.py
AVAILABLE_THEORIES = [
    'default',
    'exclusion',
    'imposition',
    'my_new_theory',  # Add your theory here
]

# Then implement:
# theory_lib/my_new_theory/semantic.py
# theory_lib/my_new_theory/operators.py 
# theory_lib/my_new_theory/examples.py
```
