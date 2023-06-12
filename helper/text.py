from pyfiglet import figlet_format

def text(main: bool = False, path=""):
    print(figlet_format("Sitorsi"))
    if not main:
        print(f"🏠 {path} \n")