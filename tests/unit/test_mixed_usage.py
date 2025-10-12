"""
Test mixed sync/async usage patterns to ensure both can be used together.
"""
import asyncio
import pytest
import responses
from aioresponses import aioresponses

from pyalby import Account, AsyncAccount, Invoice, AsyncInvoice, Payment, AsyncPayment


class TestMixedSyncAsyncUsage:
    """Test cases for mixed sync/async usage patterns."""

    def test_mixed_imports(self):
        """Test that both sync and async classes can be imported together."""
        # This test verifies that importing both sync and async classes works
        assert Account is not None
        assert AsyncAccount is not None
        assert Invoice is not None
        assert AsyncInvoice is not None
        assert Payment is not None
        assert AsyncPayment is not None

    def test_mixed_class_instantiation(self):
        """Test that both sync and async classes can be instantiated together."""
        # Mock environment variables
        import os
        os.environ['BASE_URL'] = 'https://api.getalby.com'
        os.environ['ALBY_ACCESS_TOKEN'] = 'test_token'

        # Instantiate both sync and async classes
        sync_account = Account()
        async_account = AsyncAccount()
        sync_invoice = Invoice()
        async_invoice = AsyncInvoice()
        sync_payment = Payment()
        async_payment = AsyncPayment()

        # Verify they are different classes
        assert type(sync_account) != type(async_account)
        assert type(sync_invoice) != type(async_invoice)
        assert type(sync_payment) != type(async_payment)

        # Verify they have the same headers structure
        assert sync_account.headers == async_account.headers
        assert sync_invoice.headers == async_invoice.headers
        assert sync_payment.headers == async_payment.headers

    @responses.activate
    def test_sync_operations_with_async_classes_available(self):
        """Test that sync operations work normally when async classes are available."""
        import os
        os.environ['BASE_URL'] = 'https://api.getalby.com'
        os.environ['ALBY_ACCESS_TOKEN'] = 'test_token'

        # Mock sync API responses
        responses.add(
            responses.GET,
            'https://api.getalby.com/user/value4value',
            json={'lightning_address': 'test@getalby.com'},
            status=200
        )

        responses.add(
            responses.GET,
            'https://api.getalby.com/balance',
            json={'balance': 1000, 'currency': 'sat'},
            status=200
        )

        # Use sync classes
        account = Account()
        invoice = Invoice()

        # Test sync operations
        v4v_result = account.get_value4value()
        balance_result = account.get_balance()

        assert v4v_result['lightning_address'] == 'test@getalby.com'
        assert balance_result['balance'] == 1000

    @pytest.mark.asyncio
    async def test_async_operations_with_sync_classes_available(self):
        """Test that async operations work normally when sync classes are available."""
        import os
        os.environ['BASE_URL'] = 'https://api.getalby.com'
        os.environ['ALBY_ACCESS_TOKEN'] = 'test_token'

        # Mock async API responses
        with aioresponses() as m:
            m.get(
                'https://api.getalby.com/user/value4value',
                payload={'lightning_address': 'test@getalby.com'}
            )
            m.get(
                'https://api.getalby.com/balance',
                payload={'balance': 1000, 'currency': 'sat'}
            )

            # Use async classes
            async_account = AsyncAccount()
            async_invoice = AsyncInvoice()

            # Test async operations
            v4v_result = await async_account.get_value4value()
            balance_result = await async_account.get_balance()

            assert v4v_result['lightning_address'] == 'test@getalby.com'
            assert balance_result['balance'] == 1000

    @pytest.mark.asyncio
    async def test_mixed_sync_async_in_same_function(self):
        """Test using both sync and async classes in the same function."""
        import os
        os.environ['BASE_URL'] = 'https://api.getalby.com'
        os.environ['ALBY_ACCESS_TOKEN'] = 'test_token'

        # Mock responses for both sync and async
        with aioresponses() as async_mock:
            async_mock.get(
                'https://api.getalby.com/user/value4value',
                payload={'lightning_address': 'async@getalby.com'}
            )

            with responses.RequestsMock() as sync_mock:
                sync_mock.add(
                    responses.GET,
                    'https://api.getalby.com/balance',
                    json={'balance': 2000, 'currency': 'sat'},
                    status=200
                )

                # Use both sync and async in the same function
                sync_account = Account()
                async_account = AsyncAccount()

                # Get data using sync method
                sync_balance = sync_account.get_balance()

                # Get data using async method
                async_v4v = await async_account.get_value4value()

                # Verify both work
                assert sync_balance['balance'] == 2000
                assert async_v4v['lightning_address'] == 'async@getalby.com'

    def test_mixed_usage_different_configurations(self):
        """Test that sync and async classes can have different configurations."""
        import os
        
        # Set up environment for sync
        os.environ['BASE_URL'] = 'https://api.getalby.com'
        os.environ['ALBY_ACCESS_TOKEN'] = 'sync_token'
        
        sync_account = Account()
        
        # Change environment for async (simulating different config)
        os.environ['ALBY_ACCESS_TOKEN'] = 'async_token'
        
        async_account = AsyncAccount()
        
        # Verify they have different tokens
        assert 'sync_token' in sync_account.headers['Authorization']
        assert 'async_token' in async_account.headers['Authorization']
        assert sync_account.headers['Authorization'] != async_account.headers['Authorization']

    @pytest.mark.asyncio
    async def test_concurrent_sync_and_async_operations(self):
        """Test that sync and async operations can be used concurrently."""
        import os
        import threading
        import time
        
        os.environ['BASE_URL'] = 'https://api.getalby.com'
        os.environ['ALBY_ACCESS_TOKEN'] = 'test_token'

        results = {}

        def sync_operation():
            """Sync operation running in a thread."""
            with responses.RequestsMock() as m:
                m.add(
                    responses.GET,
                    'https://api.getalby.com/balance',
                    json={'balance': 3000, 'currency': 'sat'},
                    status=200
                )
                
                account = Account()
                results['sync'] = account.get_balance()

        async def async_operation():
            """Async operation."""
            with aioresponses() as m:
                m.get(
                    'https://api.getalby.com/user/value4value',
                    payload={'lightning_address': 'concurrent@getalby.com'}
                )
                
                account = AsyncAccount()
                results['async'] = await account.get_value4value()

        # Start sync operation in a thread
        sync_thread = threading.Thread(target=sync_operation)
        sync_thread.start()

        # Run async operation
        await async_operation()

        # Wait for sync thread to complete
        sync_thread.join()

        # Verify both operations completed successfully
        assert 'sync' in results
        assert 'async' in results
        assert results['sync']['balance'] == 3000
        assert results['async']['lightning_address'] == 'concurrent@getalby.com'

    def test_class_method_compatibility(self):
        """Test that sync and async classes have compatible method signatures."""
        import os
        import inspect
        
        os.environ['BASE_URL'] = 'https://api.getalby.com'
        os.environ['ALBY_ACCESS_TOKEN'] = 'test_token'

        # Instantiate classes
        sync_account = Account()
        async_account = AsyncAccount()
        sync_invoice = Invoice()
        async_invoice = AsyncInvoice()
        sync_payment = Payment()
        async_payment = AsyncPayment()

        # Check Account methods
        sync_methods = [method for method in dir(sync_account) if not method.startswith('_') and callable(getattr(sync_account, method))]
        async_methods = [method for method in dir(async_account) if not method.startswith('_') and callable(getattr(async_account, method))]
        
        # Both should have the same public methods
        assert set(sync_methods) == set(async_methods)

        # Check method signatures (excluding 'self' parameter)
        for method_name in sync_methods:
            sync_method = getattr(sync_account, method_name)
            async_method = getattr(async_account, method_name)
            
            sync_sig = inspect.signature(sync_method)
            async_sig = inspect.signature(async_method)
            
            # Parameters should be the same (async methods just return coroutines)
            sync_params = list(sync_sig.parameters.keys())
            async_params = list(async_sig.parameters.keys())
            
            assert sync_params == async_params, f"Method {method_name} has different parameters"

    @pytest.mark.asyncio
    async def test_error_handling_consistency(self):
        """Test that sync and async classes handle errors consistently."""
        import os
        
        os.environ['BASE_URL'] = 'https://api.getalby.com'
        os.environ['ALBY_ACCESS_TOKEN'] = 'test_token'

        # Test sync error handling
        with responses.RequestsMock() as sync_mock:
            sync_mock.add(
                responses.GET,
                'https://api.getalby.com/balance',
                json={'error': 'Unauthorized'},
                status=401
            )

            sync_account = Account()
            sync_error = None
            try:
                sync_account.get_balance()
            except Exception as e:
                sync_error = e

        # Test async error handling
        with aioresponses() as async_mock:
            async_mock.get(
                'https://api.getalby.com/balance',
                payload={'error': 'Unauthorized'},
                status=401
            )

            async_account = AsyncAccount()
            async_error = None
            try:
                await async_account.get_balance()
            except Exception as e:
                async_error = e

        # Both should raise errors
        assert sync_error is not None
        assert async_error is not None
        
        # Error types should be related (both HTTP errors)
        assert hasattr(sync_error, 'response') or 'HTTP' in str(type(sync_error))
        assert hasattr(async_error, 'status') or 'HTTP' in str(type(async_error))