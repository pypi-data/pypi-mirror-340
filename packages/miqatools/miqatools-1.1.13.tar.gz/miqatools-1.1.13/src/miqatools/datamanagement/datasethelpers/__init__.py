import requests

from ...utilities import get_json_or_error


def get_ds_ids_by_name(miqa_server, pipeline_id, api_key=None):
    """
      Gets a lookup of dataset names and corresponding IDs for a particular pipeline

      :param miqa_server: Miqa server e.g. yourco.miqa.io
      :param pipeline_id: Miqa pipeline ID to get dataset info for
      :param str api_key: API key, if required by your Miqa instance (Optional)
      :return: A lookup of dataset information
      :rtype: dict
    """
    info = get_ds_ids_by_name_internal(miqa_server, pipeline_id, api_key=api_key)
    return info


def get_ds_ids_by_name_internal(miqa_server, pipeline_id, api_key=None):
    remote_url = f'https://{miqa_server}/api/get_ds_ids_by_name?pipeline_id={pipeline_id}'
    headers = {}
    if api_key:
        headers['app_key'] = api_key
    info = get_json_or_error(remote_url, headers=headers)
    return info


def tag_ds_ids_by_name(miqa_server, pipeline_id, name, tag, api_key=None):
    """
      Tags dataset(s) matching the name provided with the tag provided

      :param miqa_server: Miqa server e.g. yourco.miqa.io
      :param pipeline_id: Miqa pipeline ID to get dataset info for
      :param str name: Dataset name corresponding to the dataset to apply the tag to
      :param str tag: Tag to use for the dataset
      :param str api_key: API key, if required by your Miqa instance (Optional)
      :return: Response from the API call
      :rtype: object
    """
    info = get_ds_ids_by_name_internal(miqa_server, pipeline_id)
    source_ids_lookup = info.get('data',{})
    headers = {}
    if api_key:
        headers['app_key'] = api_key

    if source_ids_lookup and source_ids_lookup.get(name):
        tag_url = f"https://{miqa_server}/api/batch_tag_datasources/{tag}?inline=1&source_ids={source_ids_lookup.get(name)}"
        resp = requests.get(tag_url, headers=headers)
        return resp
    else:
        raise Exception("No matching datasource IDs found")


def tag_ds_ids_by_names(miqa_server, pipeline_id, names, tag, raise_if_names_not_found=False, api_key=None):
    """
      Tags dataset(s) matching the names provided with the tag provided

      :param miqa_server: Miqa server e.g. yourco.miqa.io
      :param pipeline_id: Miqa pipeline ID to get dataset info for
      :param list name: Dataset name corresponding to the dataset to apply the tag to
      :param str tag: Tag to use for the dataset
      :param bool raise_if_names_not_found: Whether to raise an exception if no datasets are found matching one of the provided names
      :param str api_key: API key, if required by your Miqa instance (Optional)
      :return: Response from the API call
      :rtype: object
    """
    info = get_ds_ids_by_name_internal(miqa_server, pipeline_id)
    source_ids_lookup = info.get('data',{})
    source_ids_for_names = [source_ids_lookup.get(name) for name in names]
    source_ids_for_names = [str(i) for i in source_ids_for_names if i]

    headers = {}
    if api_key:
        headers['app_key'] = api_key

    if source_ids_for_names and (not raise_if_names_not_found or len(source_ids_for_names) == len(names)):
        tag_url = f"https://{miqa_server}/api/batch_tag_datasources/{tag}?inline=1&source_ids={','.join(source_ids_for_names)}"
        resp = requests.get(tag_url, headers=headers)
        return resp
    else:
        raise Exception("Matching datasource IDs not found")


