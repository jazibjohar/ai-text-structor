from process_object import run_completion_for_object
from process_string import run_completion_for_string
from process_numeric import run_completion_for_numeric

prompt_builder_by_type = {
    "object": run_completion_for_object,
    "string": run_completion_for_string,
    "numeric": run_completion_for_numeric,
}