import requests

from ..adhoc_execution import create_and_upload_to_new_version_for_ds
from ...datamanagement.datasethelpers import create_dataset_and_add_truths, get_ds_ids_by_name


def get_organization_configuration(miqa_server, org_config_id, api_key):
    """
    Create new datasets with reference/truth, and upload results to evaluate accuracy

    :param str miqa_server: Miqa server e.g. yourco.miqa.io
    :param int org_config_id: Miqa organization configuration ID
    :param str api_key: API key
    """

    url = f"https://{miqa_server}/api/organization_configuration/{org_config_id}"
    headers = {
        "accept": "application/json",
        "app_key": api_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Unable to get organization configuration information. Response: {response.text}")


def get_implemented_workflow_info(miqa_server, workflow_id, api_key):
    """
    Create new datasets with reference/truth, and upload results to evaluate accuracy

    :param str miqa_server: Miqa server e.g. yourco.miqa.io
    :param int workflow_id: Miqa implemented workflow ID
    :param str api_key: API key
    """
    url = f"https://{miqa_server}/api/implemented_workflow/{workflow_id}"
    headers = {
        "accept": "application/json",
        "app_key": api_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Unable to get implemented workflow information. Response: {response.text}")


def verify_no_ds_with_name(miqa_server, pipeline_id, dataset_name, api_key):
    ds_ids_by_name = get_ds_ids_by_name(miqa_server, pipeline_id, api_key)
    ds_id = ds_ids_by_name.get("data",{}).get(dataset_name)
    if ds_id:
        raise Exception(f"Already found a dataset with name '{dataset_name}' for the provided pipeline (id={pipeline_id}). Please provide a unique name.")


def create_dataset_with_truths_and_check_results(miqa_server, org_config_id, workflow_id, dataset_name, truth_file_path, version_name, directory_containing_outputs, api_key, tags=None, recall_threshold=0.9, precision_threshold=0.9, raise_on_fail=False, filepattern_end=None, filepattern_start=None, exclude_filepattern_end=None, max_filesize=None, max_connections=None, filepatterns=None, quiet=True, per_request_timeout=None, parallel_file_upload=True, detailed_file_logs=False):
    """
    Create new datasets with reference/truth, and upload results to evaluate accuracy

    :param str miqa_server: Miqa server e.g. yourco.miqa.io
    :param int org_config_id: Miqa organization configuration ID
    :param int workflow_id: Miqa implemented workflow ID
    :param str dataset_name: Name for new dataset
    :param version_name: Name representing the version that was being tested/generated the outputs being uploaded, e.g. a commit ID ('abc123') or version number ('v1.2.3')
    :param str truth_file_path: Filepath pointing to the truth TSV file. Should be a tab-delimited file with columns and headers corresponding to your pipeline's truth type, e.g. "chr   pos ref alt"
    :param str api_key: API key
    :param list tags: Tags to use for the dataset (optional)
    :param str directory_containing_outputs: Folder containing files to upload (Optional)
    :param str filepattern_end: Pattern to match in the file suffix, e.g. '.bam' (Optional)
    :param str filepattern_start: Pattern to match in the file prefix, e.g. 'Analysis/' (Optional)
    :param str exclude_filepattern_end: Pattern to exclude in the file suffix, e.g. '.bam' (Optional)
    :param int max_connections: Maximum number of connections for parallel upload (Optional)
    :param int max_filesize: Maximum filesize to upload, i.e. if avoiding very large files (Optional)
    :param filepatterns: List of regex strings representing file patterns to match, e.g. ['*.csv','*.vcf'] (Optional)
    :param bool quiet: Whether to skip logging. Default True. (Optional)
    :param int per_request_timeout: Timeout for individual requests made during uploading. Default None. (Optional)
    :param bool parallel_file_upload: Whether to allow uploads of each file to proceed in parallel. Default True. (Optional)
    :param bool detailed_file_logs: If not in quiet mode, whether to show detailed logs of each file uploaded. Default False. (Optional)

    :return: Test result response json
    :rtype: Response
    """
    # Can we get pipeline for workflow?
    # Can we get org for workflow?
    implemented_workflow_info = get_implemented_workflow_info(miqa_server, workflow_id, api_key)
    pipeline_id = implemented_workflow_info.get("pipeline_id")
    org_config_info = get_organization_configuration(miqa_server, org_config_id, api_key)
    org_id = org_config_info.get("organization_id")

    verify_no_ds_with_name(miqa_server, pipeline_id, dataset_name, api_key)

    ds_id = create_dataset_and_add_truths(miqa_server, org_id, pipeline_id, dataset_name, truth_file_path, api_key, tags=tags)
    return check_results_for_dataset_with_truths(miqa_server, org_config_id, workflow_id, dataset_name, version_name, directory_containing_outputs, api_key, recall_threshold=recall_threshold, precision_threshold=precision_threshold, raise_on_fail=raise_on_fail, filepattern_end=filepattern_end, filepattern_start=filepattern_start, exclude_filepattern_end=exclude_filepattern_end, max_filesize=max_filesize, max_connections=max_connections, filepatterns=filepatterns, quiet=quiet, per_request_timeout=per_request_timeout, parallel_file_upload=parallel_file_upload, detailed_file_logs=detailed_file_logs)


def check_results_for_dataset_with_truths(miqa_server, org_config_id, workflow_id, dataset_name, version_name, directory_containing_outputs, api_key, recall_threshold=0.9, precision_threshold=0.9, raise_on_fail=False, filepattern_end=None, filepattern_start=None, exclude_filepattern_end=None, max_filesize=None, max_connections=None, filepatterns=None, quiet=True, per_request_timeout=None, parallel_file_upload=True, detailed_file_logs=False):
    """
       Upload results to evaluate accuracy on dataset with existing truth info

       :param str miqa_server: Miqa server e.g. yourco.miqa.io
       :param int org_config_id: Miqa organization configuration ID
       :param int workflow_id: Miqa implemented workflow ID
       :param str dataset_name: Name for new dataset
       :param version_name: Name representing the version that was being tested/generated the outputs being uploaded, e.g. a commit ID ('abc123') or version number ('v1.2.3')
       :param str api_key: API key
       :param str directory_containing_outputs: Folder containing files to upload (Optional)
       :param str filepattern_end: Pattern to match in the file suffix, e.g. '.bam' (Optional)
       :param str filepattern_start: Pattern to match in the file prefix, e.g. 'Analysis/' (Optional)
       :param str exclude_filepattern_end: Pattern to exclude in the file suffix, e.g. '.bam' (Optional)
       :param int max_connections: Maximum number of connections for parallel upload (Optional)
       :param int max_filesize: Maximum filesize to upload, i.e. if avoiding very large files (Optional)
       :param filepatterns: List of regex strings representing file patterns to match, e.g. ['*.csv','*.vcf'] (Optional)
       :param bool quiet: Whether to skip logging. Default True. (Optional)
       :param int per_request_timeout: Timeout for individual requests made during uploading. Default None. (Optional)
       :param bool parallel_file_upload: Whether to allow uploads of each file to proceed in parallel. Default True. (Optional)
       :param bool detailed_file_logs: If not in quiet mode, whether to show detailed logs of each file uploaded. Default False. (Optional)

       :return: Test result response json
       :rtype: Response
    """
    implemented_workflow_info = get_implemented_workflow_info(miqa_server, workflow_id, api_key)
    pipeline_id = implemented_workflow_info.get("pipeline_id")
    default_org_id = 1
    exec_id = create_and_upload_to_new_version_for_ds(miqa_server, version_name, dataset_name, pipeline_id, workflow_id,
                                                      org_config_id if org_config_id else default_org_id, api_key,
                                                      directory_containing_outputs, raise_on_fail=raise_on_fail,
                                                      filepattern_end=filepattern_end,
                                                      filepattern_start=filepattern_start,
                                                      exclude_filepattern_end=exclude_filepattern_end,
                                                      max_filesize=max_filesize, max_connections=max_connections,
                                                      filepatterns=filepatterns, quiet=quiet,
                                                      per_request_timeout=per_request_timeout,
                                                      parallel_file_upload=parallel_file_upload,
                                                      detailed_file_logs=detailed_file_logs)
    assertions_json = get_empty_assertions_json()
    add_assertion_obj(assertions_json, get_standard_assertion("recall", threshold=recall_threshold))
    add_assertion_obj(assertions_json, get_standard_assertion("precision", threshold=precision_threshold))
    test_result = perform_adhoc_test_on_single_exec(miqa_server, exec_id, assertions_json, api_key)
    return test_result


def perform_adhoc_test_on_single_exec(miqa_server, exec_id, assertions_json, api_key, allow_validation_failures=False):
    """
      Evaluate test assertions for a single execution in Miqa.

      :param str miqa_server: Miqa server e.g. yourco.miqa.io
      :param int exec_id: Miqa execution ID
      :param dict assertions_json: Assertions JSON in same format as used for test block assertions
      :param str api_key: API key
      :param bool allow_validation_failures: When checking whether assertion types are valid for single-execution tests, whether to allow the test to proceed (use value True) or raise an exception (use value False). Default: False (Optional)

      :return: Test results (pass/fail) per category and check
      :rtype: dict
    """
    for k,v in assertions_json.get("assertions", {}).items():
        if k in ["concordance", "filecompare"]:
            message = f"Assertions of type {k} are not valid when performing single-execution tests."
            if not allow_validation_failures:
                raise Exception(message + " You may still perform this test by using parameter allow_validation_failures=True.")
            else:
                print(f"WARNING: {message}")
        
    return perform_adhoc_test_on_paired_execs(miqa_server, exec_id, exec_id, assertions_json, api_key)


def perform_adhoc_test_on_paired_execs(miqa_server, baseline_id, test_id, assertions_json, api_key):
    """
      Evaluate test assertions for a pair of executions in Miqa.

      :param str miqa_server: Miqa server e.g. yourco.miqa.io
      :param int baseline_id: Baseline execution IDs
      :param int test_id: Baseline execution IDs
      :param dict assertions_json: Assertions JSON in same format as used for test block assertions
      :param str api_key: API key

      :return: Test results (pass/fail) per category and check
      :rtype: dict
    """
    return perform_adhoc_test(miqa_server, [baseline_id], [test_id], assertions_json, api_key)


def perform_adhoc_test(miqa_server, baseline_ids, test_ids, assertions_json, api_key):
    """
      Evaluate test assertions for a set of baseline and test executions in Miqa.

      :param str miqa_server: Miqa server e.g. yourco.miqa.io
      :param list baseline_ids: Baseline execution IDs
      :param list test_ids: Baseline execution IDs
      :param dict assertions_json: Assertions JSON in same format as used for test block assertions
      :param str api_key: API key

      :return: Test results (pass/fail) per category and check
      :rtype: dict
    """
    url = f"https://{miqa_server}/api/adhoc_test_results?inline=1&exec_ids_baseline={','.join([str(i) for i in baseline_ids])}&exec_ids_test={','.join([str(i) for i in test_ids])}"
    headers = {
        "accept": "application/json",
        "app_key": api_key
    }
    response = requests.post(url, json=assertions_json, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Unable to perform adhoc test: received an error response from the endpoint at {url}. Response: {response.text}")


def get_empty_assertions_json():
    """
      Create an empty assertions json to populate with standard assertions or custom assertions of various categories.
      :return: Empty assertions JSON
      :rtype: dict
    """
    return {"assertions": {}}


def get_standard_assertion(assertion_type, threshold=None):
    """
      Get a standard assertion as a starting point

      :param str assertion_type: Assertion type, one of ['concordance', 'recall', 'precision', 'vcf_filecompare', 'csv_filecompare']
      :param int org_id: Miqa organization ID
      :param int pipeline_id: Miqa pipeline ID to add the datasets to
      :param str dataset_name: Name for new dataset
      :param str api_key: API key
      :param list tags: Tags to use for the dataset (optional)

      :return: Assertion object ({"check":..., "category":...})
      :rtype: dict
    """

    assertion_lookup = {
        "concordance": {"check": {
                    "name": "Result-based concordance w/ Previous",
                    "check_type": "concordance",
                    "failtype": "fail",
                    "versions": [
                        -1
                    ],
                    "threshold": 0 if not threshold else threshold,
                }, "category": "concordance"},
        "recall": {"check": {
                    "name": "Overall recall",
                    "stat": "recall",
                    "check_type": "accuracy",
                    "failtype": "fail",
                    "relationship": "lt",
                    "threshold": 0 if not threshold else threshold,
                    "threshold_type": "percent",
                    "raw_tolerance": 0
                  }, "category": "accuracy"},
        "precision": {"check": {
                    "name": "Overall precision",
                    "stat": "precision",
                    "check_type": "accuracy",
                    "failtype": "fail",
                    "relationship": "lt",
                    "threshold": 0 if not threshold else threshold,
                    "threshold_type": "percent",
                    "raw_tolerance": 0
                  }, "category": "accuracy"},
        "vcf_filecompare": {"check":{
                    "name": "Line-by-line VCF Comparison w/ Previous",
                    "check_type": "filecompare",
                    "failtype": "fail",
                    "min_count": 1,
                    "delimiter": "\t",
                    "pct_diff_threshold": 0,
                    "skiprules": [],
                    "versions": [
                      -1
                    ],
                    "file_rules": {
                      "pattern": ".*vcf$"
                    },
                    "id": "blurb_vcf_1"
      }, "category":"filecompare"},
        "csv_filecompare": {"check":{
                    "name": "Line-by-line CSV Comparison w/ Previous",
                    "check_type": "filecompare",
                    "failtype": "fail",
                    "min_count": 1,
                    "delimiter": ",",
                    "pct_diff_threshold": 0,
                    "skiprules": [],
                    "versions": [
                      -1
                    ],
                    "file_rules": {
                      "pattern": ".*csv$"
                    },
                    "id": "blurb_vcf_1"
      }, "category":"filecompare"}
    }
    return assertion_lookup.get(assertion_type)


def add_assertion_obj(assertions_json, new_assertion_obj):
    """
    Add an assertion to the assertions JSON by passing a check and a category

    :param dict assertions_json: Assertions JSON to add onto
    :param dict new_assertion_obj: A JSON object containing keys {'check': {new_assertion_check...}, 'category':...}
    """
    add_assertion(assertions_json, new_assertion_obj.get('check'), new_assertion_obj.get('category'))


def add_assertion(assertions_json, new_assertion_check, new_assertion_category):
    """
    Add an assertion to the assertions JSON by passing a check and a category

    :param dict assertions_json: Assertions JSON to add onto
    :param dict new_assertion_check: New assertion "check" in JSON form
    :param str new_assertion_category: New assertion category, e.g. 'concordance' or 'accuracy'
    """
    if new_assertion_category not in assertions_json.get("assertions", {}):
        assertions_json["assertions"][new_assertion_category] = {"report":True, "checks": []}
    assertions_json["assertions"][new_assertion_category]["checks"].append(new_assertion_check)