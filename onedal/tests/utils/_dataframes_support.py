# ===============================================================================
# Copyright 2023 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================

import pytest

try:
    import dpctl
    import dpctl.tensor as dpt

    dpctl_available = True
except ImportError:
    dpctl_available = False

try:
    import dpnp

    dpnp_available = True
except ImportError:
    dpnp_available = False

import numpy as np

from onedal.tests.utils._device_selection import get_queues


def _get_dataframes_and_queues(
    dataframe_filter_="numpy,dpnp,dpctl", device_filter_="cpu,gpu"
):
    dataframes_and_queues = [
        pytest.param("numpy", None, id="numpy"),
    ]

    if dpctl_available and "dpctl" in dataframe_filter_:
        for queue in get_queues(device_filter_):
            dataframes_and_queues.append(pytest.param("dpctl", queue))
    if dpnp_available and "dpnp" in dataframe_filter_:
        for queue in get_queues(device_filter_):
            dataframes_and_queues.append(pytest.param("dpnp", queue))
    return dataframes_and_queues


def _as_numpy(obj, *args, **kwargs):
    if dpnp_available and isinstance(obj, dpnp.ndarray):
        return obj.asnumpy(*args, **kwargs)
    if dpctl_available and isinstance(obj, dpt.usm_ndarray):
        return dpt.to_numpy(obj, *args, **kwargs)
    return np.asarray(obj, *args, **kwargs)


def _convert_to_dataframe(obj, sycl_queue=None, target_df=None, *args, **kwargs):
    if target_df is None:
        return obj
    # Numpy ndarray.
    # `sycl_queue` arg is ignored.
    elif target_df == "numpy":
        return np.asarray(obj, *args, **kwargs)
    # DPNP ndarray.
    elif target_df == "dpnp":
        return dpnp.asarray(
            obj, usm_type="device", sycl_queue=sycl_queue, *args, **kwargs
        )
    # DPCtl tensor.
    elif target_df == "dpctl":
        return dpt.asarray(obj, usm_type="device", sycl_queue=sycl_queue, *args, **kwargs)
