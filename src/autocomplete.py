import os
import glob
import readline

def autocomplete_main():
    mains_dir = "./mains/"
    main_files = [f for f in os.listdir(mains_dir) if os.path.isfile(os.path.join(mains_dir, f)) and f.startswith("main_")]
    def complete(text, state):
        options = [f[len(mains_dir):] for f in glob.glob(mains_dir + "main_" + text + "*.py")]
        if state < len(options):
            return options[state]
        else:
            return None
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)
    input_str = str(input("Enter something: "))
    main = "main_" + input_str.replace("main_","")
    if "py" not in main: main = main + ".py"
    matches = glob.glob(os.path.join(mains_dir, main))
    if len(matches) == 1:
        return matches[0][len(mains_dir):]
    elif len(matches) > 1:
        print("Multiple matches found:")
        for match in matches:
            print(match[len(mains_dir):])
        return None
    else:
        print("No matches found.")
        return None