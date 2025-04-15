# data/conversion.py (adjusted snippet)

def convert_parsed_type(raw: dict) -> ParsedType:
    kind = raw.get("kind", "")
    full_name = raw.get("name", "")
    base_name, generics = extract_generics(full_name)
    bases = raw.get("bases", [])
    namespace = raw.get("namespace", "Global")
    using_directives = raw.get("usings", [])
    
    parsed = ParsedType(
        kind=kind,
        name=base_name,
        namespace=namespace,
        generics=generics,
        bases=bases,
        using_directives=using_directives,
    )

    for raw_method in raw.get("methods", []):
        method = convert_method(raw_method)
        parsed.add_method(method)
    for raw_prop in raw.get("properties", []):
        prop = convert_property(raw_prop)
        parsed.add_property(prop)

    return parsed
