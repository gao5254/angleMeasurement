from ctypes import (POINTER, byref, c_char_p, c_float, c_int32, c_uint32,
                    c_ulonglong, windll)

# macro
MT3_TEXT_SIZE = 64

# load dll
MT3dll = windll.LoadLibrary("./MT3DLL64.dll")

# =====================================================================
#  Function Prototypes
# =====================================================================

# ----------------
# Error Code Text
# ----------------

GetErrorText = MT3dll.MT3_GetErrorText
GetErrorText.restype = c_char_p
GetErrorText.argtypes = (c_int32,)

# ----------------
#  Version String
# ----------------

GetDLLVersion = MT3dll.MT3_GetDLLVersion
GetDLLVersion.restype = c_int32
GetDLLVersion.argtypes = (POINTER(c_int32), POINTER(c_int32), POINTER(c_int32))

GetDLLVersionString = MT3dll.MT3_GetDLLVersionString
GetDLLVersionString.restype = c_char_p

# -------------------------------
#  Interface Open/Close Functions
# -------------------------------

OpenInterface = MT3dll.MT3_OpenInterface
OpenInterface.restype = c_int32
OpenInterface.argtypes = (c_int32, c_uint32, POINTER(c_ulonglong))

OpenInterfaceEx = MT3dll.MT3_OpenInterfaceEx
OpenInterfaceEx.restype = c_int32
OpenInterfaceEx.argtypes = (c_int32, c_uint32, POINTER(c_ulonglong))

CloseInterface = MT3dll.MT3_CloseInterface
CloseInterface.restype = c_int32
CloseInterface.argtypes = (POINTER(c_ulonglong), )

# ---------------------------------------
#  MT3 Device Search/Definition Functions
# ---------------------------------------

StartDeviceSearch = MT3dll.MT3_StartDeviceSearch
StartDeviceSearch.restype = c_int32
StartDeviceSearch.argtypes = (c_ulonglong, )

GetDeviceSearchProgress = MT3dll.MT3_GetDeviceSearchProgress
GetDeviceSearchProgress.restype = c_int32
GetDeviceSearchProgress.argtypes = (c_ulonglong, POINTER(c_uint32), POINTER(c_float))

ClearDeviceList = MT3dll.MT3_ClearDeviceList
ClearDeviceList.restype = c_int32
ClearDeviceList.argtypes = (c_ulonglong,)

AddDevice = MT3dll.MT3_AddDevice
AddDevice.restype = c_int32
AddDevice.argtypes = (c_ulonglong, c_int32, POINTER(c_int32))

RemoveDevice = MT3dll.MT3_RemoveDevice
RemoveDevice.restype = c_int32
RemoveDevice.argtypes = (c_ulonglong, c_int32)

InitializeDeviceInformation = MT3dll.MT3_InitializeDeviceInformation
InitializeDeviceInformation.restype = c_int32
InitializeDeviceInformation.argtypes = (c_ulonglong, )

GetTotalDeviceCount = MT3dll.MT3_GetTotalDeviceCount
GetTotalDeviceCount.restype = c_int32
GetTotalDeviceCount.argtypes = (c_ulonglong, POINTER(c_int32))

FindDeviceAddress = MT3dll.MT3_FindDeviceAddress
FindDeviceAddress.restype = c_int32
FindDeviceAddress.argtypes = (c_ulonglong, c_int32, POINTER(c_int32))

FindDeviceIndex = MT3dll.MT3_FindDeviceIndex
FindDeviceIndex.restype = c_int32
FindDeviceIndex.argtypes = (c_ulonglong, c_int32, POINTER(c_int32))

# -------------------------------------
#  MT3 Communications Support Functions
# -------------------------------------

# MT3_DecodeSerialReplyPacket
# MT3_GetLastBinaryCommand
# MT3_GetLastBinaryReply

# ---------------------------------------------------
#  MT3 Control Functions (Synchronous Version)

#  Function returns after command reply is received.
# ---------------------------------------------------

SoftReset = MT3dll.MT3_SoftReset
SoftReset.restype = c_int32
SoftReset.argtypes = (c_ulonglong, c_int32)

# MT3_FactoryReset
# MT3_SetBaudRate


SetBaudIndex = MT3dll.MT3_SetBaudIndex
SetBaudIndex.restype = c_int32
SetBaudIndex.argtypes = (c_ulonglong, c_int32, c_int32)

SetNodeAddress = MT3dll.MT3_SetNodeAddress
SetNodeAddress.restype = c_int32
SetNodeAddress.argtypes = (c_ulonglong, c_int32, c_int32)

SetDisplayMode = MT3dll.MT3_SetDisplayMode
SetDisplayMode.restype = c_int32
SetDisplayMode.argtypes = (c_ulonglong, c_int32, c_int32)

