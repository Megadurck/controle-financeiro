TEMAS = {
    "dark": {
        "background": "#121212",
        "surface": "#1E1E1E",
        "primary": "#BB86FC",
        "secondary": "#03DAC6",
        "text": "#FFFFFF",
        "error": "#CF6679",
        "frame": "#252525",
        "card": "#2D2D2D",
        "tab_unselected": "#333333",
        "text_secondary": "#B3B3B3"
    },
    "blue": {
        "background": "#1A1B1E",
        "surface": "#202225",
        "primary": "#2196F3",
        "secondary": "#64B5F6",
        "text": "#FFFFFF",
        "error": "#F44336",
        "frame": "#252830",
        "card": "#2F3037",
        "tab_unselected": "#2A2D35",
        "text_secondary": "#B3B3B3"
    },
    "material": {
        "background": "#0A1929",
        "surface": "#132F4C",
        "primary": "#007FFF",
        "secondary": "#3399FF",
        "text": "#FFFFFF",
        "error": "#EB0014",
        "frame": "#1A3B57",
        "card": "#173A5E",
        "tab_unselected": "#1E3A54",
        "text_secondary": "#B3B3B3"
    },
    "cyber": {
        "background": "#000000",
        "surface": "#1A1A1A",
        "primary": "#00FF9C",
        "secondary": "#00F0FF",
        "text": "#FFFFFF",
        "error": "#FF0055",
        "frame": "#202020",
        "card": "#252525",
        "tab_unselected": "#1A1A1A",
        "text_secondary": "#B3B3B3"
    }
}

def obter_proximo_tema(tema_atual):
    temas = list(TEMAS.keys())
    atual = temas.index(tema_atual)
    return temas[(atual + 1) % len(temas)] 