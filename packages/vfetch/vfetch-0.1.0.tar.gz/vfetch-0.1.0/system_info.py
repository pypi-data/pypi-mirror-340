"""
system_info.py - Functions to gather system information for vfetch
"""

import os
import platform
import socket
import datetime
import subprocess
import re
from collections import OrderedDict
import psutil

def get_processor_info():
    """Get detailed processor information"""
    info = OrderedDict()
    
    # Get CPU info
    if platform.system() == "Linux":
        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "model name" in line:
                        info["Model"] = re.sub(r".*model name.*:", "", line, 1).strip()
                        break
        except:
            pass
        
        # Get CPU frequency
        try:
            freq = psutil.cpu_freq()
            if freq:
                if freq.current:
                    info["Current Frequency"] = f"{freq.current/1000:.2f} GHz"
                if freq.max:
                    info["Max Frequency"] = f"{freq.max/1000:.2f} GHz"
        except:
            pass
        
    elif platform.system() == "Darwin":  # macOS
        try:
            output = subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"]).decode().strip()
            info["Model"] = output
        except:
            info["Model"] = platform.processor()
            
    elif platform.system() == "Windows":
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
            info["Model"] = winreg.QueryValueEx(key, "ProcessorNameString")[0]
            winreg.CloseKey(key)
        except:
            info["Model"] = platform.processor()
    
    # Common CPU info for all platforms
    info["Cores"] = f"{psutil.cpu_count(logical=False)} (Physical), {psutil.cpu_count(logical=True)} (Logical)"
    info["Architecture"] = platform.machine()
    
    return info

def get_memory_info():
    """Get RAM information with visual representation"""
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    info = OrderedDict()
    
    # Basic memory information
    info["Total"] = f"{memory.total / (1024 ** 3):.2f} GB"
    info["Available"] = f"{memory.available / (1024 ** 3):.2f} GB"
    
    # Create a visual bar representation of memory usage
    bar_length = 20
    used_bars = int(memory.percent / 100 * bar_length)
    free_bars = bar_length - used_bars
    bar = f"[{'■' * used_bars}{'□' * free_bars}] {memory.percent}%"
    
    # Memory usage with visualization
    info["Used"] = f"{memory.used / (1024 ** 3):.2f} GB {bar}"
    
    # Detailed memory breakdown
    if hasattr(memory, 'cached') and hasattr(memory, 'buffers'):
        cached = memory.cached / (1024 ** 3)
        buffers = memory.buffers / (1024 ** 3)
        info["Cached/Buffers"] = f"Cached: {cached:.2f} GB, Buffers: {buffers:.2f} GB"
    
    # Swap information with visualization if available
    if swap.total > 0:
        swap_bar_length = 10
        swap_used_bars = int(swap.percent / 100 * swap_bar_length) if swap.percent > 0 else 0
        swap_free_bars = swap_bar_length - swap_used_bars
        swap_bar = f"[{'■' * swap_used_bars}{'□' * swap_free_bars}] {swap.percent}%"
        
        info["Swap"] = f"{swap.total / (1024 ** 3):.2f} GB (Used: {swap.used / (1024 ** 3):.2f} GB) {swap_bar}"
    else:
        info["Swap"] = "Not configured"
    
    return info

def get_disk_info():
    """Get disk information with visual representation"""
    info = OrderedDict()
    partitions = psutil.disk_partitions(all=False)
    
    for partition in partitions:
        if platform.system() == "Windows" and "cdrom" in partition.opts:
            continue
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            name = partition.mountpoint if partition.mountpoint != "/" else "Root"
            
            # Create a visual representation of disk usage
            bar_length = 15
            used_bars = int(usage.percent / 100 * bar_length)
            free_bars = bar_length - used_bars
            bar = f"[{'■' * used_bars}{'□' * free_bars}]"
            
            # Add filesystem type when available
            fs_type = getattr(partition, 'fstype', '')
            fs_info = f" ({fs_type})" if fs_type else ""
            
            # Format size with appropriate units
            total_size = usage.total / (1024 ** 3)  # GB
            if total_size < 1:
                total_size = usage.total / (1024 ** 2)  # MB
                size_str = f"{total_size:.1f} MB"
            else:
                size_str = f"{total_size:.1f} GB"
            
            # Format used space
            used_space = usage.used / (1024 ** 3)  # GB
            if used_space < 1:
                used_space = usage.used / (1024 ** 2)  # MB
                used_str = f"{used_space:.1f} MB"
            else:
                used_str = f"{used_space:.1f} GB"
            
            # Combine all information
            info[name] = f"{size_str}{fs_info} {bar} {usage.percent}% (Used: {used_str})"
        except Exception as e:
            info[name] = f"Error: {str(e)}"
    
    # Add total disk space summary if we have partitions
    if info:
        try:
            total_space = 0
            used_space = 0
            
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    total_space += usage.total
                    used_space += usage.used
                except:
                    pass
            
            if total_space > 0:
                percent = (used_space / total_space) * 100
                total_gb = total_space / (1024 ** 3)
                used_gb = used_space / (1024 ** 3)
                
                bar_length = 15
                used_bars = int(percent / 100 * bar_length)
                free_bars = bar_length - used_bars
                bar = f"[{'■' * used_bars}{'□' * free_bars}]"
                
                info["Total Storage"] = f"{total_gb:.1f} GB {bar} {percent:.1f}% (Used: {used_gb:.1f} GB)"
        except:
            pass
    
    return info

