import json
import sys
import os

try:
    # Pour Python ≥ 3.9, on peut utiliser importlib.resources
    import importlib.resources as pkg_resources
except ImportError:
    import pkg_resources

def load_config(config_path):
    """
    Charge le fichier de configuration externe (user) depuis le chemin donné.
    Si le fichier n'existe pas dans le dossier courant, on peut le créer à partir
    de la version d'exemple embarquée.
    """
    if not os.path.exists(config_path):
        # Copie du fichier d'exemple embarqué dans le dossier courant
        try:
            with pkg_resources.open_text('CodeToClassDiagram.configs', 'config.json') as src:
                default_config_data = src.read()
            with open(config_path, 'w', encoding='utf-8') as dest:
                dest.write(default_config_data)
            print(f"{config_path} créé à partir de la configuration par défaut.")
        except Exception as e:
            print(f"Erreur lors de la création du fichier de config: {e}")
            sys.exit(1)
    
    # Charger la config utilisateur en appliquant les valeurs par défaut
    default_config = {
        "exclude_files": [],
        "input_filetype": "Csharp",
        "output": {
            "mode": "console",
            "file": "diagram.md",
            "diagram": "MermaidClassDiagram",
            "hide_implemented_interface_methods": True,
            "hide_implemented_interface_properties": True,
            "exclude_namespaces": [],
            "show_dependencies": False
        }
    }
    try:
        with open(config_path, "r", encoding="utf-8") as cf:
            user_config = json.load(cf)
            default_config.update(user_config)
    except Exception as e:
        print(f"Erreur lors du chargement du fichier de config : {e}")
        sys.exit(1)
    return default_config

def load_internal_config():
    """
    Charge le fichier de configuration interne embarqué dans le package.
    """
    try:
        with pkg_resources.open_text('CodeToClassDiagram.configs', 'internal_config.json') as f:
            internal_config = json.load(f)
    except Exception as e:
        print(f"Erreur lors du chargement de la configuration interne : {e}")
        sys.exit(1)
    return internal_config

def init_config_file(config_path):
    """
    Copie le fichier de configuration par défaut depuis le package vers config_path.
    """
    try:
        with pkg_resources.open_text('CodeToClassDiagram.configs', 'config.json') as src:
            default_config_data = src.read()
        with open(config_path, 'w', encoding='utf-8') as dest:
            dest.write(default_config_data)
        print(f"Fichier de configuration par défaut créé en {config_path}.")
    except Exception as e:
        print(f"Erreur lors de la création du fichier de configuration : {e}")
        sys.exit(1)