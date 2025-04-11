import subprocess
from pathlib import Path

import pytest

from solidipes.mounters.cloud import get_cloud_info, set_cloud_info
from solidipes.mounters.s3 import S3Mounter
from solidipes.scripts.mount import main as mount_command
from solidipes.scripts.unmount import main as unmount_command

local_path = "data/s3"
remote_path = "test"
endpoint_url = "test_endpoint_url"
bucket_name = "test_bucket_name"
access_key_id = "test_access_key_id"
secret_access_key = "test_secret_access_key"
dtool_endpoint = "s3://test-bucket/1a1f9fad-8589-413e-9602-5bbd66bfe675"


class SubprocessReturn:
    def __init__(self, fail=False):
        self.fail = fail

    def check_returncode(self):
        if self.fail:
            raise subprocess.CalledProcessError(1, "test")


def test_mount_s3fs(study_dir, monkeypatch):
    mount_info = {
        "type": "s3",
        "endpoint_url": endpoint_url,
        "bucket_name": bucket_name,
        "access_key_id": access_key_id,
        "secret_access_key": secret_access_key,
        "remote_dir_name": remote_path,
    }

    # Mount without info
    with pytest.raises(ValueError):
        S3Mounter()

    with pytest.raises(ValueError):
        S3Mounter(path=local_path)

    # Mount with arg info
    # Successful mount
    monkeypatch.setattr("subprocess.run", lambda *args, **kwargs: SubprocessReturn())
    m = S3Mounter(path=local_path, **mount_info)
    # Mount with config info
    m.store_keys_publicly = True
    m.save_config()
    # Successful mount
    S3Mounter(path=local_path)

    # Unsuccessful mount
    monkeypatch.setattr("subprocess.run", lambda *args, **kwargs: SubprocessReturn(fail=True))
    with pytest.raises(RuntimeError):
        S3Mounter(local_path)


def test_mount_command(study_dir, user_path, monkeypatch):
    class Args:
        def __init__(self, **kwargs):
            self.list_existing = False
            self.all = False
            self.force = None
            self.type = "s3"
            self.remote_dir_name = None
            self.convert = None
            self.public_keys = None
            self.__dict__.update(kwargs)

    # Mount without info (print error)
    args = Args(path=local_path, allow_root=False)
    with pytest.raises(ValueError):
        mount_command(args)

    # Mount with arg info (juicefs)
    monkeypatch.setattr("subprocess.run", lambda *args, **kwargs: SubprocessReturn())
    # monkeypatch.setattr("solidipes.utils.cloud.wait_mount", lambda path: None)
    args = Args(
        local_path=local_path,
        type="s3",
        endpoint_url=endpoint_url,
        bucket_name=bucket_name,
        access_key_id=access_key_id,
        secret_access_key=secret_access_key,
        remote_dir_name=remote_path,
        allow_root=False,
    )
    mount_command(args)

    # Mount with saved info
    args = Args(
        local_path=local_path,
        allow_root=False,
    )
    mount_command(args)

    # Convert
    set_cloud_info({})  # Forget previous mount
    Path(local_path).mkdir(parents=True, exist_ok=True)
    Path(local_path, "test").touch()  # Create a file
    args = Args(
        local_path=local_path,
        type="s3",
        endpoint_url=endpoint_url,
        bucket_name=bucket_name,
        access_key_id=access_key_id,
        secret_access_key=secret_access_key,
        remote_dir_name=remote_path,
        convert=True,
        allow_root=False,
    )
    print("conversion of remote mount currently disabled")
    # mount_command(args)
    # assert not Path(local_path, "test").exists()  # File was deleted


def test_unmount_command(study_dir, monkeypatch):
    class Args:
        def __init__(self, **kwargs):
            self.forget = None
            self.local_path = None
            self.list_mounted = None
            self.all = True
            self.__dict__.update(kwargs)

    set_cloud_info({
        local_path: {
            "type": "s3",
            "endpoint_url": endpoint_url,
            "bucket_name": bucket_name,
            "access_key_id": access_key_id,
            "secret_access_key": secret_access_key,
        }
    })

    monkeypatch.setattr("os.path.ismount", lambda *args, **kwargs: True)

    # Fail
    monkeypatch.setattr("subprocess.run", lambda *args, **kwargs: SubprocessReturn(fail=True))
    args = Args()
    unmount_command(args)

    # Successes
    monkeypatch.setattr("subprocess.run", lambda *args, **kwargs: SubprocessReturn())

    # Unmount without info (all saved)
    args = Args()
    unmount_command(args)

    # Unmount with arg info
    args = Args(local_path=local_path)
    unmount_command(args)

    # Forget
    args = Args(forget=True)
    unmount_command(args)
    config = get_cloud_info()
    assert local_path not in config


def check_dtool_credentials():
    import os

    fname = os.path.join(os.path.expanduser("~"), ".config", "dtool", "dtool.json")
    print("dtool_conf: ", fname)
    script_path = os.path.dirname(__file__)
    t_fname = os.path.join(script_path, "assets", "dtool.json")
    if not os.path.exists(fname):
        if "DTOOL_S3_SECRET_ACCESS_KEY" not in os.environ:
            raise RuntimeError("cannot run dtool tests without a tets instance")
        if not os.path.exists(t_fname):
            raise RuntimeError(f"cannot find template dtool conf file {os.getcwd()} {t_fname}")
        os.makedirs(os.path.dirname(fname), exist_ok=True)
        conf = open(t_fname).read().replace("AAAA", os.environ["DTOOL_S3_SECRET_ACCESS_KEY"])
        with open(fname, "w") as f:
            f.write(conf)
    if not os.path.exists(fname):
        raise RuntimeError(f"Could not create the conf file {fname}")
    else:
        os.system(f"cat {fname}")


def test_remote_instance_connection():
    check_dtool_credentials()

    from dtoolcore import DataSet

    dtool_dataset = DataSet.from_uri(dtool_endpoint)
    manifest = dtool_dataset.generate_manifest()
    print(manifest)


def test_dtool_remote_scan(study_dir):
    check_dtool_credentials()
    ret = subprocess.run(
        ["solidipes", "report", "curation", "--remote", dtool_endpoint.replace("s3", "dtool")],
        cwd="./",
    )
    assert ret.returncode == 0


def test_dtool_download(study_dir):
    check_dtool_credentials()
    ret = subprocess.run(
        ["solidipes", "download", "dtool", dtool_endpoint],
        cwd="./",
    )
    assert ret.returncode == 0


def test_dtool_mount(study_dir):
    check_dtool_credentials()
    ret = subprocess.run(
        ["solidipes", "mount", "dtool", dtool_endpoint, "data-dtool"],
        cwd="./",
    )
    assert ret.returncode == 0

    import yaml

    cloud_info = yaml.safe_load(open("data-dtool/cloud_info.yaml", "r").read())
    assert cloud_info["endpoint"] == dtool_endpoint
    assert cloud_info["path"] == "data-dtool"
    assert cloud_info["type"] == "dtool"

    ret = subprocess.run(
        ["solidipes", "report", "curation"],
        capture_output=True,
        cwd="./",
    )

    assert ret.returncode == 0

    output = ret.stderr.decode()
    output = output.split("\n")
    valid = False
    for out in output:
        if "data-dtool/simple_text_file.txt" in out:
            valid = True
            if "OK" not in out:
                valid = False
            break

    print(out)
    assert valid
