# deterministic_uuid_from_email.py
import uuid
import unicodedata

def deterministic_uuid_from_email(email: str, namespace: uuid.UUID = uuid.NAMESPACE_DNS) -> uuid.UUID:
    """
    Return a deterministic UUIDv5 for the given email.
    By default uses the DNS namespace; you can provide a custom uuid.UUID namespace.
    """
    # Normalize: strip spaces, Unicode normalize, lowercase
    normalized = unicodedata.normalize("NFKC", email.strip().lower())
    return uuid.uuid5(namespace, normalized)

# Example
if __name__ == "__main__":
    emails = ["Alice@example.com", " alice@example.com ", "ALICE@EXAMPLE.COM"]
    for e in emails:
        print(e, "->", deterministic_uuid_from_email(e))