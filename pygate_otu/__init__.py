__author__ = 'Jan Bogaerts'
__copyright__ = "Copyright 2016, AllThingsTalk"
__credits__ = []
__maintainer__ = "Jan Bogaerts"
__email__ = "jb@allthingstalk.com"
__status__ = "Prototype"  # "Development", or "Production"

import logging
logger = logging.getLogger('ota')

import ATT_OTA as OTA
from pygate_core import cloud, modules

_gateway = None
_VersionId = 'version'
_moduleName = None


def connectToGateway(moduleName):
    '''optional
        called when the system connects to the cloud.'''
    global _moduleName
    _moduleName = moduleName



def sendFirmwareVersion():
    """sends the firmware version of the gateway to the platform
        This way, maintainers know the currently installed application that's running on the gateway.
    """
    value = OTA.getVersionNumber()
    if not value:
        value = "unknown version"
    cloud.send(_moduleName, None, _VersionId, value)


def syncGatewayAssets():
    cloud.addGatewayAsset(_moduleName, _VersionId, 'Version', 'Use this actuator to initiate a version change in the gateway software. The new version will be downloaded from the appropriate server', True, 'string')


#callback: handles values sent from the cloudapp to the device
def onActuate(id, value):
    if id == _VersionId:
        logger.info(value)
        OTA.upgradeFirmware(value)
    else:
        logger.error("unknown actuator: " + id)


def run():
    ''' optional
        main function of the plugin module
        init the assets'''
    sendFirmwareVersion()