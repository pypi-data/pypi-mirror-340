__version__ = "0.1.5"

# Importar las clases
from aletheia_quantum_genetic_optimizer.individuals import Individual
from aletheia_quantum_genetic_optimizer.bounds import BoundCreator
from aletheia_quantum_genetic_optimizer.genetic_optimizer import GenethicOptimizer

# Exportar las clases para que sean accesibles directamente desde el paquete
__all__ = ['Individual', 'BoundCreator', 'GenethicOptimizer']
