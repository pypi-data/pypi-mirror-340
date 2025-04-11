from typing import Final, Tuple

from alkindi import core
from alkindi.core import OQS_SUCCESS

STANDARDIZED_KEM_ALGORITHMS: Final[set[str]] = {
    "ML-KEM-512",
    "ML-KEM-768",
    "ML-KEM-1024",
}

liboqs = core.liboqs
ffi = core.ffi


class KEM:
    """
    A Python wrapper for the C liboqs OQS_KEM struct, providing a KEM scheme interface.

    This class encapsulates keypair generation, encapsulation, and decapsulation operations,
    mirroring key fields of the underlying OQS_KEM struct for clarity. It manages resources
    via the context manager protocol and supports various key encapsulation mechanism algorithms.

    Method mappings to C liboqs:
        Python            |  C liboqs
        ------------------|------------
        generate_keypair  |  OQS_KEM_keypair
        encaps            |  OQS_KEM_encaps
        decaps            |  OQS_KEM_decaps
    """

    __slots__ = (
        "_kem",
        "_secret_key_ptr",
        "length_secret_key",
        "length_public_key",
        "length_ciphertext",
        "length_shared_secret",
    )


    def __init__(self, alg_name: str) -> None:
        """
        Initialize the KEM scheme with a given algorithm.

        Constructs an OQS_KEM object and checks for NULL returns, indicating an invalid
        or disabled algorithm at compile-time.

        Args:
            alg_name (str): A supported KEM algorithm name from STANDARDIZED_KEM_ALGORITHMS.

        Raises:
            ValueError: If alg_name is not in STANDARDIZED_KEM_ALGORITHMS or not supported by liboqs.
        """
        if alg_name not in STANDARDIZED_KEM_ALGORITHMS:
            raise ValueError(
                f"Algorithm must be one of {STANDARDIZED_KEM_ALGORITHMS}, got {alg_name}"
            )

        kem = liboqs.OQS_KEM_new(alg_name.encode("utf-8"))
        
        if kem == ffi.NULL:
            raise ValueError(f"Algorithm {alg_name} is not supported by liboqs")

        self._kem = kem
        self._secret_key_ptr = None
        self.length_public_key = self._kem.length_public_key
        self.length_secret_key = self._kem.length_secret_key
        self.length_ciphertext = self._kem.length_ciphertext
        self.length_shared_secret = self._kem.length_shared_secret


    def __enter__(self) -> "KEM":
        """
        Enter the context manager, providing the KEM instance for use in a `with` block.

        Runs at the start of a `with` statement (e.g., `with KEM("algorithm") as kem:`).
        No additional setup is performed beyond `__init__`.

        Returns:
            KEM: The current instance, ready for encapsulation operations.
        """
        return self


    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Exit the context manager, freeing the OQS_KEM object to prevent memory leaks.

        Called when the `with` block ends, ensuring proper cleanup of C resources.

        Args:
            exc_type: Type of exception (if any), else None.
            exc_value: Exception instance (if any), else None.
            traceback: Traceback object (if any), else None.
        """
        if self._secret_key_ptr is not None:
            liboqs.OQS_MEM_cleanse(self._secret_key_ptr, self.length_secret_key)
            self._secret_key_ptr = None

        if self._kem is not None:
            liboqs.OQS_KEM_free(self._kem)
            self._kem = None


    def generate_keypair(self) -> Tuple[bytes, bytes]:
        """
        Generate a keypair (public/secret) for the KEM scheme.

        Allocates memory for public_key and secret_key based on self.length_public_key
        and self.length_secret_key, then invokes the C keypair generation function.

        Returns:
            Tuple[bytes, bytes]: A tuple of (public_key, secret_key) as Python bytes objects.

        Raises:
            RuntimeError: If keypair generation fails (e.g., due to internal liboqs error).
            MemoryError: If memory allocation fails for public or secret key.
        """
        public_key = ffi.new("uint8_t[]", self.length_public_key)
        if public_key == ffi.NULL:
            raise MemoryError("Failed to allocate memory for the public key")

        secret_key = ffi.new("uint8_t[]", self.length_secret_key)
        if secret_key == ffi.NULL:
            raise MemoryError("Failed to allocate memory for the secret key")

        result = liboqs.OQS_KEM_keypair(self._kem, public_key, secret_key)

        if result != OQS_SUCCESS:
            raise RuntimeError("Failed to generate the keypair")

        self._secret_key_ptr = secret_key

        return ffi.buffer(public_key, self.length_public_key), ffi.buffer(secret_key, self.length_secret_key)


    def encaps(self, public_key: bytes) -> Tuple[bytes, bytes]:
        """
        Encapsulation algorithm.

        Allocates memory for ciphertext and shared_secret based on self.length_ciphertext
        and self.length_shared_secret, then invokes the C encapsulation function.

        Args:
            public_key (bytes): The public key from generate_keypair, must match self.length_public_key.

        Returns:
            Tuple[bytes, bytes]: A tuple of (ciphertext, shared_secret) as Python bytes objects.

        Raises:
            ValueError: If public_key length does not match self.length_public_key.
            RuntimeError: If encapsulation fails (e.g., due to internal liboqs error).
            MemoryError: If memory allocation fails for ciphertext or shared secret.
        """
        if len(public_key) != self.length_public_key:
            raise ValueError(
                f"Public key must be {self.length_public_key} bytes, got {len(public_key)}"
            )

        ciphertext = ffi.new("uint8_t[]", self.length_ciphertext)
        if ciphertext == ffi.NULL:
            raise MemoryError("Failed to allocate memory for the ciphertext")

        shared_secret = ffi.new("uint8_t[]", self.length_shared_secret)
        if shared_secret == ffi.NULL:
            raise MemoryError("Failed to allocate memory for the shared secret")

        result = liboqs.OQS_KEM_encaps(
            self._kem, ciphertext, shared_secret, ffi.from_buffer(public_key)
        )

        if result != OQS_SUCCESS:
            raise RuntimeError(
                f"Failed to encapsulate the shared secret"
            )

        return ffi.buffer(ciphertext, self.length_ciphertext), ffi.buffer(shared_secret, self.length_shared_secret)


    def decaps(self, ciphertext: bytes, secret_key: bytes) -> bytes:
        """
        Decapsulation algorithm.

        Allocates memory for shared_secret based on self.length_shared_secret, then invokes
        the C decapsulation function to recover the shared secret.

        Args:
            ciphertext (bytes): The ciphertext from encaps, must match self.length_ciphertext.
            secret_key (bytes): The secret key from generate_keypair, must match self.length_secret_key.

        Returns:
            bytes: The shared secret as a Python bytes object.

        Raises:
            ValueError: If ciphertext or secret_key length does not match expected values.
            RuntimeError: If decapsulation fails (e.g., due to internal liboqs error).
            MemoryError: If memory allocation fails for shared secret.
        """
        if len(ciphertext) != self.length_ciphertext:
            raise ValueError(
                f"Ciphertext must be {self.length_ciphertext} bytes, got {len(ciphertext)}"
            )
        if len(secret_key) != self.length_secret_key:
            raise ValueError(
                f"Secret key must be {self.length_secret_key} bytes, got {len(secret_key)}"
            )

        shared_secret = ffi.new("uint8_t[]", self.length_shared_secret)
        if shared_secret == ffi.NULL:
            raise MemoryError("Failed to allocate memory for the shared secret")

        result = liboqs.OQS_KEM_decaps(
            self._kem,
            shared_secret,
            ffi.from_buffer(ciphertext),
            ffi.from_buffer(secret_key),
        )

        if result != OQS_SUCCESS:
            raise RuntimeError(
                f"Failed to decapsulate the shared secret"
            )

        return ffi.buffer(shared_secret, self.length_shared_secret)


__all__ = ["KEM"]
