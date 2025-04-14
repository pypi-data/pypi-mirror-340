import requests

from ..executionhelpers import complete_exec
from ..offlineexecution import upload_files_or_folder_for_exec
from ..triggertest_helpers import update_execution_start_time
from ...datamanagement.datasethelpers import get_ds_ids_by_name


def create_workflow_version(miqa_server, workflow_id, version_name, api_key):
    """
    Create a new manual-upload version for the specified workflow

    :param str miqa_server: Miqa server e.g. yourco.miqa.io
    :param int workflow_id: Miqa implemented workflow ID
    :param str version_name: Name for new version
    :param str api_key: API key

    :return: New workflow version ID
    :rtype: int
    """
    create_version_url = f"https://{miqa_server}/api/create_uploadable_version?pskel_id={workflow_id}&version_name={version_name}"
    headers = {
        "accept": "application/json",
        "app_key": api_key
    }
    create_version_response = requests.get(create_version_url, headers=headers)
    if create_version_response.status_code == 200:
        create_version_response = create_version_response.json()
        wfv_id = create_version_response.get("workflowversion_id")
        return wfv_id
    else:
        raise Exception(f"Unable to create workflow version with name '{version_name}' for {workflow_id}: received an error response from the endpoint. Response: {create_version_response.text}")


def create_execution(miqa_server, workflowversion_id, dataset_id, org_config_id, api_key):
    """
    Create a new execution for the specified dataset on the specified workflow version

    :param str miqa_server: Miqa server e.g. yourco.miqa.io
    :param int workflowversion_id: Miqa workflow version ID
    :param int dataset_id: Miqa dataset ID
    :param int org_config_id: Miqa organization configuration ID
    :param str api_key: API key

    :return: New execution ID
    :rtype: int
    """
    create_execution_url = f"https://{miqa_server}/api/workflowversion/{workflowversion_id}/execute_on_dataset/{dataset_id}?org_config_id={org_config_id}"
    headers = {
        "accept": "application/json",
        "app_key": api_key
    }
    create_execution_response = requests.get(create_execution_url, headers=headers)
    if create_execution_response.status_code == 200:
        create_execution_response = create_execution_response.json()
        exec_id = create_execution_response.get("exec_id")
        return exec_id
    else:
        raise Exception(f"Unable to create execution for {dataset_id} on {workflowversion_id}: received an error response from the endpoint at {create_execution_url}. Response: {create_execution_response.text}")


def create_and_upload_to_new_version_for_ds(miqa_server, version_name, dataset_name, pipeline_id, workflow_id, org_config_id, api_key, directory_containing_outputs, raise_on_fail=False, filepattern_end=None, filepattern_start=None, exclude_filepattern_end=None, max_filesize=None, max_connections=None, filepatterns=None, quiet=True, per_request_timeout=None, parallel_file_upload=True, detailed_file_logs=False):
    """
      Create and execute a new version for an existing dataset, retrieved by name

      :param str miqa_server: Miqa server e.g. yourco.miqa.io
      :param str version_name: Name for new version
      :param str dataset_name: Name for new dataset
      :param int pipeline_id: Miqa pipeline ID to add the datasets to
      :param int workflow_id: Miqa implemented workflow ID for the new version
      :param int org_config_id: Miqa organization configuration ID
      :param str api_key: API key
      :param str directory_containing_outputs: Folder containing files to upload (Optional)
      :param bool raise_on_fail: Whether to raise an exception if the file upload fails. Default: False, i.e. the execution will be failed but an exception won't be raised (Optiona)
      :param str filepattern_end: Pattern to match in the file suffix, e.g. '.bam' (Optional)
      :param str filepattern_start: Pattern to match in the file prefix, e.g. 'Analysis/' (Optional)
      :param str exclude_filepattern_end: Pattern to exclude in the file suffix, e.g. '.bam' (Optional)
      :param str api_key: API key, if required by your Miqa instance (Optional)
      :param int max_connections: Maximum number of connections for parallel upload (Optional)
      :param int max_filesize: Maximum filesize to upload, i.e. if avoiding very large files (Optional)
      :param filepatterns: List of regex strings representing file patterns to match, e.g. ['*.csv','*.vcf'] (Optional)
      :param bool quiet: Whether to skip logging. Default True. (Optional)
      :param int per_request_timeout: Timeout for individual requests made during uploading. Default None. (Optional)
      :param int parallel_file_upload: Whether to allow uploads of each file to proceed in parallel. Default True. (Optional)
      :param bool detailed_file_logs: If not in quiet mode, whether to show detailed logs of each file uploaded. Default False. (Optional)

    """
    exec_id = create_and_execute_for_new_version_for_ds(miqa_server, version_name, dataset_name, pipeline_id, workflow_id, org_config_id, api_key)
    upload_and_complete_execution(miqa_server, exec_id, api_key, directory_containing_outputs, raise_on_fail=raise_on_fail, filepattern_end=filepattern_end, filepattern_start=filepattern_start, exclude_filepattern_end=exclude_filepattern_end, max_filesize=max_filesize, max_connections=max_connections, filepatterns=filepatterns, quiet=quiet, per_request_timeout=per_request_timeout, parallel_file_upload=parallel_file_upload, detailed_file_logs=detailed_file_logs)
    return exec_id


