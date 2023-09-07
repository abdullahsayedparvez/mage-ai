import pandas as pd
from typing import Dict

from mage_ai.api.operations import constants
from mage_ai.api.operations.base import BaseOperation
from mage_ai.data_preparation.models.widget import Widget
from mage_ai.data_preparation.variable_manager import get_global_variables
from mage_ai.presenters.charts.data_sources.base import ChartDataSourceBase
from mage_ai.shared.hash import merge_dict


class ChartDataSourcePipelineRuns(ChartDataSourceBase):
    async def load_data(
        self,
        user = None,
        meta: Dict = None,
        variables: Dict = None,
        **kwargs,
    ):
        response = await BaseOperation(
            action=constants.LIST,
            meta=merge_dict({
                constants.META_KEY_LIMIT: 10000,
            }, meta or {}),
            query=variables,
            resource='pipeline_runs',
            resource_parent='pipeline_schedules' if self.pipeline_schedule_id else None,
            resource_parent_id=self.pipeline_schedule_id if self.pipeline_schedule_id else None,
            user=user,
        ).execute()

        return pd.DataFrame(response['pipeline_runs'])