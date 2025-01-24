import boto3
from typing import Dict, List
from ..models.pricing_models import ServicePricing, EC2Instance
from config.config import Config

class AWSPriceService:
    def __init__(self):
        self.pricing_client = boto3.client(
            'pricing',
            region_name=Config.AWS_REGION,
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
        )
    
    def get_ec2_pricing(self, instance_type: str, region: str) -> ServicePricing:
        try:
            response = self.pricing_client.get_products(
                ServiceCode='AmazonEC2',
                Filters=[
                    {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instance_type},
                    {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region},
                    {'Type': 'TERM_MATCH', 'Field': 'operatingSystem', 'Value': 'Linux'},
                    {'Type': 'TERM_MATCH', 'Field': 'tenancy', 'Value': 'Shared'}
                ]
            )
            
            # Process response and return pricing
            # This is a simplified version - you'd need to parse the actual response
            return ServicePricing(
                service_type='EC2',
                region=region,
                price_per_unit=Config.EC2_PRICING.get(instance_type, 0.0),
                unit_type='hour'
            )
        except Exception as e:
            print(f"Error fetching EC2 pricing: {str(e)}")
            return None 