import streamlit as st
from typing import Any, List, Optional, Set


class StateManager:
    """
    State Manager for Streamlit applications that combines a static interface
    """

    @staticmethod
    def _get_key(namespace: Optional[str], key: str) -> str:
        """Generate a full key with optional namespace prefix."""
        if namespace:
            return f"{namespace}_{key}"
        return key

    @classmethod
    def exists(cls, key: str, namespace: Optional[str] = None) -> bool:
        """Check if a key exists in session state."""
        full_key = cls._get_key(namespace, key)
        return full_key in st.session_state

    @classmethod
    def init(
        cls, key: str, default_value: Any = None, namespace: Optional[str] = None
    ) -> Any:
        """Initialize a key with a default value if it doesn't exist."""
        full_key = cls._get_key(namespace, key)
        if full_key not in st.session_state:
            st.session_state[full_key] = default_value
        return st.session_state[full_key]

    @classmethod
    def get(
        cls, key: str, default_value: Any = None, namespace: Optional[str] = None
    ) -> Any:
        """Get a value from session state, initializing it if needed."""
        return cls.init(key, default_value, namespace)

    @classmethod
    def set(cls, key: str, value: Any, namespace: Optional[str] = None) -> None:
        """Set a value in session state."""
        full_key = cls._get_key(namespace, key)
        st.session_state[full_key] = value

    @classmethod
    def delete(cls, key: str, namespace: Optional[str] = None) -> None:
        """Delete a key from session state if it exists."""
        full_key = cls._get_key(namespace, key)
        if full_key in st.session_state:
            del st.session_state[full_key]

    @classmethod
    def clear_namespace(cls, namespace: str) -> None:
        """Clear all keys belonging to a specific namespace."""
        prefix = f"{namespace}_"
        keys_to_delete = [
            key for key in st.session_state.keys() if key.startswith(prefix)
        ]
        for key in keys_to_delete:
            del st.session_state[key]

    @classmethod
    def clear_all(cls) -> None:
        """Clear all keys in session state."""
        for key in list(st.session_state.keys()):
            del st.session_state[key]

    @classmethod
    def get_keys(cls, namespace: Optional[str] = None) -> List[str]:
        """Get all keys or keys in a specific namespace."""
        if namespace:
            prefix = f"{namespace}_"
            return [key for key in st.session_state.keys() if key.startswith(prefix)]
        return list(st.session_state.keys())

    @classmethod
    def get_namespaces(cls) -> Set[str]:
        """Get all namespaces currently in use."""
        namespaces = set()
        for key in st.session_state.keys():
            if "_" in key:
                namespace = key.split("_", 1)[0]
                namespaces.add(namespace)
        return namespaces
