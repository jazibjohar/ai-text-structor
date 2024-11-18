from process_object import run_completion_for_object
from process_string import run_completion_for_string
from process_numeric import run_completion_for_numeric
from process_list import run_completion_for_list

class DataExecutor:
    """
    Manages the execution and state management of data processing from prompts
    """
    def __init__(self, data_dict=None, model=None):
        """
        Initialize DataExecutor with a data dictionary and LangChain model
        
        Args:
            data_dict (dict): Dictionary containing data fields and their configurations
            model: LangChain AI model instance
            
        Raises:
            ValueError: If data_dict is None or empty
            ValueError: If model is None
        """
        if not data_dict:
            raise ValueError("data_dict must be provided and cannot be empty")
        if model is None:
            raise ValueError("model must be provided")
            
        self.data_dict = data_dict
        self.model = model
        self.executors = {}
        self._initialize_executors()
    
    def _initialize_executors(self):
        """
        Initialize executor functions that return chain components for each key.
        Each executor returns a dict with:
        - prompts: The prompts to be used
        - parser: Function to parse the output
        - args: Additional arguments for the chain
        """
        for key, config in self.data_dict.items():
            data_type = config.get('type')
            if not data_type:
                raise ValueError(f"Configuration for key '{key}' must specify a type")
                
            if data_type == 'object':
                self.executors[key] = lambda content, c=config, m=self.model: self._execute_chain(
                    run_completion_for_object(content, c), m
                )
            elif data_type == 'string':
                self.executors[key] = lambda content, c=config, m=self.model: self._execute_chain(
                    run_completion_for_string(content, c), m
                )
            elif data_type == 'numeric':
                self.executors[key] = lambda content, c=config, m=self.model: self._execute_chain(
                    run_completion_for_numeric(content, c), m
                )
            elif data_type == 'list':
                self.executors[key] = lambda content, c=config, m=self.model: self._execute_chain(
                    run_completion_for_list(content, c), m
                )
            else:
                raise ValueError(f"Invalid type '{data_type}' for key '{key}'")
    
    def _execute_chain(self, chain_components, model):
        """
        Execute a LangChain chain with the provided components
        
        Args:
            chain_components (dict): Dictionary containing prompts, parser, and args
            model: LangChain model instance
            
        Returns:
            The parsed result from the chain execution
        """
        prompts = chain_components["prompts"]
        parser = chain_components["parser"]
        args = chain_components["args"]
        
        chain = prompts | model | parser
        return chain.invoke(args)
    
    def get_executor(self, key):
        """
        Get executor function for a specific key
        
        Args:
            key (str): Key to fetch executor for
            
        Returns:
            callable: The executor function for the specified key
        """
        return self.executors.get(key)
