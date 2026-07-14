HTTP_401_RESPONSE = {
    "description": "Authentication required. A valid JWT access token must be provided."
}

HTTP_404_RESPONSE = {
    "description": (
        "The requested resource was not found. "
        "For tasks, this also includes resources owned by another user."
    )
}

HTTP_422_RESPONSE = {
    "description": "Validation error. The request data is invalid."
}