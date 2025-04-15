import sys
import os
import importlib
from CodeToClassDiagram.config import load_config, load_internal_config, init_config_file

def validate_config(config, internal_config):
    inp_type = config.get("input_filetype")
    out_type = config.get("output", {}).get("diagram")
    
    if inp_type not in internal_config.get("input_filetype_mapping", {}):
        print(f"Erreur : l'input_filetype '{inp_type}' n'est pas supporté dans la config interne.")
        sys.exit(1)
    if out_type not in internal_config.get("output_diagram_mapping", {}):
        print(f"Erreur : le diagramme '{out_type}' n'est pas supporté dans la config interne.")
        sys.exit(1)

def dynamic_import(module_path):
    module_dot = module_path.replace("/", ".").removesuffix(".py")
    try:
        return importlib.import_module(module_dot)
    except Exception as e:
        print(f"Erreur lors de l'importation du module '{module_dot}' : {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  code2class init [config_file]  # Crée le fichier de configuration par défaut")
        print("  code2class <folder_path> <config_file>  # Exécute le parsing et génère le diagramme")
        sys.exit(1)

    # Mode init : permet de générer le config.json par défaut
    if sys.argv[1] == "init":
        # Si un second argument est passé, on le considère comme le chemin du config.json à créer
        config_path = sys.argv[2] if len(sys.argv) >= 3 else "config.json"
        init_config_file(config_path)
        sys.exit(0)

    # Mode exécution classique
    if len(sys.argv) != 3:
        print("Usage: code2class <folder_path> <config_file>")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    config_path = sys.argv[2]
    
    # Charge la configuration externe : si le fichier n'existe pas, il est créé automatiquement
    config = load_config(config_path)
    internal_config = load_internal_config()
    
    validate_config(config, internal_config)
    
    input_type = config.get("input_filetype")
    parser_module_path = internal_config["input_filetype_mapping"][input_type]
    parser_module = dynamic_import(parser_module_path)
    
    output_obj = config.get("output", {})
    output_type = output_obj.get("diagram")
    diagram_module_path = internal_config["output_diagram_mapping"][output_type]
    diagram_module = dynamic_import(diagram_module_path)
    
    classes = parser_module.parse_project(folder_path, exclude_files=config.get("exclude_files"))
    
    try:
        diagram_generator = diagram_module.create_generator(classes, output_obj)
    except AttributeError:
        print("Erreur : Le module diagram ne fournit pas la fonction 'create_generator'.")
        sys.exit(1)
    
    diagram = diagram_generator.generate()
    
    if output_obj.get("mode", "console") == "file":
        output_file = output_obj.get("file", "diagram.md")
        try:
            with open(output_file, "w", encoding="utf-8") as out:
                out.write(diagram)
            print(f"Diagramme écrit dans {output_file}")
        except Exception as e:
            print(f"Erreur lors de l'écriture du fichier : {e}")
    else:
        print("Diagramme généré :")
        print(diagram)

if __name__ == "__main__":
    main()