def get_gpu_info():
    """Get GPU information (if available)"""
    info = OrderedDict()
    
    if platform.system() == "Linux":
        try:
            # Try to get NVIDIA GPU info
            output = subprocess.check_output(["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"]).decode().strip()
            if output:
                for i, gpu in enumerate(output.split('\n')):
                    values = gpu.split(', ')
                    if len(values) >= 3:
                        gpu_name, gpu_memory, driver_version = values
                        info[f"GPU {i+1}"] = f"{gpu_name.strip()} ({gpu_memory.strip()})"
                        if i == 0:  # Add driver info for only the first GPU
                            info["Driver"] = driver_version.strip()
        except:
            # Try lspci as fallback
            try:
                output = subprocess.check_output(["lspci", "-v"]).decode().strip()
                vga_devices = re.findall(r"VGA compatible controller: (.*)", output)
                for i, device in enumerate(vga_devices):
                    info[f"GPU {i+1}"] = device.strip()
            except:
                pass
    
    elif platform.system() == "Darwin":  # macOS
        try:
            output = subprocess.check_output(["system_profiler", "SPDisplaysDataType"]).decode().strip()
            gpu_name = re.search(r"Chipset Model: (.*)", output)
            vram = re.search(r"VRAM \(Total\): (.*)", output)
            
            if gpu_name:
                info["GPU"] = gpu_name.group(1).strip()
            if vram:
                info["VRAM"] = vram.group(1).strip()
        except:
            pass
    
    elif platform.system() == "Windows":
        try:
            output = subprocess.check_output(["wmic", "path", "win32_VideoController", "get", "Name,AdapterRAM", "/format:csv"]).decode().strip()
            lines = output.split('\n')
            if len(lines) > 1:
                headers = lines[0].split(',')
                for i in range(1, len(lines)):
                    if lines[i].strip():
                        values = lines[i].split(',')
                        if len(values) >= 3:
                            gpu_name = values[2]
                            info[f"GPU {i}"] = gpu_name.strip()
        except:
            pass
    
    # If no GPU info was detected
    if not info:
        info["GPU"] = "Not detected"
    
    return info

def get_os_info():
    """Get operating system information"""
    info = OrderedDict()
    
    # Basic OS info
    info["System"] = platform.system()
    
    if platform.system() == "Linux":
        # Get Linux distribution info
        try:
            with open("/etc/os-release", "r") as f:
                distro = {}
                for line in f:
                    if "=" in line:
                        key, value = line.rstrip().split("=", 1)
                        distro[key] = value.strip('"')
            
            if "PRETTY_NAME" in distro:
                info["Distribution"] = distro["PRETTY_NAME"]
            elif "NAME" in distro and "VERSION" in distro:
                info["Distribution"] = f"{distro['NAME']} {distro['VERSION']}"
        except:
            info["Distribution"] = "Unknown Linux Distribution"
    
    elif platform.system() == "Darwin":
        info["Distribution"] = f"macOS {platform.mac_ver()[0]}"
    
    elif platform.system() == "Windows":
        info["Distribution"] = f"Windows {platform.version()}"
    
    # Kernel version
    if platform.system() != "Windows":
        info["Kernel"] = platform.release()
    
    # Add system architecture and endianness
    info["Architecture"] = f"{platform.machine()} ({platform.architecture()[0]})"
    
    # Get uptime
    try:
        import time
        uptime = datetime.timedelta(seconds=int(time.time() - psutil.boot_time()))
        info["Uptime"] = str(uptime).split('.')[0]  # Remove microseconds
    except Exception as e:
        try:
            # Alternative method for Linux
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
                uptime = datetime.timedelta(seconds=int(uptime_seconds))
                info["Uptime"] = str(uptime).split('.')[0]
        except:
            info["Uptime"] = "Unknown"
    
    return info

