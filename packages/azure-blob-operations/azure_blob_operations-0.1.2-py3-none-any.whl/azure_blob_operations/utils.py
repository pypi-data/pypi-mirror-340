def validate_params(**kwargs) -> None:
    """Validate that parameters are not None or empty."""
    for param_name, param_value in kwargs.items():
        if not param_value:
            raise ValueError(f"{param_name.replace('_', ' ').title()} is required")