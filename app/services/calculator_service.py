from typing import Dict
from ..models.pricing_models import CostCalculation
from .aws_price_service import AWSPriceService
from config.config import Config

class CalculatorService:
    def __init__(self):
        self.price_service = AWSPriceService()
    
    def calculate_ec2_cost(self, instance_type: str, hours: float, region: str) -> CostCalculation:
        pricing = self.price_service.get_ec2_pricing(instance_type, region)
        if not pricing:
            return None
            
        total_cost = pricing.price_per_unit * hours
        return CostCalculation(
            service='EC2',
            usage=hours,
            unit_price=pricing.price_per_unit,
            total_cost=total_cost,
            details={
                'instance_type': instance_type,
                'region': region,
                'price_per_hour': pricing.price_per_unit
            }
        )
    
    def calculate_s3_cost(self, storage_gb: float, storage_class: str = 'standard') -> CostCalculation:
        unit_price = Config.S3_PRICING.get(storage_class.lower(), Config.S3_PRICING['standard'])
        total_cost = storage_gb * unit_price
        
        return CostCalculation(
            service='S3',
            usage=storage_gb,
            unit_price=unit_price,
            total_cost=total_cost,
            details={
                'storage_class': storage_class,
                'price_per_gb': unit_price
            }
        )
    
    def calculate_rds_cost(self, instance_type: str, hours: float, storage_gb: float) -> CostCalculation:
        instance_price = Config.RDS_PRICING.get(instance_type, 0.0)
        storage_price = 0.115  # $0.115 per GB-month for General Purpose SSD (gp2)
        
        compute_cost = instance_price * hours
        storage_cost = storage_price * storage_gb
        total_cost = compute_cost + storage_cost
        
        return CostCalculation(
            service='RDS',
            usage=hours,
            unit_price=instance_price,
            total_cost=total_cost,
            details={
                'instance_type': instance_type,
                'compute_cost': compute_cost,
                'storage_gb': storage_gb,
                'storage_cost': storage_cost,
                'price_per_hour': instance_price
            }
        )

    def calculate_lambda_cost(self, memory_mb: int, executions: int, duration_ms: float) -> CostCalculation:
        gb_seconds = (memory_mb / 1024) * (duration_ms / 1000) * executions
        duration_cost = gb_seconds * Config.LAMBDA_PRICING['duration']
        request_cost = (executions / 1000000) * Config.LAMBDA_PRICING['request']
        total_cost = duration_cost + request_cost
        
        return CostCalculation(
            service='Lambda',
            usage=executions,
            unit_price=Config.LAMBDA_PRICING['request'],
            total_cost=total_cost,
            details={
                'memory': f"{memory_mb}MB",
                'executions': executions,
                'duration': f"{duration_ms}ms",
                'compute_cost': duration_cost,
                'request_cost': request_cost
            }
        )

    def calculate_dynamodb_cost(self, read_capacity: int, write_capacity: int, storage_gb: float) -> CostCalculation:
        read_cost = (read_capacity * 720 * Config.DYNAMODB_PRICING['read']) / 1000000
        write_cost = (write_capacity * 720 * Config.DYNAMODB_PRICING['write']) / 1000000
        storage_cost = storage_gb * Config.DYNAMODB_PRICING['storage']
        total_cost = read_cost + write_cost + storage_cost
        
        return CostCalculation(
            service='DynamoDB',
            usage=storage_gb,
            unit_price=Config.DYNAMODB_PRICING['storage'],
            total_cost=total_cost,
            details={
                'read_capacity': read_capacity,
                'write_capacity': write_capacity,
                'storage_gb': storage_gb,
                'read_cost': read_cost,
                'write_cost': write_cost,
                'storage_cost': storage_cost
            }
        )

    def calculate_api_gateway_cost(self, requests: float, data_transfer: float) -> CostCalculation:
        request_cost = requests * Config.API_GATEWAY_PRICING['requests']
        transfer_cost = data_transfer * Config.API_GATEWAY_PRICING['data_transfer']
        total_cost = request_cost + transfer_cost
        
        return CostCalculation(
            service='API Gateway',
            usage=requests,
            unit_price=Config.API_GATEWAY_PRICING['requests'],
            total_cost=total_cost,
            details={
                'requests_millions': requests,
                'data_transfer_gb': data_transfer,
                'request_cost': request_cost,
                'transfer_cost': transfer_cost
            }
        )

    def calculate_aurora_cost(self, instance_type: str, storage_gb: float, io_requests: float) -> CostCalculation:
        instance_cost = Config.AURORA_PRICING[instance_type] * 730  # Hours in a month
        storage_cost = storage_gb * Config.AURORA_PRICING['storage']
        io_cost = io_requests * Config.AURORA_PRICING['io']
        total_cost = instance_cost + storage_cost + io_cost
        
        return CostCalculation(
            service='Aurora',
            usage=storage_gb,
            unit_price=Config.AURORA_PRICING['storage'],
            total_cost=total_cost,
            details={
                'instance_type': instance_type,
                'storage_gb': storage_gb,
                'io_requests_millions': io_requests,
                'instance_cost': instance_cost,
                'storage_cost': storage_cost,
                'io_cost': io_cost
            }
        )

    def calculate_cloudfront_cost(self, data_transfer_tb: float, http_requests: float, https_requests: float) -> CostCalculation:
        # Calculate data transfer cost with tiered pricing
        data_transfer_gb = data_transfer_tb * 1024
        if data_transfer_tb <= 10:
            transfer_cost = data_transfer_gb * Config.CLOUDFRONT_PRICING['data_transfer']['first_10tb']
        elif data_transfer_tb <= 50:
            transfer_cost = (10 * 1024 * Config.CLOUDFRONT_PRICING['data_transfer']['first_10tb'] +
                            (data_transfer_gb - 10 * 1024) * Config.CLOUDFRONT_PRICING['data_transfer']['next_40tb'])
        else:
            transfer_cost = (10 * 1024 * Config.CLOUDFRONT_PRICING['data_transfer']['first_10tb'] +
                            40 * 1024 * Config.CLOUDFRONT_PRICING['data_transfer']['next_40tb'] +
                            (data_transfer_gb - 50 * 1024) * Config.CLOUDFRONT_PRICING['data_transfer']['next_100tb'])
        
        http_cost = (http_requests / 10000) * Config.CLOUDFRONT_PRICING['requests']['http']
        https_cost = (https_requests / 10000) * Config.CLOUDFRONT_PRICING['requests']['https']
        total_cost = transfer_cost + http_cost + https_cost
        
        return CostCalculation(
            service='CloudFront',
            usage=data_transfer_gb,
            unit_price=Config.CLOUDFRONT_PRICING['data_transfer']['first_10tb'],
            total_cost=total_cost,
            details={
                'data_transfer_tb': data_transfer_tb,
                'http_requests_millions': http_requests,
                'https_requests_millions': https_requests,
                'transfer_cost': transfer_cost,
                'http_cost': http_cost,
                'https_cost': https_cost
            }
        )

    def calculate_ecr_cost(self, storage_gb: float, data_transfer_gb: float) -> CostCalculation:
        storage_cost = storage_gb * Config.ECR_PRICING['storage']
        transfer_cost = data_transfer_gb * Config.ECR_PRICING['data_transfer']
        total_cost = storage_cost + transfer_cost
        
        return CostCalculation(
            service='ECR',
            usage=storage_gb,
            unit_price=Config.ECR_PRICING['storage'],
            total_cost=total_cost,
            details={
                'storage_gb': storage_gb,
                'data_transfer_gb': data_transfer_gb,
                'storage_cost': storage_cost,
                'transfer_cost': transfer_cost
            }
        )

    def calculate_ecs_cost(self, vcpu_hours: float, memory_gb_hours: float) -> CostCalculation:
        vcpu_cost = vcpu_hours * Config.ECS_PRICING['fargate']['vcpu']
        memory_cost = memory_gb_hours * Config.ECS_PRICING['fargate']['memory']
        total_cost = vcpu_cost + memory_cost
        
        return CostCalculation(
            service='ECS',
            usage=vcpu_hours,
            unit_price=Config.ECS_PRICING['fargate']['vcpu'],
            total_cost=total_cost,
            details={
                'vcpu_hours': vcpu_hours,
                'memory_gb_hours': memory_gb_hours,
                'vcpu_cost': vcpu_cost,
                'memory_cost': memory_cost
            }
        )

    def calculate_eks_cost(self, cluster_hours: float, fargate_vcpu: float, fargate_memory: float) -> CostCalculation:
        cluster_cost = cluster_hours * Config.EKS_PRICING['cluster']
        fargate_vcpu_cost = fargate_vcpu * Config.EKS_PRICING['fargate']['vcpu']
        fargate_memory_cost = fargate_memory * Config.EKS_PRICING['fargate']['memory']
        total_cost = cluster_cost + fargate_vcpu_cost + fargate_memory_cost
        
        return CostCalculation(
            service='EKS',
            usage=cluster_hours,
            unit_price=Config.EKS_PRICING['cluster'],
            total_cost=total_cost,
            details={
                'cluster_hours': cluster_hours,
                'fargate_vcpu_hours': fargate_vcpu,
                'fargate_memory_hours': fargate_memory,
                'cluster_cost': cluster_cost,
                'fargate_compute_cost': fargate_vcpu_cost + fargate_memory_cost
            }
        )

    def calculate_elb_cost(self, lb_type: str, hours: float, processed_bytes_gb: float) -> CostCalculation:
        lb_cost = hours * Config.ELB_PRICING[lb_type]
        processing_cost = processed_bytes_gb * (
            Config.ELB_PRICING['data_processing']['alb'] 
            if lb_type == 'application' 
            else Config.ELB_PRICING['data_processing']['nlb']
        )
        total_cost = lb_cost + processing_cost
        
        return CostCalculation(
            service='Elastic Load Balancer',
            usage=hours,
            unit_price=Config.ELB_PRICING[lb_type],
            total_cost=total_cost,
            details={
                'load_balancer_type': lb_type,
                'hours': hours,
                'processed_gb': processed_bytes_gb,
                'lb_cost': lb_cost,
                'processing_cost': processing_cost
            }
        )

    def calculate_redshift_cost(self, node_type: str, nodes: int, storage_gb: float) -> CostCalculation:
        compute_cost = nodes * Config.REDSHIFT_PRICING[node_type] * 730  # Hours in a month
        storage_cost = nodes * storage_gb * Config.REDSHIFT_PRICING['storage']
        total_cost = compute_cost + storage_cost
        
        return CostCalculation(
            service='Redshift',
            usage=storage_gb * nodes,
            unit_price=Config.REDSHIFT_PRICING['storage'],
            total_cost=total_cost,
            details={
                'node_type': node_type,
                'nodes': nodes,
                'storage_per_node': storage_gb,
                'compute_cost': compute_cost,
                'storage_cost': storage_cost
            }
        )

    def calculate_route53_cost(self, hosted_zones: int, queries_millions: float) -> CostCalculation:
        hosted_zone_cost = hosted_zones * Config.ROUTE53_PRICING['hosted_zone']
        
        # Calculate query cost with tiered pricing
        if queries_millions <= 1000:
            query_cost = queries_millions * Config.ROUTE53_PRICING['queries']['first_billion']
        else:
            query_cost = (1000 * Config.ROUTE53_PRICING['queries']['first_billion'] +
                         (queries_millions - 1000) * Config.ROUTE53_PRICING['queries']['over_billion'])
        
        total_cost = hosted_zone_cost + query_cost
        
        return CostCalculation(
            service='Route 53',
            usage=queries_millions,
            unit_price=Config.ROUTE53_PRICING['queries']['first_billion'],
            total_cost=total_cost,
            details={
                'hosted_zones': hosted_zones,
                'queries_millions': queries_millions,
                'hosted_zone_cost': hosted_zone_cost,
                'query_cost': query_cost
            }
        )

    def calculate_sns_cost(self, publish_requests: float, http_deliveries: float, email_deliveries: float) -> CostCalculation:
        publish_cost = publish_requests * Config.SNS_PRICING['publish']
        http_cost = http_deliveries * Config.SNS_PRICING['http']
        email_cost = (email_deliveries / 100) * Config.SNS_PRICING['email']
        total_cost = publish_cost + http_cost + email_cost
        
        return CostCalculation(
            service='SNS',
            usage=publish_requests,
            unit_price=Config.SNS_PRICING['publish'],
            total_cost=total_cost,
            details={
                'publish_requests_millions': publish_requests,
                'http_deliveries_millions': http_deliveries,
                'email_deliveries_thousands': email_deliveries,
                'publish_cost': publish_cost,
                'http_delivery_cost': http_cost,
                'email_delivery_cost': email_cost
            }
        )

    def calculate_sqs_cost(self, queue_type: str, requests_millions: float) -> CostCalculation:
        unit_price = Config.SQS_PRICING['fifo'] if queue_type == 'fifo' else Config.SQS_PRICING['requests']
        total_cost = requests_millions * unit_price
        
        return CostCalculation(
            service='SQS',
            usage=requests_millions,
            unit_price=unit_price,
            total_cost=total_cost,
            details={
                'queue_type': queue_type,
                'requests_millions': requests_millions,
                'price_per_million': unit_price
            }
        )

    def calculate_vpc_cost(self, endpoints: int, nat_gateways: int, vpn_connections: int) -> CostCalculation:
        endpoint_cost = endpoints * Config.VPC_PRICING['endpoint'] * 730  # Hours in a month
        nat_cost = nat_gateways * Config.VPC_PRICING['nat_gateway'] * 730
        vpn_cost = vpn_connections * Config.VPC_PRICING['vpn'] * 730
        total_cost = endpoint_cost + nat_cost + vpn_cost
        
        return CostCalculation(
            service='VPC',
            usage=endpoints + nat_gateways + vpn_connections,
            unit_price=Config.VPC_PRICING['endpoint'],
            total_cost=total_cost,
            details={
                'vpc_endpoints': endpoints,
                'nat_gateways': nat_gateways,
                'vpn_connections': vpn_connections,
                'endpoint_cost': endpoint_cost,
                'nat_gateway_cost': nat_cost,
                'vpn_connection_cost': vpn_cost
            }
        ) 