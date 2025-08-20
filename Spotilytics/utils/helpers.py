def truncate_text(text, max_length):
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text

def format_number(number): 
    return f"{number:,}".replace(",", ".")