def get_host_info():
    """Get hostname and user information"""
    info = OrderedDict()
    
    info["Hostname"] = socket.gethostname()
    
    # Get user info safely
    try:
        info["User"] = os.getlogin()
    except:
        try:
            import pwd
            info["User"] = pwd.getpwuid(os.getuid()).pw_name
        except:
            info["User"] = os.environ.get("USER", "unknown")
    
    try:
        info["Shell"] = os.path.basename(os.environ.get("SHELL", "Not detected"))
    except:
        info["Shell"] = "Not detected"
    
    # Get terminal info when possible
    terminal = os.environ.get("TERM_PROGRAM") or os.environ.get("TERM")
    if terminal:
        info["Terminal"] = terminal
    
    return info

def get_package_info():
    """Get package manager and installed packages information"""
    info = OrderedDict()
    
    if platform.system() == "Linux":
        # Check for apt (Debian, Ubuntu, etc.)
        try:
            output = subprocess.check_output(["apt", "list", "--installed"], stderr=subprocess.DEVNULL).decode().strip()
            count = len(output.split('\n')) - 1  # Subtract header line
            if count > 0:
                info["apt"] = str(count)
        except:
            pass
        
        # Check for dnf/yum (Fedora, RHEL, etc.)
        try:
            output = subprocess.check_output(["rpm", "-qa"], stderr=subprocess.DEVNULL).decode().strip()
            count = len(output.split('\n'))
            if count > 0:
                info["rpm"] = str(count)
        except:
            pass
        
        # Check for pacman (Arch, Manjaro, etc.)
        try:
            output = subprocess.check_output(["pacman", "-Q"], stderr=subprocess.DEVNULL).decode().strip()
            count = len(output.split('\n'))
            if count > 0:
                info["pacman"] = str(count)
        except:
            pass
    
    elif platform.system() == "Darwin":
        # Check for Homebrew
        try:
            output = subprocess.check_output(["brew", "list", "--formula"], stderr=subprocess.DEVNULL).decode().strip()
            formula_count = len(output.split('\n')) if output else 0
            
            output = subprocess.check_output(["brew", "list", "--cask"], stderr=subprocess.DEVNULL).decode().strip()
            cask_count = len(output.split('\n')) if output else 0
            
            if formula_count > 0 or cask_count > 0:
                info["Homebrew"] = f"{formula_count} formula, {cask_count} casks"
        except:
            pass
    
    elif platform.system() == "Windows":
        # Check for Windows packages
        try:
            output = subprocess.check_output(["powershell", "-Command", "Get-AppxPackage | Measure-Object | Select-Object -ExpandProperty Count"], stderr=subprocess.DEVNULL).decode().strip()
            if output:
                info["Windows Store"] = output
        except:
            pass
    
    # Check for pip packages (cross-platform)
    try:
        output = subprocess.check_output(["pip", "list"], stderr=subprocess.DEVNULL).decode().strip()
        count = len(output.split('\n')) - 2  # Subtract header lines
        if count > 0:
            info["pip"] = str(count)
    except:
        pass
    
    # Check for npm packages (cross-platform)
    try:
        output = subprocess.check_output(["npm", "list", "-g", "--depth=0"], stderr=subprocess.DEVNULL).decode().strip()
        count = len(output.split('\n')) - 1  # Subtract header line
        if count > 0:
            info["npm (global)"] = str(count)
    except:
        pass
    
    if not info:
        info["Packages"] = "None detected"
    
    return info

def get_network_info():
    """Get network information"""
    info = OrderedDict()
    
    # Get network interfaces info (excluding loopback)
    interfaces = psutil.net_if_addrs()
    
    for iface, addrs in interfaces.items():
        if iface == "lo" or iface == "lo0" or "Loopback" in iface:
            continue
        
        for addr in addrs:
            if addr.family == socket.AF_INET:  # IPv4
                info[iface] = f"IPv4: {addr.address}"
            elif addr.family == socket.AF_INET6 and not addr.address.startswith("fe80"):  # IPv6 (non-link-local)
                if iface in info:
                    info[iface] += f", IPv6: {addr.address}"
                else:
                    info[iface] = f"IPv6: {addr.address}"
    
    # Get hostname
    info["Hostname"] = socket.gethostname()
    
    return info

