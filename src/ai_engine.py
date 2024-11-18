from data_executor import DataExecutor
from workflow_executor import WorkflowExecutor
import asyncio
from typing import List, Union

class AIEngine:
    """
    Manages the execution of AI processing workflows and data operations
    """
    def __init__(self, engine_config, model, parallel: bool = True):
        """
        Initialize AIEngine with configuration
        
        Args:
            engine_config (dict): Configuration containing data and workflow definitions
            model: The LangChain AI model to use for processing
            
        Raises:
            ValueError: If data is missing or empty in engine_config
            ValueError: If model is not provided
        """
        if not engine_config or 'data' not in engine_config or not engine_config['data']:
            raise ValueError("engine_config must contain non-empty data configuration")
        
        if not model:
            raise ValueError("A LangChain model must be provided")
            
        self.model = model
        self.data_executor = DataExecutor(engine_config['data'], model)
        self.workflow_executor = None
        self.data_cache = {}
        self.parallel = parallel
        self._cache_lock = asyncio.Lock()
        
        if 'workflow' in engine_config and engine_config['workflow']:
            self.workflow_executor = WorkflowExecutor(engine_config['workflow'])
    
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
        
        execute_ids = data_ids or list(self.data_executor.executors)
        
        if self.parallel:
            tasks = [self._get_or_execute_data(key, content) for key in execute_ids]
            results_list = await asyncio.gather(*tasks)
            return dict(zip(execute_ids, results_list))
        else:
            results = {}
            for key in execute_ids:
                results[key] = await self._get_or_execute_data(key, content)
            return results

    async def execute(self, content):
        """
        Execute AI processing based on configuration
        
        Args:
            content (str): Content to process
            
        Returns:
            dict: Results of processing
        """
        if not self.workflow_executor:
            return await self.execute_data(content)
        
        results = {}
        for workflow_id in self.workflow_executor.get_root_workflows():
            # Process data requirements
            data_requirements = self.workflow_executor.get_data_requirements(workflow_id)
            results[workflow_id] = await self.execute_data(content, data_requirements)
            
            # Process dependencies
            for dep_workflow in self.workflow_executor.get_explain_dependencies(workflow_id):
                dep_requirements = self.workflow_executor.get_data_requirements(dep_workflow)
                results[dep_workflow] = await self.execute_data(content, dep_requirements)
        
        return results

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
