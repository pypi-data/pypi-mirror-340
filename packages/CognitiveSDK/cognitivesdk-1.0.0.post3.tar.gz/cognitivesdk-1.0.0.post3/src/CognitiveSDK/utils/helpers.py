import asyncio
import importlib
import re
from typing import Dict, Any, Optional, Coroutine, Union, Tuple

# Use relative import based on file location within utils
from .logger import logger 

def camel_to_snake(word: str) -> str:
    """Convert CamelCase string to snake_case."""
    # Add _ between acronym and next word (e.g., HTTPRequest -> HTTP_Request)
    word = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', word)
    # Add _ between lowercase/digit and uppercase (e.g., SimpleCase -> Simple_Case)
    word = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', word)
    # Optional: handle dashes if needed, uncomment below
    # word = word.replace("-", "_")
    return word.lower()

async def start_single_external_subscriber(
    config_item: Union[str, Dict[str, Any]], 
    metadata_port: int
) -> Optional[Tuple[str, Dict[str, Any]]]:
    """
    Loads, instantiates, and starts a single external subscriber based on config.

    Args:
        config_item: Configuration (either class name string or dictionary).
        metadata_port: The port for the metadata service.

    Returns:
        A tuple containing (subscriber_key, {"instance": obj, "task": task}) or None on failure.
    """
    class_name = None
    module_path = None
    init_args = {}

    # Determine module_path, class_name, and init_args based on config_item type
    if isinstance(config_item, str):
        class_name = config_item
        module_name_part = camel_to_snake(class_name)
        # Construct the path assuming subscribers are in a top-level 'subscriber' directory.
        module_path = f"subscriber.{module_name_part}"
        logger.debug(f"Inferred module path '{module_path}' for class '{class_name}'")
    elif isinstance(config_item, dict):
        module_path = config_item.get("module_path")
        class_name = config_item.get("class_name")
        init_args = config_item.get("init_args", {})
    else:
        logger.error(f"Invalid configuration type in ExternalSubscriberList: {config_item}")
        return None
    
    if not module_path or not class_name:
        logger.error(f"Could not determine module_path or class_name for config: {config_item}")
        return None

    subscriber_key = f"{module_path}.{class_name}"

    try:
        logger.debug(f"Loading external subscriber: {subscriber_key}")
        module = importlib.import_module(module_path)
        SubscriberClass = getattr(module, class_name)
        
        # Add metadata_port (always add this)
        init_args["metadata_port"] = metadata_port
        
        instance = SubscriberClass(**init_args)
        logger.info(f"Instantiated: {subscriber_key} with args {init_args}")

        # Ensure instance.start exists and is callable
        if not (hasattr(instance, 'start') and callable(instance.start)):
             logger.error(f"Subscriber class {subscriber_key} does not have a callable 'start' method.")
             return None
        
        task = asyncio.create_task(instance.start())
        logger.info(f"Started task for: {subscriber_key}")
        
        return subscriber_key, {"instance": instance, "task": task}
        
    except ModuleNotFoundError:
        logger.error(f"Module not found: {module_path}")
    except AttributeError:
        # More specific error if start() is missing vs class not found
        logger.error(f"Class '{class_name}' not found in '{module_path}' or instance missing 'start' method") 
    except TypeError as e:
         logger.error(f"Error instantiating '{subscriber_key}' with args {init_args}: {e}")
    except Exception as e:
        logger.error(f"Error starting {subscriber_key}: {e}", exc_info=True)
        
    return None

async def stop_single_external_subscriber(
    key: str, 
    instance: Any, 
    task: asyncio.Task
) -> Optional[asyncio.Task]: # Return task if cancellation needed
    """Stops and cleans up a single external subscriber instance and task.
    
    Returns the task if it needed cancellation, otherwise None.
    """
    logger.debug(f"Stopping: {key}")
    try:
        if hasattr(instance, 'stop') and callable(instance.stop):
            stop_method = instance.stop
            if asyncio.iscoroutinefunction(stop_method):
                await stop_method()
            else:
                # If stop is synchronous, call it directly. 
                # Consider asyncio.to_thread if it might block significantly.
                stop_method()
            logger.debug(f"Called stop() on {key}")
    except Exception as e:
        logger.error(f"Error calling stop() on {key}: {e}")

    # Cancel the task if it's still running
    if task and not task.done():
         logger.debug(f"Cancelling task for {key}")
         task.cancel()
         return task # Return task to be awaited by caller
    return None 

def extract_topics_with_rates(devices_state: Dict[str, Any]) -> Dict[str, Optional[int]]:
    """
    Extracts a dictionary of {topic_name: sampling_rate} from the devices state structure.

    Args:
        devices_state: The 'Devices' dictionary from SharedState.

    Returns:
        A dictionary mapping full topic names to their sampling rates (or None).
    """
    extracted_topics = {}
    logger.debug(f"Extracting topics from {len(devices_state)} devices provided...")
    for device_name, device_info in devices_state.items():
        if isinstance(device_info, dict):
            selected_middleware = device_info.get("SelectedMiddleware")
            if selected_middleware:
                middlewares = device_info.get("AvailableMiddlewares", {})
                middleware_info = middlewares.get(selected_middleware, {})
                subdevices = middleware_info.get("SubDevices", {})
                if not subdevices:
                    logger.debug(f"No SubDevices found for {device_name} under middleware {selected_middleware}.")
            else:
                logger.debug(f"No SelectedMiddleware found for device '{device_name}'.")
                subdevices = {}
                
            for sub_name, sub_info in subdevices.items():
                if isinstance(sub_info, dict): # Ensure sub_info is a dict before accessing keys
                    full_topic_name = f"{device_name}.{sub_name}"
                    # Use the correct key from the state structure
                    sampling_rate = sub_info.get("SamplingFrequency") 
                    extracted_topics[full_topic_name] = sampling_rate
                else:
                    logger.warning(f"Expected dict for subdevice '{sub_name}' under device '{device_name}', but got {type(sub_info)}. Skipping.")
        else:
            logger.warning(f"Expected dict for device '{device_name}', but got {type(device_info)}. Skipping.")
                
    return extracted_topics 