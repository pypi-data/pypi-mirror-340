"""
腾讯云 VPC 相关操作工具模块
"""
import json
from tencentcloud.vpc.v20170312 import models as vpc_models
from .client import get_vpc_client

def describe_security_groups(region: str, security_group_ids: list[str] = None) -> str:
    """查询安全组列表"""
    client = get_vpc_client(region)
    req = vpc_models.DescribeSecurityGroupsRequest()
    
    params = {}
    if security_group_ids:
        params["SecurityGroupIds"] = security_group_ids
        
    if params:
        req.from_json_string(json.dumps(params))
    resp = client.DescribeSecurityGroups(req)
    return resp.to_json_string()

def describe_vpcs(region: str, vpc_ids: list[str] = None) -> str:
    """查询VPC列表"""
    client = get_vpc_client(region)
    req = vpc_models.DescribeVpcsRequest()
    
    params = {}
    if vpc_ids:
        params["VpcIds"] = vpc_ids
        
    if params:
        req.from_json_string(json.dumps(params))
    resp = client.DescribeVpcs(req)
    return resp.to_json_string()

def describe_subnets(region: str, vpc_id: str = None, subnet_ids: list[str] = None) -> str:
    """查询子网列表"""
    client = get_vpc_client(region)
    req = vpc_models.DescribeSubnetsRequest()
    
    params = {}
    if vpc_id:
        params["Filters"] = [{
            "Name": "vpc-id",
            "Values": [vpc_id]
        }]
    if subnet_ids:
        params["SubnetIds"] = subnet_ids
        
    if params:
        req.from_json_string(json.dumps(params))
    resp = client.DescribeSubnets(req)
    return resp.to_json_string() 