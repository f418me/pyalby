"""
Test module for verifying package imports and exports.
Tests that both sync and async classes can be imported successfully
and that __all__ exports work correctly.
"""

import pytest


def test_sync_class_imports():
    """Test that all sync classes can be imported from the main package."""
    from pyalby import Account, Invoice, Payment
    
    # Verify classes are importable and are the correct types
    assert Account is not None
    assert Invoice is not None
    assert Payment is not None
    
    # Verify they are classes
    assert isinstance(Account, type)
    assert isinstance(Invoice, type)
    assert isinstance(Payment, type)


def test_async_class_imports():
    """Test that all async classes can be imported from the main package."""
    from pyalby import AsyncAccount, AsyncInvoice, AsyncPayment
    
    # Verify classes are importable and are the correct types
    assert AsyncAccount is not None
    assert AsyncInvoice is not None
    assert AsyncPayment is not None
    
    # Verify they are classes
    assert isinstance(AsyncAccount, type)
    assert isinstance(AsyncInvoice, type)
    assert isinstance(AsyncPayment, type)


def test_mixed_imports():
    """Test that sync and async classes can be imported together."""
    from pyalby import Account, AsyncAccount, Invoice, AsyncInvoice, Payment, AsyncPayment
    
    # Verify all classes are available
    classes = [Account, AsyncAccount, Invoice, AsyncInvoice, Payment, AsyncPayment]
    for cls in classes:
        assert cls is not None
        assert isinstance(cls, type)


def test_all_exports():
    """Test that __all__ exports work correctly."""
    import pyalby
    
    # Verify __all__ contains expected classes
    expected_classes = ['Account', 'Invoice', 'Payment', 'AsyncAccount', 'AsyncInvoice', 'AsyncPayment']
    assert hasattr(pyalby, '__all__')
    assert set(pyalby.__all__) == set(expected_classes)
    
    # Verify all classes in __all__ are actually available
    for class_name in pyalby.__all__:
        assert hasattr(pyalby, class_name)
        cls = getattr(pyalby, class_name)
        assert isinstance(cls, type)


def test_star_import():
    """Test that 'from pyalby import *' works correctly."""
    # This test uses exec to simulate star import
    namespace = {}
    exec("from pyalby import *", namespace)
    
    # Verify all expected classes are in the namespace
    expected_classes = ['Account', 'Invoice', 'Payment', 'AsyncAccount', 'AsyncInvoice', 'AsyncPayment']
    for class_name in expected_classes:
        assert class_name in namespace
        assert isinstance(namespace[class_name], type)


def test_backward_compatibility():
    """Test that existing import patterns still work (backward compatibility)."""
    # Test individual class imports (existing pattern)
    from pyalby.account import Account
    from pyalby.invoice import Invoice
    from pyalby.payment import Payment
    
    # Test async class imports (new pattern)
    from pyalby.async_account import AsyncAccount
    from pyalby.async_invoice import AsyncInvoice
    from pyalby.async_payment import AsyncPayment
    
    # Verify all are classes
    classes = [Account, Invoice, Payment, AsyncAccount, AsyncInvoice, AsyncPayment]
    for cls in classes:
        assert isinstance(cls, type)


def test_class_names():
    """Test that imported classes have correct names."""
    from pyalby import Account, Invoice, Payment, AsyncAccount, AsyncInvoice, AsyncPayment
    
    # Test sync class names
    assert Account.__name__ == 'Account'
    assert Invoice.__name__ == 'Invoice'
    assert Payment.__name__ == 'Payment'
    
    # Test async class names
    assert AsyncAccount.__name__ == 'AsyncAccount'
    assert AsyncInvoice.__name__ == 'AsyncInvoice'
    assert AsyncPayment.__name__ == 'AsyncPayment'