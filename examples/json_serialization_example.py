"""
VBaaS SDK JSON Serialization Example

This example demonstrates how to use the VBaaS SDK models
in API responses with proper JSON serialization.
"""

import json
import os

from vbaas import VBaaSClient
from vbaas.models import serialize_models


def main():
    """Demonstrate JSON serialization for API responses."""
    print("VBaaS SDK JSON Serialization Example")
    print("=" * 50)
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
        environment="test",
    )

    try:
        # Example 1: Using the _dict methods (recommended for API responses)
        print("1. Using _dict methods for API responses:")
        print("-" * 40)

        categories_dict = client.get_biller_categories_dict()

        # This works perfectly with json.dumps()
        json_response = json.dumps(
            {
                "status": "success",
                "data": categories_dict,
                "count": len(categories_dict),
            },
            indent=2,
        )

        print("JSON Response:")
        print(json_response)
        print()

        # Example 2: Using serialize_models utility function
        print("2. Using serialize_models utility function:")
        print("-" * 40)

        categories = client.get_biller_categories()
        serialized_categories = serialize_models(categories)

        json_response = json.dumps(
            {
                "status": "success",
                "data": serialized_categories,
                "count": len(serialized_categories),
            },
            indent=2,
        )

        print("JSON Response:")
        print(json_response)
        print()

        # Example 3: Using model.to_dict() method directly
        print("3. Using model.to_dict() method directly:")
        print("-" * 40)

        categories = client.get_biller_categories()
        if categories:
            category = categories[0]
            category_dict = category.to_dict()

            json_response = json.dumps(
                {"status": "success", "data": category_dict}, indent=2
            )

            print("JSON Response:")
            print(json_response)
            print()

        # Example 4: Complete API response structure
        print("4. Complete API response structure:")
        print("-" * 40)

        try:
            billers_dict = client.get_billers_dict("Airtime")

            api_response = {
                "status": "success",
                "message": "Billers retrieved successfully",
                "data": {
                    "billers": billers_dict,
                    "category": "Airtime",
                    "count": len(billers_dict),
                },
                "metadata": {
                    "timestamp": "2024-01-01T00:00:00Z",
                    "version": "1.0.2",
                },
            }

            json_response = json.dumps(api_response, indent=2)
            print("Complete API Response:")
            print(json_response)

        except Exception as e:
            print(f"Error getting billers: {e}")
            print()

        # Example 5: Error response structure
        print("5. Error response structure:")
        print("-" * 40)

        error_response = {
            "status": "error",
            "message": "Invalid parameters",
            "error_code": "VALIDATION_ERROR",
            "data": None,
        }

        json_response = json.dumps(error_response, indent=2)
        print("Error Response:")
        print(json_response)
        print()

        print("✅ All JSON serialization examples completed successfully!")
        print("\nKey points:")
        print(
            "- Use _dict methods (e.g., get_biller_categories_dict()) "
            "for API responses"
        )
        print("- Use serialize_models() utility for lists of models")
        print("- Use model.to_dict() for individual models")
        print("- All methods return dictionaries that work with json.dumps()")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
