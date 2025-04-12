"""
Varnish Shared Memory Log (VSL) integration.
"""

import os
import sys
import time
from typing import Optional
from ctypes import CDLL, c_int, c_char_p, c_void_p, POINTER, Structure, byref
from .parser import DocumentBuffer, BufferConfig

# Load Varnish shared library
try:
    libvarnishapi = CDLL("libvarnishapi.so")
except OSError:
    raise ImportError("Could not load libvarnishapi.so. Make sure Varnish is installed.")

# VSL API structures and functions
class VSL_data(Structure):
    _fields_ = [
        ("magic", c_int),
        ("fd", c_int),
        ("len", c_int),
        ("ptr", c_void_p),
    ]

class VSL_handle(Structure):
    _fields_ = [
        ("magic", c_int),
        ("fd", c_int),
        ("cursor", c_int),
        ("data", POINTER(VSL_data)),
    ]

# Initialize VSL API functions
libvarnishapi.VSL_New.restype = POINTER(VSL_handle)
libvarnishapi.VSL_Open.argtypes = [POINTER(VSL_handle), c_int]
libvarnishapi.VSL_Next.argtypes = [POINTER(VSL_handle)]
libvarnishapi.VSL_Next.restype = c_int
libvarnishapi.VSL_Close.argtypes = [POINTER(VSL_handle)]

class VarnishLogReader:
    """Reads logs directly from Varnish Shared Memory."""
    
    def __init__(self, buffer_config: BufferConfig):
        """Initialize Varnish log reader.
        
        Args:
            buffer_config: Configuration for document buffering
        """
        self.buffer_config = buffer_config
        self.document_buffer = DocumentBuffer(buffer_config)
        self.vsl_handle = libvarnishapi.VSL_New()
        if not self.vsl_handle:
            raise RuntimeError("Failed to create VSL handle")
        
        # Open VSL in read-only mode
        if libvarnishapi.VSL_Open(self.vsl_handle, 0) != 0:
            raise RuntimeError("Failed to open VSL")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def close(self):
        """Close VSL connection."""
        if self.vsl_handle:
            libvarnishapi.VSL_Close(self.vsl_handle)
            self.vsl_handle = None
    
    def read_logs(self):
        """Read logs from Varnish Shared Memory."""
        doc = {}
        start_time = None
        resp_time = None
        inside_request = False
        
        while True:
            if libvarnishapi.VSL_Next(self.vsl_handle) <= 0:
                time.sleep(0.1)  # Wait for new logs
                continue
            
            # Process log entry
            vsl_data = self.vsl_handle.contents.data.contents
            line = c_char_p(vsl_data.ptr).value.decode('utf-8')
            
            if line.startswith("*") and "Request" in line:
                if inside_request:
                    if start_time and resp_time:
                        doc["duration_ms"] = round((resp_time - start_time) * 1000, 3)
                    env_val = doc.get("env", "false")
                    env_type = "prod" if env_val.lower() == "true" else "stage"
                    doc["env"] = env_type
                    doc["timestamp"] = time.strftime('%Y-%m-%dT%H:%M:%S%z')
                    
                    for field in ["backend_url", "backend_host", "backend_method", "backend_status"]:
                        doc.setdefault(field, None)
                    
                    self.document_buffer.add(doc)
                    if self.document_buffer.should_flush():
                        self.document_buffer.flush()
                    
                    doc = {}
                    start_time = None
                    resp_time = None
                inside_request = True
                continue
            
            # Process the rest of the log entry similar to the parser
            # ... (rest of the parsing logic)

def main():
    """Main entry point for VSL-based logging."""
    try:
        buffer_config = BufferConfig(
            max_size=int(os.getenv('ES_BUFFER_SIZE', '100')),
            flush_interval=int(os.getenv('ES_FLUSH_INTERVAL', '5'))
        )
        
        with VarnishLogReader(buffer_config) as reader:
            reader.read_logs()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1) 