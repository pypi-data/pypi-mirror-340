"""
腾讯云 CVM 相关操作工具模块
"""
import json
from tencentcloud.cvm.v20170312 import cvm_client, models as cvm_models
from .client import get_cvm_client
from asyncio.log import logger
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException

def describe_regions() -> str:
    """查询地域列表"""
    client = get_cvm_client("ap-guangzhou")  # 使用默认地域
    req = cvm_models.DescribeRegionsRequest()
    resp = client.DescribeRegions(req)
    return resp.to_json_string()

def describe_zones(region: str) -> str:
    """查询可用区列表"""
    client = get_cvm_client(region)
    req = cvm_models.DescribeZonesRequest()
    resp = client.DescribeZones(req)
    return resp.to_json_string()

def describe_instances(region: str, offset: int, limit: int, instance_ids: list[str]) -> str:
    """查询实例列表"""
    client = get_cvm_client(region)
    req = cvm_models.DescribeInstancesRequest()
    
    params = {
        "Offset": offset,
        "Limit": limit
    }
    if instance_ids:
        params["InstanceIds"] = instance_ids
        
    req.from_json_string(json.dumps(params))
    resp = client.DescribeInstances(req)
    return resp.to_json_string()

def describe_images(region: str, image_ids: list[str] = None, image_type: str = None,
                  platform: str = None, image_name: str = None,
                  offset: int = None, limit: int = None) -> str:
    """查询镜像列表
    
    Args:
        region (str): 地域ID
        image_ids (list[str], optional): 镜像ID列表
        image_type (str, optional): 镜像类型
        platform (str, optional): 操作系统平台
        image_name (str, optional): 镜像名称
        offset (int, optional): 偏移量
        limit (int, optional): 返回数量
        
    Returns:
        str: API响应结果的JSON字符串
    """
    client = get_cvm_client(region)
    req = cvm_models.DescribeImagesRequest()
    
    # 构建参数
    params = {}
    filters = []
    
    # 添加过滤条件
    if image_type:
        filters.append({
            "Name": "image-type",
            "Values": [image_type]
        })
    if platform:
        filters.append({
            "Name": "platform",
            "Values": [platform]
        })
    if image_name:
        filters.append({
            "Name": "image-name",
            "Values": [image_name]
        })
        
    if filters:
        params["Filters"] = filters
    if image_ids:
        params["ImageIds"] = image_ids
    if offset is not None:
        params["Offset"] = offset
    if limit is not None:
        params["Limit"] = limit
        
    if params:
        req.from_json_string(json.dumps(params))
    resp = client.DescribeImages(req)
    return resp.to_json_string()

def describe_instance_type_configs(region: str, zone: str = None, instance_family: str = None) -> str:
    """查询实例机型配置"""
    client = get_cvm_client(region)
    req = cvm_models.DescribeInstanceTypeConfigsRequest()
    
    params = {}
    if zone:
        params["Filters"] = [{
            "Name": "zone",
            "Values": [zone]
        }]
    if instance_family:
        if "Filters" not in params:
            params["Filters"] = []
        params["Filters"].append({
            "Name": "instance-family",
            "Values": [instance_family]
        })
        
    if params:
        req.from_json_string(json.dumps(params))
    resp = client.DescribeInstanceTypeConfigs(req)
    return resp.to_json_string()

def reboot_instances(region: str, instance_ids: list[str], stop_type: str) -> str:
    """重启实例"""
    client = get_cvm_client(region)
    req = cvm_models.RebootInstancesRequest()
    
    params = {
        "InstanceIds": instance_ids,
        "StopType": stop_type
    }
    req.from_json_string(json.dumps(params))
    resp = client.RebootInstances(req)
    return resp.to_json_string()

def start_instances(region: str, instance_ids: list[str]) -> str:
    """启动实例"""
    client = get_cvm_client(region)
    req = cvm_models.StartInstancesRequest()
    
    params = {
        "InstanceIds": instance_ids
    }
    req.from_json_string(json.dumps(params))
    resp = client.StartInstances(req)
    return resp.to_json_string()

def stop_instances(region: str, instance_ids: list[str], stop_type: str, stopped_mode: str) -> str:
    """关闭实例"""
    client = get_cvm_client(region)
    req = cvm_models.StopInstancesRequest()
    
    params = {
        "InstanceIds": instance_ids,
        "StopType": stop_type,
        "StoppedMode": stopped_mode
    }
    req.from_json_string(json.dumps(params))
    resp = client.StopInstances(req)
    return resp.to_json_string()

def terminate_instances(region: str, instance_ids: list[str]) -> str:
    """销毁实例"""
    client = get_cvm_client(region)
    req = cvm_models.TerminateInstancesRequest()
    
    params = {
        "InstanceIds": instance_ids
    }
    req.from_json_string(json.dumps(params))
    resp = client.TerminateInstances(req)
    return resp.to_json_string()

def reset_instances_password(region: str, instance_ids: list[str], password: str, force_stop: bool) -> str:
    """重置实例密码"""
    client = get_cvm_client(region)
    req = cvm_models.ResetInstancesPasswordRequest()
    
    params = {
        "InstanceIds": instance_ids,
        "Password": password,
        "ForceStop": force_stop
    }
    req.from_json_string(json.dumps(params))
    resp = client.ResetInstancesPassword(req)
    return resp.to_json_string()

def run_instances(region: str, params: dict) -> str:
    """创建实例"""
    try:
        from .run_instances import run_instances as run_instances_impl
        return run_instances_impl(
            region=region,
            zone=params.get("Zone"),
            instance_type=params.get("InstanceType"),
            image_id=params.get("ImageId"),
            vpc_id=params.get("VpcId"),
            subnet_id=params.get("SubnetId"),
            security_group_ids=params.get("SecurityGroupIds"),
            password=params.get("Password"),
            instance_name=params.get("InstanceName"),
            instance_charge_type=params.get("InstanceChargeType"),
            instance_count=params.get("InstanceCount"),
            dry_run=params.get("DryRun", False)
        )
    except Exception as e:
        logger.error(f"创建实例失败: {str(e)}")
        raise e

def reset_instance(region: str, instance_id: str, image_id: str, password: str = None) -> str:
    """重装实例操作系统
    
    Args:
        region (str): 实例所在地域
        instance_id (str): 实例ID
        image_id (str): 重装使用的镜像ID
        password (str, optional): 实例重装后的密码。如果不指定，保持原密码不变
        
    Returns:
        str: API响应结果的JSON字符串
        
    Raises:
        Exception: 当API调用失败时抛出异常
    """
    try:
        client = get_cvm_client(region)
        # 设置实例登录配置
        login_settings = cvm_models.LoginSettings()
        if password:
            login_settings.Password = password
        
        req = cvm_models.ResetInstanceRequest()
        req.InstanceId = instance_id
        req.ImageId = image_id
        req.LoginSettings = login_settings
        resp = client.ResetInstance(req)
        return resp.to_json_string()
    except Exception as e:
        logger.error(f"重装实例操作系统失败: {str(e)}")
        raise e 