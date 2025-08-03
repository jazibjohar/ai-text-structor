from .data_executor import DataExecutor
from .workflow_executor import WorkflowExecutor
import asyncio
from typing import List, Union


class AITextStructor:
    """
    Manages the execution of AI processing workflows and data operations
    """

    def __init__(self, engine_config, model, parallel: bool = True):
        """
        Initialize AITextStructor with configuration

        Args:
            engine_config (dict): Configuration containing data and workflow definitions
            model: The LangChain AI model to use for processing

        Raises:
            ValueError: If data is missing or empty in engine_config
            ValueError: If model is not provided
        """
        if (
            not engine_config
            or "data" not in engine_config
            or not engine_config["data"]
        ):
            raise ValueError("engine_config must contain non-empty data configuration")

        if not model:
            raise ValueError("A LangChain model must be provided")

        self.model = model
        self.data_executor = DataExecutor(engine_config["data"], model)
        self.workflow_executor = None
        self.data_cache = {}
        self.parallel = parallel
        self._cache_lock = asyncio.Lock()

        if "workflow" in engine_config and engine_config["workflow"]:
            self.workflow_executor = WorkflowExecutor(engine_config["workflow"], model)

    async def execute_data(self, content: str, data_ids: Union[str, List[str]] = None):
        """
        Execute specific data IDs or all available data executors

        Args:
            content (str): Content to process
            data_ids (Union[str, List[str]], optional): Specific data ID(s) to execute

        Returns:
            dict: Results of processing
        """
        if isinstance(data_ids, str):
            data_ids = [data_ids]

        execute_ids = data_ids if data_ids else (
            list(self.data_executor.executors) if not self.workflow_executor 
            else []
        )

        if self.parallel:
            tasks = [self._get_or_execute_data(key, content) for key in execute_ids]
            results_list = await asyncio.gather(*tasks)
            results = dict(zip(execute_ids, results_list))
            titles = {key: self.data_executor.get_data_name(key) for key in execute_ids}
            return {'results': results, 'titles': titles}
        else:
            results = {}
            titles = {}
            for key in execute_ids:
                print(execute_ids)
                results[key] = await self._get_or_execute_data(key, content)
                titles[key] = self.data_executor.get_data_name(key)
            return {'results': results, 'titles': titles}

    async def execute(self, content):
        """
        Execute AI processing based on configuration, running workflows in parallel

        Args:
            content (str): Content to process

        Returns:
            dict: Results of processing
        """
        if not self.workflow_executor:
            return await self.execute_data(content)

        async def process_workflow(workflow_id):
            workflow_results = {}
            workflow_titles = {}
            
            # Process data requirements
            data_requirements = self.workflow_executor.get_data_requirements(workflow_id)
            data_execution = await self.execute_data(content, data_requirements)
            workflow_results[workflow_id] = data_execution['results']
            workflow_titles[workflow_id] = {
                'workflow': self.workflow_executor.get_workflow_name(workflow_id),
                'data': data_execution['titles']
            }

            workflow_executor = self.workflow_executor.get_workflow_executor_by_id(workflow_id)
            explain_workflow_id = workflow_executor(content)
            if explain_workflow_id:
                explain_data_requirements = self.workflow_executor.get_data_requirements(
                    explain_workflow_id
                )
                explain_execution = await self.execute_data(content, explain_data_requirements)
                workflow_results[workflow_id][explain_workflow_id] = explain_execution['results']
                workflow_titles[workflow_id][explain_workflow_id] = {
                    'workflow': self.workflow_executor.get_workflow_name(explain_workflow_id),
                    'data': explain_execution['titles']
                }
            return {'results': workflow_results, 'titles': workflow_titles}

        if self.parallel:
            workflow_tasks = [
                process_workflow(workflow_id)
                for workflow_id in self.workflow_executor.get_root_workflows()
            ]
            workflow_results_list = await asyncio.gather(*workflow_tasks)
            
            # Merge all workflow results into a single dictionary
            results = {}
            titles = {}
            for workflow_result in workflow_results_list:
                results.update(workflow_result['results'])
                titles.update(workflow_result['titles'])
            return {'results': results, 'titles': titles}
        else:
            results = {}
            titles = {}
            for workflow_id in self.workflow_executor.get_root_workflows():
                workflow_result = await process_workflow(workflow_id)
                results.update(workflow_result['results'])
                titles.update(workflow_result['titles'])
            return {'results': results, 'titles': titles}

    async def _get_or_execute_data(self, data_key: str, content: str):
        """
        Get data from cache or execute data executor if not cached

        Args:
            data_key (str): Key for the data executor
            content (str): Content to process

        Returns:
            The result of the data execution or cached value
        """
        cache_key = f"{data_key}"
        async with self._cache_lock:
            if cache_key not in self.data_cache:
                executor = self.data_executor.get_executor(data_key)
                loop = asyncio.get_running_loop()
                self.data_cache[cache_key] = await loop.run_in_executor(
                    None, executor, content
                )
            return self.data_cache[cache_key]
