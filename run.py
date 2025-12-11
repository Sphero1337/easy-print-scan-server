import argparse

from app.main import PrinterScannerApp


def parse_args():
    parser = argparse.ArgumentParser(
        description="Easy Print & Scan server",
    )
    parser.add_argument(
        "--printer",
        help="Printer name to use (overrides printing.default_printer)",
    )
    parser.add_argument(
        "--scanner",
        help=(
            "Scanner identifier: SANE device name on Unix "
            "or numeric device index on Windows (overrides scanning settings)"
        ),
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    while True:
        try:
            app = PrinterScannerApp(printer=args.printer, scanner=args.scanner)
            app.run()
        except Exception as e:
            print("application crashed, will restart\n%s" % e)