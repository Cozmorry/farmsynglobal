# backend/core/module_registry.py

PRODUCTION_MODULES = {
    "crop": ["agronomy", "hr", "finance", "store_inventory"],
    "livestock": ["hr", "finance", "store_inventory", "vet"],
    "poultry": ["hr", "finance", "store_inventory", "vet"],
    "aquaculture": ["hr", "finance", "store_inventory", "vet"],
}

DEPENDENT_MODULES = [
    "agronomy",
    "hr",
    "finance",
    "store_inventory",
    "vet",
]


def resolve_modules(selected_modules: list[str]) -> list[str]:
    """
    Expands selected production modules with their dependencies.
    Removes duplicates.
    """

    final_modules = set()

    for module in selected_modules:
        final_modules.add(module)

        if module in PRODUCTION_MODULES:
            dependencies = PRODUCTION_MODULES[module]
            for dep in dependencies:
                final_modules.add(dep)

    return list(final_modules)