def upload_and_complete_execution(miqa_server, exec_id, api_key, directory_containing_outputs, raise_on_fail=False, filepattern_end=None, filepattern_start=None, exclude_filepattern_end=None, max_filesize=None, max_connections=None, filepatterns=None, quiet=True, per_request_timeout=None, parallel_file_upload=True, detailed_file_logs=False):
    """
      Uploads the test output files for each specified dataset, from the specified filepath to the corresponding Miqa execution, and then marks that execution as complete.

      :param int exec_id: Miqa execution ID
      :param str miqa_server: Miqa server e.g. yourco.miqa.io
      :param str directory_containing_outputs: Folder containing files to upload (Optional)
      :param bool raise_on_fail: Whether to raise an exception if the file upload fails. Default: False, i.e. the execution will be failed but an exception won't be raised (Optiona)
      :param str filepattern_end: Pattern to match in the file suffix, e.g. '.bam' (Optional)
      :param str filepattern_start: Pattern to match in the file prefix, e.g. 'Analysis/' (Optional)
      :param str exclude_filepattern_end: Pattern to exclude in the file suffix, e.g. '.bam' (Optional)
      :param str api_key: API key, if required by your Miqa instance (Optional)
      :param int max_connections: Maximum number of connections for parallel upload (Optional)
      :param int max_filesize: Maximum filesize to upload, i.e. if avoiding very large files (Optional)
      :param filepatterns: List of regex strings representing file patterns to match, e.g. ['*.csv','*.vcf'] (Optional)
      :param bool quiet: Whether to skip logging. Default True. (Optional)
      :param int per_request_timeout: Timeout for individual requests made during uploading. Default None. (Optional)
      :param int parallel_file_upload: Whether to allow uploads of each file to proceed in parallel. Default True. (Optional)
      :param bool detailed_file_logs: If not in quiet mode, whether to show detailed logs of each file uploaded. Default False. (Optional)
       """
    update_execution_start_time(miqa_server, exec_id, api_key=api_key, quiet=quiet)
    failed = False
    try:
        upload_files_or_folder_for_exec(exec_id, miqa_server, directory_containing_outputs, args_files=None,
                                        filepattern_end=filepattern_end,
                                        filepattern_start=filepattern_start,
                                        exclude_filepattern_end=exclude_filepattern_end, max_filesize=max_filesize,
                                        api_key=api_key,
                                        max_connections=max_connections, filepatterns=filepatterns, quiet=quiet,
                                        per_request_timeout=per_request_timeout,
                                        parallel_file_upload=parallel_file_upload,
                                        detailed_file_logs=detailed_file_logs)

    except Exception as e2:
        if raise_on_fail:
            raise
        failed = True
        if not quiet:
            print(
                f"Failing execution {exec_id} due to unhandled exception (see below). Will mark execution as failed and continue any remaining samples.")
            print(e2)
            complete_exec(exec_id, miqa_server, quiet=quiet, api_key=api_key, failed=failed)
    complete_exec(exec_id, miqa_server, quiet=quiet, api_key=api_key, failed=failed)


def create_and_execute_for_new_version_for_ds(miqa_server, version_name, dataset_name, pipeline_id, workflow_id, org_config_id, api_key):
    """
      Create and execute a new version for an existing dataset, retrieved by name

      :param str miqa_server: Miqa server e.g. yourco.miqa.io
      :param str version_name: Name for new version
      :param str dataset_name: Name for new dataset
      :param int pipeline_id: Miqa pipeline ID to add the datasets to
      :param int workflow_id: Miqa implemented workflow ID for the new version
      :param int org_config_id: Miqa organization configuration ID
      :param str api_key: API key
    """
    ds_ids_by_name = get_ds_ids_by_name(miqa_server, pipeline_id, api_key)
    ds_id = ds_ids_by_name.get("data",{}).get(dataset_name)
    if not ds_id:
        raise Exception(f"Could not find a dataset by the name '{dataset_name}' for the provided pipeline (id={pipeline_id}). Do you have a typo or the wrong pipeline?")
    wfv_id = create_workflow_version(miqa_server, workflow_id, version_name, api_key)
    exec_id = create_execution(miqa_server, wfv_id, ds_id, org_config_id, api_key)
    return exec_id
