# utils/logging_helper.py
import logging
import traceback

def safe_action(action_desc: str, action_fn, default=None, record_fn=None, details=None):
    """
    Executes an action safely with logging and optional reporting.

    Args:
        action_desc (str): Description of the action (e.g., "fill username").
        action_fn (callable): Function to execute.
        default: Value to return if an exception occurs (instead of raising).
        record_fn (callable): Optional function to record step results into a report.
                              Signature: record_fn(step_name: str, success: bool, details: dict).
        details (dict): Optional extra info to pass into record_fn.

    Returns:
        Result of action_fn() if successful, otherwise `default`.
    """
    try:
        result = action_fn()
        logging.info(f"Success: {action_desc}")
        if record_fn:
            record_fn(action_desc, True, details or {})
        return result
    except Exception as e:
        logging.error(f"Failed to {action_desc}. Exception: {e.__class__.__name__}: {e}")
        logging.debug(traceback.format_exc())
        if record_fn:
            record_fn(action_desc, False, {"error": str(e), **(details or {})})
        if default is not None:
            return default
        raise
