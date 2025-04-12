# setup.py
from setuptools import setup, find_packages
import os
import re
import sys

# --- Helper Functions ---

def get_version(package_name):
    """
    Return package version as listed in `__version__` in `init.py`.
    Reads the version dynamically from the package's __init__.py file.
    """
    try:
        # Construct the path to the __init__.py file
        init_py_path = os.path.join(package_name, '__init__.py')
        # Open and read the file content
        with open(init_py_path, 'r', encoding='utf-8') as init_py_file:
            init_py_content = init_py_file.read()
        # Use regex to find the __version__ string
        match = re.search(r"""^__version__\s*=\s*['"]([^'"]+)['"]""", init_py_content, re.MULTILINE)
        if match:
            return match.group(1) # Return the matched version string
        # Raise error if __version__ is not found
        raise RuntimeError(f"Unable to find __version__ string in {init_py_path}.")
    except FileNotFoundError:
        # Raise error if __init__.py file itself is missing
        raise RuntimeError(f"Could not find {init_py_path} to read version.")
    except Exception as e:
        # Raise error for any other exceptions during reading
        raise RuntimeError(f"Error reading version from {init_py_path}: {e}")

def get_long_description(file_path="README.md"):
    """
    Return the contents of the README file for the long description.
    Handles cases where the README file might be missing.
    """
    base_dir = os.path.abspath(os.path.dirname(__file__))
    readme_path = os.path.join(base_dir, file_path)
    # Check if README file exists
    if not os.path.exists(readme_path):
        # Print a warning and return a short fallback description
        print(f"WARNING: {file_path} not found. Using short description only.", file=sys.stderr)
        return "TrainSense: Toolkit for PyTorch analysis, profiling, and optimization." # Short fallback
    try:
        # Read the content of the README file
        with open(readme_path, encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        # Print a warning and return fallback description if reading fails
        print(f"WARNING: Could not read {file_path}: {e}", file=sys.stderr)
        return "TrainSense: Toolkit for PyTorch analysis, profiling, and optimization." # Short fallback

# --- Package Definition ---

PACKAGE_NAME = "TrainSense"
# Read version dynamically from __init__.py using the helper function
VERSION = get_version(PACKAGE_NAME)

# Core dependencies - absolutely required to run the main features
CORE_DEPS = [
    'psutil>=5.8.0',        # For system diagnostics (CPU, RAM)
    'torch>=1.8.0',         # Core dependency for PyTorch interaction
    'GPUtil>=1.4.0'         # For GPU monitoring features (optional at runtime if unavailable)
]

# Optional dependencies grouped by feature
EXTRAS_DEPS = {
    'plotting': [           # Dependencies for generating plots
        'matplotlib>=3.3.0',
        'numpy'             # Often needed with matplotlib for array operations
    ],
    'html': [               # Dependencies for generating HTML reports
        'jinja2>=3.0.0'
    ],
    'trl': [                # Dependencies for Hugging Face TRL Callback integration
        'transformers>=4.0.0' # Added for potential Transformer support/integration
    ],
    'dev': [                # Dependencies for development and testing
        'pytest>=6.0',      # Testing framework
        'flake8>=3.8',      # Code linting
        'black>=21.0b0',    # Code formatting
        'coverage>=5.0',    # Code coverage measurement
        'mypy>=0.900',      # Optional: Static type checking
        'ipykernel',        # For running Jupyter notebooks if used in dev
    ]
}

# Create an 'all' extra that includes common optional features
EXTRAS_DEPS['all'] = EXTRAS_DEPS['plotting'] + EXTRAS_DEPS['html'] + EXTRAS_DEPS['trl']

setup(
    name=PACKAGE_NAME,
    version=VERSION,        # Version read dynamically
    author="RDTvlokip",
    author_email="rdtvlokip@gmail.com", # Public email
    description="Toolkit for PyTorch model analysis, profiling, and training optimization.", # Concise description
    long_description=get_long_description(), # Read from README.md
    long_description_content_type="text/markdown", # Specify README format
    url="https://github.com/RDTvlokip/TrainSense", # Project URL
    project_urls={ # Additional relevant links
        'Bug Tracker': 'https://github.com/RDTvlokip/TrainSense/issues',
        'Source Code': 'https://github.com/RDTvlokip/TrainSense',
        # 'Documentation': f'https://{PACKAGE_NAME}.readthedocs.io/en/latest/', # Example link for docs
    },
    license="MIT", # Specify the license
    license_files=('LICENSE',), # Include the LICENSE file in the distribution
    packages=find_packages(exclude=["tests*", "examples*"]), # Automatically find packages, exclude test/example folders
    install_requires=CORE_DEPS, # Core dependencies
    extras_require=EXTRAS_DEPS, # Optional dependencies
    python_requires='>=3.7', # Specify minimum Python version compatibility
    keywords=[ # Keywords for discoverability on PyPI
        "pytorch", "torch", "deep learning", "machine learning", "ai",
        "profiling", "profiler", "performance", "optimization", "analysis",
        "diagnostics", "monitoring", "gpu", "cuda", "nvidia", "memory usage",
        "gradients", "training", "debugging", "developer tools", "mlops",
        "hyperparameters", "dataloader", "trainsense", # Include package name
        "hyperparameter tuning", "transformers", "explainability", # Added keywords for 0.5.0 scope
    ],
    # Entry points for potential future CLI tools (currently commented out)
    # entry_points={
    #     'console_scripts': [
    #         'trainsense-analyze=TrainSense.cli:main_analyze', # Example entry point
    #     ],
    # },
    classifiers=[ # PyPI classifiers for categorization and filtering
        # Development Status: 4 - Beta (Still under active development, potential API changes)
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License", # Standard classifier for MIT license
        "Operating System :: OS Independent", # Should work on Windows, macOS, Linux
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12", # Include recent Python versions
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring", # Relevant topic for monitoring features
        "Topic :: Utilities", # Fits the "toolkit" nature of the package
        "Typing :: Typed", # Indicates the package uses type hints
    ],
)