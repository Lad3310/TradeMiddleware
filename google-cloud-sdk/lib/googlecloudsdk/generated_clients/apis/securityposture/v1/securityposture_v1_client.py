"""Generated client library for securityposture version v1."""
# NOTE: This file is autogenerated and should not be edited by hand.

from __future__ import absolute_import

from apitools.base.py import base_api
from googlecloudsdk.generated_clients.apis.securityposture.v1 import securityposture_v1_messages as messages


class SecuritypostureV1(base_api.BaseApiClient):
  """Generated client library for service securityposture version v1."""

  MESSAGES_MODULE = messages
  BASE_URL = 'https://securityposture.googleapis.com/'
  MTLS_BASE_URL = 'https://securityposture.mtls.googleapis.com/'

  _PACKAGE = 'securityposture'
  _SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
  _VERSION = 'v1'
  _CLIENT_ID = 'CLIENT_ID'
  _CLIENT_SECRET = 'CLIENT_SECRET'
  _USER_AGENT = 'google-cloud-sdk'
  _CLIENT_CLASS_NAME = 'SecuritypostureV1'
  _URL_VERSION = 'v1'
  _API_KEY = None

  def __init__(self, url='', credentials=None,
               get_credentials=True, http=None, model=None,
               log_request=False, log_response=False,
               credentials_args=None, default_global_params=None,
               additional_http_headers=None, response_encoding=None):
    """Create a new securityposture handle."""
    url = url or self.BASE_URL
    super(SecuritypostureV1, self).__init__(
        url, credentials=credentials,
        get_credentials=get_credentials, http=http, model=model,
        log_request=log_request, log_response=log_response,
        credentials_args=credentials_args,
        default_global_params=default_global_params,
        additional_http_headers=additional_http_headers,
        response_encoding=response_encoding)
    self.organizations_locations_operations = self.OrganizationsLocationsOperationsService(self)
    self.organizations_locations_postureDeployments = self.OrganizationsLocationsPostureDeploymentsService(self)
    self.organizations_locations_postureTemplates = self.OrganizationsLocationsPostureTemplatesService(self)
    self.organizations_locations_postures = self.OrganizationsLocationsPosturesService(self)
    self.organizations_locations_predictions = self.OrganizationsLocationsPredictionsService(self)
    self.organizations_locations_reports = self.OrganizationsLocationsReportsService(self)
    self.organizations_locations = self.OrganizationsLocationsService(self)
    self.organizations = self.OrganizationsService(self)
    self.projects_locations = self.ProjectsLocationsService(self)
    self.projects = self.ProjectsService(self)

  class OrganizationsLocationsOperationsService(base_api.BaseApiService):
    """Service class for the organizations_locations_operations resource."""

    _NAME = 'organizations_locations_operations'

    def __init__(self, client):
      super(SecuritypostureV1.OrganizationsLocationsOperationsService, self).__init__(client)
      self._upload_configs = {
          }

    def Cancel(self, request, global_params=None):
      r"""Starts asynchronous cancellation on a long-running operation. The server makes a best effort to cancel the operation, but success is not guaranteed. If the server doesn't support this method, it returns `google.rpc.Code.UNIMPLEMENTED`. Clients can use Operations.GetOperation or other methods to check whether the cancellation succeeded or whether the operation completed despite cancellation. On successful cancellation, the operation is not deleted; instead, it becomes an operation with an Operation.error value with a google.rpc.Status.code of 1, corresponding to `Code.CANCELLED`.

      Args:
        request: (SecuritypostureOrganizationsLocationsOperationsCancelRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Empty) The response message.
      """
      config = self.GetMethodConfig('Cancel')
      return self._RunMethod(
          config, request, global_params=global_params)

    Cancel.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/organizations/{organizationsId}/locations/{locationsId}/operations/{operationsId}:cancel',
        http_method='POST',
        method_id='securityposture.organizations.locations.operations.cancel',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1/{+name}:cancel',
        request_field='cancelOperationRequest',
        request_type_name='SecuritypostureOrganizationsLocationsOperationsCancelRequest',
        response_type_name='Empty',
        supports_download=False,
    )

    def Delete(self, request, global_params=None):
      r"""Deletes a long-running operation. This method indicates that the client is no longer interested in the operation result. It does not cancel the operation. If the server doesn't support this method, it returns `google.rpc.Code.UNIMPLEMENTED`.

      Args:
        request: (SecuritypostureOrganizationsLocationsOperationsDeleteRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Empty) The response message.
      """
      config = self.GetMethodConfig('Delete')
      return self._RunMethod(
          config, request, global_params=global_params)

    Delete.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/organizations/{organizationsId}/locations/{locationsId}/operations/{operationsId}',
        http_method='DELETE',
        method_id='securityposture.organizations.locations.operations.delete',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1/{+name}',
        request_field='',
        request_type_name='SecuritypostureOrganizationsLocationsOperationsDeleteRequest',
        response_type_name='Empty',
        supports_download=False,
    )

    def Get(self, request, global_params=None):
      r"""Gets the latest state of a long-running operation. Clients can use this method to poll the operation result at intervals as recommended by the API service.

      Args:
        request: (SecuritypostureOrganizationsLocationsOperationsGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/organizations/{organizationsId}/locations/{locationsId}/operations/{operationsId}',
        http_method='GET',
        method_id='securityposture.organizations.locations.operations.get',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1/{+name}',
        request_field='',
        request_type_name='SecuritypostureOrganizationsLocationsOperationsGetRequest',
        response_type_name='Operation',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""Lists operations that match the specified filter in the request. If the server doesn't support this method, it returns `UNIMPLEMENTED`.

      Args:
        request: (SecuritypostureOrganizationsLocationsOperationsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListOperationsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/organizations/{organizationsId}/locations/{locationsId}/operations',
        http_method='GET',
        method_id='securityposture.organizations.locations.operations.list',
        ordered_params=['name'],
        path_params=['name'],
        query_params=['filter', 'pageSize', 'pageToken'],
        relative_path='v1/{+name}/operations',
        request_field='',
        request_type_name='SecuritypostureOrganizationsLocationsOperationsListRequest',
        response_type_name='ListOperationsResponse',
        supports_download=False,
    )

  class OrganizationsLocationsPostureDeploymentsService(base_api.BaseApiService):
    """Service class for the organizations_locations_postureDeployments resource."""

    _NAME = 'organizations_locations_postureDeployments'

    def __init__(self, client):
      super(SecuritypostureV1.OrganizationsLocationsPostureDeploymentsService, self).__init__(client)
      self._upload_configs = {
          }

    def Create(self, request, global_params=None):
      r"""Creates a new PostureDeployment in a given project and location.

      Args:
        request: (SecuritypostureOrganizationsLocationsPostureDeploymentsCreateRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Create')
      return self._RunMethod(
          config, request, global_params=global_params)

    Create.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/organizations/{organizationsId}/locations/{locationsId}/postureDeployments',
        http_method='POST',
        method_id='securityposture.organizations.locations.postureDeployments.create',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=['postureDeploymentId'],
        relative_path='v1/{+parent}/postureDeployments',
        request_field='postureDeployment',
        request_type_name='SecuritypostureOrganizationsLocationsPostureDeploymentsCreateRequest',
        response_type_name='Operation',
        supports_download=False,
    )

    def Delete(self, request, global_params=None):
      r"""Deletes a PostureDeployment.

      Args:
        request: (SecuritypostureOrganizationsLocationsPostureDeploymentsDeleteRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Delete')
      return self._RunMethod(
          config, request, global_params=global_params)

    Delete.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/organizations/{organizationsId}/locations/{locationsId}/postureDeployments/{postureDeploymentsId}',
        http_method='DELETE',
        method_id='securityposture.organizations.locations.postureDeployments.delete',
        ordered_params=['name'],
        path_params=['name'],
        query_params=['etag'],
        relative_path='v1/{+name}',
        request_field='',
        request_type_name='SecuritypostureOrganizationsLocationsPostureDeploymentsDeleteRequest',
        response_type_name='Operation',
        supports_download=False,
    )

    def Get(self, request, global_params=None):
      r"""Gets details for a PostureDeployment.

      Args:
        request: (SecuritypostureOrganizationsLocationsPostureDeploymentsGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (PostureDeployment) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/organizations/{organizationsId}/locations/{locationsId}/postureDeployments/{postureDeploymentsId}',
        http_method='GET',
        method_id='securityposture.organizations.locations.postureDeployments.get',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1/{+name}',
        request_field='',
        request_type_name='SecuritypostureOrganizationsLocationsPostureDeploymentsGetRequest',
        response_type_name='PostureDeployment',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""Lists every PostureDeployment in a project and location.

      Args:
        request: (SecuritypostureOrganizationsLocationsPostureDeploymentsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListPostureDeploymentsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/organizations/{organizationsId}/locations/{locationsId}/postureDeployments',
        http_method='GET',
        method_id='securityposture.organizations.locations.postureDeployments.list',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=['filter', 'pageSize', 'pageToken'],
        relative_path='v1/{+parent}/postureDeployments',
        request_field='',
        request_type_name='SecuritypostureOrganizationsLocationsPostureDeploymentsListRequest',
        response_type_name='ListPostureDeploymentsResponse',
        supports_download=False,
    )

    def Patch(self, request, global_params=None):
      r"""Updates an existing PostureDeployment. To prevent concurrent updates from overwriting each other, always follow the read-modify-write pattern when you update a posture deployment: 1. Call GetPostureDeployment to get the current version of the deployment. 2. Update the fields in the deployment as needed. 3. Call UpdatePostureDeployment to update the deployment. Ensure that your request includes the `etag` value from the GetPostureDeployment response. **Important:** If you omit the `etag` when you call UpdatePostureDeployment, then the updated deployment unconditionally overwrites the existing deployment.

      Args:
        request: (SecuritypostureOrganizationsLocationsPostureDeploymentsPatchRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Patch')
      return self._RunMethod(
          config, request, global_params=global_params)

    Patch.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/organizations/{organizationsId}/locations/{locationsId}/postureDeployments/{postureDeploymentsId}',
        http_method='PATCH',
        method_id='securityposture.organizations.locations.postureDeployments.patch',
        ordered_params=['name'],
        path_params=['name'],
        query_params=['updateMask'],
        relative_path='v1/{+name}',
        request_field='postureDeployment',
        request_type_name='SecuritypostureOrganizationsLocationsPostureDeploymentsPatchRequest',
        response_type_name='Operation',
        supports_download=False,
    )

  class OrganizationsLocationsPostureTemplatesService(base_api.BaseApiService):
    """Service class for the organizations_locations_postureTemplates resource."""

    _NAME = 'organizations_locations_postureTemplates'

    def __init__(self, client):
      super(SecuritypostureV1.OrganizationsLocationsPostureTemplatesService, self).__init__(client)
      self._upload_configs = {
          }

    def Get(self, request, global_params=None):
      r"""Gets a single revision of a PostureTemplate.

      Args:
        request: (SecuritypostureOrganizationsLocationsPostureTemplatesGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (PostureTemplate) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/organizations/{organizationsId}/locations/{locationsId}/postureTemplates/{postureTemplatesId}',
        http_method='GET',
        method_id='securityposture.organizations.locations.postureTemplates.get',
        ordered_params=['name'],
        path_params=['name'],
        query_params=['revisionId'],
        relative_path='v1/{+name}',
        request_field='',
        request_type_name='SecuritypostureOrganizationsLocationsPostureTemplatesGetRequest',
        response_type_name='PostureTemplate',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""Lists every PostureTemplate in a given organization and location.

      Args:
        request: (SecuritypostureOrganizationsLocationsPostureTemplatesListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListPostureTemplatesResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/organizations/{organizationsId}/locations/{locationsId}/postureTemplates',
        http_method='GET',
        method_id='securityposture.organizations.locations.postureTemplates.list',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=['filter', 'pageSize', 'pageToken'],
        relative_path='v1/{+parent}/postureTemplates',
        request_field='',
        request_type_name='SecuritypostureOrganizationsLocationsPostureTemplatesListRequest',
        response_type_name='ListPostureTemplatesResponse',
        supports_download=False,
    )

  class OrganizationsLocationsPosturesService(base_api.BaseApiService):
    """Service class for the organizations_locations_postures resource."""

    _NAME = 'organizations_locations_postures'

    def __init__(self, client):
      super(SecuritypostureV1.OrganizationsLocationsPosturesService, self).__init__(client)
      self._upload_configs = {
          }

    def Create(self, request, global_params=None):
      r"""Creates a new Posture.

      Args:
        request: (SecuritypostureOrganizationsLocationsPosturesCreateRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Create')
      return self._RunMethod(
          config, request, global_params=global_params)

    Create.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/organizations/{organizationsId}/locations/{locationsId}/postures',
        http_method='POST',
        method_id='securityposture.organizations.locations.postures.create',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=['postureId'],
        relative_path='v1/{+parent}/postures',
        request_field='posture',
        request_type_name='SecuritypostureOrganizationsLocationsPosturesCreateRequest',
        response_type_name='Operation',
        supports_download=False,
    )

    def Delete(self, request, global_params=None):
      r"""Deletes all revisions of a Posture. You can only delete a posture if none of its revisions are deployed.

      Args:
        request: (SecuritypostureOrganizationsLocationsPosturesDeleteRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Delete')
      return self._RunMethod(
          config, request, global_params=global_params)

    Delete.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/organizations/{organizationsId}/locations/{locationsId}/postures/{posturesId}',
        http_method='DELETE',
        method_id='securityposture.organizations.locations.postures.delete',
        ordered_params=['name'],
        path_params=['name'],
        query_params=['etag'],
        relative_path='v1/{+name}',
        request_field='',
        request_type_name='SecuritypostureOrganizationsLocationsPosturesDeleteRequest',
        response_type_name='Operation',
        supports_download=False,
    )

    def Extract(self, request, global_params=None):
      r"""Extracts existing policies from an organization, folder, or project, and applies them to another organization, folder, or project as a Posture. If the other organization, folder, or project already has a posture, then the result of the long-running operation is an ALREADY_EXISTS error.

      Args:
        request: (SecuritypostureOrganizationsLocationsPosturesExtractRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Extract')
      return self._RunMethod(
          config, request, global_params=global_params)

    Extract.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/organizations/{organizationsId}/locations/{locationsId}/postures:extract',
        http_method='POST',
        method_id='securityposture.organizations.locations.postures.extract',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=[],
        relative_path='v1/{+parent}/postures:extract',
        request_field='extractPostureRequest',
        request_type_name='SecuritypostureOrganizationsLocationsPosturesExtractRequest',
        response_type_name='Operation',
        supports_download=False,
    )

    def Get(self, request, global_params=None):
      r"""Gets a single revision of a Posture.

      Args:
        request: (SecuritypostureOrganizationsLocationsPosturesGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Posture) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/organizations/{organizationsId}/locations/{locationsId}/postures/{posturesId}',
        http_method='GET',
        method_id='securityposture.organizations.locations.postures.get',
        ordered_params=['name'],
        path_params=['name'],
        query_params=['revisionId'],
        relative_path='v1/{+name}',
        request_field='',
        request_type_name='SecuritypostureOrganizationsLocationsPosturesGetRequest',
        response_type_name='Posture',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""Lists the most recent revisions of all Posture resources in a specified organization and location.

      Args:
        request: (SecuritypostureOrganizationsLocationsPosturesListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListPosturesResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/organizations/{organizationsId}/locations/{locationsId}/postures',
        http_method='GET',
        method_id='securityposture.organizations.locations.postures.list',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=['filter', 'pageSize', 'pageToken'],
        relative_path='v1/{+parent}/postures',
        request_field='',
        request_type_name='SecuritypostureOrganizationsLocationsPosturesListRequest',
        response_type_name='ListPosturesResponse',
        supports_download=False,
    )

    def ListRevisions(self, request, global_params=None):
      r"""Lists all revisions of a single Posture.

      Args:
        request: (SecuritypostureOrganizationsLocationsPosturesListRevisionsRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListPostureRevisionsResponse) The response message.
      """
      config = self.GetMethodConfig('ListRevisions')
      return self._RunMethod(
          config, request, global_params=global_params)

    ListRevisions.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/organizations/{organizationsId}/locations/{locationsId}/postures/{posturesId}:listRevisions',
        http_method='GET',
        method_id='securityposture.organizations.locations.postures.listRevisions',
        ordered_params=['name'],
        path_params=['name'],
        query_params=['pageSize', 'pageToken'],
        relative_path='v1/{+name}:listRevisions',
        request_field='',
        request_type_name='SecuritypostureOrganizationsLocationsPosturesListRevisionsRequest',
        response_type_name='ListPostureRevisionsResponse',
        supports_download=False,
    )

    def Patch(self, request, global_params=None):
      r"""Updates a revision of an existing Posture. If the posture revision that you update is currently deployed, then a new revision of the posture is created. To prevent concurrent updates from overwriting each other, always follow the read-modify-write pattern when you update a posture: 1. Call GetPosture to get the current version of the posture. 2. Update the fields in the posture as needed. 3. Call UpdatePosture to update the posture. Ensure that your request includes the `etag` value from the GetPosture response. **Important:** If you omit the `etag` when you call UpdatePosture, then the updated posture unconditionally overwrites the existing posture.

      Args:
        request: (SecuritypostureOrganizationsLocationsPosturesPatchRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Patch')
      return self._RunMethod(
          config, request, global_params=global_params)

    Patch.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/organizations/{organizationsId}/locations/{locationsId}/postures/{posturesId}',
        http_method='PATCH',
        method_id='securityposture.organizations.locations.postures.patch',
        ordered_params=['name'],
        path_params=['name'],
        query_params=['revisionId', 'updateMask'],
        relative_path='v1/{+name}',
        request_field='posture',
        request_type_name='SecuritypostureOrganizationsLocationsPosturesPatchRequest',
        response_type_name='Operation',
        supports_download=False,
    )

  class OrganizationsLocationsPredictionsService(base_api.BaseApiService):
    """Service class for the organizations_locations_predictions resource."""

    _NAME = 'organizations_locations_predictions'

    def __init__(self, client):
      super(SecuritypostureV1.OrganizationsLocationsPredictionsService, self).__init__(client)
      self._upload_configs = {
          }

    def CreatePrediction(self, request, global_params=None):
      r"""Creates a AI generated prediction. Used to predict postures based on user provided intent and user's cloud environment.

      Args:
        request: (SecuritypostureOrganizationsLocationsPredictionsCreatePredictionRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('CreatePrediction')
      return self._RunMethod(
          config, request, global_params=global_params)

    CreatePrediction.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/organizations/{organizationsId}/locations/{locationsId}/predictions:CreatePrediction',
        http_method='POST',
        method_id='securityposture.organizations.locations.predictions.createPrediction',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=[],
        relative_path='v1/{+parent}/predictions:CreatePrediction',
        request_field='createPredictionRequest',
        request_type_name='SecuritypostureOrganizationsLocationsPredictionsCreatePredictionRequest',
        response_type_name='Operation',
        supports_download=False,
    )

    def Get(self, request, global_params=None):
      r"""Gets a Prediction in a given organization and location.

      Args:
        request: (SecuritypostureOrganizationsLocationsPredictionsGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Prediction) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/organizations/{organizationsId}/locations/{locationsId}/predictions/{predictionsId}',
        http_method='GET',
        method_id='securityposture.organizations.locations.predictions.get',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1/{+name}',
        request_field='',
        request_type_name='SecuritypostureOrganizationsLocationsPredictionsGetRequest',
        response_type_name='Prediction',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""Lists predictions in a given organization and location.

      Args:
        request: (SecuritypostureOrganizationsLocationsPredictionsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListPredictionsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/organizations/{organizationsId}/locations/{locationsId}/predictions',
        http_method='GET',
        method_id='securityposture.organizations.locations.predictions.list',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=['filter', 'pageSize', 'pageToken'],
        relative_path='v1/{+parent}/predictions',
        request_field='',
        request_type_name='SecuritypostureOrganizationsLocationsPredictionsListRequest',
        response_type_name='ListPredictionsResponse',
        supports_download=False,
    )

  class OrganizationsLocationsReportsService(base_api.BaseApiService):
    """Service class for the organizations_locations_reports resource."""

    _NAME = 'organizations_locations_reports'

    def __init__(self, client):
      super(SecuritypostureV1.OrganizationsLocationsReportsService, self).__init__(client)
      self._upload_configs = {
          }

    def CreateIaCValidationReport(self, request, global_params=None):
      r"""Validates a specified infrastructure-as-code (IaC) configuration, and creates a Report with the validation results. Only Terraform configurations are supported. Only modified assets are validated.

      Args:
        request: (SecuritypostureOrganizationsLocationsReportsCreateIaCValidationReportRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('CreateIaCValidationReport')
      return self._RunMethod(
          config, request, global_params=global_params)

    CreateIaCValidationReport.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/organizations/{organizationsId}/locations/{locationsId}/reports:createIaCValidationReport',
        http_method='POST',
        method_id='securityposture.organizations.locations.reports.createIaCValidationReport',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=[],
        relative_path='v1/{+parent}/reports:createIaCValidationReport',
        request_field='createIaCValidationReportRequest',
        request_type_name='SecuritypostureOrganizationsLocationsReportsCreateIaCValidationReportRequest',
        response_type_name='Operation',
        supports_download=False,
    )

    def Get(self, request, global_params=None):
      r"""Gets details for a Report.

      Args:
        request: (SecuritypostureOrganizationsLocationsReportsGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Report) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/organizations/{organizationsId}/locations/{locationsId}/reports/{reportsId}',
        http_method='GET',
        method_id='securityposture.organizations.locations.reports.get',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1/{+name}',
        request_field='',
        request_type_name='SecuritypostureOrganizationsLocationsReportsGetRequest',
        response_type_name='Report',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""Lists every Report in a given organization and location.

      Args:
        request: (SecuritypostureOrganizationsLocationsReportsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListReportsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/organizations/{organizationsId}/locations/{locationsId}/reports',
        http_method='GET',
        method_id='securityposture.organizations.locations.reports.list',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=['filter', 'pageSize', 'pageToken'],
        relative_path='v1/{+parent}/reports',
        request_field='',
        request_type_name='SecuritypostureOrganizationsLocationsReportsListRequest',
        response_type_name='ListReportsResponse',
        supports_download=False,
    )

  class OrganizationsLocationsService(base_api.BaseApiService):
    """Service class for the organizations_locations resource."""

    _NAME = 'organizations_locations'

    def __init__(self, client):
      super(SecuritypostureV1.OrganizationsLocationsService, self).__init__(client)
      self._upload_configs = {
          }

  class OrganizationsService(base_api.BaseApiService):
    """Service class for the organizations resource."""

    _NAME = 'organizations'

    def __init__(self, client):
      super(SecuritypostureV1.OrganizationsService, self).__init__(client)
      self._upload_configs = {
          }

  class ProjectsLocationsService(base_api.BaseApiService):
    """Service class for the projects_locations resource."""

    _NAME = 'projects_locations'

    def __init__(self, client):
      super(SecuritypostureV1.ProjectsLocationsService, self).__init__(client)
      self._upload_configs = {
          }

    def Get(self, request, global_params=None):
      r"""Gets information about a location.

      Args:
        request: (SecuritypostureProjectsLocationsGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Location) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/projects/{projectsId}/locations/{locationsId}',
        http_method='GET',
        method_id='securityposture.projects.locations.get',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1/{+name}',
        request_field='',
        request_type_name='SecuritypostureProjectsLocationsGetRequest',
        response_type_name='Location',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""Lists information about the supported locations for this service.

      Args:
        request: (SecuritypostureProjectsLocationsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListLocationsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/projects/{projectsId}/locations',
        http_method='GET',
        method_id='securityposture.projects.locations.list',
        ordered_params=['name'],
        path_params=['name'],
        query_params=['filter', 'includeUnrevealedLocations', 'pageSize', 'pageToken'],
        relative_path='v1/{+name}/locations',
        request_field='',
        request_type_name='SecuritypostureProjectsLocationsListRequest',
        response_type_name='ListLocationsResponse',
        supports_download=False,
    )

  class ProjectsService(base_api.BaseApiService):
    """Service class for the projects resource."""

    _NAME = 'projects'

    def __init__(self, client):
      super(SecuritypostureV1.ProjectsService, self).__init__(client)
      self._upload_configs = {
          }
