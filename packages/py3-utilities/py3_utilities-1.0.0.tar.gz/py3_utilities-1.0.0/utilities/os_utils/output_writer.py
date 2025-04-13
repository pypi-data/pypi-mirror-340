import aiofiles
import asyncio
import pandas as pd
from typing import List, Union
from contextlib import asynccontextmanager
from pathlib import Path


@asynccontextmanager
async def open_buffered_output_file(file_path: Union[str, Path], buffer_size: int = 1000):
    """
    Asynchronous context manager for writing to a file with optional buffering.
    Supports both plain text files and special formats like CSV and Excel.

    :param file_path: Path to the output file.
    :param buffer_size: Maximum number of lines to buffer before writing to a plain text file.
    :yield: A callable that takes a file path string and buffers it for writing.
    """
    buffer = []
    output_path = Path(file_path)
    is_special_format = output_path.suffix.lower() in ['.csv', '.xls', '.xlsx']

    try:
        if is_special_format:
            yield lambda file: _buffered_append(str(file), buffer)
        else:
            async with aiofiles.open(output_path, 'w', encoding='utf-8') as f:
                yield lambda file: _buffered_write(str(file), buffer, f, buffer_size)

    except Exception as e:
        print(f"Error during file operation: {e}")
        raise
    
    finally:
        if buffer:
            try:
                if is_special_format:
                    loop = asyncio.get_event_loop()
                    await loop.run_in_executor(None, _write_with_pandas_sync, output_path, buffer)
                else:
                    async with aiofiles.open(output_path, mode='a', encoding='utf-8') as f:
                        await f.write('\n'.join(buffer) + '\n')
            except Exception as e:
                print(f"Error flushing buffer: {e}")
                raise

async def _buffered_write(file: str, buffer: List[str], f, buffer_size: int):
    """
    Buffers and writes lines to a file asynchronously when buffer reaches specified size.

    :param file: String representing a file path to write.
    :param buffer: List storing buffered strings.
    :param f: Asynchronously opened file object.
    :param buffer_size: Maximum number of buffered lines before flushing to file.
    """
    buffer.append(file)
    if len(buffer) >= buffer_size:
        try:
            await f.write('\n'.join(buffer) + '\n')
            buffer.clear()
        except Exception as e:
            print(f"Error writing buffer to file: {e}")
            raise

async def _buffered_append(file: str, buffer: List[str]):
    """
    Appends a file path string to the buffer (used for CSV/Excel formats).

    :param file: String representing a file path to append.
    :param buffer: List storing buffered strings.
    """
    buffer.append(file)

def _write_with_pandas_sync(output_path: Path, buffer: List[str]):
    """
    Writes buffered file path strings to a CSV or Excel file synchronously using pandas.

    :param output_path: Path to the output file.
    :param buffer: List of strings representing file paths.
    :raises Exception: If writing with pandas fails.
    """
    df = pd.DataFrame(buffer, columns=['Path'])
    try:
        if output_path.suffix.lower() == '.csv':
            df.to_csv(output_path, index=False)
        else:
            df.to_excel(output_path, index=False, engine='openpyxl')
    except Exception as e:
        print(f"Error writing with pandas: {e}")
        raise
