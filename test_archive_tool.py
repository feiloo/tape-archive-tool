import pytest
from pathlib import Path
import hashlib
import time
import subprocess
import json
import os

import random
import re
import string
import socket

import archive_tool

# test config parameters
tmp_testpath = '/data/'
seed = 42

# unimportant/unused numbers were replaced with X

dsmc_query_filespace_output = '''IBM Storage Protect
Command Line Backup-Archive Client Interface
  Client Version X, Release X, Level XX.X
  Client date/time: XX/XX/XXXX XX:XX:XX
(c) Copyright IBM Corp. 1990, 2025. All Rights Reserved.

Node Name: XXXXXXXXXXX
Session established with server XXXXXXX: XXX
  Server Version X, Release X, Level XX.XXX
  Server date/time: XX/XX/XXXX XX:XX:XX  Last access: XX/XX/XXXX XX:XX:XX

  #     Last Incr Date          Type    File Space Name
--------------------------------------------------------------------------------
  1     00/00/0   00:00:00     BTRFS   /a
  2     00/00/0   00:00:00     XFS     /b
  3     00/00/0   00:00:00     EXT4    /c
  4     00/00/0   00:00:00     CIFS    /d
'''
DSMC_SPY = []

def fake_dsmc(cmd, **kwargs):
    ''' this is a test-spy-object for "mocking" out the dsmc tool '''
    global DSMC_SPY

    DSMC_SPY += [cmd]

    print(cmd)
    if cmd[:3] == ['dsmc', 'query', 'filespace']:
        class FakeRes:
            stdout = dsmc_query_filespace_output
            stderr = ""
        return FakeRes()
    elif cmd[:2] == ['dsmc', 'archive']:
        objnames = cmd[2:]
        class FakeRes:
            stdout = ""
            stderr = ""
        return FakeRes()
    elif cmd[:3] == ['dsmc', 'query', 'archive']:
        class FakeRes:
            stdout = ""
            stderr = ""
        return FakeRes()
    elif cmd[:2] == ['dsmc', 'retrieve']:
        class FakeRes:
            stdout = ""
            stderr = ""
        return FakeRes()
    elif cmd[:2] == ['dsmc', 'delete']:
        class FakeRes:
            stdout = ""
            stderr = ""
        return FakeRes()
    elif cmd[:3] == ['dsmc', 'query','systeminfo']:
        class FakeRes:
            stdout = ""
            stderr = ""
        return FakeRes()
    elif cmd[0] == 'sha256sum':
        # passthrough this one

        result = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='strict'
        )
        return result

    # should not reach here
    assert False, "unexpected dmsc command invoked during testing"

@pytest.fixture
def spy_dsmc(monkeypatch):
    monkeypatch.setattr(archive_tool, "subproc", fake_dsmc)


def create_many_flat_folders_and_files(path, num_folders=10000):
    for i in range(1, num_folders + 1):
        folder_path = os.path.join(path, f'folder_{i}')
        try:
            os.makedirs(folder_path, exist_ok=True)
        except Exception as e:
            print(f"Directory creation failed: {folder_path} - {e}")
            continue

        file_path = os.path.join(folder_path, 'number.txt')
        try:
            with open(file_path, 'w') as f:
                f.write(f"{i}\n")
        except Exception as e:
            print(f"File write failed: {file_path} - {e}")


def create_deep_folder_hierarchy(path, num_levels=200):
    for i in range(1, num_levels + 1):
        new_dir = os.path.join(path, f'folder_{i}')
        try:
            os.makedirs(new_dir, exist_ok=True)
        except Exception as e:
            print(f"Directory creation failed: {new_dir} - {e}")
            break  # Stop if directory can't be created
        current_dir = new_dir  # Update path for next level

        file_path = os.path.join(path, 'number.txt')
        try:
            with open(file_path, 'w') as f:
                f.write(f"{i}\n")
        except Exception as e:
            print(f"File write failed: {file_path} - {e}")

    print(f"Created {i} folders out of {num_levels} requested.")


