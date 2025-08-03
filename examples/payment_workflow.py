#!/usr/bin/env python3
"""
VBaaS SDK Payment Workflow Example

This example demonstrates a complete payment workflow including validation.
"""

import os
import time
import uuid

from vbaas import VBaaSClient, VBaaSError


def generate_unique_reference():
    """Generate a unique payment reference."""
    return f"payment-{uuid.uuid4().hex[:8]}-{int(time.time())}"


def main():
    # Initialize client
    consumer_key = os.getenv("VBAAS_CONSUMER_KEY", "your_consumer_key_here")
    consumer_secret = os.getenv(
        "VBAAS_CONSUMER_SECRET", "your_consumer_secret_here"
    )

    if consumer_key == "your_consumer_key_here":
        print(
            "Please set VBAAS_CONSUMER_KEY and "
            "VBAAS_CONSUMER_SECRET environment variables"
        )
        return

    try:
        client = VBaaSClient(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            environment="test",
        )

        print("VBaaS Payment Workflow Example")
        print("=" * 40)

        # Step 1: Get available categories
        print("Step 1: Getting biller categories...")
        categories = client.get_biller_categories()

        # Step 2: Choose a category and get billers
        target_category = "Utility"  # Example: utility bills
        print(f"Step 2: Getting billers for '{target_category}' category...")

        try:
            billers = client.get_billers(target_category)
            if not billers:
                print(f"No billers found for category '{target_category}'")
                return

            print(f"Found {len(billers)} billers:")
            for i, biller in enumerate(billers[:5], 1):
                print(f"  {i}. {biller.name} (ID: {biller.id})")

        except VBaaSError as e:
            print(f"Error getting billers: {e.message}")
            return

        # Step 3: Get items for the first biller
        selected_biller = billers[0]
        print(f"\nStep 3: Getting items for '{selected_biller.name}'...")

        try:
            items = client.get_biller_items(
                biller_id=selected_biller.id,
                division_id=selected_biller.division,
                product_id=selected_biller.product,
            )

            if not items:
                print("No items found for this biller")
                return

            selected_item = items[0]
            print(f"Selected item: {selected_item.payment_item_name}")
            print(f"Amount fixed: {selected_item.is_amount_fixed}")
            print(f"Currency: {selected_item.currency_symbol}")

        except VBaaSError as e:
            print(f"Error getting biller items: {e.message}")
            return

        # Step 4: Customer validation (for utility bills)
        customer_id = "1234567890"  # Example customer ID
        print(f"\nStep 4: Validating customer ID '{customer_id}'...")

        try:
            is_valid = client.validate_customer(
                division_id=selected_biller.division,
                payment_item=selected_item.payment_code,
                customer_id=customer_id,
                biller_id=selected_biller.id,
            )
            print(
                f"Customer validation: {'Success' if is_valid else 'Failed'}"
            )

        except VBaaSError as e:
            print(f"Customer validation failed: {e.message}")
            print("Proceeding anyway for demonstration...")

        # Step 5: Make payment (commented out to avoid charges)
        print("\nStep 5: Payment simulation...")
        print("The following payment would be made:")

        payment_data = {
            "customer_id": customer_id,
            "amount": "5000",  # Example amount
            "division": selected_biller.division,
            "payment_item": selected_item.payment_code,
            "product_id": selected_biller.product,
            "biller_id": selected_biller.id,
            "reference": generate_unique_reference(),
            "phone_number": "08012345678",
        }

        for key, value in payment_data.items():
            print(f"  {key}: {value}")

        print("\n--- PAYMENT COMMENTED OUT FOR SAFETY ---")
        print("To make actual payment, uncomment the following code:")
        print(
            """
        try:
            payment_result = client.pay_bill(**payment_data)
            print(f"Payment Status: {payment_result.status}")
            print(f"Message: {payment_result.message}")
            print(f"Reference: {payment_result.reference}")

            # Step 6: Check transaction status
            if payment_result.status == "00":
                print("\\nChecking transaction status...")
                status = client.get_transaction_status(
                    payment_result.reference
                )
                print(f"Transaction Status: {status.transaction_status}")
                print(f"Amount: {status.amount}")

        except VBaaSError as e:
            print(f"Payment failed: {e.message}")
        """
        )

        print("\nWorkflow completed successfully!")

    except VBaaSError as e:
        print(f"VBaaS API Error: {e.message}")
        if e.status_code:
            print(f"Status Code: {e.status_code}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
    finally:
        if "client" in locals():
            client.close()


if __name__ == "__main__":
    main()