def batch_create_datasets_and_tag_or_group(miqa_server, org_id, pipeline_id, new_ds_names, tags, dsg_name=None, api_key=None):
    """
      Create stand-in datasets (i.e. no data upload) and tag them

      :param str miqa_server: Miqa server e.g. yourco.miqa.io
      :param int org_id: Miqa organization ID
      :param int pipeline_id: Miqa pipeline ID to add the datasets to
      :param list new_ds_names: Names for new datasets
      :param list tags: Tags to use for the dataset
      :param str dsg_name: Name to use to create a dataset group, if wanting to create a group (Optional)
      :param str api_key: API key, if required by your Miqa instance (Optional)
      :return: Response from the API call
      :rtype: Response
    """
    tag_url = f"https://{miqa_server}/api/batch_create_dataset_and_tag?org_id={org_id}&pipeline_id={pipeline_id}&names={','.join(new_ds_names)}"

    if tags:
        tag_url += f"&tags={','.join(tags)}"
    if dsg_name:
        tag_url += f"&create_dsg={dsg_name}"

    headers = {}
    if api_key:
        headers['app_key'] = api_key

    resp = requests.get(tag_url, headers=headers)
    return resp


def add_truths_to_dataset(miqa_server, dataset_id, pipeline_id, truth_file_path, api_key):
    """
      Create a single stand-in dataset (i.e. no data upload) and optionally tag it

      :param str miqa_server: Miqa server e.g. yourco.miqa.io
      :param int dataset_id: Miqa dataset ID to add the truths to
      :param int pipeline_id: Miqa pipeline ID corresponding to the dataset and truth type
      :param str truth_file_path: Filepath pointing to the truth TSV file. Should be a tab-delimited file with columns and headers corresponding to your pipeline's truth type, e.g. "chr   pos ref alt"
      :param str api_key: API key
    """
    headers = {
        "accept": "application/json",
        "app_key": api_key
    }
    upload_truths_url = f"https://{miqa_server}/api/datasource/{dataset_id}/upload_truths?pipeline_id={pipeline_id}&inline=1"
    response = requests.post(upload_truths_url, files={'file': open(truth_file_path, 'rb')}, data={}, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Unable to add truths to dataset {dataset_id}: received an error response from the server at url {upload_truths_url}. Response: {response.text}")
    return response


def create_dataset_with_name(miqa_server, org_id, pipeline_id, dataset_name, api_key, tags=None):
    """
      Create a single stand-in dataset (i.e. no data upload) and optionally tag it

      :param str miqa_server: Miqa server e.g. yourco.miqa.io
      :param int org_id: Miqa organization ID
      :param int pipeline_id: Miqa pipeline ID to add the datasets to
      :param str dataset_name: Name for new dataset
      :param str api_key: API key
      :param list tags: Tags to use for the dataset (optional)

      :return: New Dataset ID
      :rtype: int
    """
    create_ds_response = batch_create_datasets_and_tag_or_group(miqa_server, org_id, pipeline_id,
                                                                new_ds_names=[dataset_name],
                                                                tags=tags if tags else [], api_key=api_key)  # Add tags if desired
    if create_ds_response.status_code == 200:
        create_ds_response = create_ds_response.json()
        ds_id_lookup = create_ds_response.get("data")
        ds_id = ds_id_lookup.get(dataset_name)
        return ds_id
    else:
        raise Exception(f"Unable to create dataset with name '{dataset_name}': received an error response from the endpoint. Response: {create_ds_response.text}")


def create_dataset_and_add_truths(miqa_server, org_id, pipeline_id, dataset_name, truth_file_path, api_key, tags=None):
    """
      Create a single stand-in dataset (i.e. no input file upload), add truth data, and optionally tag it

      :param str miqa_server: Miqa server e.g. yourco.miqa.io
      :param int org_id: Miqa organization ID
      :param int pipeline_id: Miqa pipeline ID corresponding to the dataset and truth type
      :param str dataset_name: Name for new dataset
      :param str truth_file_path: Filepath pointing to the truth TSV file. Should be a tab-delimited file with columns and headers corresponding to your pipeline's truth type, e.g. "chr   pos ref alt"
      :param str api_key: API key
      :param list tags: Tags to use for the dataset (optional)

      :return: New Dataset ID
      :rtype: int
    """
    dataset_id = create_dataset_with_name(miqa_server, org_id, pipeline_id, dataset_name, api_key, tags=tags)
    add_truths_to_dataset(miqa_server, dataset_id, pipeline_id, truth_file_path, api_key)
    return dataset_id
