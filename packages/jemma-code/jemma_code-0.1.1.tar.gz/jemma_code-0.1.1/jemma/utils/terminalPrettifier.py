from colorama import Fore, Style, init

# Initialize colorama for Windows compatibility
init(autoreset=True)


import re
 

def responseFormatter(text: str):
    if text is None:
        return ''
    
    reset = Style.RESET_ALL
    
 
    def bold_replacer(match):
        return Style.BRIGHT + Fore.YELLOW + match.group(1) + reset
    text = re.sub(r'\*\*(.*?)\*\*', bold_replacer, text)
    
 
    def italic_replacer(match):
        return Fore.CYAN + match.group(1) + reset
    text = re.sub(r'\*(.*?)\*', italic_replacer, text)
    
 
    def code_replacer(match):
        return Fore.GREEN + match.group(1) + reset
    text = re.sub(r'\`(.*?)\`', code_replacer, text)
    
 
    text = text.replace('Framework:', "\n" + Fore.MAGENTA + "Framework:" + reset)
    text = text.replace('Critical Logic:', "\n" + Fore.MAGENTA + "Critical Logic:" + reset)
    text = text.replace('Potential Issues:', "\n" + Fore.RED + "Potential Issues:" + reset)

    return text


def errorText(text: str):
    formatted = Style.BRIGHT + Fore.RED + text
    return formatted

def warningText(text: str):
    formatted = Style.BRIGHT + Fore.YELLOW + text
    return formatted

def successText(text: str):
    formatted = Style.BRIGHT + Fore.GREEN + text
    return formatted

def colouredText( text: str, colour: str, textStyle: str):
    formatted = Style.textStyle + Fore.colour + text
    return formatted