def calculate_hash(file_path):
    """Calculate SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()


def test_deep_nested_folder():
    ''' tests whether the archive tool correctly archives 
    and restores 200 folder deep file hierarchies 
    '''

    assert True

def test_ensure_follows_symlinks():
    pass

def test_delete_actually_deletes():
    pass

def test_many_flat_folders():
    ''' tests whether the archive tool correctly archives 
    and restores 10000 subfolder folder
    '''
    assert True

def test_carries_all_file_attributes():
    ''' tests whether the archive tool correctly archives 
    and restores 10000 subfolder folder
    '''
    assert True

def test_parallel_write_race():
    ''' tests whether racing parallel writes can cause data loss '''
    pass

def test_attempt_overwrite():
    ''' tests to block overwriting archives '''
    pass

def test_stress_many_parallel_archive():
    ''' performance test many parallel archivings and retrievals
    '''

def test_stress_many_parallel_retrieve():
    ''' performance test many parallel retrievals
    '''

def test_archive_delete_archive():

    pass

# AI-generated by Qwen3-235B-A22B-Instruct-2507


# Constants
MIN_FILESIZE_BYTES = archive_tool.MIN_FILESIZE_BYTES
MAX_FILENAME_LEN = archive_tool.MAX_FILENAME_LEN
MAX_DEPTH = archive_tool.MAX_DEPTH
MAX_TOTAL_LEN = archive_tool.MAX_TOTAL_LEN

UNSUPPORTED_FILETYPES = ['symlink', 'fifo', 'socket', 'hardlink','noneexistent']
ALLOWED_SIMPLE_CHARS = string.ascii_letters + string.digits + "._-"

def _random_simple_string(length):
    return ''.join(random.choices(ALLOWED_SIMPLE_CHARS, k=length))

def _random_complicated_string(length):
    # Mix of Unicode, shell-meta, control-like, problematic chars
    chars = (string.ascii_letters + string.digits + "._-~!@#$%^&(){}[]\"';`,=?+/\\ ")
    chars += "".join([chr(i) for i in [0x0000, 0xFFFE, 0xFFFF, 0xD800, 0xDFFF]])  # Invalid Unicode
    chars += "éñçô∂∆µΩ中華ßäöü"
    return ''.join(random.choices(chars, k=length))

def _generate_filename(simple, max_length):
    if simple:
        length = random.randint(1, min(16, max_length))
        return _random_simple_string(length)
    else:
        length = random.randint(50, min(200, max_length))
        return _random_complicated_string(length)

def _generate_path(path_prefix, path_complicated, max_path_length, max_depth, violate_depth):
    prefix = Path(path_prefix).resolve()
    parts = []
    remaining = max_path_length - len(str(prefix)) - 1
    path_depth = len(Path(prefix).parents)
    while remaining > 0 and (violate_depth or ( path_depth < max_depth)) :
        part_len = min(random.randint(5, 30), remaining)
        part = _generate_filename(not path_complicated, part_len)
        if len(part) == 0:
            break
        parts.append(part)
        test_path = str(prefix / Path(*parts))
        if len(test_path) > max_path_length:
            parts.pop()
            break
        remaining = max_path_length - len(test_path)
        path_depth = len(Path(test_path).parents)
    return prefix / Path(*parts)

def _write_random_file_iterative(filepath, filesize, chunk_size=64*1024):
    with open(filepath, 'wb') as f:
        while filesize > 0:
            chunk = os.urandom(min(chunk_size, filesize))
            f.write(chunk)
            filesize -= len(chunk)


def get_file_checksum(filepath):
    checksum = hashlib.md5(open(filepath,'rb').read()).hexdigest()
    return checksum

def gen_random_file(
    small_file=False,
    max_filesize=MIN_FILESIZE_BYTES*1.2,  # 10MB default
    max_path_length=MAX_TOTAL_LEN,
    max_path_depth=MAX_DEPTH,
    violate_depth=False,
    invalid_filetypes=False,
    path_prefix=".",
    path_complicated=False,
    fail_on_invalid=True
):
    # Determine file size
    if small_file:
        filesize = random.randint(0, MIN_FILESIZE_BYTES - 1)
    else:
        filesize = random.randint(MIN_FILESIZE_BYTES, min(MIN_FILESIZE_BYTES, max_filesize))  # Cap at 100MB

    # Select filetype
    if invalid_filetypes:
        filetype = random.choice(UNSUPPORTED_FILETYPES)
    else:
        filetype = 'regular'

    # Generate path
    try:
        filepath = _generate_path(path_prefix, path_complicated, max_path_length, max_path_depth, violate_depth)
    except Exception as e:
        if fail_on_invalid:
            raise ValueError(f"Failed to generate path: {e}")
        else:
            return None

    # Ensure parent dirs exist
    filepath.parent.mkdir(parents=True, exist_ok=True)

    try:
        if filetype == 'regular':
            _write_random_file_iterative(filepath, filesize)

        elif filetype == 'symlink':
            target = _generate_path(path_prefix, path_complicated, max_path_length - len(str(filepath)) - 10, max_depth, violate_depth)
            while target.exists():
                target = Path(str(target) + "_target")
            target.write_bytes(_create_file_content(random.randint(0, 1024)))
            filepath.symlink_to(target.relative_to(filepath.parent))

        elif filetype == 'fifo':
            os.mkfifo(filepath)

        elif filetype == 'socket':
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            try:
                sock.bind(str(filepath))
            finally:
                sock.close()

        elif filetype == 'hardlink':
            target = _generate_path(path_prefix, path_complicated, max_path_length - len(str(filepath)) - 10, max_depth, violate_depth)
            while target.exists():
                target = Path(str(target) + "_hard_target")
            target.write_bytes(b"hardlink_target_data")
            os.link(target, filepath)
        elif filetype == 'noneexistent':
            pass

    except (OSError, IOError) as e:
        if fail_on_invalid:
            raise OSError(f"Failed to create {filetype} at {filepath}: {e}")
        else:
            return None

    return filepath

# end AI-generated by Qwen3-235B-A22B-Instruct-2507



def test_archive_retrieve():
    ''' simply test to archive and retrieve a file, check through checksums before and after '''

def test_error_archive_directory_noflag():
    ''' archiving a directory should require a flag, so its explicit '''
    ''' actually should be -r for recursive (all subdirs and subfiles, including hidden) 
        -d for dir only, (fails on files)
        -b for batch mode (allow multiple files)
    '''



@pytest.mark.skip(reason="Feature not implemented yet")
def test_stress_archive_retrieval(tmp_path):
    # Configuration
    tmp_path = Path('tmp')
    NUM_FILES = 1000
    TEST_DIR = tmp_path / "test_files"
    RETRIEVE_DIR = tmp_path / "retrieved"
    TIMINGS_FILE = tmp_path / "dsmc_timings.json"

    TEST_DIR.mkdir()
    RETRIEVE_DIR.mkdir()

    # Generate 1KB random files and store original hashes
    file_paths = []
    original_hashes = {}

    for i in range(NUM_FILES):
        file_path = TEST_DIR / f"file_{i}"
        data = os.urandom(1024)  # 1KB random data
        with open(file_path, "wb") as f:
            f.write(data)
        hash_val = calculate_hash(file_path)
        original_hashes[file_path.name] = hash_val
        file_paths.append(file_path)

    timings = []

    # Archive operation: archive individual files (simulate stress)
    for file_path in file_paths:
        start = time.time()
        try:
            subprocess.run(
                ["python", "archive_tool.py", "archive", str(file_path)],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Archive failed for {file_path}: {e}")
        end = time.time()
        timings.append({
            "operation": "archive",
            "file": file_path.name,
            "duration_sec": end - start
        })

    # Retrieve and verify each file
    for file_path in file_paths:
        retrieve_dest = RETRIEVE_DIR
        start = time.time()
        try:
            subprocess.run(
                ["python", "archive_tool.py", "retrieve", str(file_path), "-d", str(retrieve_dest)],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Retrieve failed for {file_path.name}: {e}")
        end = time.time()
        timings.append({
            "operation": "retrieve",
            "file": file_path.name,
            "duration_sec": end - start
        })

    # Verify checksums of retrieved files
    for i in range(NUM_FILES):
        filename = f"file_{i}"
        retrieved_path = RETRIEVE_DIR / filename

        if not retrieved_path.exists():
            pytest.fail(f"Retrieved file {retrieved_path} does not exist")

        with open(retrieved_path, "rb") as f:
            data = f.read()

        current_hash = hashlib.sha256(data).hexdigest()
        assert current_hash == original_hashes[filename], f"Checksum mismatch for {filename}"

    # Write timing data to JSON
    with open(TIMINGS_FILE, "w") as f:
        json.dump(timings, f)

    print(f"{NUM_FILES} files archived and retrieved successfully")


# test scenarios:

# 1. just archive a lot of objects

# 2. retrieve a single object

# 3. recall a single object

# 4. delete a single object

# 5. list the objects

# 6. combinations of scenarios with 1..N objects


#@pytest.mark.skip(reason="very slow")
def test_full_lifecycle_two_files():
    """ tests the full file lifecycle
    the file can transfer from local to archive,
    migrate back
    archive again
    deleted in archive

    make sure retrieval and listing works as expected
    """

    # use 2 files to test some combinations

    testfile1 = str(gen_random_file())
    testfile2 = str(gen_random_file())
    checksum1 = get_file_checksum(testfile1)
    checksum2 = get_file_checksum(testfile2)
    
    print("ensuring errors on invalid commands for the state where nothing is archived")
    assert Path(testfile1).exists()
    with pytest.raises(SystemExit):
        archive_tool.delete_object(testfile1)
    assert Path(testfile1).exists()
    with pytest.raises(SystemExit):
        archive_tool.retrieve_object(testfile1, Path(tmp_testpath) / 'fullscale_test_retrieve_file1')
    assert Path(testfile1).exists()
    with pytest.raises(SystemExit):
        archive_tool.recall(t, Path(tmp_testpath) / 'fullscale_test_retrieve_file1')
    assert Path(testfile1).exists()

    print("ensuring dryrun is dry")
    archive_tool.archive_objects(testfile1, dry_run=True)
    assert Path(testfile1).exists()
    assert not Path(archive_tool.stubname(testfile1)).exists()

    print('ensuring files were replaced with their stubfiles')
    archive_tool.archive_objects([testfile1, testfile2], dry_run=False)
    assert not Path(testfile1).exists()
    assert Path(archive_tool.stubname(testfile1)).exists()

    print('ensuring archiving is at-most-once')
    with pytest.raises(SystemExit):
        archive_tool.archive_objects([testfile1], dry_run=False)
    with pytest.raises(SystemExit):
        archive_tool.archive_objects([testfile2], dry_run=False)
    with pytest.raises(SystemExit):
        archive_tool.archive_objects([testfile1, testfile2], dry_run=False)


    print('ensuring retrieved correctly')
    dest = Path(tmp_testpath) / 'fullscale_test_retrieve_file1b'
    assert not dest.exists() # test cleanliness check
    archive_tool.retrieve_object(testfile1, dest)
    assert get_file_checksum(dest) == checksum1
    dest.unlink() # cleanup

    dest2 = Path(tmp_testpath) / 'fullscale_test_retrieve_file2b'
    assert not dest2.exists() # test cleanliness check
    archive_tool.retrieve_object(testfile2, dest)
    assert get_file_checksum(dest2) == checksum2
    dest2.unlink() # cleanup

    archive_tool.recall(testfile1)
    assert Path(testfile1).exists()
    assert not Path(archive_tool.stubname(testfile1)).exists()
    assert get_file_checksum(testfile1) == checksum1

    archive_tool.recall(testfile2)
    assert Path(testfile2).exists()
    assert not Path(archive_tool.stubname(testfile2)).exists()
    assert get_file_checksum(testfile2) == checksum2

    print('ensuring archiving again now still works')
    archive_tool.archive_objects([testfile1, testfile2], dry_run=False)
    assert not Path(testfile1).exists()
    assert Path(archive_tool.stubname(testfile1)).exists()

    print('ensuring deletion and also cleanup')
    archive_tool.delete(testfile1)
    archive_tool.delete(testfile2)

    print("ensuring errors on invalid commands for the state where nothing is archived")
    assert Path(testfile1).exists()
    with pytest.raises(SystemExit):
        archive_tool.delete_object(testfile1)
    assert Path(testfile1).exists()
    with pytest.raises(SystemExit):
        archive_tool.retrieve_object(testfile1, Path(tmp_testpath) / 'fullscale_test_retrieve_file1')
    assert Path(testfile1).exists()
    with pytest.raises(SystemExit):
        archive_tool.recall(t, Path(tmp_testpath) / 'fullscale_test_retrieve_file1')
    assert Path(testfile1).exists()



@pytest.mark.skip(reason="very slow")
def test_small_with_spy(spy_dsmc):
    global DSMC_SPY
    archive_tool.list_archived_objects([], ignore_missing=True)
    assert DSMC_SPY[0] == ['dsmc', 'query', 'filespace'], DSMC_SPY
    assert DSMC_SPY[1][:2] == ['dsmc', 'query'], DSMC_SPY
    DSMC_SPY = []
    testfile = str(gen_random_file())
    archive_tool.archive_objects([testfile], False)
    assert DSMC_SPY[0][:2] == ['sha256sum', testfile], DSMC_SPY
    assert DSMC_SPY[1][:2] == ['dsmc', 'archive'], DSMC_SPY
    DSMC_SPY = []
    retrieve_target_filename = _generate_filename(True, MAX_FILENAME_LEN)
    archive_tool.retrieve_object(testfile, retrieve_target_filename)
    assert DSMC_SPY[0][:2] == ['dsmc', 'retrieve'], DSMC_SPY
    DSMC_SPY = []
    archive_tool.recall(testfile)
    assert DSMC_SPY[0][:2] == ['dsmc', 'retrieve'], DSMC_SPY
    DSMC_SPY = []
    archive_tool.delete_object(testfile)
    assert DSMC_SPY[0][:2] == ['dsmc', 'delete'], DSMC_SPY
    DSMC_SPY = []
    archive_tool.print_info()
    assert DSMC_SPY[0][:3] == ['dsmc', 'query', 'systeminfo'], DSMC_SPY
    DSMC_SPY = []

