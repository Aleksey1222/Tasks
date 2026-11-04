try:
    import colorama
    colorama.init(autoreset=True)
    COLOR = True
except ImportError:
    colorama = None
    COLOR = False

GREEN_TEXT = colorama.Fore.GREEN if COLOR else ""
RESET_TEXT = colorama.Style.RESET_ALL if COLOR else ""

def get_status_line(message: str) -> str:
    """Возвращает зелёную строку состояния при COLOR=True и обычную без неё."""
    return f"{GREEN_TEXT}{message}{RESET_TEXT}"

if __name__ == "__main__":
    print(get_status_line("Здоровье: 100% | Мана: 50%"))

#Lib5
CYAN_TEXT = colorama.Fore.CYAN if COLOR else ""
def print_victory_message() -> None:
    print(f"{CYAN_TEXT}Вы победили врага и очистили комнату подземелья!{RESET_TEXT}")

if __name__ == "__main__":
    print(get_status_line("Здоровье: 100% | Мана: 50%"))
    
    print_victory_message()
