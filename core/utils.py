# -*- coding: utf-8 -*-

import os
import json
import string
import random
from contextlib import contextmanager

from maya import cmds as mc
from pymel import core as pm
import maya.OpenMaya as OpenMaya

def save_maya_file(export_path=None):
    from hz.naming_api import NamingAPI
    file_path = pm.system.saveFile(force=True)
    naming = NamingAPI.parser(file_path)
    export_source_path = export_path if export_path else naming.get_publish_full_path()
    root_path = os.path.dirname(export_source_path)
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    file_path.copyfile(export_source_path)


def maya_version():
    return OpenMaya.MGlobal.mayaVersion()


def get_time_range_in_slider():
    start_frame = pm.playbackOptions(minTime=True, query=True)
    end_frame = pm.playbackOptions(maxTime=True, query=True)
    return start_frame, end_frame


def api_version():
    return OpenMaya.MGlobal.apiVersion()


def get_root_dag():
    """
    Get asset name from root (oytline)
    :return:
    """
    root_nodes = filter(lambda i: pm.nodeType(i.listRelatives()) == 'transform', pm.ls(assemblies=True, recursive=True))
    assert len(root_nodes) == 1
    return root_nodes[0]


def random_text_generator(length):
    """
    Generate a random string.
    length = int
    """
    return ''.join(random.choice(string.ascii_letters) for i in xrange(length))


def get_all_cameras():
    available_cam = []
    for camera_shape in pm.ls(type='camera'):
        camera_transform = camera_shape.getParent().longName()
        for start_key in ["|cam|", "|camera|"]:
            if camera_shape.getParent() not in ['front', 'persp', 'side', 'top']:
                item = camera_shape.getParent().name()
                if camera_transform.lower().startswith(start_key):
                    if item not in available_cam:
                        available_cam.insert(0, item)
                else:
                    if item not in available_cam:
                        available_cam.append(item)
    return available_cam


def ensure_pynode(node):
    """
    The function convert node name to its entity if necessary.
    """
    source = node
    if not isinstance(source, pm.PyNode):
        source = pm.PyNode(source)
    return source


def ensure_list(source):
    source_list = source
    if not isinstance(source_list, list) and not isinstance(source_list, tuple):
        source_list = [source_list]
    return source_list


def write_out_json(file_path, dict=None):
    with open(file_path, "w") as f:
        json.dump(dict, f)


def get_reference_dict():
    asset_dict = {}
    for ref in pm.ls(rf=True):
        asset_name = ref.referenceFile().getReferenceEdits()[0].split(':')[1].split('"')[0]
        if asset_name not in asset_dict.keys():
            asset_dict[asset_name] = {}
        asset_dict[asset_name][ref.shortName()] = str(ref.referenceFile().path)
    return asset_dict

