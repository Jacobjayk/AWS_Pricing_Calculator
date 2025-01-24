import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    
    # AWS Service pricing defaults
    EC2_PRICING = {
        # General Purpose
        't2.nano': 0.0058, 't2.micro': 0.0116, 't2.small': 0.023, 't2.medium': 0.0464,
        't3.nano': 0.0052, 't3.micro': 0.0104, 't3.small': 0.0208, 't3.medium': 0.0416,
        'm5.large': 0.096, 'm5.xlarge': 0.192, 'm5.2xlarge': 0.384, 'm5.4xlarge': 0.768,
        'm6g.medium': 0.0385, 'm6g.large': 0.077, 'm6g.xlarge': 0.154,
        
        # Compute Optimized
        'c5.large': 0.085, 'c5.xlarge': 0.17, 'c5.2xlarge': 0.34, 'c5.4xlarge': 0.68,
        'c6g.medium': 0.034, 'c6g.large': 0.068, 'c6g.xlarge': 0.136,
        
        # Memory Optimized
        'r5.large': 0.126, 'r5.xlarge': 0.252, 'r5.2xlarge': 0.504, 'r5.4xlarge': 1.008,
        'r6g.medium': 0.0504, 'r6g.large': 0.1008, 'r6g.xlarge': 0.2016,
        'x1.16xlarge': 6.669, 'x1.32xlarge': 13.338,
        
        # Storage Optimized
        'i3.large': 0.156, 'i3.xlarge': 0.312, 'i3.2xlarge': 0.624,
        'd2.xlarge': 0.69, 'd2.2xlarge': 1.38, 'd2.4xlarge': 2.76,
        
        # GPU Instances
        'p3.2xlarge': 3.06, 'p3.8xlarge': 12.24, 'p3.16xlarge': 24.48,
        'g4dn.xlarge': 0.526, 'g4dn.2xlarge': 0.752
    }
    
    S3_PRICING = {
        'standard': 0.023,
        'intelligent_tiering': 0.0125,
        'standard_ia': 0.0125,
        'one_zone_ia': 0.01,
        'glacier': 0.004,
        'glacier_deep_archive': 0.00099,
        'glacier_instant_retrieval': 0.01
    }
    
    RDS_PRICING = {
        # MySQL, PostgreSQL, MariaDB
        'db.t3.micro': 0.017, 'db.t3.small': 0.034, 'db.t3.medium': 0.068,
        'db.t3.large': 0.136, 'db.t3.xlarge': 0.272, 'db.t3.2xlarge': 0.544,
        'db.r5.large': 0.29, 'db.r5.xlarge': 0.58, 'db.r5.2xlarge': 1.16,
        'db.r5.4xlarge': 2.32, 'db.r5.8xlarge': 4.64, 'db.r5.12xlarge': 6.96,
        'db.r5.16xlarge': 9.28, 'db.r5.24xlarge': 13.92,
        
        # Storage pricing
        'storage': 0.115  # GP2 storage per GB-month
    }
    
    LAMBDA_PRICING = {
        'request': 0.20,  # per 1M requests
        'duration': 0.0000166667  # per GB-second
    }
    
    DYNAMODB_PRICING = {
        'write': 1.25,    # per million write request units
        'read': 0.25,     # per million read request units
        'storage': 0.25   # per GB per month
    }
    
    ELASTICACHE_PRICING = {
        'cache.t3.micro': 0.017, 'cache.t3.small': 0.034, 'cache.t3.medium': 0.068,
        'cache.m5.large': 0.127, 'cache.m5.xlarge': 0.254, 'cache.m5.2xlarge': 0.508,
        'cache.m5.4xlarge': 1.016, 'cache.m5.12xlarge': 3.048, 'cache.m5.24xlarge': 6.096,
        'cache.r5.large': 0.168, 'cache.r5.xlarge': 0.336, 'cache.r5.2xlarge': 0.672,
        'cache.r5.4xlarge': 1.344, 'cache.r5.12xlarge': 4.032, 'cache.r5.24xlarge': 8.064
    }
    
    EBS_PRICING = {
        'gp2': 0.10,      # General Purpose SSD (gp2)
        'gp3': 0.08,      # General Purpose SSD (gp3)
        'io1': 0.125,     # Provisioned IOPS SSD (io1)
        'io2': 0.125,     # Provisioned IOPS SSD (io2)
        'st1': 0.045,     # Throughput Optimized HDD
        'sc1': 0.015,     # Cold HDD
        'standard': 0.05  # Magnetic
    }
    
    # API Gateway Pricing
    API_GATEWAY_PRICING = {
        'requests': 1.00,     # per million requests
        'data_transfer': 0.09 # per GB
    }

    # Aurora Pricing
    AURORA_PRICING = {
        'db.r5.large': 0.29, 'db.r5.xlarge': 0.58, 'db.r5.2xlarge': 1.16,
        'db.r5.4xlarge': 2.32, 'db.r5.8xlarge': 4.64, 'db.r5.12xlarge': 6.96,
        'db.r5.16xlarge': 9.28, 'db.r5.24xlarge': 13.92,
        'db.r6g.large': 0.26, 'db.r6g.xlarge': 0.52, 'db.r6g.2xlarge': 1.04,
        'db.r6g.4xlarge': 2.08, 'db.r6g.8xlarge': 4.16, 'db.r6g.16xlarge': 8.32,
        'storage': 0.10,
        'io': 0.20
    }

    # CloudFront Pricing
    CLOUDFRONT_PRICING = {
        'data_transfer': {
            'first_10tb': 0.085,
            'next_40tb': 0.080,
            'next_100tb': 0.060
        },
        'requests': {
            'http': 0.0075,   # per 10,000
            'https': 0.01     # per 10,000
        }
    }

    # ECR Pricing
    ECR_PRICING = {
        'storage': 0.10,      # per GB-month
        'data_transfer': 0.09 # per GB
    }

    # ECS Pricing
    ECS_PRICING = {
        'fargate': {
            'vcpu': 0.04048,  # per vCPU-hour
            'memory': 0.004445 # per GB-hour
        }
    }

    # EKS Pricing
    EKS_PRICING = {
        'cluster': 0.10,      # per hour
        'fargate': {
            'vcpu': 0.04048,
            'memory': 0.004445
        }
    }

    # Elastic Beanstalk
    BEANSTALK_PRICING = {
        'environment': 0.0    # No additional charge beyond resources
    }

    # ELB Pricing
    ELB_PRICING = {
        'application': 0.0225,  # Application Load Balancer per hour
        'network': 0.0225,      # Network Load Balancer per hour
        'gateway': 0.0225,      # Gateway Load Balancer per hour
        'classic': 0.025,       # Classic Load Balancer per hour
        'data_processing': {
            'alb': 0.008,       # per LCU-hour
            'nlb': 0.006,       # per NLCU-hour
            'gwlb': 0.004       # per GWLCU-hour
        }
    }

    # Redshift Pricing
    REDSHIFT_PRICING = {
        'dc2.large': 0.25, 'dc2.8xlarge': 4.80,
        'ra3.xlplus': 0.85, 'ra3.4xlarge': 3.40, 'ra3.16xlarge': 13.60,
        'ds2.xlarge': 0.85, 'ds2.8xlarge': 6.80,
        'storage': 0.024  # per GB-month
    }

    # Route 53 Pricing
    ROUTE53_PRICING = {
        'hosted_zone': 0.50,  # per hosted zone per month
        'queries': {
            'first_billion': 0.40,  # per million queries
            'over_billion': 0.20    # per million queries
        }
    }

    # SNS Pricing
    SNS_PRICING = {
        'publish': 0.50,      # per million requests
        'http': 0.60,         # per million notifications
        'email': 2.00         # per 100,000 notifications
    }

    # SQS Pricing
    SQS_PRICING = {
        'requests': 0.40,     # per million requests
        'fifo': 0.50         # per million requests (FIFO queues)
    }

    # VPC Pricing
    VPC_PRICING = {
        'endpoint': 0.01,     # per endpoint per hour
        'nat_gateway': 0.045, # per hour
        'vpn': 0.05          # per VPN connection per hour
    } 