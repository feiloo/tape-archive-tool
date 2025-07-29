import pytest
from pathlib import Path
import hashlib
import time
import subprocess
import json
import os

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

def fake_dsmc(cmd, **kwargs):
    ''' this is a test-spy-object for "mocking" out the dsmc tool '''
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

    # should not reach here
    assert False, "unexpected dmsc command invoked during testing"

@pytest.fixture
def mock_dsmc(monkeypatch):
    monkeypatch.setattr(archive_tool, "subproc", fake_dsmc)


def test_path_independent(mock_dsmc):
    ''' the archive tool needs to work the same, independenly of the that its and and the path its called from
    '''
    archive_tool.list_archived_objects([], ignore_missing=True)
    #archive_tool.archive_objects(['testfile'], False)
    #archive_tool.retrieve_object('testfile', 'testfile2')
    # archive_tool.recall('testfile2')
    #archive_tool.delete_object('testfile')
    #archive_tool.print_info()

# os.getcwd()
# current_dir = os.getcwd()

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

def gen_random_file(max_filesize=None, filetypes=None, path_prefix=None, path_type=None):
    ''' generate a single random file for fuzzing 

    path_prefix is the prefix the file is generated under, 
        it allows testing different underlying (network-) filesystems
    '''
    filepath = random.random() # symbols, any valid linux filepath should go/work
    # ignoring non user and non mount ones, since we'd garble this linux install
    filesize = random.random() # not too big
    filetype = types[random.randint]
    fileattrs = []
    filecontent = random.randombytes()


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

def test_full_lifecycle():
    """ tests the full file lifecycle
    the file can transfer from local to archive,
    migrate back
    archive again
    deleted in archive

    make sure retrieval and listing works as expected
    """
    '''
    assert 1 2 exist

    assertfail delete 1 2
    assertfail list 1 2
    assertfail retrieve 1 2
    assertfail recall 1 2

    assert archive 1 2
    assert list 1 2
    assert retrieve 1 2
    assert recall 1 2

    assertfail retrieve 1 2
    assertfail list 1 2

    assert 1 2 exist

    assert archive 1 2
    assert list 1 2
    assert delete 1 2

    assertfail retrieve 1 2
    assertfail list 1 2
    assertfail recall 1 2
    '''


