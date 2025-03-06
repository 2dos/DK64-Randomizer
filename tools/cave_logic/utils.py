def deep_merge(dict1, dict2):
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result

def array_to_object(arr):
    obj = {}
    for item in arr:
        if "Key" in item:
            obj[item["Key"]] = item
        else:
            obj[item["Name"]] = item
    return obj
