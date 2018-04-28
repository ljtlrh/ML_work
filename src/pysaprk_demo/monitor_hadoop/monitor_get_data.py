#!/usr/bin/env python
# -*- coding:utf-8 -*-  
"""
@version: python2.7
@author: ‘liujiantao‘ 
@contact: 1329331182@qq.com
@site: 
@software: PyCharm
@file: monitor_get_data.py
@time: 18-4-27 下午5:54
"""
import urllib.request as urllib2
import json
import os

# settings section
ZABBIX_NAME = "namenode"
CLUSTER_HOST = "127.0.0.1"


class MonitorGetData(object):

    def GetHeapMemory(self):
        # --------------------------------------------------------------------------------------------
        # HeapMemory
        # --------------------------------------------------------------------------------------------
        HeapMemory = {}
        url1 = "http://" + CLUSTER_HOST + ":50070/jmx?qry=java.lang:type=Memory"
        response = urllib2.Request(url1)
        res_data = urllib2.urlopen(response)
        res = res_data.read()
        hjson = json.loads(res.decode())
        heap_memory_committed = round(float(hjson['beans'][0]["HeapMemoryUsage"]["committed"]) / 1024 / 1024, 2)
        heap_memory_init = round(float(hjson['beans'][0]["HeapMemoryUsage"]["init"]) / 1024 / 1024, 2)
        heap_memory_max = round(float(hjson['beans'][0]["HeapMemoryUsage"]["max"]) / 1024 / 1024, 2)
        heap_memory_used = round(float(hjson['beans'][0]["HeapMemoryUsage"]["used"]) / 1024 / 1024, 2)
        nonheap_memory_committed = round(float(hjson['beans'][0]["NonHeapMemoryUsage"]["committed"]) / 1024 / 1024, 2)
        nonheap_memory_init = round(float(hjson['beans'][0]["NonHeapMemoryUsage"]["init"]) / 1024 / 1024, 2)
        nonheap_memory_max = round(float(hjson['beans'][0]["NonHeapMemoryUsage"]["max"]) / 1024 / 1024, 2)
        nonheap_memory_used = round(float(hjson['beans'][0]["NonHeapMemoryUsage"]["used"]) / 1024 / 1024, 2)
        HeapMemory['heap_memory_committed']=heap_memory_committed
        HeapMemory['heap_memory_max']=heap_memory_max
        HeapMemory['heap_memory_init']=heap_memory_init
        HeapMemory['heap_memory_used']=heap_memory_used
        HeapMemory['nonheap_memory_committed']=nonheap_memory_committed
        HeapMemory['nonheap_memory_init']=nonheap_memory_init
        HeapMemory['nonheap_memory_max']=nonheap_memory_max
        HeapMemory['nonheap_memory_used']=nonheap_memory_used
        return HeapMemory

    def FSNamesystemState(self):
        """

        :return:
        """
        fsn_amesystem_state = {}
        url2 = "http://" + CLUSTER_HOST + ":50070/jmx?qry=Hadoop:service=NameNode,name=FSNamesystemState"
        response = urllib2.Request(url2)
        res_data = urllib2.urlopen(response)
        res = res_data.read()
        hjson = json.loads(res.decode())

        live_nodes = hjson['beans'][0]["NumLiveDataNodes"]
        dead_nodes = hjson['beans'][0]["NumDeadDataNodes"]
        decom_live_nodes = hjson['beans'][0]["NumDecomLiveDataNodes"]
        decom_dead_nodes = hjson['beans'][0]["NumDecomDeadDataNodes"]
        volume_failures_total = hjson['beans'][0]["VolumeFailuresTotal"]
        estimated_capacitylost_total = hjson['beans'][0]["EstimatedCapacityLostTotal"]
        decommissioning_nodes = hjson['beans'][0]["NumDecommissioningDataNodes"]
        pending_repllicated_blocks = hjson['beans'][0]["PendingReplicationBlocks"]
        under_repllicated_blocks = hjson['beans'][0]["UnderReplicatedBlocks"]
        scheduled_repllicated_blocks = hjson['beans'][0]["ScheduledReplicationBlocks"]
        pending_deletion_blocks = hjson['beans'][0]["PendingDeletionBlocks"]
        fsn_amesystem_state['live_nodes']=live_nodes
        fsn_amesystem_state['dead_nodes']=dead_nodes
        fsn_amesystem_state['decom_live_nodes']=decom_live_nodes
        fsn_amesystem_state['decom_dead_nodes']=decom_dead_nodes
        fsn_amesystem_state['volume_failures_total']=volume_failures_total
        fsn_amesystem_state['estimated_capacitylost_total']=estimated_capacitylost_total
        fsn_amesystem_state['decommissioning_nodes']=decommissioning_nodes
        fsn_amesystem_state['pending_repllicated_blocks']=pending_repllicated_blocks
        fsn_amesystem_state['under_repllicated_blocks']=under_repllicated_blocks
        fsn_amesystem_state['scheduled_repllicated_blocks']=scheduled_repllicated_blocks
        fsn_amesystem_state['pending_deletion_blocks']=pending_deletion_blocks
        return fsn_amesystem_state

    def NameNodeInfo(self):
        name_node_info = {}
        url1 = "http://" + CLUSTER_HOST + ":50070/jmx?qry=Hadoop:service=NameNode,name=NameNodeInfo"
        response = urllib2.Request(url1)
        res_data = urllib2.urlopen(response)
        res = res_data.read()
        hjson = json.loads(res.decode())
        start_time = hjson['beans'][0]["NNStarted"]
        name_node_info['start_time'] = start_time
        hadoop_version = hjson['beans'][0]["SoftwareVersion"]
        file_and_directory_count = hjson['beans'][0]["TotalFiles"]
        dfs_blocks = hjson['beans'][0]["TotalBlocks"]
        storage_unit = "TB"
        name_node_info['hadoop_version']= hadoop_version
        name_node_info['file_and_directory_count']= file_and_directory_count
        name_node_info['dfs_blocks']= dfs_blocks
        name_node_info['storage_unit']= storage_unit
        configured_cluster_storage = hjson['beans'][0]["Total"]
        configured_cluster_storage = round(float(configured_cluster_storage) / 1024 / 1024 / 1024 / 1024, 2)
        name_node_info['configured_cluster_storage'] = configured_cluster_storage
        dfs_use_storage = hjson['beans'][0]["Used"]
        dfs_use_storage = round(float(dfs_use_storage) / 1024 / 1024 / 1024 / 1024, 2)
        non_dfs_use_storage = hjson['beans'][0]["NonDfsUsedSpace"]
        non_dfs_use_storage = round(float(non_dfs_use_storage) / 1024 / 1024 / 1024 / 1024, 2)
        available_dfs_storage = hjson['beans'][0]["Free"]
        available_dfs_storage = round(float(available_dfs_storage) / 1024 / 1024 / 1024 / 1024, 2)
        used_storage_pct = hjson['beans'][0]["PercentUsed"]
        used_storage_pct = round(float(used_storage_pct), 2)
        available_storage_pct = hjson['beans'][0]["PercentRemaining"]
        available_storage_pct = round(float(available_storage_pct), 2)
        name_node_info['dfs_use_storage'] = dfs_use_storage
        name_node_info['non_dfs_use_storage'] = non_dfs_use_storage
        name_node_info['available_dfs_storage'] = available_dfs_storage
        name_node_info['used_storage_pct'] = used_storage_pct
        name_node_info['available_storage_pct'] = available_storage_pct
        test = hjson['beans'][0]["LiveNodes"]
        test1 = test.replace("\\", "")
        LiveNodes = json.loads(test1)
        name_node_info['LiveNodes'] = LiveNodes
        max_configured_storage_node_name = ""
        max_configured_storage = 0
        max_used_storage_node_name = ""
        max_used_storage = 0
        max_non_dfs_used_storage_node_name = ""
        max_non_dfs_used_storage = 0
        max_free_storage_node_name = ""
        max_free_storage = 0
        max_used_storage_pct_node_name = ""
        max_used_storage_pct = 0
        max_free_storage_pct_node_name = ""
        max_free_storage_pct = 0

        for key in LiveNodes:
            if (isinstance(LiveNodes[key], dict)):
                if LiveNodes[key]["capacity"] > max_configured_storage:
                    max_configured_storage = LiveNodes[key]["capacity"]
                    max_configured_storage_node_name = key
                    name_node_info['LiveNodes']['max_configured_storage_node_name'] = max_configured_storage_node_name
                if LiveNodes[key]["used"] > max_used_storage:
                    max_used_storage = LiveNodes[key]["used"]
                    max_used_storage_node_name = key
                    name_node_info['LiveNodes']['max_used_storage_node_name']=max_used_storage_node_name
                if LiveNodes[key]["nonDfsUsedSpace"] > max_non_dfs_used_storage:
                    max_non_dfs_used_storage = LiveNodes[key]["nonDfsUsedSpace"]
                    max_non_dfs_used_storage_node_name = key
                    name_node_info['LiveNodes']['max_non_dfs_used_storage_node_name'] = max_non_dfs_used_storage_node_name
                if LiveNodes[key]["remaining"] > max_free_storage:
                    max_free_storage = LiveNodes[key]["remaining"]
                    max_free_storage_node_name = key
                    name_node_info['LiveNodes']['max_free_storage_node_name'] = max_free_storage_node_name
                if LiveNodes[key]["used"] * 100 / LiveNodes[key]["capacity"] > max_used_storage_pct:
                    max_used_storage_pct = round(float(LiveNodes[key]["used"] * 100) / LiveNodes[key]["capacity"], 2)
                    max_used_storage_pct_node_name = key
                if LiveNodes[key]["remaining"] * 100 / LiveNodes[key]["capacity"] > max_free_storage_pct:
                    max_free_storage_pct = round(float(LiveNodes[key]["remaining"] * 100) / LiveNodes[key]["capacity"], 2)
                    max_free_storage_pct_node_name = key

        min_configured_storage_node_name = max_configured_storage_node_name
        name_node_info['LiveNodes']['min_configured_storage_node_name'] = min_configured_storage_node_name
        min_configured_storage = max_configured_storage
        name_node_info['LiveNodes']['min_configured_storage'] = min_configured_storage
        min_used_storage_node_name = ""
        min_used_storage = max_used_storage
        name_node_info['LiveNodes']['min_used_storage'] = min_used_storage
        min_non_dfs_used_storage_node_name = ""
        min_non_dfs_used_storage = max_non_dfs_used_storage
        name_node_info['LiveNodes']['max_non_dfs_used_storage'] = max_non_dfs_used_storage
        min_free_storage_node_name = ""
        min_free_storage = max_free_storage
        name_node_info['LiveNodes']['max_free_storage'] = max_free_storage
        min_used_storage_pct_node_name = max_used_storage_pct_node_name
        name_node_info['LiveNodes']['min_used_storage_pct_node_name'] = min_used_storage_pct_node_name
        min_used_storage_pct = 100
        min_free_storage_pct_node_name = max_free_storage_pct_node_name
        name_node_info['LiveNodes']['min_free_storage_pct_node_name'] = min_free_storage_pct_node_name
        min_free_storage_pct = 100
        for key in LiveNodes:
            if (isinstance(LiveNodes[key], dict)):
                if LiveNodes[key]["capacity"] < min_configured_storage:
                    min_configured_storage = LiveNodes[key]["capacity"]
                    min_configured_storage_node_name = key
                    name_node_info['LiveNodes']['min_configured_storage_node_name'] = min_configured_storage_node_name
                if LiveNodes[key]["used"] < min_used_storage:
                    min_used_storage = LiveNodes[key]["used"]
                    min_used_storage_node_name = key
                    name_node_info['LiveNodes']['min_used_storage_node_name'] = min_used_storage_node_name
                if LiveNodes[key]["nonDfsUsedSpace"] < min_non_dfs_used_storage:
                    min_non_dfs_used_storage = LiveNodes[key]["nonDfsUsedSpace"]
                    min_non_dfs_used_storage_node_name = key
                    name_node_info['LiveNodes']['min_non_dfs_used_storage_node_name'] = min_non_dfs_used_storage_node_name
                if LiveNodes[key]["remaining"] < min_free_storage:
                    min_free_storage = LiveNodes[key]["remaining"]
                    min_free_storage_node_name = key
                    name_node_info['LiveNodes']['min_free_storage_node_name'] = min_free_storage_node_name
                if LiveNodes[key]["used"] * 100 / LiveNodes[key]["capacity"] < min_used_storage_pct:
                    min_used_storage_pct = round(float(LiveNodes[key]["used"] * 100) / LiveNodes[key]["capacity"], 2)
                    min_used_storage_pct_node_name = key
                    name_node_info['LiveNodes']['min_used_storage_pct_node_name'] = min_used_storage_pct_node_name
                if LiveNodes[key]["remaining"] * 100 / LiveNodes[key]["capacity"] < min_free_storage_pct:
                    min_free_storage_pct = round(float(LiveNodes[key]["remaining"] * 100) / LiveNodes[key]["capacity"], 2)
                    min_free_storage_pct_node_name = key
                    name_node_info['LiveNodes']['min_free_storage_pct_node_name'] = min_free_storage_pct_node_name
        max_configured_storage = round(float(max_configured_storage) / 1024 / 1024 / 1024 / 1024, 2)
        max_used_storage = round(float(max_used_storage) / 1024 / 1024 / 1024 / 1024, 2)
        max_non_dfs_used_storage = round(float(max_non_dfs_used_storage) / 1024 / 1024 / 1024 / 1024, 2)
        max_free_storage = round(float(max_free_storage) / 1024 / 1024 / 1024 / 1024, 2)
        max_used_storage_pct = round(float(max_used_storage_pct), 2)
        max_free_storage_pct = round(float(max_free_storage_pct), 2)
        min_configured_storage = round(float(min_configured_storage) / 1024 / 1024 / 1024 / 1024, 2)
        min_used_storage = round(float(min_used_storage) / 1024 / 1024 / 1024 / 1024, 2)
        min_non_dfs_used_storage = round(float(min_non_dfs_used_storage) / 1024 / 1024 / 1024 / 1024, 2)
        min_free_storage = round(float(min_free_storage) / 1024 / 1024 / 1024 / 1024, 2)
        min_used_storage_pct = round(float(min_used_storage_pct), 2)
        min_free_storage_pct = round(float(min_free_storage_pct), 2)
        name_node_info['max_configured_storage'] = max_configured_storage
        name_node_info['max_used_storage'] = max_used_storage
        name_node_info['max_non_dfs_used_storage'] = max_non_dfs_used_storage
        name_node_info['max_free_storage'] = max_free_storage
        name_node_info['max_used_storage_pct'] = max_used_storage_pct
        name_node_info['max_free_storage_pct'] = max_free_storage_pct
        name_node_info['min_configured_storage'] = min_configured_storage
        name_node_info['min_used_storage'] = min_used_storage
        name_node_info['min_non_dfs_used_storage'] = min_non_dfs_used_storage
        name_node_info['min_free_storage'] = min_free_storage
        name_node_info['min_used_storage_pct'] = min_used_storage_pct
        name_node_info['min_free_storage_pct'] = min_free_storage_pct
        return name_node_info

    def HadoopResourceManager(self):
        """
         Resource Manager
        :return:
        """
        hadoop_resource_manager = {}
        url1 = "http://" + CLUSTER_HOST + ":8088/jmx?qry=Hadoop:service=ResourceManager,name=ClusterMetrics"
        response = urllib2.Request(url1)
        res_data = urllib2.urlopen(response)
        res = res_data.read()
        hjson = json.loads(res.decode())

        num_active_nms = hjson['beans'][0]["NumActiveNMs"]
        num_decommissioned_nms = hjson['beans'][0]["NumDecommissionedNMs"]
        num_lost_nms = hjson['beans'][0]["NumLostNMs"]
        num_unhealthy_nms = hjson['beans'][0]["NumUnhealthyNMs"]
        num_rebooted_nms = hjson['beans'][0]["NumRebootedNMs"]
        hadoop_resource_manager['num_active_nms'] = num_active_nms
        hadoop_resource_manager['num_decommissioned_nms'] = num_decommissioned_nms
        hadoop_resource_manager['num_lost_nms']=num_lost_nms
        hadoop_resource_manager['num_unhealthy_nms']=num_unhealthy_nms
        hadoop_resource_manager['num_rebooted_nms']=num_rebooted_nms

        url1 = "http://" + CLUSTER_HOST + ":8088/jmx?qry=Hadoop:service=ResourceManager,name=QueueMetrics,q0=root"
        response = urllib2.Request(url1)
        res_data = urllib2.urlopen(response)
        res = res_data.read()
        hjson = json.loads(res.decode())

        running_0 = hjson['beans'][0]["running_0"]
        running_60 = hjson['beans'][0]["running_60"]
        running_300 = hjson['beans'][0]["running_300"]
        running_1440 = hjson['beans'][0]["running_1440"]
        apps_submitted = hjson['beans'][0]["AppsSubmitted"]
        apps_running = hjson['beans'][0]["AppsRunning"]
        apps_pending = hjson['beans'][0]["AppsPending"]
        apps_completed = hjson['beans'][0]["AppsCompleted"]
        apps_killed = hjson['beans'][0]["AppsKilled"]
        apps_failed = hjson['beans'][0]["AppsFailed"]
        hadoop_resource_manager['running_0'] = running_0
        hadoop_resource_manager['running_60'] = running_60
        hadoop_resource_manager['running_300'] = running_300
        hadoop_resource_manager['running_1440'] = running_1440
        hadoop_resource_manager['apps_submitted'] = apps_submitted
        hadoop_resource_manager['apps_running'] = apps_running
        hadoop_resource_manager['apps_completed'] = apps_completed
        hadoop_resource_manager['apps_killed'] = apps_killed
        hadoop_resource_manager['apps_failed'] = apps_failed

        allocated_mb = hjson['beans'][0]["AllocatedMB"] / 1024
        allocated_vcores = hjson['beans'][0]["AllocatedVCores"]
        allocated_containers = hjson['beans'][0]["AllocatedContainers"]
        aggregate_containers_allocated = hjson['beans'][0]["AggregateContainersAllocated"]
        avaliable_mb = hjson['beans'][0]["AvailableMB"] / 1024
        avaliable_vcores = hjson['beans'][0]["AvailableVCores"]
        hadoop_resource_manager['allocated_mb'] = allocated_mb
        hadoop_resource_manager['allocated_vcores'] = allocated_vcores
        hadoop_resource_manager['allocated_containers'] = allocated_containers
        hadoop_resource_manager['aggregate_containers_allocated'] = aggregate_containers_allocated
        hadoop_resource_manager['avaliable_mb'] = avaliable_mb
        hadoop_resource_manager['avaliable_vcores'] = avaliable_vcores

        pending_mb = hjson['beans'][0]["PendingMB"] / 1024
        pending_vcores = hjson['beans'][0]["PendingVCores"]
        pending_containers = hjson['beans'][0]["PendingContainers"]
        reserved_mb = hjson['beans'][0]["ReservedMB"] / 1024
        reserved_vcores = hjson['beans'][0]["ReservedVCores"]
        reserved_containers = hjson['beans'][0]["ReservedContainers"]
        active_users = hjson['beans'][0]["ActiveUsers"]
        active_applications = hjson['beans'][0]["ActiveApplications"]
        hadoop_resource_manager['pending_mb'] = pending_mb
        hadoop_resource_manager['pending_vcores'] = pending_vcores
        hadoop_resource_manager['pending_containers'] = pending_containers
        hadoop_resource_manager['reserved_mb'] = reserved_mb
        hadoop_resource_manager['reserved_vcores'] = reserved_vcores
        hadoop_resource_manager['reserved_containers'] = reserved_containers
        hadoop_resource_manager['active_users'] = active_users
        hadoop_resource_manager['active_applications'] = active_applications
        return hadoop_resource_manager




