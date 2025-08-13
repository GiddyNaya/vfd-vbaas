#!/usr/bin/env python3
"""
VBaaS SDK Basic Usage Example

This example demonstrates basic usage of the VBaaS Python SDK.
"""

import os

from vbaas import VBaaSClient


def main():
    """Main example function."""
    print("VBaaS SDK Basic Usage Example")
    print("=" * 40)
    print()

    # Get credentials from environment variables
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

    # Initialize client
    client = VBaaSClient(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        environment="test",  # Use 'live' for production
    )

    try:
        # 1. Get biller categories
        print("1. Getting biller categories...")
        categories = client.get_biller_categories()
        print(f"Found {len(categories)} categories:")
        for category in categories:
            print(f"  - {category.category}")

        # 1b. Get biller categories as dictionaries (for API responses)
        print("\n1b. Getting biller categories as dictionaries...")
        categories_dict = client.get_biller_categories_dict()
        print(f"Found {len(categories_dict)} categories (serializable):")
        for category in categories_dict:
            print(f"  - {category['category']}")

        # 2. Get billers for a category
        print("\n2. Getting billers for 'Airtime' category...")
        billers = client.get_billers("Airtime")
        print(f"Found {len(billers)} billers:")
        for biller in billers:
            print(f"  - {biller.name} (ID: {biller.id})")

        # 2b. Get billers as dictionaries (for API responses)
        print("\n2b. Getting billers as dictionaries...")
        billers_dict = client.get_billers_dict("Airtime")
        print(f"Found {len(billers_dict)} billers (serializable):")
        for biller in billers_dict:
            print(f"  - {biller['name']} (ID: {biller['id']})")

        # 3. Get items for a biller
        if billers:
            print("\n3. Getting items for biller 'AIRTEL'...")
            airtel_biller = billers[0]  # Use first biller
            items = client.get_biller_items(
                biller_id=airtel_biller.id,
                division_id=airtel_biller.division,
                product_id=airtel_biller.product,
            )
            print(f"Found {len(items)} items:")
            for item in items[:2]:  # Show first 2
                print(
                    f"  - {item.payment_item_name} "
                    f"(Fixed: {item.is_amount_fixed})"
                )

            # 3b. Get items as dictionaries (for API responses)
            print("\n3b. Getting items as dictionaries...")
            items_dict = client.get_biller_items_dict(
                biller_id=airtel_biller.id,
                division_id=airtel_biller.division,
                product_id=airtel_biller.product,
            )
            print(f"Found {len(items_dict)} items (serializable):")
            for item in items_dict[:2]:  # Show first 2
                print(
                    f"  - {item['payment_item_name']} "
                    f"(Fixed: {item['is_amount_fixed']})"
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

        # 4b. Example payment with dictionary response
        print("\n4b. Payment example with dictionary response:")
        print(
            """
        # Example payment with serializable response
        payment_result_dict = client.pay_bill_dict(
            customer_id="09071046909",
            amount="1000",
            division="C",
            payment_item="airtime",
            product_id="423",
            biller_id="airng",
            reference=f"test-{int(time.time())}",
            phone_number="09000000000"
        )
        # This can be directly used in API responses
        # json.dumps(payment_result_dict)  # Works perfectly!
        """
        )

        # 5. Transaction status check example
        print("\n5. Transaction status check example:")
        print(
            """
        # Check transaction status
        status = client.get_transaction_status("your-transaction-id")
        print(f"Transaction status: {status.transaction_status}")
        print(f"Amount: {status.amount}")
        """
        )

        # 5b. Transaction status with dictionary response
        print("\n5b. Transaction status with dictionary response:")
        print(
            """
        # Check transaction status with serializable response
        status_dict = client.get_transaction_status_dict("your-transaction-id")
        # This can be directly used in API responses
        # json.dumps(status_dict)  # Works perfectly!
        """
        )

        print("\nExample completed successfully!")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
