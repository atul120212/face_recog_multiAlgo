import importlib.util
import json
import os
from detector import process_frame
from recognize import Recogonise

def run_file(filename):
    # Load the specified module
    spec = importlib.util.spec_from_file_location("module.name", filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if hasattr(module, 'run'):
        module.run()
    else:
        print(f"The file {filename} does not have a 'run' function.")

def main():
    config_filename = 'config.json'
    
    if not os.path.isfile(config_filename):
        print(f"Configuration file {config_filename} not found.")
        return
    
    try:
        with open(config_filename, 'r') as config_file:
            config = json.load(config_file)
        
        print(config['IsF1'])

        if config['IsF1']=="1":
            Recogonise('testvideo.mp4')
        # elif config['IsF1']=="":
        #     #process_frame()
        elif config['IsF3']=="1":
            print("printing f3")
            process_frame('testvideo.mp4')

        # for filename, should_run in config.items():
        #     if should_run:
        #         if os.path.isfile(filename):
        #             run_file(filename)
        #         else:
        #             print(f"File {filename} does not exist.")
        #     else:
        #         print(f"Skipping {filename}.")
    
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file {config_filename}.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
