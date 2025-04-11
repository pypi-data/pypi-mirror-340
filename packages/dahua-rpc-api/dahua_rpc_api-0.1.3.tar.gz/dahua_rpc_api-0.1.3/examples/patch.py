import argparse
from dahua.client import DahuaRpc
from dahua.utils.upgrade import Upgrade


def main(args) -> None:
    dahua = DahuaRpc(host=args.host, port=args.port)

    # Login to the Dahua device
    print(f"Connecting to {args.host}:{args.port}...")
    dahua.login(username=args.username, password=args.password)

    # Start the upgrade process
    upgrader = Upgrade(client=dahua)
    upgrader.upgrade(
        firmware_path=args.firmware_file,
        backup_settings=args.backup,
        backup_path=args.backup_path,
    )

    dahua.logout()
    print("Done.")


if __name__ == "__main__":
    argparse = argparse.ArgumentParser(description="Dahua Firmware Upgrade")
    argparse.add_argument(
        "-f",
        "--firmware-file",
        type=str,
        required=True,
        help="Path to the firmware file",
    )
    argparse.add_argument(
        "-u", "--username", type=str, required=True, help="Username for authentication"
    )
    argparse.add_argument(
        "-p", "--password", type=str, required=True, help="Password for authentication"
    )
    argparse.add_argument(
        "--host", type=str, required=True, help="Host address of the device"
    )
    argparse.add_argument(
        "--port", type=int, default=80, help="Port number of the device"
    )
    argparse.add_argument(
        "--backup", type=bool, default=True, help="Backup settings before upgrade"
    )
    argparse.add_argument(
        "--backup-path",
        type=str,
        default="/tmp/dahua/configFileExport.backup",
        help="Path to save the backup file",
    )

    args = argparse.parse_args()
    main(args)
