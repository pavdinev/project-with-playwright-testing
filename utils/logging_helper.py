# utils/logging_helper.py
import logging
import traceback

def safe_action(action_desc: str, action_fn, default=None):
    """
    Wrap an action with error logging. If an exception occurs, log it and re-raise.
    """
    try:
        result = action_fn()
        logging.info(f"✅ Success: {action_desc}")
        return result
    except Exception as e:
        logging.error(
            f" Failed to {action_desc}. Exception: {e.__class__.__name__}: {e}"
        )
        logging.debug(traceback.format_exc())
        raise   
