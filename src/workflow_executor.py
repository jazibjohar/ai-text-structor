class WorkflowExecutor:
    """
    Manages the execution and validation of workflows based on their dependencies
    """
    def __init__(self, workflow_dict=None):
        """
        Initialize WorkflowExecutor with a workflow dictionary
        
        Args:
            workflow_dict (dict): Dictionary containing workflow definitions
            
        Raises:
            ValueError: If workflow_dict is None or empty
        """
        if not workflow_dict:
            raise ValueError("workflow_dict must be provided and cannot be empty")
            
        self.workflow_dict = workflow_dict
        self.prompt_workflows = {}  # Prompt-based workflows (independent execution steps)
        self.explain_workflows = {}  # Explanation-based workflows (dependent steps)
        self.explain_dependencies = {}  # Mapping of prompt workflows to their explain dependencies
        self.workflow_data = {}  # Mapping of workflows to their data requirements
        
        if self._validate():
            self._initialize()
    
    def _validate(self):
        """
        Validates workflow configurations
        
        Returns:
            bool: True if validation passes
            
        Raises:
            ValueError: If validation fails
        """
        for workflow_id, config in self.workflow_dict.items():
            # Check for either prompt or explain
            if not (config.get('prompt') or config.get('explain')):
                raise ValueError(f"Workflow '{workflow_id}' must have either 'prompt' or 'explain'")
            
            # Validate explain workflows have dependencies
            if config.get('explain') and not config.get('requires'):
                raise ValueError(f"Explain workflow '{workflow_id}' must have dependencies")
            
            # Validate explain workflows don't depend on other explain workflows
            if config.get('explain'):
                for dep in config.get('requires', []):
                    if self.workflow_dict.get(dep, {}).get('explain'):
                        raise ValueError(f"Explain workflow '{workflow_id}' cannot depend on another explain workflow")
            
            # Validate data field references exist
            if not isinstance(config.get('data', []), list):
                raise ValueError(f"Data field for workflow '{workflow_id}' must be a list")
            
            # Add new validations from documentation
            if config.get('prompt') and config.get('requires'):
                for dep in config.get('requires', []):
                    if self.workflow_dict.get(dep, {}).get('prompt'):
                        raise ValueError(
                            f"Prompt-based workflow '{workflow_id}' cannot depend on another prompt-based workflow"
                        )
            
            # Validate data types
            for data_field in config.get('data', []):
                if not isinstance(data_field, str):
                    raise ValueError(
                        f"Data field references in workflow '{workflow_id}' must be strings"
                    )
        
        return True
    
    def _initialize(self):
        """
        Initializes internal workflow mappings
        """
        for workflow_id, config in self.workflow_dict.items():
            # Store data requirements for all workflows
            self.workflow_data[workflow_id] = config.get('data', [])
            
            if config.get('prompt'):
                # Store prompt-based workflows
                self.prompt_workflows[workflow_id] = {
                    'prompt': config['prompt'],
                    'requires': config.get('requires', []),
                    'name': config.get('name', workflow_id),
                    'description': config.get('description', '')
                }
                
                # Initialize explain dependencies list
                self.explain_dependencies[workflow_id] = []
            
            if config.get('explain'):
                # Store explanation-based workflows
                self.explain_workflows[workflow_id] = {
                    'explain': config['explain'],
                    'requires': config.get('requires', []),
                    'name': config.get('name', workflow_id),
                    'description': config.get('description', '')
                }
                
                # Map explain workflows to their prompt workflow dependencies
                for dep in config.get('requires', []):
                    if dep in self.prompt_workflows:
                        self.explain_dependencies[dep].append(workflow_id)
    
    def get_root_workflows(self):
        """
        Returns prompt-based workflows with no dependencies
        
        Returns:
            dict: Dictionary of root workflow IDs and their prompts
        """
        return {
            wf_id: config['prompt'] 
            for wf_id, config in self.prompt_workflows.items() 
            if not config['requires']
        }
    
    def get_explain_dependencies(self, workflow_id):
        """
        Returns explain workflow IDs dependent on the given workflow
        
        Args:
            workflow_id (str): Workflow ID to get dependencies for
            
        Returns:
            list: List of dependent explain workflow IDs
        """
        return self.explain_dependencies.get(workflow_id, [])
    
    def get_data_requirements(self, workflow_id):
        """
        Returns data field requirements for a workflow
        
        Args:
            workflow_id (str): Workflow ID to get data requirements for
            
        Returns:
            list: List of required data field IDs
        """
        return self.workflow_data.get(workflow_id, [])