def get_performance_metrics():
    """Get performance metrics data"""
    info = OrderedDict()
    
    # CPU load with per-core information
    cpu_percent = psutil.cpu_percent(interval=0.5, percpu=True)
    avg_cpu = sum(cpu_percent) / len(cpu_percent)
    
    # Format overall CPU load
    info["CPU Load"] = f"{avg_cpu:.1f}% (avg), {max(cpu_percent):.1f}% (max)"
    
    # Add per-core CPU load if multiple cores
    if len(cpu_percent) > 1:
        core_info = []
        for i, percent in enumerate(cpu_percent):
            core_info.append(f"Core {i}: {percent:.1f}%")
        
        # Group cores in sets of 4 for better display
        if len(core_info) <= 4:
            info["CPU Cores"] = ", ".join(core_info)
        else:
            for i in range(0, len(core_info), 4):
                group = core_info[i:i+4]
                info[f"CPU Cores {i//4+1}"] = ", ".join(group)
    
    # Memory usage with detailed breakdown
    memory = psutil.virtual_memory()
    info["Memory Usage"] = f"{memory.percent}% ({memory.used / (1024 ** 3):.2f} GB of {memory.total / (1024 ** 3):.2f} GB)"
    
    # Memory breakdown
    info["Memory Breakdown"] = f"Used: {memory.used / (1024 ** 3):.2f} GB, Available: {memory.available / (1024 ** 3):.2f} GB"
    
    # Swap usage
    swap = psutil.swap_memory()
    if swap.total > 0:
        info["Swap Usage"] = f"{swap.percent}% ({swap.used / (1024 ** 3):.2f} GB of {swap.total / (1024 ** 3):.2f} GB)"
    
    # Disk I/O with read/write rates
    try:
        disk_io = psutil.disk_io_counters()
        if disk_io:
            # Get read/write counts
            reads = disk_io.read_count
            writes = disk_io.write_count
            
            # Format disk I/O information
            io_str = (
                f"Read: {disk_io.read_bytes / (1024 ** 3):.2f} GB ({reads:,} operations), "
                f"Write: {disk_io.write_bytes / (1024 ** 3):.2f} GB ({writes:,} operations)"
            )
            info["Disk I/O"] = io_str
    except Exception:
        pass
    
    # Network I/O with packets
    try:
        net_io = psutil.net_io_counters()
        if net_io:
            # Calculate data transferred
            recv_mb = net_io.bytes_recv / (1024 ** 2)
            sent_mb = net_io.bytes_sent / (1024 ** 2)
            
            # Format with packets information
            net_str = (
                f"↓ {recv_mb:.1f} MB ({net_io.packets_recv:,} packets), "
                f"↑ {sent_mb:.1f} MB ({net_io.packets_sent:,} packets)"
            )
            info["Network I/O"] = net_str
    except Exception:
        pass
    
    # Get network connection count
    try:
        connections = len(psutil.net_connections())
        info["Active Connections"] = f"{connections} connections"
    except Exception:
        pass
    
    # Process information
    try:
        processes = len(psutil.pids())
        info["Processes"] = f"{processes} running processes"
    except Exception:
        pass
    
    # Battery (for laptops) with time remaining
    try:
        battery = psutil.sensors_battery()
        if battery and hasattr(battery, 'percent') and hasattr(battery, 'power_plugged'):
            status = "Charging" if battery.power_plugged else "Discharging"
            
            # Add time remaining if available and discharging
            if hasattr(battery, 'secsleft') and battery.secsleft != -1 and not battery.power_plugged:
                seconds = battery.secsleft
                hours, remainder = divmod(seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                time_str = f"{hours}h {minutes}m remaining"
                info["Battery"] = f"{battery.percent}% ({status}, {time_str})"
            else:
                info["Battery"] = f"{battery.percent}% ({status})"
    except Exception:
        pass
    
    # CPU temperature if available
    try:
        temperatures = psutil.sensors_temperatures()
        if temperatures:
            # Get the first temperature sensor
            for name, entries in temperatures.items():
                if entries:
                    info["CPU Temperature"] = f"{entries[0].current:.1f}°C"
                    break
    except Exception:
        pass
    
    # System load averages (Linux/Unix only)
    try:
        load1, load5, load15 = os.getloadavg()
        info["Load Average"] = f"1m: {load1:.2f}, 5m: {load5:.2f}, 15m: {load15:.2f}"
    except Exception:
        pass
    
    return info

def gather_system_info(include_performance=False):
    """Gather all system information and return in a dictionary"""
    system_data = OrderedDict()
    
    try:
        # Basic info
        system_data["Host"] = get_host_info()
        system_data["OS"] = get_os_info()
        system_data["CPU"] = get_processor_info()
        system_data["Memory"] = get_memory_info()
        system_data["GPU"] = get_gpu_info()
        system_data["Disk"] = get_disk_info()
        system_data["Network"] = get_network_info()
        system_data["Packages"] = get_package_info()
        
        # Add performance metrics if requested
        if include_performance:
            system_data["Performance"] = get_performance_metrics()
    
    except Exception as e:
        print(f"Error gathering system info: {e}")
    
    return system_data

# Import here to avoid circular imports
import time
