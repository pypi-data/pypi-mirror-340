# CognitiveSDK Documentation: System Architecture and Data Flow

## Overview

CognitiveSDK is a flexible framework designed for real-time data acquisition and streaming from various input devices and sensors. It provides a modular architecture for connecting to devices (like Muse-S, Emotibit, MetaGlass), transmitting their data through a queuing system, and processing that data in real-time applications.

The core of the framework uses a distributed publish-subscribe (XPub/XSub) pattern built on ZeroMQ, allowing multiple components to share data efficiently across processes or even different machines on a network.

CognitiveSDK implements automatic sensor management that creates dedicated Subdevices for each sensor on a physical device. For example, when connecting to a device with EEG, PPG, and MAG sensors, CognitiveSDK automatically creates three dedicated subdevices—one for each sensor type. Each subdevice functions as a ZeroMQ Publisher, contributing data to the central queuing system.

The SDK leverages ZeroMQ's topic-based messaging system, where each publisher (subdevice) is assigned a unique topic. This allows users to subscribe to specific data streams using a hierarchical naming convention. For example, if a device named "my_device" has EEG, PPG, and MAG sensors, users can subscribe to "my_device.EEG", "my_device.PPG", or "my_device.MAG" to access each specific data stream.

## System Architecture Diagram

The following diagram illustrates the overall architecture of CognitiveSDK, showing how data flows from devices through the system:

![CognitiveSDK Architecture](arch.png)

The diagram shows the relationship between devices, subdevices, the messaging system, and how applications can consume the data through subscribers.

## Core Architecture

The system consists of several key components:

### Key Components

1. **Device Layer**: Connects to physical devices and loads their configurations
2. **Subdevice Layer**: Handles specific data streams from devices (e.g., EEG, PPG, Video)
3. **Middleware Layer**: Provides adapters for different device communication protocols (BrainFlow, LSL, etc.)
4. **Messaging Layer**: Uses ZeroMQ for efficient publish-subscribe data distribution
5. **Metadata Responder**: Implements a ZeroMQ Rep/Req pattern to provide metadata about currently streaming devices

## Data Flow

### Acquisition and Distribution Flow

1. **Physical Device → Middleware Interface**
   - Middleware interfaces (BrainFlow, LSL, etc.) connect to physical devices
   - Raw data samples are acquired in batches

2. **Middleware Interface → SubDevice → Publisher**
   - Raw data is passed to the appropriate SubDevice based on sensor type
   - Each SubDevice processes the incoming data according to its sensor type
   - SubDevices act as Publishers that serialize and format the data for distribution

3. **Publisher → ZeroMQ Proxy → Subscribers**
   - Publishers send data to a central XPubXSubProxy on specific topics (e.g., "museA.EEG", "metaglassA.Video")
   - The proxy distributes messages to all interested subscribers
   - Subscribers deserialize the data and invoke user-defined callbacks

4. **Subscribers → Applications**
   - Applications consume the data for visualization, processing, or analysis
   - Data can be further processed for specific application needs
   - SDK includes two built-in subscriber implementations: local_cache (for storing data locally) and send_data_to_server (for transmitting data to remote servers)

## Key Components in Detail

### 1. Device Layer

#### `Device` (base.py)
- Represents a physical device (e.g., Muse-S, Emotibit, MetaGlass)
- Loads presets from JSON files, which contain essential device information such as channel names and middleware compatibility
- Manages subdevices and middleware connections
- Provides uniform interface regardless of device type

#### `DeviceManager` (device_manager.py)
- Factory for creating and managing multiple devices
- Provides concurrent connect/disconnect operations
- Central point for device lifecycle management

### 2. Subdevice Layer

#### `SubDevice` (subdevice.py)
- Represents a specific data stream from a device (e.g., EEG, PPG, Video)
- Handles data forwarding to publishers
- Manages topic naming based on prefix
- Processes streaming data specific to the sensor type

### 3. Middleware Layer

#### `BrainflowInterface` (brainflow.py)
- Connects to BrainFlow-compatible devices
- Manages data acquisition loops
- Handles device-specific configuration