SetUpperLimit = MT3dll.MT3_SetUpperLimit
SetUpperLimit.restype = c_int32
SetUpperLimit.argtypes = (c_ulonglong, c_int32, c_float)

SetLowerLimit = MT3dll.MT3_SetLowerLimit
SetLowerLimit.restype = c_int32
SetLowerLimit.argtypes = (c_ulonglong, c_int32, c_float)

SetUnits = MT3dll.MT3_SetUnits
SetUnits.restype = c_int32
SetUnits.argtypes = (c_ulonglong, c_int32, c_int32)

SetFilterFrequency = MT3dll.MT3_SetFilterFrequency
SetFilterFrequency.restype = c_int32
SetFilterFrequency.argtypes = (c_ulonglong, c_int32, c_float)

SetFilterIndex = MT3dll.MT3_SetFilterIndex
SetFilterIndex.restype = c_int32
SetFilterIndex.argtypes = (c_ulonglong, c_int32, c_int32)

SetUserCalFactor = MT3dll.MT3_SetUserCalFactor
SetUserCalFactor.restype = c_int32
SetUserCalFactor.argtypes = (c_ulonglong, c_int32, c_float)

SetUserCalSign = MT3dll.MT3_SetUserCalSign
SetUserCalSign.restype = c_int32
SetUserCalSign.argtypes = (c_ulonglong, c_int32, c_int32)

SetLCDContrast = MT3dll.MT3_SetLCDContrast
SetLCDContrast.restype = c_int32
SetLCDContrast.argtypes = (c_ulonglong, c_int32, c_int32)

SetLevelCutTime = MT3dll.MT3_SetLevelCutTime
SetLevelCutTime.restype = c_int32
SetLevelCutTime.argtypes = (c_ulonglong, c_int32, c_float)

SetAutoZero = MT3dll.MT3_SetAutoZero
SetAutoZero.restype = c_int32
SetAutoZero.argtypes = (c_ulonglong, c_int32, c_int32)

SetLaserPower = MT3dll.MT3_SetLaserPower
SetLaserPower.restype = c_int32
SetLaserPower.argtypes = (c_ulonglong, c_int32, c_int32)

SetManualLaserPowerControl = MT3dll.MT3_SetManualLaserPowerControl
SetManualLaserPowerControl.restype = c_int32
SetManualLaserPowerControl.argtypes = (c_ulonglong, c_int32, c_int32)

SetLaserPWM = MT3dll.MT3_SetLaserPWM
SetLaserPWM.restype = c_int32
SetLaserPWM.argtypes = (c_ulonglong, c_int32, c_float)

SetVideoMode = MT3dll.MT3_SetVideoMode
SetVideoMode.restype = c_int32
SetVideoMode.argtypes = (c_ulonglong, c_int32, c_int32)

# ---------------------------------------------------
#  MT3 Information Functions (Synchronous Version)

#  Function returns after command reply is received.
#  Requested data is returned by function
# ---------------------------------------------------

# MT3_GetBaudRate

GetBaudIndex = MT3dll.MT3_GetBaudIndex
GetBaudIndex.restype = c_int32
GetBaudIndex.argtypes = (c_ulonglong, c_int32, POINTER(c_int32))

GetNodeAddress = MT3dll.MT3_GetNodeAddress
GetNodeAddress.restype = c_int32
GetNodeAddress.argtypes = (c_ulonglong, c_int32, POINTER(c_int32))

GetDisplayMode = MT3dll.MT3_GetDisplayMode
GetDisplayMode.restype = c_int32
GetDisplayMode.argtypes = (c_ulonglong, c_int32, POINTER(c_int32))

GetUpperLimit = MT3dll.MT3_GetUpperLimit
GetUpperLimit.restype = c_int32
GetUpperLimit.argtypes = (c_ulonglong, c_int32, POINTER(c_float))

GetLowerLimit = MT3dll.MT3_GetLowerLimit
GetLowerLimit.restype = c_int32
GetLowerLimit.argtypes = (c_ulonglong, c_int32, POINTER(c_float))

GetUnits = MT3dll.MT3_GetUnits
GetUnits.restype = c_int32
GetUnits.argtypes = (c_ulonglong, c_int32, POINTER(c_int32), POINTER(c_float), POINTER(c_int32), c_char_p)

GetFilterFrequency = MT3dll.MT3_GetFilterFrequency
GetFilterFrequency.restype = c_int32
GetFilterFrequency.argtypes = (c_ulonglong, c_int32, POINTER(c_float))

GetFilterIndex = MT3dll.MT3_GetFilterIndex
GetFilterIndex.restype = c_int32
GetFilterIndex.argtypes = (c_ulonglong, c_int32, POINTER(c_int32))

GetUserCalFactor = MT3dll.MT3_GetUserCalFactor
GetUserCalFactor.restype = c_int32
GetUserCalFactor.argtypes = (c_ulonglong, c_int32, POINTER(c_float))

