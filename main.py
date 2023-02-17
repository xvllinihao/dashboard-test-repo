from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import argparse

if __name__ == '__main__':
    print("hello world")
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--branch', type=str)
    parser.add_argument('--sha', type=str)
    parser.add_argument('--account_url', type=str)

    args = parser.parse_args()

    azure_access_token = DefaultAzureCredential()
    account_url = args.account_url

    blob_service_client = BlobServiceClient(
        account_url, azure_access_token
    )

    branch_name = args.branch.replace("_", "-")
    baseline_container_name = f"test-baseline-{branch_name}-linux"
    test_container_name = f"test-{args.branch}-{args.sha[0:7]}-linux"

    print(f"this is the {args.branch} branch")
    print("baseline-container-name: ", baseline_container_name)
    print("test-container-name: ", test_container_name)

    container_list = list(blob_service_client.list_containers())
    existing_container = set()
    for c in container_list:
        existing_container.add(c.name)

    if baseline_container_name not in existing_container:
        baseline_container_client = blob_service_client.create_container(
            baseline_container_name
        )
    else:
        baseline_container_client = blob_service_client.get_container_client(
            baseline_container_name
        )

    if test_container_name not in existing_container:
        test_container_client = blob_service_client.create_container(
            test_container_name
        )
    else:
        test_container_client = blob_service_client.get_container_client(
            test_container_name
        )

    test_img_name = "tudelft_logo"
    test_img_path = "test-img.png"

    baseline_img_name = "tudelft_logo"
    baseline_img_path = "baseline.png"

    test_blob_client = blob_service_client.get_blob_client(
        test_container_name, test_img_name
    )
    with open(test_img_path, "rb") as img:
        test_blob_client.upload_blob(img, overwrite=True)

    baseline_blob_client = blob_service_client.get_blob_client(
        baseline_container_name, baseline_img_name
    )
    with open(baseline_img_path, "rb") as img:
        baseline_blob_client.upload_blob(img, overwrite=True)