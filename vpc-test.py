import boto3

client = boto3.client('ec2',region_name='us-east-1')
# vpc = client.describe_vpcs(
#     test1=[
#         {
#             'Name': 'tag:Environment',
#             'Values': [
#                 'dev',
#             ]
#         },        
#     ]
# )
# print(vpc)
# for i in vpc['Vpcs']:
#     print(i['CidrBlock'])
#     print(i['InstanceTenancy'])
# assert ipaddress.ip_address(i['PublicIp'])


# resp1 = vpc['Vpcs'][0]['InstanceTenancy']

# vpc = client.describe_vpcs(VpcIds=["vpc-322cca4f"])
# vpc_cidr = vpc['Vpcs'][0]['CidrBlock']
# print(vpc_cidr)
# assert "172.31.0.0/s16" == vpc_cidr

# internet_gateway = client.describe_internet_gateways(InternetGatewayIds=["igw-a7792cdc"])
# test = internet_gateway['InternetGateways'][0]['Attachments'][0]['State']
# assert "avasilable" in test
# nat_gateway = client.describe_nat_gateways(NatGatewayIds=["nat-0cffb130600a25246"])
# print(nat_gateway['NatGateways'][0]['NatGatewayAddresses'][0]['PublicIp'])
# for i in nat_gateway['InternetGateways']:
#     for index in i['Attachments']:
#         assert index['State']



# subnet = client.describe_subnets(SubnetIds=['subnet-07b1686b35f965782'])
# print(subnet)
# # print(subnet)
# for i in subnet['Subnets']:
# print(subnet['Subnets'][0])
# subnet_cidr = subnet[0]['CidrBlock']
#     print(subnet_cidr)
#     assert "172.31.32.0/20" in subnet_cidr and "172.31.32.0/20" in subnet_cidr
    # assert private_subnet in subnet_cidr
# for i in subnet['Subnets']:
#     print(i['CidrBlock'])
# print(subnet['Subnets']['CidrBlock'])

# print(subnet)

# internet_gateway = client.describe_internet_gateways(
#     test1=[
#         {
#             'Name': 'tag:Environment',
#             'Values': [
#                 'dev',
#             ]
#         },        
#     ]
# )

# for i in internet_gateway['InternetGateways']:
#     for index in i['Attachments']:
#         print(index['State'])

# nat_eip = client.describe_addresses(
#     Filters=[
#         {
#             'Name': 'tag:Environment',
#             'Values': [
#                 'dev',
#             ]
#         },        
#     ]
# )
# print(nat_eip)
# for i in nat_eip['Addresses']:
#     print(i['PublicIp'])
    # for index in i['PublicIp']:
    #     print(index)


# filters=[{'Name': 'tag:Environment', 'Values': ['dev']}]
# nat_eip = client.describe_addresses(Filters=filters)
# # print(nat_eip['Addresses'][0]['PublicIp'])
# # print(nat_eip['Addresses']['PublicIp'])
# for i in nat_eip:
#     print(i['Addresses'][i]['PublicIp'])

# route_tables = client.describe_route_tables(RouteTableIds=['rtb-0124477eac89d7dd1']
    #     Filters=[
    #     {
    #         'Name': 'tag:Environment',
    #         'Values': [
    #             'dev',
    #         ]
    #     },        
    # ]
# )
# routes = []
# for i in route_tables['RouteTables']:
#     if i['Routes'][0]['DestinationCidrBlock'] == "10.0.0.0/24" and i['Routes'][0]['GatewayId'] == "local": 
#         print('success')
#     if i['Routes'][1]['DestinationCidrBlock'] == "0.0.0.0/0" and i['Routes'][1]['GatewayId'] == "igw-0dfde4e9a40cbc9d0": 
#         print('success')
    
    # for j in i['Routes']:
    #     routes.append(j['DestinationCidrBlock'])

# if routes[0] == "10.0.0.0/24" and routes[1] == "0.0.0.0/0":
#     print("success")
# print(routes)
# for i in route_tables['RouteTables']:
#     for j in i['Routes']:
#         print(j)

# print(route_tables)

# nat_gateway = client.describe_nat_gateways(NatGatewayIds=['nat-076f28fb93a1244d2'])

# for i in nat_gateway['NatGateways']:
#     for j in i['NatGatewayAddresses']:
#         if j['PublicIp'] == "54.146.205.86" and i['NatGatewayId'] == "nat-076f28fb93a1244d2":
#             print('success')
        # print(i['NatGatewayId'])
    # print(i['NatGatewayId'])
    # for k in i['NatGatewayId']:
    #     print(k)


# resp2 = subnet['Subnets']
# if resp2:
#     print(resp2)
# else:
#     print('No vpcs found')

# if resp1:
#     print(resp1)
# else:
#     print('No vpcs found')

route_table = client.describe_route_tables(RouteTableIds=["rtb-0a2e6d3ef943c3107"])
first_route = route_table['RouteTables'][0]['Routes'][0]
second_route = route_table['RouteTables'][0]['Routes'][1]
print(first_route)

# print(second_route)

# private_subnet_id = 'subnet-0ca701e469f4a7d23'
# private_subnet = client.describe_subnets(SubnetIds=[private_subnet_id])
# print(private_subnet[)
# print(first_route['DestinationCidrBlock'])