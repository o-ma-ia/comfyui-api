def replace_placeholders(data, variables_dict):
    if isinstance(data, dict):
        return {k: replace_placeholders(v, variables_dict) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_placeholders(element, variables_dict) for element in data]
    elif isinstance(data, str):
        placeholder = data.strip('<>')
        if placeholder in variables_dict:
            return variables_dict[placeholder]
        else:
            for key, value in variables_dict.items():
                placeholder = f"<{key}>"
                if placeholder in data:
                    data = data.replace(placeholder, str(value))
            return data
    else:
        return data