GetUserCalSign = MT3dll.MT3_GetUserCalSign
GetUserCalSign.restype = c_int32
GetUserCalSign.argtypes = (c_ulonglong, c_int32, POINTER(c_int32))

GetLCDContrast = MT3dll.MT3_GetLCDContrast
GetLCDContrast.restype = c_int32
GetLCDContrast.argtypes = (c_ulonglong, c_int32, POINTER(c_int32))

GetIntensity = MT3dll.MT3_GetIntensity
GetIntensity.restype = c_int32
GetIntensity.argtypes = (c_ulonglong, c_int32, POINTER(c_int32), POINTER(c_int32), POINTER(c_float))

GetLevelCutTime = MT3dll.MT3_GetLevelCutTime
GetLevelCutTime.restype = c_int32
GetLevelCutTime.argtypes = (c_ulonglong, c_int32, POINTER(c_float))

# MT3_GetBothPeaks
# MT3_GetThicknessScaleFactor

GetHeadModel = MT3dll.MT3_GetHeadModel
GetHeadModel.restype = c_int32
GetHeadModel.argtypes = (c_ulonglong, c_int32, c_char_p)

GetHeadSerialNumber = MT3dll.MT3_GetHeadSerialNumber
GetHeadSerialNumber.restype = c_int32
GetHeadSerialNumber.argtypes = (c_ulonglong, c_int32, c_char_p)

GetVersionNumbers = MT3dll.MT3_GetVersionNumbers
GetVersionNumbers.restype = c_int32
GetVersionNumbers.argtypes = (c_ulonglong, c_int32, c_char_p)

# ----------------------------------------------
#  MT3 Telemetry Functions (Synchronous Version)
# ----------------------------------------------

SetTelemetryProtocol = MT3dll.MT3_SetTelemetryProtocol
SetTelemetryProtocol.restype = c_int32
SetTelemetryProtocol.argtypes = (c_ulonglong, c_int32)

SetTelemetryDestinationAddress = MT3dll.MT3_SetTelemetryDestinationAddress
SetTelemetryDestinationAddress.restype = c_int32
SetTelemetryDestinationAddress.argtypes = (c_ulonglong, c_int32, c_int32)

SetTelemetryTimer = MT3dll.MT3_SetTelemetryTimer
SetTelemetryTimer.restype = c_int32
SetTelemetryTimer.argtypes = (c_ulonglong, c_int32, c_float)

GetTelemetryDestinationAddress = MT3dll.MT3_GetTelemetryDestinationAddress
GetTelemetryDestinationAddress.restype = c_int32
GetTelemetryDestinationAddress.argtypes = (c_ulonglong, c_int32, POINTER(c_int32))

GetTelemetryTimer = MT3dll.MT3_GetTelemetryTimer
GetTelemetryTimer.restype = c_int32
GetTelemetryTimer.argtypes = (c_ulonglong, c_int32, POINTER(c_float))

GetTelemetry = MT3dll.MT3_GetTelemetry
GetTelemetry.restype = c_int32
GetTelemetry.argtypes = (c_ulonglong, c_int32, POINTER(c_float), POINTER(c_uint32))

# MT3_SetTelemetryReceiver
# MT3_GetTelemetryFromHandle
# MT3_StartTelemetry
# MT3_StopTelemetry
# MT3_TriggerTelemetryReading


# define by gaoxu
def open_device(portNumber, deviceAddress=0, baudRate=57600):
    '''打开一个串口上的MT3激光位移计设备。

    返回其错误代码，串口句柄及设备编号。
    '''
    handle = c_ulonglong(0)
    deviceIndex = c_int32(0)
    err = OpenInterface(portNumber, baudRate, byref(handle))
    if err != 0:
        return (err, handle, deviceIndex)
    err = AddDevice(handle, 0, byref(deviceIndex))
    if err != 0:
        return (err, handle, deviceIndex)

    err = InitializeDeviceInformation(handle)
    return (err, handle.value, deviceIndex.value)


def get_number(handle, deviceIndex):
    '''读取激光位移计设备读数

    返回错误代码，其读数，以及一个状态量
    '''
    reading = c_float(0.0)
    status = c_uint32(0)
    err = GetTelemetry(handle, deviceIndex, byref(reading), byref(status))
    return (err, reading.value, status.value)


def close_device(handle):
    '''关闭串口及其关联设备

    返回错误代码
    '''
    handle = c_ulonglong(handle)
    err = CloseInterface(byref(handle))
    return err


def turnonoff_device(handle, deviceIndex, laserOnOff):
    '''打开或关闭激光器光点

    返回错误代码
    '''
    err = SetLaserPower(handle, deviceIndex, laserOnOff)
    return err
