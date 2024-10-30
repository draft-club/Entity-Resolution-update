# Kubeflow Pipeline Project  

This repo demonstrates how to set up and run a data processing and entity resolution pipeline using Kubeflow. The pipeline components are modularized and organized into Python scripts that perform various tasks, including data preparation, concatenation, entity resolution with Splink, and data analysis.  

## Project Structure  

```  project_root/  ├── components/  │   ├── prepare_ref_component.py  │   ├── prepare_source_component.py  │   ├── concat_source_component.py  │   ├── splink_component.py  │   └── analyze_component.py  ├── utils/  │   ├── data_utils.py  │   ├── file_utils.py  │   └── mapping_utils.py  ├── constants.py  ├── config.yaml  ├── .env  ├── requirements.txt  ├── Dockerfile  └── main_pipeline.py   `

Prerequisites
-------------

*   **Python 3.9+** installed locally for testing
    
*   **Docker** to containerize and run the pipeline
    
*   **Kubeflow** to deploy and manage the pipeline
    
*   **Kubeflow Pipelines SDK** to interact with Kubeflow from Python (optional but recommended)
    

### Setting Up Kubeflow

1.  bashCopy codepip install kfp
    
2.  Ensure you have access to a Kubeflow instance. You can set up Kubeflow locally using Minikube or on the cloud using managed Kubeflow services.
    

Building and Running the Project Locally
----------------------------------------

1.  bashCopy codegit clone https://github.com/your-repository/kubeflow-pipeline-project.gitcd kubeflow-pipeline-project
    
2.  bashCopy codedocker build -t your\_project\_image\_name .
    
3.  bashCopy codedocker run -it --rm your\_project\_image\_name
    

Deploying the Project on Kubeflow
---------------------------------

To deploy this pipeline on Kubeflow, follow these steps:

### Step 1: Compile the Pipeline

The pipeline defined in main\_pipeline.py must be compiled to a YAML file that Kubeflow can interpret. Use the following Python script or command to compile the pipeline:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pythonCopy code# compile_pipeline.py  from kfp import dsl  from kfp.compiler import Compiler  from main_pipeline import data_pipeline  if __name__ == "__main__":      Compiler().compile(data_pipeline, "data_pipeline.yaml")   `

Run the script to create data\_pipeline.yaml:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bashCopy codepython compile_pipeline.py   `

This will generate a data\_pipeline.yaml file in the project directory.

### Step 2: Upload the Pipeline to Kubeflow

1.  **Log in to the Kubeflow dashboard**.
    
2.  Navigate to the **Pipelines** section.
    
3.  Click on **Upload pipeline** and select data\_pipeline.yaml.
    
4.  Follow the prompts to upload and version the pipeline.
    

### Step 3: Run the Pipeline on Kubeflow

1.  After uploading, click **Create run** to start a new run of the pipeline.
    
2.  Configure the runtime parameters as needed.
    
3.  Start the pipeline run and monitor its progress from the Kubeflow dashboard.
    

### Environment Variables

Configure environment variables in the .env file to manage project settings, such as the PROJECT\_ID and other configurations.

### Configuration

Edit the config.yaml file to customize paths, thresholds, and other parameters for the pipeline components.

Troubleshooting
---------------

*   **Pipeline Component Failures**: Check the logs of each component on the Kubeflow dashboard to identify any issues.
    
*   **Docker Build Errors**: Ensure all dependencies in requirements.txt are correct and compatible. Rebuild the Docker image after modifying dependencies.
    
*   **Environment Configuration**: Ensure the .env file and config.yaml are correctly set up for the Kubeflow environment.
    

Notes
-----

*   **Scalability**: This pipeline can be scaled on Kubernetes by setting up the resources (CPU, memory) allocated to each component in Kubeflow.
    
*   **Modularity**: Each component in the components/ folder can be modified independently, making it easy to update or add new stages to the pipeline.
    

Requirements
------------

Install project dependencies locally if you need to run or test any components outside of Docker or Kubeflow:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bashCopy codepip install -r requirements.txt   `
