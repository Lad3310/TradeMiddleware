# -*- coding: utf-8 -*- #
# Copyright 2024 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""A library used to support Managed Service for Apache Kafka commands."""

from apitools.base.py import encoding
from googlecloudsdk import core
from googlecloudsdk.api_lib.util import apis
from googlecloudsdk.calliope import exceptions

# Retrieve all message type for conversions from gcloud primitives to
# apitool types.
_MESSAGE = apis.GetMessagesModule("managedkafka", "v1")


def ValidateCPU(cpu):
  """Validate CPU >= 3."""
  if cpu < 3:
    raise exceptions.BadArgumentException(
        "--cpu", "CPU must be at least 3"
    )
  return cpu


def PrepareUpdateWithSubnets(_, args, request):
  """Prepare the update request with the information from the subnet flag.

  Args:
    _:  resource parameter required but unused variable.
    args: list of flags.
    request:  the payload to return.

  Returns:
    The updated request with the subnet.
  """
  if not args.subnets:
    return request

  # The cluster is not created yet if only the subnet flag is set. This is
  # because we don't formally map the subnet to the request the same way we do
  # for other flags. Instead, subnets require special handling with the use of
  # hooks.
  if not request.cluster:
    request.cluster = {}

  subnet_update_mask = "gcpConfig.accessConfig.networkConfigs"
  request.updateMask = AppendUpdateMask(request.updateMask, subnet_update_mask)
  return MapSubnetsToNetworkConfig(_, args, request)


def AppendUpdateMask(update_mask, new_mask):
  """Handles appending a new mask to an existing mask.

  Args:
    update_mask: the existing update mask.
    new_mask: the new mask to append.

  Returns:
    The fully appended update mask.
  """
  update_mask = f"{update_mask},{new_mask}"
  return update_mask if update_mask[0] != "," else update_mask[1:]


def MapSubnetsToNetworkConfig(_, args, request):
  """Maps the list of subnets from the flag to the API fields in the request.

  Args:
    _:  resource parameter required but unused variable.
    args: list of flags.
    request:  the payload to return.

  Returns:
    The updated request with networkConfig in the JSON format.
  """
  # Reference the existing GCP config if already created for the request.
  if not request.cluster.gcpConfig:
    request.cluster.gcpConfig = {}
  request.cluster.gcpConfig.accessConfig = {"networkConfigs": []}
  for subnet in args.subnets:
    network_config = {"subnet": subnet}
    request.cluster.gcpConfig.accessConfig.networkConfigs.append(
        encoding.DictToMessage(
            network_config, _MESSAGE.NetworkConfig
        )
    )
  return request


def ListWithBootstrapAddr(response, _):
  """Synthesizes the bootstrap address to the response for a list request.

  Args:
    response: the payload to return.
    _: list of flags.

  Returns:
    The updated clusters with the bootstrap.
  """
  return [
      SynthesizeBootstrapAddr(cluster, cluster.name) for cluster in response
  ]


def DescribeWithBootstrapAddr(response, _):
  """Synthesizes the bootstrap address to the response for a describe request.

  Args:
    response: the payload to return.
    _: list of flags.

  Returns:
    The updated cluster with the bootstrap.
  """
  return SynthesizeBootstrapAddr(response, response.name)


def SynthesizeBootstrapAddr(response, cluster):
  """Synthesizes the bootstrap address to the response.

  Args:
    response: the payload to update.
    cluster: the fully qualifed name of the cluster.

  Returns:
    The updated cluster with the bootstrap
  """
  # The fully qualified name will always be consistent. We also have to use the
  # fully qualifed name instead of the resource directly to support both
  # `describe` and `list`.
  name = cluster.split("/")[5]
  location = cluster.split("/")[3]
  project = core.properties.VALUES.core.project.Get()
  domain_prefixed_project = project.split(":")
  if len(domain_prefixed_project) == 2:
    project = f"{domain_prefixed_project[1]}.{domain_prefixed_project[0]}"
  bootstrap = (
      f"bootstrap.{name}.{location}.managedkafka.{project}.cloud.goog"
  )
  synthesized = core.resource.resource_projector.MakeSerializable(response)
  synthesized["bootstrapAddress"] = bootstrap
  return synthesized


def UpdateTopics(_, args, request):
  """Load the topics JSON from the argument to the request.

  Args:
    _:  resource parameter required but unused variable.
    args: list of flags.
    request:  the payload to return.

  Returns:
    The updated request with topics.
  """
  topics = core.yaml.load(args.topics_file)
  request.consumerGroup = {
      "topics": encoding.DictToMessage(
          topics, _MESSAGE.ConsumerGroup.TopicsValue
      )
  }
  request.updateMask = "topics"
  return request


def PatchConfigs(_, args, request):
  """Unnest the configs dictionary to the update mask.

  Args:
    _:  resource parameter required but unused variable.
    args: list of flags.
    request:  the payload to return.

  Returns:
    The new update mask with the configs.
  """
  if args.configs:
    update_mask = request.updateMask.split(",")
    update_mask.remove("configs")
    configs_list = []
    for key, _ in args.configs.items():
      configs_list.append(f'configs["{key}"]')
    request.updateMask = AppendUpdateMask(
        ",".join(update_mask), ",".join(configs_list)
    )
  # This flag is guarded with a mutex so it won't conflict with the above.
  if args.clear_configs:
    request.updateMask = AppendUpdateMask(request.updateMask, "configs")
  return request
