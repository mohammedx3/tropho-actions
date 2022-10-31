import boto3
# from taskcat.testing import CFNTest
import atexit
# import time

region = "us-east-1"
vpc_cidr = '10.0.0.0/24'
private_subnet_cidr = '10.0.0.0/26'
public_subnet_cidr = '10.0.0.64/26'
protected_subnet_cidr = '10.0.0.128/26'
template_file_location = 'dev.json'
stack_name = 'test-template-generator1'

client = boto3.client('ec2', region_name=region)
cf_client = boto3.client("cloudformation", region_name="us-east-1")
cf_resource = boto3.resource("cloudformation", region_name="us-east-1")

def find_output(output_key, stack):
    for output in stack.outputs:
        key = output["OutputKey"]
        value = output["OutputValue"]
        if key == output_key:
            return value

    for output in stack.outputs:
        if output.key == output_key:
            return output.value

def ids(stack):
    return {
        "nat_gateway_id" : find_output("NatGatewayId", stack),
        "nat_eip" : find_output("NatEip", stack),
        "internet_gateway_id" : find_output("InternetGatewayId", stack),
        "private_subnet_id" : find_output("PrivateSubnetId", stack),
        "public_subnet_id" : find_output("PublicSubnetId", stack),
        "protected_subnet_id" : find_output("ProtectedSubnetId", stack),
        "public_route_table_id" : find_output("PublicRouteTableId", stack),
        "protected_route_table_id" : find_output("ProtectedRouteTableId", stack),
        "vpc_id" : find_output("VPCId", stack)
    }

with open(template_file_location, "r") as template_file:
    template_content = template_file.read()

print("Creating {}".format(stack_name))
cf_client.create_stack(
    StackName=stack_name,
    TemplateBody=template_content,
)

print("Waiting for stack creation to complete...")
waiter = cf_client.get_waiter('stack_create_complete').wait(StackName=stack_name)
stack = cf_resource.Stack(stack_name)

nat_gateway_id = ids(stack)["nat_gateway_id"]
nat_eip = ids(stack)["nat_eip"]
internet_gateway_id = ids(stack)["internet_gateway_id"]
private_subnet_id = ids(stack)["private_subnet_id"]
public_subnet_id = ids(stack)["public_subnet_id"]
protected_subnet_id = ids(stack)["protected_subnet_id"]
public_route_table_id = ids(stack)["public_route_table_id"]
protected_route_table_id = ids(stack)["protected_route_table_id"]
vpc_id = ids(stack)["vpc_id"]

def test_nat_gateway():
    nat_gateway = client.describe_nat_gateways(NatGatewayIds=[nat_gateway_id])
    public_ip = nat_gateway['NatGateways'][0]['NatGatewayAddresses'][0]['PublicIp']
    assert public_ip == nat_eip

def test_internet_gateway():
    internet_gateway = client.describe_internet_gateways(InternetGatewayIds=[internet_gateway_id])
    state = internet_gateway['InternetGateways'][0]['Attachments'][0]['State']
    assert 'available' == state

def test_protected_route_table():
    route_table = client.describe_route_tables(RouteTableIds=[protected_route_table_id])
    first_route = route_table['RouteTables'][0]['Routes'][0]
    second_route = route_table['RouteTables'][0]['Routes'][1]
    assert first_route['DestinationCidrBlock'] == vpc_cidr and first_route['GatewayId'] == "local"
    assert second_route['DestinationCidrBlock'] == "0.0.0.0/0" and second_route['NatGatewayId'] == nat_gateway_id

def test_public_route_table():
    route_table = client.describe_route_tables(RouteTableIds=[public_route_table_id])
    first_route = route_table['RouteTables'][0]['Routes'][0]
    second_route = route_table['RouteTables'][0]['Routes'][1]
    assert first_route['DestinationCidrBlock'] == vpc_cidr and first_route['GatewayId'] == "local"
    assert second_route['DestinationCidrBlock'] == "0.0.0.0/0" and second_route['GatewayId'] == internet_gateway_id

def test_vpc():
    vpc = client.describe_vpcs(VpcIds=[vpc_id])
    vpc_cidr = vpc['Vpcs'][0]['CidrBlock']
    vpc_instance_tenancy = vpc['Vpcs'][0]['InstanceTenancy']
    assert vpc_cidr == vpc_cidr
    assert 'default' == vpc_instance_tenancy

def test_subnets():
    private_subnet = client.describe_subnets(SubnetIds=[private_subnet_id])
    public_subnet = client.describe_subnets(SubnetIds=[public_subnet_id])
    protected_subnet = client.describe_subnets(SubnetIds=[protected_subnet_id])
    assert private_subnet_cidr == private_subnet['Subnets'][0]['CidrBlock']
    assert public_subnet_cidr == public_subnet['Subnets'][0]['CidrBlock']
    assert protected_subnet_cidr == protected_subnet['Subnets'][0]['CidrBlock']



def exit_handler():
    cf_client.delete_stack(
    StackName=stack_name
)

atexit.register(exit_handler)