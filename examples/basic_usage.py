#!/usr/bin/env python3
"""
VBaaS SDK Basic Usage Example

This example demonstrates basic usage of the VBaaS Python SDK.
"""

import os

from vbaas import VBaaSClient, VBaaSError


def main():
    # Initialize client with credentials
    # In production, use environment variables or secure credential storage
    consumer_key = os.getenv("VBAAS_CONSUMER_KEY", "your_consumer_key_here")
    consumer_secret = os.getenv(
        "VBAAS_CONSUMER_SECRET", "your_consumer_secret_here"
    )

    try:
        # Create client instance
        client = VBaaSClient(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            environment="test",  # Use "live" for production
        )

        print("VBaaS SDK Basic Usage Example")
        print("=" * 40)

        # 1. Get biller categories
        print("\n1. Getting biller categories...")
        categories = client.get_biller_categories()
        print(f"Found {len(categories)} categories:")
        for category in categories:
            print(f"  - {category.category}")

        # 2. Get billers for a specific category (e.g., Airtime)
        if categories:
            category_name = "Airtime"
            print(f"\n2. Getting billers for '{category_name}' category...")
            billers = client.get_billers(category_name)
            print(f"Found {len(billers)} billers:")
            for biller in billers[:3]:  # Show first 3
                print(f"  - {biller.name} (ID: {biller.id})")

            # 3. Get biller items for a specific biller
            if billers:
                biller = billers[0]
                print(f"\n3. Getting items for biller '{biller.name}'...")
                items = client.get_biller_items(
                    biller_id=biller.id,
                    division_id=biller.division,
                    product_id=biller.product,
                )
                print(f"Found {len(items)} items:")
                for item in items[:2]:  # Show first 2
                    print(
                        f"  - {item.payment_item_name} "
                        f"(Fixed: {item.is_amount_fixed})"
                    )

        # 4. Example payment (commented out to avoid accidental charges)
        print("\n4. Payment example (commented out):")
        print(
            """
        # Example payment - uncomment and modify as needed
        payment_result = client.pay_bill(
            customer_id="09071046909",
            amount="1000",
            division="C",
            payment_item="airtime",
            product_id="423",
            biller_id="airng",
            reference=f"test-{int(time.time())}",  # Unique reference
            phone_number="09000000000"
        )
        print(f"Payment status: {payment_result.status}")
        print(f"Message: {payment_result.message}")
        """
        )

        # 5. Example transaction status check
        print("\n5. Transaction status check example:")
        print(
            """
        # Check transaction status
        status = client.get_transaction_status("your-transaction-id")
        print(f"Transaction status: {status.transaction_status}")
        print(f"Amount: {status.amount}")
        """
        )

        print("\nExample completed successfully!")

    except VBaaSError as e:
        print(f"VBaaS API Error: {e.message}")
        if e.status_code:
            print(f"Status Code: {e.status_code}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
    finally:
        # Clean up
        if "client" in locals():
            client.close()


if __name__ == "__main__":
    main()
