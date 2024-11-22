from app.main import PrinterScannerApp

if __name__ == "__main__":
    while True:
        try:
            app = PrinterScannerApp()
            app.run()
        except Exception as e:
            print("application crashed, will restart\n%s" % e)