import base64
import functools
import inspect
import json
import os
import traceback
from pathlib import Path
from typing import Annotated, Any, Tuple, Union

import cv2
import numpy as np
import pandas as pd
from huggingface_hub import HfApi
from loguru import logger
from pydantic import BeforeValidator, PlainSerializer
from rich import print

from phosphobot.types import VideoCodecs


class NumpyEncoder(json.JSONEncoder):
    """Custom encoder for numpy data types"""

    def default(self, obj):
        logger.info(f"Encoding with NumpyEncoder object type({type(obj)}) {obj}")
        if isinstance(obj, np.ndarray):
            logger.debug(f"Encoding NumpyEncoder numpy array of shape {obj.shape}")
            return {
                "_type": "ndarray",
                "data": obj.tolist(),
                "dtype": str(obj.dtype),
                "shape": obj.shape,
            }
        return json.JSONEncoder.default(self, obj)


def decode_numpy(dct: dict) -> Union[np.ndarray, dict]:
    """Custom decoder. Reads the encoded numpy array from the JSON file."""
    if isinstance(dct, dict) and dct.get("_type") == "ndarray":
        return np.array(dct["data"], dtype=np.dtype(dct["dtype"]))
    if "__numpy__" in dct:
        data = base64.b64decode(dct["__numpy__"])
        arr = np.frombuffer(data, dtype=np.dtype(dct["dtype"]))
        arr = arr.reshape(dct["shape"])
        return arr
    return dct


def nd_array_custom_before_validator(x: Any) -> np.ndarray:
    # custom before validation logic
    if isinstance(x, list):
        return np.array(x)
    elif isinstance(x, np.ndarray):
        return x
    elif isinstance(x, float) or isinstance(x, int):
        # Convert scalar to 1D array
        # This shouldn't happen with normal serialization, but can happen due to bugs.
        return np.array([x])
    else:
        raise ValueError("Invalid type for numpy array")


def nd_array_custom_serializer(x: np.ndarray):
    # custom serialization logic: convert to list
    return x.tolist()


# Custom type for numpy array. Stores np.ndarray as list in JSON.
NdArrayAsList = Annotated[
    np.ndarray,
    BeforeValidator(nd_array_custom_before_validator),
    PlainSerializer(nd_array_custom_serializer, return_type=list),
]


