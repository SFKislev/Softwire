import importlib
import sys
import traceback


try:
    previous = sys.modules.get("creative_adapter_bridge")
    if previous is not None and hasattr(previous, "stop_bridge"):
        previous.stop_bridge()

    import creative_adapter_bridge
    importlib.reload(creative_adapter_bridge)
    creative_adapter_bridge.start_bridge()
except Exception:
    traceback.print_exc()
