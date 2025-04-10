import logging
from pydash import py_

logger = logging.getLogger(__name__)

def _check_org_group(org_groups):
    for org_group in org_groups:
        if isinstance(org_group, dict):
            if org_group.get("id") == "8256":
                return True
            if py_.get(org_group, "title.el", "") == 'myKEPlive':
                return True
        elif isinstance(org_group, str):
            if org_group == "8256":
                return True
        else:
            logger.warning("Unexpected type in org group list: %s", type(org_group).__name__)
    return False

def _is_my_keplive(payload):
    provision_org_group = py_.get(
        payload,
        'metadata.process.provision_org_group',
        [],
    )
    provision_org_group_remote = py_.get(
        payload,
        'metadata.process.provision_org_group_remote',
        [],
    )
    is_my_keplive = _check_org_group(provision_org_group)
    if is_my_keplive is False:
        is_my_keplive = _check_org_group(provision_org_group_remote)
    return is_my_keplive

