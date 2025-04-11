{%- if cookiecutter.base_class == "CWorkflowTask" %}
{%-   set base_class_fqdn = "core.CWorkflowTask" %}
{%- else %}
{%-   set base_class_fqdn = "dataprocess." + cookiecutter.base_class %}
{%- endif %}
import copy

from ikomia import core, dataprocess


# --------------------
# - Class to handle the process parameters
# - Inherits core.CWorkflowTaskParam from Ikomia API
# --------------------
class {{ cookiecutter.class_name }}Param(core.CWorkflowTaskParam):

    def __init__(self):
        core.CWorkflowTaskParam.__init__(self)
        # Place default value initialization here
        # Example : self.windowSize = 25

    def set_values(self, params):
        # Set parameters values from Ikomia application
        # Parameters values are stored as string and accessible like a python dict
        # Example : self.windowSize = int(params["windowSize"])
        pass

    def get_values(self):
        # Send parameters values to Ikomia application
        # Create the specific dict structure (string container)
        params = {}
        # Example : params["windowSize"] = str(self.windowSize)
        return params


# --------------------
# - Factory class to create parameters object
# --------------------
class {{ cookiecutter.class_name }}ParamFactory(dataprocess.CTaskParamFactory):
    def __init__(self):
        dataprocess.CTaskParamFactory.__init__(self)
        self.name = "{{ cookiecutter.algo_name }}"

    def create(self):
        return {{ cookiecutter.class_name }}Param()


# --------------------
# - Class which implements the process
# - Inherits core.CWorkflowTask or derived from Ikomia API
# --------------------
class {{ cookiecutter.class_name }}({{ base_class_fqdn }}):

    def __init__(self, name, param):
        {{ base_class_fqdn }}.__init__(self, name)
        # Add input/output of the process here
        # Example :  self.add_input(dataprocess.CImageIO())
        #           self.add_output(dataprocess.CImageIO())

        # Create parameters class
        if param is None:
            self.set_param_object({{ cookiecutter.class_name }}Param())
        else:
            self.set_param_object(copy.deepcopy(param))

    def get_progress_steps(self):
        # Function returning the number of progress steps for this process
        # This is handled by the main progress bar of Ikomia application
        return 1

    def run(self):
        # Core function of your process
        # Call begin_task_run() for initialization
        self.begin_task_run()

        # Examples :
        # Get input :
        # task_input = self.get_input(index_of_input)

        # Get output :
        # task_output = self.get_output(index_of_output)

        # Get parameters :
        # param = self.get_param_object()

        # Get image from input/output (numpy array):
        # src_image = task_input.get_image()

        # Call to the process main routine
        # dst_image = ...

        # Set image of input/output (numpy array):
        # task_output.set_image(dst_image)

        # Step progress bar:
        self.emit_step_progress()

        # Call end_task_run() to finalize process
        self.end_task_run()


# --------------------
# - Factory class to build process object
# - Inherits dataprocess.CTaskFactory from Ikomia API
# --------------------
class {{ cookiecutter.class_name }}Factory(dataprocess.CTaskFactory):

    def __init__(self):
        dataprocess.CTaskFactory.__init__(self)
        # Set process information as string here
        self.info.name = "{{ cookiecutter.algo_name }}"
        self.info.short_description = "your short description"
        # relative path -> as displayed in Ikomia Studio process tree
        self.info.path = "Plugins/Python"
        self.info.version = "1.0.0"
        # self.info.icon_path = "your path to a specific icon"
        self.info.authors = "algorithm author"
        self.info.article = "title of associated research article"
        self.info.article_url = ""
        self.info.journal = "publication journal"
        self.info.year = 2024
        self.info.license = ""

        # Ikomia API compatibility
        # self.info.min_ikomia_version = "0.10.0"
        # self.info.max_ikomia_version = "0.11.0"

        # Python compatibility
        # self.info.min_python_version = "3.10.0"
        # self.info.max_python_version = "3.11.0"

        # URL of documentation
        self.info.documentation_link = ""

        # Code source repository
        self.info.repository = ""
        self.info.original_repository = ""

        # Keywords used for search
        self.info.keywords = "your,keywords,here"

        # General type: INFER, TRAIN, DATASET or OTHER
        # self.info.algo_type = core.AlgoType.OTHER

        # Algorithms tasks: CLASSIFICATION, COLORIZATION, IMAGE_CAPTIONING, IMAGE_GENERATION,
        # IMAGE_MATTING, INPAINTING, INSTANCE_SEGMENTATION, KEYPOINTS_DETECTION,
        # OBJECT_DETECTION, OBJECT_TRACKING, OCR, OPTICAL_FLOW, OTHER, PANOPTIC_SEGMENTATION,
        # SEMANTIC_SEGMENTATION or SUPER_RESOLUTION
        # self.info.algo_tasks = "OTHER"

    def create(self, param=None):
        # Create process object
        return {{ cookiecutter.class_name }}(self.info.name, param)
