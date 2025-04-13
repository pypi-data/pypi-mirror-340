import os
import ctypes
import platform

GPUPixelWrapper = None


if platform.system() == 'Windows':
    # load libgpupixel_pywrapper.dll
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # print("current_dir", current_dir)
    os.environ['Path'] += os.path.join(current_dir, 'lib', 'windows')
    dll_path = os.path.join(current_dir, 'lib', 'windows','libgpupixel_pywrapper.dll')
    # print("dll_path", dll_path)
    GPUPixelWrapper = ctypes.CDLL(dll_path,winmode=0)
else:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.environ['PATH'] += os.pathsep + os.path.join(current_dir, 'lib', 'linux')
    dll_path = os.path.join(current_dir, 'lib', 'linux','libgpupixel_pywrapper.so')
    GPUPixelWrapper = ctypes.CDLL(dll_path)

# define types of arguments and returns
GPUPixelWrapper.GPUPixelWrapper_create.restype = ctypes.c_void_p
GPUPixelWrapper.GPUPixelWrapper_initialize.argtypes = [ctypes.c_void_p]
GPUPixelWrapper.GPUPixelWrapper_setCallbacks.argtypes = [ctypes.c_void_p]
GPUPixelWrapper.GPUPixelWrapper_setParameters.argtypes = [ctypes.c_void_p, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float]
GPUPixelWrapper.GPUPixelWrapper_run.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint8), ctypes.c_int, ctypes.c_int, ctypes.c_int]
GPUPixelWrapper.GPUPixelWrapper_run.restype = ctypes.POINTER(ctypes.c_uint8)
GPUPixelWrapper.GPUPixelWrapper_destroy.argtypes = [ctypes.POINTER(ctypes.c_uint8)]
GPUPixelWrapper.GPUPixelWrapper_release.argtypes = [ctypes.c_void_p]

