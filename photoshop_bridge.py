from creative_adapters.com_bridge import run_bridge


if __name__ == "__main__":
    raise SystemExit(
        run_bridge(
            app_name="Photoshop",
            default_progid="Photoshop.Application",
            process_name="Photoshop.exe",
            execute_method="DoJavaScript",
        )
    )
