# Define base project directory
$ProjectDir = "project_root"
$ComponentsDir = "$ProjectDir/components"
$UtilsDir = "$ProjectDir/utils"
$AnalyzeDir = "$ProjectDir/analyze"

# Create directories
New-Item -ItemType Directory -Force -Path $ProjectDir, $ComponentsDir, $UtilsDir, $AnalyzeDir | Out-Null

# Create component files
$Components = @("prepare_ref_component", "prepare_source_component", "concat_source_component", "splink_component", "analyze_component")
ForEach ($component in $Components) {
    New-Item -ItemType File -Path "$ComponentsDir/$component.py" | Out-Null
}

# Create utility files
$Utils = @("data_utils.py", "file_utils.py", "mapping_utils.py")
ForEach ($util in $Utils) {
    New-Item -ItemType File -Path "$UtilsDir/$util" | Out-Null
}

# Create additional files
$Files = @("constants.py", ".env", "config.yaml", "requirements.txt", "main_pipeline.py")
ForEach ($file in $Files) {
    New-Item -ItemType File -Path "$ProjectDir/$file" | Out-Null
}

Write-Output "Project folder structure and files created successfully!"
