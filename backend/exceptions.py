"""Application-specific HTTP exceptions for inference errors."""


class UnknownCategoryError(ValueError):
  """Raised when a categorical value is absent from the training vocabulary."""

  def __init__(self, field: str, value: str, allowed: list[str]) -> None:
    self.field = field
    self.value = value
    self.allowed = allowed
    preview = ", ".join(allowed[:5])
    suffix = "..." if len(allowed) > 5 else ""
    message = (
      f"Unknown {field}: '{value}'. "
      f"Allowed values include: {preview}{suffix}"
    )
    super().__init__(message)