#### Other Middleware Adapters (extensible)
- The system can be extended with additional middleware adapters
- Examples include LSL (Lab Streaming Layer), custom device protocols, etc.
- Each adapter presents a uniform interface to the Device layer

### 4. Messaging System

#### `XPubXSubProxy` (proxy.py)
- Core message broker for distributing data
- Uses ZeroMQ XPUB/XSUB pattern for efficient message routing
- Dynamically allocates ports for communication

#### `Publisher` (publisher.py)
- Serializes data with binary encoding
- Handles control commands (START, PAUSE, RESUME, STOP)
- Publishes to specific topics with metadata
- Implements a consistent binary serialization format:
  - 4-byte sequence number (uint32)
  - 8-byte timestamp (float64)
  - Channel data (float32 array)

#### `DataSubscriber` (subscriber.py)
- Subscribes to topics and receives binary messages
- Parses binary data back into NumPy arrays
- Provides callback mechanism for data processing

#### `ProxyManager` (manager.py)
- Ensures a single global proxy instance
- Manages proxy lifecycle
- Shares proxy port information through SharedState

#### `MetadataResponder` (metadata.py)
- Implements a ZeroMQ Rep pattern to distribute metadata about active devices
- Provides information such as device types, active channels, sampling rates, and stream status
- Allows applications to discover and monitor available data streams

### 5. Shared State Management

#### `SharedState` (shared_state.py)
- Provides persistence between processes using a temp file
- Stores critical information like proxy ports
- Tracks active topics for discovery
- Maintains control flags

## Configuration System

The SDK uses JSON preset files to specify device properties. These presets define how the system should interact with different device types and how to configure their data streams:

```json
{
    "model": "Muse-S",
    "id": "203498120",
    "middleware": {
        "brainflow": {
            "device_board_name": "MUSE_S_BOARD",
            "board_id": 39,
            "sub_devices": {
              "PPG": {
                "channels_name": ["PPG1", "PPG2", "PPG3"],
                "channels_index": [1, 2, 3],
                "type": "PPG",
                "sampling_rate": 64,
                "preset": "AUXILIARY"
              },
              "EEG": {
                "channels_name": ["TP9", "AF7", "AF8", "TP10"],
                "channels_index": [1, 2, 3, 4],
                "type": "EEG",
                "sampling_rate": 256,
                "preset": "DEFAULT"
              },
              "ACCELEROMETER": {
                "channels_name": ["X", "Y", "Z"],
                "channels_index": [1, 2, 3],
                "type": "ACCELEROMETER",
                "sampling_rate": 52,
                "preset": "ANCILLARY"
              }
            }
        },
        "lsl": {
            "sub_devices": {
              "PPG": {
                "channels_name": ["PPG1", "PPG2", "PPG3"],
                "channels_index": [4, 5, 6],
                "type": "PPG",
                "sampling_rate": 64
              },
              "EEG": {
                "channels_name": ["TP9", "AF7", "AF8", "TP10"],
                "channels_index": [0, 1, 2, 3],
                "type": "EEG",
                "sampling_rate": 256
              },
              "ACCELEROMETER": {
                "channels_name": ["X", "Y", "Z"],
                "channels_index": [0, 1, 2],
                "type": "ACCELEROMETER",
                "sampling_rate": 52
              }
            }
        }
    }
}
```

These preset files specify:
- Device identifiers and model information
- Middleware compatibility and settings
- Channel information and indices for each sensor type
- Sampling rates and data characteristics
- Data processing parameters and presets

## Supported Device Types

The framework is designed to work with a variety of input devices, not limited to EEG hardware:

### Examples of Supported Devices

1. **Muse-S**
   - EEG (brain activity)
   - PPG (blood pulse)
   - Accelerometer (motion)

2. **Incoming**

The extensible architecture allows for integration with virtually any device that can stream data, regardless of the sensor type or data format.

## Installation

```
pip install -r requirements.txt
```


## Launching on raspberry:
`python main.py --done_callback_path ./playground/success-melody.py --error_callback_path ./playground/done-melody.py`
launching logger

`npm install watch-http-server -g`

`watch-http-server ./logs`