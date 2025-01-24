from flask import Blueprint, render_template, request, jsonify
from ..services.calculator_service import CalculatorService

calculator_bp = Blueprint('calculator', __name__)
calculator_service = CalculatorService()

@calculator_bp.route('/')
def home():
    return render_template('calculator.html')

@calculator_bp.route('/api/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        service = data.get('service')
        
        if service == 'apigateway':
            requests = float(data.get('apiRequests', 0))
            data_transfer = float(data.get('apiDataTransfer', 0))
            result = calculator_service.calculate_api_gateway_cost(requests, data_transfer)
            
        elif service == 'aurora':
            instance_type = data.get('auroraInstance')
            storage_gb = float(data.get('auroraStorage', 0))
            io_requests = float(data.get('auroraIO', 0))
            result = calculator_service.calculate_aurora_cost(instance_type, storage_gb, io_requests)
            
        elif service == 'cloudfront':
            data_transfer = float(data.get('cfDataTransfer', 0))
            http_requests = float(data.get('cfHttpRequests', 0))
            https_requests = float(data.get('cfHttpsRequests', 0))
            result = calculator_service.calculate_cloudfront_cost(data_transfer, http_requests, https_requests)
            
        elif service == 'dynamodb':
            read_capacity = int(data.get('readCapacity', 0))
            write_capacity = int(data.get('writeCapacity', 0))
            storage = float(data.get('storageGB', 0))
            result = calculator_service.calculate_dynamodb_cost(read_capacity, write_capacity, storage)
            
        elif service == 'ebs':
            volume_type = data.get('ebsType')
            size = float(data.get('ebsSize', 0))
            result = calculator_service.calculate_ebs_cost(volume_type, size)
            
        elif service == 'ec2':
            instance_type = data.get('instanceType')
            hours = float(data.get('hours', 0))
            region = data.get('region', 'us-east-1')
            result = calculator_service.calculate_ec2_cost(instance_type, hours, region)
            
        elif service == 'ecr':
            storage = float(data.get('ecrStorage', 0))
            data_transfer = float(data.get('ecrDataTransfer', 0))
            result = calculator_service.calculate_ecr_cost(storage, data_transfer)
            
        elif service == 'ecs':
            vcpu_hours = float(data.get('ecsVCPU', 0))
            memory_hours = float(data.get('ecsMemory', 0))
            result = calculator_service.calculate_ecs_cost(vcpu_hours, memory_hours)
            
        elif service == 'eks':
            cluster_hours = float(data.get('eksClusterHours', 0))
            fargate_vcpu = float(data.get('eksFargateVCPU', 0))
            fargate_memory = float(data.get('eksFargateMemory', 0))
            result = calculator_service.calculate_eks_cost(cluster_hours, fargate_vcpu, fargate_memory)
            
        elif service == 'elasticache':
            instance_type = data.get('cacheInstanceType')
            nodes = int(data.get('nodes', 1))
            result = calculator_service.calculate_elasticache_cost(instance_type, nodes)
            
        elif service == 'elb':
            lb_type = data.get('elbType')
            hours = float(data.get('elbHours', 0))
            processed_gb = float(data.get('elbProcessedBytes', 0))
            result = calculator_service.calculate_elb_cost(lb_type, hours, processed_gb)
            
        elif service == 'lambda':
            memory = int(data.get('memorySize', 128))
            executions = int(data.get('executions', 0))
            duration = float(data.get('avgDuration', 0))
            result = calculator_service.calculate_lambda_cost(memory, executions, duration)
            
        elif service == 'rds':
            instance_type = data.get('dbInstanceType')
            hours = float(data.get('dbHours', 0))
            storage_gb = float(data.get('storageGB', 20))
            result = calculator_service.calculate_rds_cost(instance_type, hours, storage_gb)
            
        elif service == 'redshift':
            node_type = data.get('redshiftType')
            nodes = int(data.get('redshiftNodes', 1))
            storage = float(data.get('redshiftStorage', 0))
            result = calculator_service.calculate_redshift_cost(node_type, nodes, storage)
            
        elif service == 'route53':
            zones = int(data.get('route53Zones', 0))
            queries = float(data.get('route53Queries', 0))
            result = calculator_service.calculate_route53_cost(zones, queries)
            
        elif service == 's3':
            storage_gb = float(data.get('storage', 0))
            storage_class = data.get('storageClass', 'standard')
            result = calculator_service.calculate_s3_cost(storage_gb, storage_class)
            
        elif service == 'sns':
            publish_requests = float(data.get('snsPublishRequests', 0))
            http_deliveries = float(data.get('snsHttpDeliveries', 0))
            email_deliveries = float(data.get('snsEmailDeliveries', 0))
            result = calculator_service.calculate_sns_cost(publish_requests, http_deliveries, email_deliveries)
            
        elif service == 'sqs':
            queue_type = data.get('sqsType', 'standard')
            requests = float(data.get('sqsRequests', 0))
            result = calculator_service.calculate_sqs_cost(queue_type, requests)
            
        elif service == 'vpc':
            endpoints = int(data.get('vpcEndpoints', 0))
            nat_gateways = int(data.get('vpcNatGateways', 0))
            vpn_connections = int(data.get('vpcVpnConnections', 0))
            result = calculator_service.calculate_vpc_cost(endpoints, nat_gateways, vpn_connections)
            
        else:
            return jsonify({'error': 'Invalid service specified'}), 400
            
        if result:
            return jsonify({
                'success': True,
                'calculation': {
                    'service': result.service,
                    'usage': result.usage,
                    'unitPrice': result.unit_price,
                    'totalCost': result.total_cost,
                    'details': result.details
                }
            })
        else:
            return jsonify({'error': 'Calculation failed'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500 