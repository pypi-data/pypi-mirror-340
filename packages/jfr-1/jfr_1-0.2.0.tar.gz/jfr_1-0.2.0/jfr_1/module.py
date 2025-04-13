# jfr_1/module.py

import inspect
from .storage import load_all, save_all

# Store algorithms in a list
algorithms = []

def register_algorithm(name, function, description):
    """Register a new algorithm and save it."""
    algorithms.append({
        'name': name,
        'function': function,
        'description': description
    })

    # Save source code to JSON
    try:
        source = inspect.getsource(function)
        data = load_all()
        data.append({
            'name': name,
            'description': description,
            'source_code': source
        })
        save_all(data)
    except Exception as e:
        print(f"[ERROR] Could not save {name}: {e}")

def list_algorithms():
    """List all registered algorithms."""
    return [algo['name'] for algo in algorithms]

def get_algorithm(name):
    """Retrieve an algorithm by name."""
    for algo in algorithms:
        if algo['name'] == name:
            return algo
    raise ValueError(f"Algorithm '{name}' not found.")
