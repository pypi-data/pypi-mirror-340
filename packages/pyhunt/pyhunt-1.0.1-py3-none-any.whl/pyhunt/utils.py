import types


def _filter_traceback(tb):
    frames_to_keep = []
    while tb is not None:
        filename = tb.tb_frame.f_code.co_filename
        # Exclude frames from the decorator file
        if "pyhunt/decorator.py" not in filename.replace("\\", "/"):
            frames_to_keep.append((tb.tb_frame, tb.tb_lasti, tb.tb_lineno))
        tb = tb.tb_next

    # Reconstruct the traceback from the kept frames
    filtered_tb = None
    for frame, lasti, lineno in reversed(frames_to_keep):
        filtered_tb = types.TracebackType(filtered_tb, frame, lasti, lineno)

    return filtered_tb


def extract_first_traceback(traceback_text):
    """
    Extracts and returns the first traceback block from a traceback string.

    Parameters:
        traceback_text (str): The full traceback string.

    Returns:
        str: The first traceback block, including the error message.
    """
    lines = traceback_text.splitlines()
    first_tb_lines = []
    in_first_tb = False

    for line in lines:
        if line.startswith("Traceback (most recent call last):"):
            if not in_first_tb:
                in_first_tb = True
                first_tb_lines.append(line)
            elif in_first_tb:
                # Encountered another traceback start, stop at the first one
                break
        elif in_first_tb:
            # Stop if we reach the "During handling..." line
            if (
                "During handling of the above exception, another exception occurred:"
                in line
            ):
                break
            first_tb_lines.append(line)

    return "\n".join(first_tb_lines)
