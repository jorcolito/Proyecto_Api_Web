import argparse
import time

from fastapi_cloud_cli.utils.api import APIClient


def complete_upload(deployment_id: str, attempts: int, delay: int) -> bool:
    with APIClient() as client:
        for attempt in range(1, attempts + 1):
            try:
                response = client.post(
                    f"/deployments/{deployment_id}/upload-complete"
                )
                print(f"attempt={attempt} status={response.status_code}")
                if response.is_success:
                    return True
            except Exception as error:
                print(f"attempt={attempt} error={type(error).__name__}")

            if attempt < attempts:
                time.sleep(min(delay * attempt, 30))

    return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Retry FastAPI Cloud upload completion after a transient 5xx."
    )
    parser.add_argument("deployment_id")
    parser.add_argument("--attempts", type=int, default=10)
    parser.add_argument("--delay", type=int, default=3)
    args = parser.parse_args()

    if not complete_upload(args.deployment_id, args.attempts, args.delay):
        raise SystemExit(1)

    print("UPLOAD_COMPLETE_OK")


if __name__ == "__main__":
    main()