def create_video_file(
    frames: np.ndarray,
    target_size: Tuple[int, int],
    output_path: str,
    fps: float,
    codec: VideoCodecs,
) -> str | Tuple[str, str]:
    """
    Create a video file from a list of frames and resize video to target size.
    For stereo cameras (aspect ratio >= 8/3), creates separate left and right video files.

    Args:
        frames (list of np.ndarray): List of frames in RGB format.
        target_size (Tuple[int, int]): Target dimensions (width, height) for the output video.
        output_path (str): Path to save the video file.
        fps (float): Frames per second for the video.
        codec (str): FourCC codec for the video. Defaults to "mp4v" (MPEG-4 for MP4).

    Returns:
        Union[str, Tuple[str, str]]: Path(s) to created video file(s). Returns tuple of paths for stereo.

    Raises:
        ValueError: If frames are empty or incorrectly formatted.
        RuntimeError: If the video writer cannot be initialized.
    """
    # Check if stereo camera based on aspect ratio
    sample_frame = frames[0]
    aspect_ratio = sample_frame.shape[1] / sample_frame.shape[0]  # width/height
    is_stereo = aspect_ratio >= 8 / 3

    logger.info(
        f"Creating video file - stereo: {is_stereo} - Aspect ratio: {aspect_ratio}"
    )

    def init_video_writer(path: str, size: Tuple[int, int]) -> cv2.VideoWriter:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        logger.info(f"Creating video file at path: {path}")

        fourcc = cv2.VideoWriter_fourcc(*codec)  # type: ignore
        out = cv2.VideoWriter(path, fourcc, fps, size)

        if not out.isOpened():
            try:
                out.open(path, fourcc, fps, size)
            except Exception as e:
                logger.error(f"Error while creating video file: {e}")
                raise RuntimeError(f"Error while creating video: {e}")
        return out

    def process_frame(frame: np.ndarray, target_size: Tuple[int, int]) -> np.ndarray:
        if frame.dtype != np.uint8:
            frame = np.clip(frame, 0, 255).astype(np.uint8)
        resized_frame = cv2.resize(frame, target_size, interpolation=cv2.INTER_AREA)
        return cv2.cvtColor(resized_frame, cv2.COLOR_RGB2BGR)

    if is_stereo:
        # Split path for stereo output
        path = output_path.split("/episode")
        left_path = f"{path[0]}.left/episode{path[1]}"
        right_path = f"{path[0]}.right/episode{path[1]}"

        # Split width in half for stereo
        target_size = (target_size[0] // 2, target_size[1])

        logger.info(
            f"Splitting stereo video into left and right - paths: {left_path}, {right_path}"
        )

        # Initialize writers for both streams
        out_left = init_video_writer(left_path, target_size)
        out_right = init_video_writer(right_path, target_size)

        frame_width = sample_frame.shape[1] // 2  # Split width in half for stereo

        for frame in frames:
            # Split frame into left and right
            left_frame = frame[:, :frame_width]
            right_frame = frame[:, frame_width:]

            # Process and write each frame
            out_left.write(process_frame(left_frame, target_size))
            out_right.write(process_frame(right_frame, target_size))

        out_left.release()
        out_right.release()

        print(f"""[green]Left output path: {left_path}
Right output path: {right_path}
fps: {fps}
codec: {codec}
target_size of each video: {target_size}[/green]""")
        return left_path, right_path

    else:
        # Single camera processing
        out = init_video_writer(output_path, target_size)

        for frame in frames:
            out.write(process_frame(frame, target_size))

        out.release()

        print(f"""[green]Output path: {output_path}
Fps: {fps}
codec: {codec}
Target_size of video: {target_size}[/green]""")
        return output_path


def get_home_app_path() -> Path:
    """
    Return the path to the app's folder in the user's home directory.
    This is used to store user-specific data.

    It's platform dependent.

    user_home/
        phosphobot/
            calibration/
            recordings/
            ...
    """
    home_path = Path.home() / "phosphobot"
    # Create the folder if it doesn't exist
    home_path.mkdir(parents=True, exist_ok=True)
    # Create subfolders
    (home_path / "calibration").mkdir(parents=True, exist_ok=True)
    (home_path / "recordings").mkdir(parents=True, exist_ok=True)
    return home_path


def compute_sum_squaresum_framecount_from_video(
    video_path: str,
) -> Tuple[np.ndarray, np.ndarray, int]:
    """
    Process a video file and calculate the sum of RGB values and sum of squares of RGB values for each frame.
    Returns a list of np.ndarray corresponding respectively to the sum of RGB values, sum of squares of RGB values and nb_pixel.
    We divide by 255.0 RGB values to normalize the values to the range [0, 1].
    """
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise FileNotFoundError(f"Error: Could not open video at path: {video_path}")

    nb_pixel = 0
    total_sum_rgb = np.zeros(3, dtype=np.float32)  # To store sum of RGB values
    total_sum_squares = np.zeros(
        3, dtype=np.float32
    )  # To store sum of squares of RGB values
    while True:
        # Read a frame from the video
        ret, frame = cap.read()
        # If the frame was not read successfully, break the loop
        if not ret:
            break

        # Convert the frame from BGR to RGB (OpenCV uses BGR by default)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) / 255.0
        # Calculate the sum of RGB values for the frame
        sum_rgb = np.sum(frame_rgb, axis=(0, 1))
        # Calculate the sum of squares of RGB values for the frame
        sum_squares = np.sum(frame_rgb**2, axis=(0, 1))
        # Accumulate the sums
        # Cannot cast ufunc 'add' output from dtype('float64') to dtype('uint64') with casting rule 'same_kind'
        total_sum_rgb = total_sum_rgb + sum_rgb
        total_sum_squares = total_sum_squares + sum_squares

        # nb Pixel
        nb_pixel += frame_rgb.shape[0] * frame_rgb.shape[1]

    # Release the video capture object
    # TODO: If problem of dimension maybe transposing arrays is needed.
    cap.release()
    return (total_sum_rgb, total_sum_squares, nb_pixel)


def get_field_min_max(df: pd.DataFrame, field_name: str) -> tuple:
    """
    Compute the minimum value for the given field in the DataFrame.

    If the field values are numeric, returns a scalar minimum.
    If the field values are lists/arrays, returns an element-wise minimum array.

    Parameters:
        df (pd.DataFrame): DataFrame containing the data.
        field_name (str): The name of the field/column to compute the min,max for.

    Returns:
        The minimum value(s) for the specified field.

    Raises:
        ValueError: If the field does not exist or if list/array values have inconsistent shapes.
    """
    if field_name not in df.columns:
        raise ValueError(f"Field '{field_name}' not found in DataFrame")

    # Get a sample value (skip any nulls)
    sample_value = df[field_name].dropna().iloc[0]

    # If the field values are lists or arrays, compute element-wise min, max
    if isinstance(sample_value, (list, np.ndarray)):
        # Check that df[field_name].values is a np.ndarray
        array_values = df[field_name].values

        # No overload variant of "vstack" matches argument type "ndarray[Any, Any]"
        return (
            np.min(np.vstack(array_values), axis=0),  # type: ignore
            np.max(np.vstack(array_values), axis=0),  # type: ignore
        )
    else:
        # Otherwise, assume the field is numeric and return the scalar min.
        return (df[field_name].min(), df[field_name].max())


def parse_hf_username_or_orgid(user_info: dict) -> str | None:
    """
    Extract the username or organization name from the user info dictionary.
    user_info = api.whoami(token=hf_token)
    """
    # Extract the username
    username = user_info.get("name", "Unknown")

    # If no fine grained permissions, return the username
    if user_info.get("auth", {}).get("accessToken", {}).get("role") == "write":
        return username

    # Extract fine-grained permissions
    fine_grained_permissions = (
        user_info.get("auth", {}).get("accessToken", {}).get("fineGrained", {})
    )
    scoped_permissions = fine_grained_permissions.get("scoped", [])

    # Check if the token has write access to the user account
    user_has_write_access = False
    org_with_write_access = None

    for scope in scoped_permissions:
        entity = scope.get("entity", {})
        entity_type = entity.get("type")
        entity_name = entity.get("name")
        permissions = scope.get("permissions", [])

        # Check if the entity is the user and has write access
        if entity_type == "user" and "repo.write" in permissions:
            user_has_write_access = True
            # Return the username
            return username

        # Check if the entity is an org and has write access
        if entity_type == "org" and "repo.write" in permissions:
            org_with_write_access = entity_name
            return org_with_write_access

    logger.warning(
        "No user or org with write access found. Wont be able to push to Hugging Face."
    )

    return None


def get_hf_username_or_orgid() -> str | None:
    """
    Returns the username or organization name from the Hugging Face token file.
    Returns None if we can't write anywhere.
    """
    token_file = get_home_app_path() / "huggingface.token"

    # Check the file exists
    if not token_file.exists():
        logger.info("Token file not found.")
        return None

    with open(token_file, "r") as file:
        hf_token = file.read().strip()
    if hf_token:
        try:
            api = HfApi()
            user_info = api.whoami(token=hf_token)
            # Get the username or org where we have write access
            username_or_orgid = parse_hf_username_or_orgid(user_info)
            return username_or_orgid
        except Exception as e:
            logger.warning(f"Error logging in to Hugging Face: {e}")
            return None
    else:
        logger.warning(f"Empty token file: {token_file}. Won't push to HuggingFace.")
        return None


def get_hf_token() -> str | None:
    """
    Returns the hf token from the token file.
    Returns None if there is no token.
    """
    token_file = get_home_app_path() / "huggingface.token"

    # Check the file exists
    if not token_file.exists():
        logger.info("Token file not found.")
        return None

    with open(token_file, "r") as file:
        hf_token = file.read().strip()
    if hf_token:
        return hf_token
    else:
        logger.warning(f"Empty token file: {token_file}.")
        return None


def background_task_log_exceptions(func):
    """
    Decorator to log exceptions in background tasks (works for both sync/async functions).
    Otherwise, the exception is silently swallowed.
    """

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Background task error: {str(e)}\n{traceback.format_exc()}")
            raise

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Background task error: {str(e)}\n{traceback.format_exc()}")
            raise

    if inspect.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper
