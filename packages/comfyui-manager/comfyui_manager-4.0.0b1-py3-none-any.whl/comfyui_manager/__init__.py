import os
import logging
from comfy.cli_args import args

ENABLE_LEGACY_COMFYUI_MANAGER_FRONT_DEFAULT = True # Enable legacy ComfyUI Manager frontend while new UI is in beta phase

def prestartup():
    from . import prestartup_script  # noqa: F401
    logging.info('[PRE] ComfyUI-Manager')


def start():
    logging.info('[START] ComfyUI-Manager')
    from .glob import manager_server  # noqa: F401
    from .glob import share_3rdparty  # noqa: F401
    from .glob import cm_global       # noqa: F401

    should_show_legacy_manager_front = os.environ.get('ENABLE_LEGACY_COMFYUI_MANAGER_FRONT', 'false') == 'true' or ENABLE_LEGACY_COMFYUI_MANAGER_FRONT_DEFAULT
    if not args.disable_manager and should_show_legacy_manager_front:
        try:
            import nodes
            nodes.EXTENSION_WEB_DIRS['comfyui-manager-legacy'] = os.path.join(os.path.dirname(__file__), 'js')
        except Exception as e:
            print("Error enabling legacy ComfyUI Manager frontend:", e)


def should_be_disabled(fullpath:str) -> bool:
    """
    1. Disables the legacy ComfyUI-Manager.
    2. The blocklist can be expanded later based on policies.
    """

    if not args.disable_manager:
        # In cases where installation is done via a zip archive, the directory name may not be comfyui-manager, and it may not contain a git repository.
        # It is assumed that any installed legacy ComfyUI-Manager will have at least 'comfyui-manager' in its directory name.
        dir_name = os.path.basename(fullpath).lower()
        if 'comfyui-manager' in dir_name:
            return True

    return False
