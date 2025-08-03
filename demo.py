#!/usr/bin/env python3
"""
VBaaS Python SDK Demo

A comprehensive demonstration of the VBaaS Python SDK capabilities.
This script shows how to use all the main features of the library.
"""

import os
import sys

from vbaas import VBaaSClient, VBaaSError


def print_header(title):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")


def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'-'*40}")
    print(f" {title}")
    print(f"{'-'*40}")


def main():
    """Main demo function."""
    print_header("VBaaS Python SDK - Comprehensive Demo")

    # Check for credentials
    consumer_key = os.getenv("VBAAS_CONSUMER_KEY")
    consumer_secret = os.getenv("VBAAS_CONSUMER_SECRET")

    if not consumer_key or not consumer_secret:
        print("\n⚠️  CREDENTIALS REQUIRED")
        print("Please set the following environment variables:")
        print("  export VBAAS_CONSUMER_KEY='your_consumer_key'")
        print("  export VBAAS_CONSUMER_SECRET='your_consumer_secret'")
        print("\nFor demo purposes, you can also modify this script directly.")
        return

    try:
        # Initialize the client
        print_section("1. Initializing VBaaS Client")
        client = VBaaSClient(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            environment="test",  # Use "live" for production
        )
        print("✅ Client initialized successfully")
        print(f"   Environment: {client.environment}")
        print(f"   Auth URL: {client.auth_base_url}")
        print(f"   Bills URL: {client.bills_base_url}")

        # Get biller categories
        print_section("2. Fetching Biller Categories")
        categories = client.get_biller_categories()
        print(f"✅ Found {len(categories)} biller categories:")
        for i, category in enumerate(categories, 1):
            print(f"   {i}. {category.category}")

        # Get billers for each category
        print_section("3. Exploring Billers by Category")
        for category in categories[:3]:  # Show first 3 categories
            try:
                print(f"\n📂 Category: {category.category}")
                billers = client.get_billers(category.category)
                print(f"   Found {len(billers)} billers:")

                for biller in billers[:3]:  # Show first 3 billers
                    fee_info = (
                        f" (Fee: {biller.convenience_fee})"
                        if biller.convenience_fee
                        else ""
                    )
                    print(f"   • {biller.name} (ID: {biller.id}){fee_info}")

                # Get items for the first biller
                if billers:
                    first_biller = billers[0]
                    print(f"\n   🔍 Items for '{first_biller.name}':")
                    try:
                        items = client.get_biller_items(
                            biller_id=first_biller.id,
                            division_id=first_biller.division,
                            product_id=first_biller.product,
                        )
                        for item in items[:2]:  # Show first 2 items
                            fixed = (
                                "Fixed"
                                if item.is_amount_fixed == "true"
                                else "Variable"
                            )
                            print(
                                f"     - {item.payment_item_name} ({fixed} amount)"
                            )
                    except VBaaSError as e:
                        print(f"     ⚠️  Could not fetch items: {e.message}")

            except VBaaSError as e:
                print(
                    f"   ⚠️  Error fetching billers for {category.category}: {e.message}"
                )

        # Demonstrate customer validation
        print_section("4. Customer Validation Example")
        print(
            "Demonstrating customer validation (required for utilities/cable TV)..."
        )

        # Find a utility biller for demonstration
        try:
            utility_billers = client.get_billers("Utility")
            if utility_billers:
                biller = utility_billers[0]
                items = client.get_biller_items(
                    biller_id=biller.id,
                    division_id=biller.division,
                    product_id=biller.product,
                )
                if items:
                    item = items[0]
                    print(f"   Testing validation for: {biller.name}")
                    print(f"   Using test customer ID: 1234567890")

                    try:
                        is_valid = client.validate_customer(
                            division_id=biller.division,
                            payment_item=item.payment_code,
                            customer_id="1234567890",
                            biller_id=biller.id,
                        )
                        print(
                            f"   ✅ Validation result: {'Success' if is_valid else 'Failed'}"
                        )
                    except VBaaSError as e:
                        print(f"   ⚠️  Validation failed: {e.message}")
        except VBaaSError as e:
            print(f"   ⚠️  Could not test validation: {e.message}")

        # Payment simulation
        print_section("5. Payment Simulation")
        print("🚨 PAYMENT SIMULATION (No actual charges will be made)")
        print("\nExample payment parameters:")
        payment_example = {
            "customer_id": "09071046909",
            "amount": "1000",
            "division": "C",
            "payment_item": "airtime",
            "product_id": "423",
            "biller_id": "airng",
            "reference": "demo-payment-123",
            "phone_number": "08012345678",
        }

        for key, value in payment_example.items():
            print(f"   {key}: {value}")

        print("\n💡 To make actual payments, use:")
        print("   result = client.pay_bill(**payment_params)")
        print(
            "   print(f'Status: {result.status}, Message: {result.message}')"
        )

        # Transaction status example
        print_section("6. Transaction Status Check Example")
        print("Example of checking transaction status:")
        print("   status = client.get_transaction_status('transaction-id')")
        print("   print(f'Status: {status.transaction_status}')")
        print("   print(f'Amount: {status.amount}')")

        # Error handling demonstration
        print_section("7. Error Handling")
        print("The SDK provides comprehensive error handling:")
        print("   • VBaaSError: Base exception for all SDK errors")
        print("   • AuthenticationError: Authentication failures")
        print("   • APIError: API request failures")
        print("   • ValidationError: Input validation errors")
        print("   • NetworkError: Network-related errors")
        print("   • ConfigurationError: Configuration issues")

        # Best practices
        print_section("8. Best Practices")
        print("📋 Recommended practices when using this SDK:")
        print("   1. Always use environment variables for credentials")
        print("   2. Use try-catch blocks for proper error handling")
        print(
            "   3. Validate customer info before making payments (utilities/cable)"
        )
        print("   4. Use unique references for each payment")
        print("   5. Check transaction status after payments")
        print("   6. Use test environment for development")
        print("   7. Close the client when done: client.close()")

        print_header("Demo Completed Successfully! 🎉")
        print("The VBaaS Python SDK is ready for use.")
        print(
            "Check the examples/ directory for more detailed usage examples."
        )

    except VBaaSError as e:
        print(f"\n❌ VBaaS Error: {e.message}")
        if e.status_code:
            print(f"   Status Code: {e.status_code}")
    except Exception as e:
        print(f"\n❌ Unexpected Error: {str(e)}")
    finally:
        # Clean up
        if "client" in locals():
            client.close()
            print("\n🔒 Client connection closed.")


if __name__ == "__main__":
    main()
