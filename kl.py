from homeharvest import scrape_property
from datetime import datetime
import json

# Parameters for scraping
scrape_params = {
    "location": "San Diego, CA",
    "listing_type": "sold",
    "property_type": ['single_family', 'multi_family'],
    "radius": 5.5,
    "past_days": 30,
    "mls_only": True,
    "foreclosure": False,
    "proxy": None,
    "extra_property_data": True,
    "exclude_pending": False,
    "limit": 10000,
}

# Generate filename based on current timestamp
current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"HomeHarvest_{current_timestamp}.csv"

# Scrape properties
properties = scrape_property(**scrape_params)
print(f"Number of properties: {len(properties)}")

# Export to CSV
properties.to_csv(filename, index=False)
print(properties.head())

# Organize data according to the schema
organized_properties = []
for property in properties.to_dict(orient='records'):
    organized_properties.append({
        "Basic Information": {
            "property_url": property.get("property_url", "N/A"),
            "property_id": property.get("property_id", "N/A"),
            "listing_id": property.get("listing_id", "N/A"),
            "mls": property.get("mls", "N/A"),
            "mls_id": property.get("mls_id", "N/A"),
            "status": property.get("status", "N/A"),
        },
        "Address Details": {
            "street": property.get("street", "N/A"),
            "unit": property.get("unit", "N/A"),
            "city": property.get("city", "N/A"),
            "state": property.get("state", "N/A"),
            "zip_code": property.get("zip_code", "N/A"),
        },
        "Property Description": {
            "style": property.get("style", "N/A"),
            "beds": property.get("beds", "N/A"),
            "full_baths": property.get("full_baths", "N/A"),
            "half_baths": property.get("half_baths", "N/A"),
            "sqft": property.get("sqft", "N/A"),
            "year_built": property.get("year_built", "N/A"),
            "stories": property.get("stories", "N/A"),
            "garage": property.get("garage", "N/A"),
            "lot_sqft": property.get("lot_sqft", "N/A"),
        },
        "Property Listing Details": {
            "days_on_mls": property.get("days_on_mls", "N/A"),
            "list_price": property.get("list_price", "N/A"),
            "list_price_min": property.get("list_price_min", "N/A"),
            "list_price_max": property.get("list_price_max", "N/A"),
            "list_date": property.get("list_date", "N/A"),
            "pending_date": property.get("pending_date", "N/A"),
            "sold_price": property.get("sold_price", "N/A"),
            "last_sold_date": property.get("last_sold_date", "N/A"),
            "price_per_sqft": property.get("price_per_sqft", "N/A"),
            "new_construction": property.get("new_construction", "N/A"),
            "hoa_fee": property.get("hoa_fee", "N/A"),
        },
        "Location Details": {
            "latitude": property.get("latitude", "N/A"),
            "longitude": property.get("longitude", "N/A"),
            "nearby_schools": property.get("nearby_schools", []),  # Assuming a list
        },
        "Agent Info": {
            "agent_id": property.get("agent_id", "N/A"),
            "agent_name": property.get("agent_name", "N/A"),
            "agent_email": property.get("agent_email", "N/A"),
            "agent_phone": property.get("agent_phone", "N/A"),
        },
        "Broker Info": {
            "broker_id": property.get("broker_id", "N/A"),
            "broker_name": property.get("broker_name", "N/A"),
        },
        "Builder Info": {
            "builder_id": property.get("builder_id", "N/A"),
            "builder_name": property.get("builder_name", "N/A"),
        },
        "Office Info": {
            "office_id": property.get("office_id", "N/A"),
            "office_name": property.get("office_name", "N/A"),
            "office_phones": property.get("office_phones", []),  # Assuming a list
            "office_email": property.get("office_email", "N/A"),
        },
    })

# Create JSON with organized data
package_data = {
    "name": "homeharvest-data",
    "version": "1.0.0",
    "description": "Scraped property data from HomeHarvest",
    "timestamp": current_timestamp,
    "parameters_used": scrape_params,
    "data": organized_properties
}

# Save to package.json
package_filename = "package.json"
with open(package_filename, 'w') as json_file:
    json.dump(package_data, json_file, indent=4)

print(f"Organized data saved to {package_filename}")
