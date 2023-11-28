def evaluate_severity(severity: str) -> bool:
    # Ensure the severity is not None or empty
    if not severity:
        return False

    severity = severity.lower().strip()

    # Handle textual severity labels
    low_severity_labels: list = ['low', 'medium']
    if any(label in severity for label in low_severity_labels):
        return False

    # Handle numeric severity scores
    severity_parts = severity.split()
    if severity_parts:
        try:
            score = float(severity_parts[0])
            if score < 7.5:
                return False
        except ValueError:
            pass  # If conversion to float fails, proceed without excluding

    return True  # Include the CVE if it doesn't match the exclusion criteria, for just-in-case
