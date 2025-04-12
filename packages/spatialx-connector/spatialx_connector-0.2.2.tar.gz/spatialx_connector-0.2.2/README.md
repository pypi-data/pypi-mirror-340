## SpatialX Connector
###  1.1. <a name='InstallationSpatialXConnector'></a>Installation SpatialX Connector


```python
!pip install -U spatialx_connector
```

###  1.2. <a name='Importtherelatedpackages'></a>Import the related packages


```python
import warnings
warnings.filterwarnings("ignore")
```


```python
import os

import spatialx_connector
from spatialx_connector import SpatialXConnector
from spatialx_connector import Technologies
from spatialx_connector import DefaultGroup
from spatialx_connector import Species
from spatialx_connector import ConnectorKeys
from spatialx_connector import SubmissionElementKeys
from spatialx_connector import SegmentationSubmission
from spatialx_connector import ExpressionSubmission
```

###  1.3. <a name='DomainandToken'></a>Domain and Token
To obtain your domain URL and personal token, navigate to "SpatialX SDK" in the left panel of your SpatialX interface. Then, enter the information in the fields below. For example:

DOMAIN = "https://example.bioturing.com/spatialx/"

TOKEN = "000000000000000000000000NM"

```python
DOMAIN = ""
TOKEN = ""
```

###  1.4. <a name='ExploreYourAccount'></a>Explore Your Account
With your domain and token added, you can now connect to your SpatialX account and workspace and explore your account details.
####  1.4.1. <a name='UsersInformation:'></a>User's Information:


```python
connector = SpatialXConnector(domain=DOMAIN, token=TOKEN)
spatialx_connector.format_print(connector.info)
```


####  1.4.2. <a name='Groups:'></a>Groups:
This function provides the group name and ID needed for the submission process. <br>The returned data is formatted as follows: `Group name: Group ID`.

```python
spatialx_connector.format_print(connector.groups)
```
```yaml
{
    Personal workspace: 0eebe305688d82fe6c5ce361a43c64da
    All members: GLOBAL_GROUP
    BioTuring Public Studies: bioturing_public_studies
}
```

###  1.5. <a name='ListofStorages'></a>List of Storages
If you have configured your cloud storages or would like to check your data list in SpatialX, the list of functions below can help you to get the information:

####  1.5.1. <a name='AWSbuckets'></a> AWS buckets


```python
spatialx_connector.format_print(connector.s3)
```
```yaml
{
    bioturingpublic: /.../bioturingpublic
}
```

####  1.5.2. <a name='PersonalandSharedFolders'></a> Personal and Shared Folders


```python
spatialx_connector.format_print(connector.folders)
```
```yaml
{
    shared: /.../4e3de55d66ef57b14c9119c90fd7f4e1/shared_folder/shared
    Converted: /.../4e3de55d66ef57b14c9119c90fd7f4e1/converted
    Submitted: /.../4e3de55d66ef57b14c9119c90fd7f4e1/study
    Upload: /.../4e3de55d66ef57b14c9119c90fd7f4e1/upload
}
```

####  1.5.3. <a name='BrowsingStorage'></a> Browsing Storage


```python
connector.listdir(connector.s3["bioturingpublic"])
```
```yaml
[
    'python3.9.13_linux.zip',
    'genes_annotation.human.json',
    'genes_annotation.mouse.json',
    'genes_annotation.primate.json',
    'ontology.mouse.sql',
    'ontology.human.sql',
    'SpatialX_datasets',
    'anotation',
    'binary',
    'examples',
    'mount'
]
```

```python
connector.listdir(os.path.join(connector.s3["bioturingpublic"], "SpatialX_datasets"))
```
```yaml
[
    'AnnData',
    'COSMX_VER1',
    'COSMX_VER2',
    'GeoMx',
    'Human_Colon_Cancer_P2',
    'MERSCOPE_VER1',
    'MERSCOPE_VER2',
    'Slide-Seq',
    'SpatialData'
]
```

```python
connector.listdir(os.path.join(connector.s3["bioturingpublic"], "SpatialX_datasets/COSMX_VER1"))
```
```yaml
['Lung6', 'Lung9_Rep1', 'Lung9_Rep2']
```


###  1.6. <a name='Accessingstudyinformation'></a>Accessing study information
Use these functions to get detailed information about your studies in different workspaces.

####  1.6.1. <a name='Listingstudies:'></a> Listing studies:
The following code retrieves a list of your studies within your personal workspace. To list studies in a different group, replace `DefaultGroup.PERSONAL_WORKSPACE.value` with the desired group name (e.g., `"Demo"`).

```python
studies = connector.list_study(
    group=DefaultGroup.PERSONAL_WORKSPACE.value,
    species=Species.HUMAN.value,
)
spatialx_connector.format_print(studies)
```


####  1.6.2. <a name='RetrievingStudyDetails:'></a> Retrieving Study Details:
To get detailed information about a specific study, use the function below. The example retrieves details for the first study in the list. To retrieve details for a different study, replace the `studies[0][ConnectorKeys.STUDY_ID.value]` (e.g., `"ST-..."`) with the desired study's identifier.

```python
study_details = connector.get_study_detail(study_id=studies[0][ConnectorKeys.STUDY_ID.value])
spatialx_connector.format_print(study_details)
```


####  1.6.3. <a name='ListingSampleswithinaStudy:'></a> Listing Samples within a Study:
You can retrieve a list of samples associated with a particular study using the following code.

```python
samples = connector.list_sample(study_id=studies[0][ConnectorKeys.STUDY_ID.value])
spatialx_connector.format_print(samples)
```


####  1.6.4. <a name='RetrievingSampleDetails:'></a> Retrieving Sample Details:
To get detailed information about a specific sample, use the function below. Similar to the previous example, replace the `samples[0][ConnectorKeys.SAMPLE_ID.value]` (e.g., `"SP-..."`) with the desired sample's identifier to retrieve its details.

```python
sample_details = connector.get_sample_detail(sample_id=samples[0][ConnectorKeys.SAMPLE_ID.value])
spatialx_connector.format_print(sample_details)
```


###  1.7. <a name='Uploadingfiles'></a>Uploading files
To upload files to your personal folders within your SpatialX account, execute the code below. Be sure to replace the placeholder `file_path` with the complete path to the file you wish to upload.

```python
uploading_results = connector.upload_file(file_path="/s3/colab/content/xenium/experiment.xenium")
spatialx_connector.format_print(uploading_results)
```


```python
uploading_results = connector.upload_big_file(file_path="/s3/colab/content/xenium/morphology_mip.ome.tif", debug_mode=True)
spatialx_connector.format_print(uploading_results)
```


```python
uploading_results = connector.upload_folder(dir_path="/s3/colab/content/xenium", debug_mode=True)
spatialx_connector.format_print(uploading_results)
```

###  1.8. <a name='Submission'></a>Submission

####  1.8.1. <a name='ParsingDataInformationforSubmission:'></a> Parsing Data Information for Submission:
* **`data_name`:** Name of the dataset.
* **`technology`:** Technology used for the dataset.
* **`data_path`:** Path to the dataset.


```python
Visium_V2_Human_Colon_Cancer_P2_submission_information = connector.parse_data_information(
    data_name="Visium_V2_Human_Colon_Cancer_P2",
    technology=Technologies.VISIUM.value,
    data_path=os.path.join(
        connector.s3["bioturingpublic"],
        "SpatialX_datasets/Human_Colon_Cancer_P2/Visium_V2_Human_Colon_Cancer_P2"
    )
)
spatialx_connector.format_print(Visium_V2_Human_Colon_Cancer_P2_submission_information)
```
```yaml
[
    {
        name: Visium_V2_Human_Colon_Cancer_P2
        submission_type: SUBMIT_SPATIAL_BULK
        technology: VISIUM
        files: [
            {
                key: images
                value: /.../bioturingpublic/SpatialX_datasets/Human_Colon_Cancer_P2/Visium_V2_Human_Colon_Cancer_P2/Visium_V2_Human_Colon_Cancer_P2_tissue_image.btf
            }
            {
                key: matrix
                value: /.../bioturingpublic/SpatialX_datasets/Human_Colon_Cancer_P2/Visium_V2_Human_Colon_Cancer_P2/Visium_V2_Human_Colon_Cancer_P2_raw_feature_bc_matrix.h5
            }
            {
                key: tissue_positions
                value: /.../bioturingpublic/SpatialX_datasets/Human_Colon_Cancer_P2/Visium_V2_Human_Colon_Cancer_P2/spatial/tissue_positions.csv
            }
            {
                key: scalefactors
                value: /.../bioturingpublic/SpatialX_datasets/Human_Colon_Cancer_P2/Visium_V2_Human_Colon_Cancer_P2/spatial/scalefactors_json.json
            }
        ]
        folders: []
        args: []
        kwargs: []
        identities: []
    }
]
```


```python
Xenium_V1_Human_Colon_Cancer_P2_submission_information = connector.parse_data_information(
    data_name="Xenium_V1_Human_Colon_Cancer_P2_CRC_Add_on_FFPE",
    technology=Technologies.XENIUM.value,
    data_path=os.path.join(
        connector.s3["bioturingpublic"],
        "SpatialX_datasets/Human_Colon_Cancer_P2/Xenium_V1_Human_Colon_Cancer_P2_CRC_Add_on_FFPE"
    )
)
spatialx_connector.format_print(Xenium_V1_Human_Colon_Cancer_P2_submission_information)
```
```yaml
[
    {
        name: Xenium_V1_Human_Colon_Cancer_P2_CRC_Add_on_FFPE
        submission_type: SUBMIT_SPATIAL_TRANSCRIPTOMICS
        technology: XENIUM
        files: [
            {
                key: experiment
                value: /.../bioturingpublic/SpatialX_datasets/Human_Colon_Cancer_P2/Xenium_V1_Human_Colon_Cancer_P2_CRC_Add_on_FFPE/experiment.xenium
            }
            {
                key: images
                value: /.../bioturingpublic/SpatialX_datasets/Human_Colon_Cancer_P2/Xenium_V1_Human_Colon_Cancer_P2_CRC_Add_on_FFPE/morphology.ome.tif
            }
            {
                key: alignment
                value: /.../bioturingpublic/SpatialX_datasets/Human_Colon_Cancer_P2/Xenium_V1_Human_Colon_Cancer_P2_CRC_Add_on_FFPE/Xenium_V1_Human_Colon_Cancer_P2_CRC_Add_on_FFPE_he_imagealignment.csv
            }
            {
                key: segmentation
                value: /.../bioturingpublic/SpatialX_datasets/Human_Colon_Cancer_P2/Xenium_V1_Human_Colon_Cancer_P2_CRC_Add_on_FFPE/cell_boundaries.csv.gz
            }
            {
                key: transcripts
                value: /.../bioturingpublic/SpatialX_datasets/Human_Colon_Cancer_P2/Xenium_V1_Human_Colon_Cancer_P2_CRC_Add_on_FFPE/transcripts.csv.gz
            }
        ]
        folders: []
        args: []
        kwargs: []
        identities: []
    }
]
```

####  1.8.2. <a name='SubmittingaNewStudywithaSingleSampleandData:'></a> Submitting a New Study with a Single Sample and Data:
* **`group`:** User's group.
* **`species`:** Species of the dataset.
* **`title`:** Title of the new study.
* **`sample_name`:** Name of the new sample.
* **`sample_data`:** Data information, obtained from `connector.parse_data_information` or a combination of its results.


```python
submission_results = connector.submit(
    group=DefaultGroup.PERSONAL_WORKSPACE.value,
    species=Species.HUMAN.value,
    title="Human Colon Cancer - 10xgenomics",
    sample_name="Human_Colon_Cancer_P2",
    sample_data=Xenium_V1_Human_Colon_Cancer_P2_submission_information + Visium_V2_Human_Colon_Cancer_P2_submission_information,
)
spatialx_connector.format_print(submission_results)
```
```yaml
{
    study_id: ST-01JMGMH3AT8HH8S23QV8ZC2G9T
    sample_id: SP-01JMGMH408Q5QDH2YPNXRR2WS6
    sample_data: [
        {
            data_id: DA-01JMGMH409ZPBZPQGHBCF4RXF6
            submit_id: SB-01JMGMH408Q5QDH2YPNWG5ZH46
            submit_name: Xenium_V1_Human_Colon_Cancer_P2_CRC_Add_on_FFPE
        }
        {
            data_id: DA-01JMGMH43QEYAC44YPGTQY80XY
            submit_id: SB-01JMGMH43QEYAC44YPGWMFTJ54
            submit_name: Visium_V2_Human_Colon_Cancer_P2
        }
    ]
    submit_id: SB-01JMGMH408Q5QDH2YPNWG5ZH46
    job_id: 2
    err_message:
}
```

####  1.8.3. <a name='AddingaNewSampletoanExistingStudy:'></a> Adding a New Sample to an Existing Study:
* **`study_id`:** ID of the study to which the sample is added.
* **`name`:** Name of the new sample.
* **`sample_data`:** Data information, obtained from `connector.parse_data_information` or a combination of its results.


```python
adding_sample_results = connector.add_sample(
    study_id=submission_results[ConnectorKeys.STUDY_ID.value],
    sample_name="Human_Colon_Cancer_P2 - New Sample",
    sample_data=Visium_V2_Human_Colon_Cancer_P2_submission_information,
)
spatialx_connector.format_print(adding_sample_results)
```
```yaml
{
    study_id: ST-01JMGMH3AT8HH8S23QV8ZC2G9T
    sample_id: SP-01JMGMH7K19M32CWQ1RH5TBDKM
    sample_data: [
        {
            data_id: DA-01JMGMH7K19M32CWQ1RMY7ZF8A
            submit_id: SB-01JMGMH7K19M32CWQ1RDWJ1KDW
            submit_name: Visium_V2_Human_Colon_Cancer_P2
        }
    ]
    submit_id: SB-01JMGMH7K19M32CWQ1RDWJ1KDW
    job_id: 3
    err_message:
}
```

####  1.8.4. <a name='AddingNewDatatoanExistingSample:'></a> Adding New Data to an Existing Sample:

* **`study_id`:** ID of the study containing the sample.
* **`sample_id`:** ID of the existing sample.
* **`sample_data`:** Data information, obtained from `connector.parse_data_information` or a combination of its results.


```python
adding_sample_data_results = connector.add_sample_data(
    study_id=adding_sample_results[ConnectorKeys.STUDY_ID.value],
    sample_id=adding_sample_results[ConnectorKeys.SAMPLE_ID.value],
    sample_data=Xenium_V1_Human_Colon_Cancer_P2_submission_information,
)
spatialx_connector.format_print(adding_sample_data_results)
```
```yaml
{
    study_id: ST-01JMGMH3AT8HH8S23QV8ZC2G9T
    sample_id: SP-01JMGMH7K19M32CWQ1RH5TBDKM
    sample_data: [
        {
            data_id: DA-01JMGMHCZRFGANB8H36BSEBS3V
            submit_id: SB-01JMGMHCZRFGANB8H369FA1ZP7
            submit_name: Xenium_V1_Human_Colon_Cancer_P2_CRC_Add_on_FFPE
        }
    ]
    submit_id: SB-01JMGMHCZRFGANB8H369FA1ZP7
    job_id: 4
    err_message:
}
```

####  1.8.5. <a name='ParsingSubmissionInformationforMultipleSamples:'></a> Parsing Submission Information for Multiple Samples:

* **`technology`:** Technology used for all samples (supports a single technology).
* **`data_path`:** Path to the directory containing multiple dataset subfolders (each subfolder represents a dataset).
* **`sample_name_mapping`:** Mapping of subfolder names to sample names.
* **`data_name_mapping`:** Mapping of subfolder names to dataset names.



```python
multiple_cosmx_samples_submission_information = connector.parse_multiple_samples_information(
    technology=Technologies.COSMX_VER1.value,
    data_path=os.path.join(connector.s3["bioturingpublic"], "SpatialX_datasets/COSMX_VER1"),
    sample_name_mapping={
        "Lung6": "Human Lung Cancer - Sample 6",
        "Lung9_Rep1": "Human Lung Cancer - Sample 9 Rep 1",
        "Lung9_Rep2": "Human Lung Cancer - Sample 9 Rep 2",
    },
    data_name_mapping={
        "Lung6": "Sample 6",
        "Lung9_Rep1": "Sample 9 Rep 1",
        "Lung9_Rep2": "Sample 9 Rep 2",
    },
)
spatialx_connector.format_print(multiple_cosmx_samples_submission_information)
```
```yaml
[
    {
        sample_name: Human Lung Cancer - Sample 6
        data: [
            {
                name: Sample 6
                submission_type: SUBMIT_SPATIAL_TRANSCRIPTOMICS
                technology: COSMX_VER1
                files: [
                    {
                        key: fov_positions
                        value: /.../bioturingpublic/SpatialX_datasets/COSMX_VER1/Lung6/Lung6-Flat_files_and_images/Lung6_fov_positions_file.csv
                    }
                    {
                        key: transcripts
                        value: /.../bioturingpublic/SpatialX_datasets/COSMX_VER1/Lung6/Lung6-Flat_files_and_images/Lung6_tx_file.csv
                    }
                ]
                folders: [
                    {
                        key: images
                        value: /.../bioturingpublic/SpatialX_datasets/COSMX_VER1/Lung6/Lung6-RawMorphologyImages
                    }
                    {
                        key: segmentation
                        value: /.../bioturingpublic/SpatialX_datasets/COSMX_VER1/Lung6/Lung6-Flat_files_and_images/CellLabels
                    }
                ]
                args: [
                    {
                        key: mpp
                        value: 0.18
                    }
                ]
                kwargs: []
                identities: []
            }
        ]
    }
    {
        sample_name: Human Lung Cancer - Sample 9 Rep 1
        data: [
            {
                name: Sample 9 Rep 1
                submission_type: SUBMIT_SPATIAL_TRANSCRIPTOMICS
                technology: COSMX_VER1
                files: [
                    {
                        key: fov_positions
                        value: /.../bioturingpublic/SpatialX_datasets/COSMX_VER1/Lung9_Rep1/Lung9_Rep1-Flat_files_and_images/Lung9_Rep1_fov_positions_file.csv
                    }
                    {
                        key: transcripts
                        value: /.../bioturingpublic/SpatialX_datasets/COSMX_VER1/Lung9_Rep1/Lung9_Rep1-Flat_files_and_images/Lung9_Rep1_tx_file.csv
                    }
                ]
                folders: [
                    {
                        key: images
                        value: /.../bioturingpublic/SpatialX_datasets/COSMX_VER1/Lung9_Rep1/Lung9_Rep1-RawMorphologyImages
                    }
                    {
                        key: segmentation
                        value: /.../bioturingpublic/SpatialX_datasets/COSMX_VER1/Lung9_Rep1/Lung9_Rep1-Flat_files_and_images/CellLabels
                    }
                ]
                args: [
                    {
                        key: mpp
                        value: 0.18
                    }
                ]
                kwargs: []
                identities: []
            }
        ]
    }
    {
        sample_name: Human Lung Cancer - Sample 9 Rep 2
        data: [
            {
                name: Sample 9 Rep 2
                submission_type: SUBMIT_SPATIAL_TRANSCRIPTOMICS
                technology: COSMX_VER1
                files: [
                    {
                        key: fov_positions
                        value: /.../bioturingpublic/SpatialX_datasets/COSMX_VER1/Lung9_Rep2/Lung9_Rep2-Flat_files_and_images/Lung9_Rep2_fov_positions_file.csv
                    }
                    {
                        key: transcripts
                        value: /.../bioturingpublic/SpatialX_datasets/COSMX_VER1/Lung9_Rep2/Lung9_Rep2-Flat_files_and_images/Lung9_Rep2_tx_file.csv
                    }
                ]
                folders: [
                    {
                        key: images
                        value: /.../bioturingpublic/SpatialX_datasets/COSMX_VER1/Lung9_Rep2/Lung9_Rep2-RawMorphologyImages
                    }
                    {
                        key: segmentation
                        value: /.../bioturingpublic/SpatialX_datasets/COSMX_VER1/Lung9_Rep2/Lung9_Rep2-Flat_files_and_images/CellLabels
                    }
                ]
                args: [
                    {
                        key: mpp
                        value: 0.18
                    }
                ]
                kwargs: []
                identities: []
            }
        ]
    }
]
```


```python
multiple_samples_submission_results = connector.submit_multiple_samples(
    group=DefaultGroup.PERSONAL_WORKSPACE.value,
    species=Species.HUMAN.value,
    title="Multiple Human Lung Cancer - CosMX Ver1",
    sample_data=multiple_cosmx_samples_submission_information,
)
spatialx_connector.format_print(multiple_samples_submission_results)
```
```yaml
[
    {
        study_id: ST-01JMGMHYDGZ6G1VM6QNNYR4492
        sample_id: SP-01JMGMHZ2QWSXH2DHE3C8X6TCZ
        sample_data: [
            {
                data_id: DA-01JMGMHZ2QWSXH2DHE3FBFSD00
                submit_id: SB-01JMGMHZ2QWSXH2DHE38VKV8NS
                submit_name: Sample 6
            }
        ]
        submit_id: SB-01JMGMHZ2QWSXH2DHE38VKV8NS
        job_id: 5
        err_message:
    }
    {
        study_id: ST-01JMGMHYDGZ6G1VM6QNNYR4492
        sample_id: SP-01JMGMHZRSPPD8PH8CS157RWZX
        sample_data: [
            {
                data_id: DA-01JMGMHZRTJQXH6Z32WGYT9MDK
                submit_id: SB-01JMGMHZRSPPD8PH8CRZ0X1C30
                submit_name: Sample 9 Rep 1
            }
        ]
        submit_id: SB-01JMGMHZRSPPD8PH8CRZ0X1C30
        job_id: 6
        err_message:
    }
    {
        study_id: ST-01JMGMHYDGZ6G1VM6QNNYR4492
        sample_id: SP-01JMGMJ0ET0PYY4PRZMKQ9XXDT
        sample_data: [
            {
                data_id: DA-01JMGMJ0ET0PYY4PRZMN6R7SKW
                submit_id: SB-01JMGMJ0ET0PYY4PRZMJ5JF5H7
                submit_name: Sample 9 Rep 2
            }
        ]
        submit_id: SB-01JMGMJ0ET0PYY4PRZMJ5JF5H7
        job_id: 7
        err_message:
    }
]
```

####  1.8.6. <a name='DataDetailsandElementManagement'></a> Data Details and Element Management
- **Retrieving Data ID**: Obtain the `data_id` for adding extended elements and running analyses.


```python
DATA_ID = submission_results[ConnectorKeys.SAMPLE_DATA.value][0][ConnectorKeys.DATA_ID.value]
```

- **Retrieving Detailed Data Information**: Access comprehensive details about a specific dataset.


```python
sample_data_info = connector.get_sample_data_detail(DATA_ID)
spatialx_connector.format_print(sample_data_info)
```
```yaml
{
    data_id: DA-01JMGMH409ZPBZPQGHBCF4RXF6
    sample_id: SP-01JMGMH408Q5QDH2YPNXRR2WS6
    study_id: ST-01JMGMH3AT8HH8S23QV8ZC2G9T
    submit_id: SB-01JMGMH408Q5QDH2YPNWG5ZH46
    email_id: nhatnm@bioturing.com
    title: Xenium_V1_Human_Colon_Cancer_P2_CRC_Add_on_FFPE
    species_version:
    submission_type: SUBMIT_SPATIAL_TRANSCRIPTOMICS
    technology: XENIUM
    files:
    files_map: [
        {
            key: experiment
            value: /.../bioturingpublic/SpatialX_datasets/Human_Colon_Cancer_P2/Xenium_V1_Human_Colon_Cancer_P2_CRC_Add_on_FFPE/experiment.xenium
        }
        {
            key: images
            value: /.../bioturingpublic/SpatialX_datasets/Human_Colon_Cancer_P2/Xenium_V1_Human_Colon_Cancer_P2_CRC_Add_on_FFPE/morphology.ome.tif
        }
        {
            key: alignment
            value: /.../bioturingpublic/SpatialX_datasets/Human_Colon_Cancer_P2/Xenium_V1_Human_Colon_Cancer_P2_CRC_Add_on_FFPE/Xenium_V1_Human_Colon_Cancer_P2_CRC_Add_on_FFPE_he_imagealignment.csv
        }
        {
            key: segmentation
            value: /.../bioturingpublic/SpatialX_datasets/Human_Colon_Cancer_P2/Xenium_V1_Human_Colon_Cancer_P2_CRC_Add_on_FFPE/cell_boundaries.csv.gz
        }
        {
            key: transcripts
            value: /.../bioturingpublic/SpatialX_datasets/Human_Colon_Cancer_P2/Xenium_V1_Human_Colon_Cancer_P2_CRC_Add_on_FFPE/transcripts.csv.gz
        }
    ]
    folders:
    folders_map: []
    args:
    args_map: []
    identities:
    identities_map: []
    enable_status: 2
    by_bioturing_status: 0
    percent: 1
    setting:
    map_setting: {}
    submit_result: None
    map_submit_result: None
    extend_items:
    map_extend_items: []
    created_at: 1740020158
    updated_at: 1740020159
    job_id: 1
    analysis_id:
    sub_log_path:
}
```

- **Adding New Segmentation:** Add a new segmentation layer to the dataset.


```python
add_segmentation_result = connector.add_sample_data_element(
    title="Proteomics Segmentation",
    study_id=sample_data_info[ConnectorKeys.STUDY_ID.value],
    sample_id=sample_data_info[ConnectorKeys.SAMPLE_ID.value],
    data_id=sample_data_info[ConnectorKeys.DATA_ID.value],
    adding_types=[SegmentationSubmission.PARQUET.value],
    paths={
        SubmissionElementKeys.SEGMENTATION.value: os.path.join(
            connector.s3["bioturingpublic"],
            "mount/examples/spatialx/human_pancreas_codex/human_pancreas_segmentation.parquet",
        )
    }
)
spatialx_connector.format_print(add_segmentation_result)
```
```yaml
{
    study_id: ST-01JMGMH3AT8HH8S23QV8ZC2G9T
    sample_id: SP-01JMGMH408Q5QDH2YPNXRR2WS6
    sample_data: None
    submit_id: SB-01JMGMJG55Z7QT8V4S8V40M8Q5
    job_id: 8
    err_message:
}
```

- **Retrieving Existing Elements:** List the existing elements associated with the dataset.

```python
sample_data_elements = connector.get_sample_data_elements(DATA_ID)
spatialx_connector.format_print(sample_data_elements)
```


- **Adding New Expression Matrix:** Add a new expression matrix to the dataset.

```python
add_expression_result = connector.add_sample_data_element(
    title="Proteomics Expression",
    study_id=sample_data_info[ConnectorKeys.STUDY_ID.value],
    sample_id=sample_data_info[ConnectorKeys.SAMPLE_ID.value],
    data_id=sample_data_info[ConnectorKeys.DATA_ID.value],
    adding_types=[ExpressionSubmission.IMPORT_ANNDATA.value],
    paths={
        SubmissionElementKeys.EXPRESSION.value: os.path.join(
            connector.s3["bioturingpublic"],
            "mount/examples/spatialx/human_pancreas_codex/human_pancreas_protein.h5ad",
        ),
    },
    args={
        SubmissionElementKeys.SPATIAL_ID.value: sample_data_elements[SubmissionElementKeys.CELL_CENTERS.value][0],
    }
)
spatialx_connector.format_print(add_expression_result)
```

####  1.8.7. <a name='CustomSubmission'></a> Customizing Submission Data Structure
This section enables users to submit data with customized data structures, facilitating the upload of diverse spatial omics datasets, such as spatial proteomics data from Akoya CODEX.

**Process Overview:**

1.  **Create an Empty Study:** Begin by establishing a new, empty study within the platform.

```python
study_id = connector.create_study(
    group=DefaultGroup.PERSONAL_WORKSPACE,
    species=Species.HUMAN,
    title="Human Pancreas - CODEX"
)
study_id
```

2.  **Define Custom Data Structure:** Specify the desired data structure using a combination of element types, file paths, and optional arguments. This customization involves two key steps:

    **Step 1: Define Element Types**

    Specify the types of data elements that will be included in the submission. This is achieved using enumerations (`Enum`) that categorize data based on technology and data type.

    **Example Element Type Definitions:**

    ```
    Image:
        # Transcriptomics Technologies
        ImagesSubmission.COSMX_VER1
        ImagesSubmission.COSMX_VER2
        ImagesSubmission.MERSCOPE_VER1
        ImagesSubmission.MERSCOPE_VER2
        ImagesSubmission.XENIUM
        ImagesSubmission.XENIUM_HE

        # Bulk Technologies
        ImagesSubmission.VISIUM
        ImagesSubmission.VISIUM_HD

        # Proteomics Technologies
        ImagesSubmission.PROTEIN_OME_TIFF
        ImagesSubmission.PROTEIN_QPTIFF
        ImagesSubmission.PROTEIN_MCD
        ImagesSubmission.PROTEIN_COSMX_VER2

        # Processed Data
        ImagesSubmission.ZARR_SPATIALDATA

        # Specific cases
        ImagesSubmission.TIFFFILE
        ImagesSubmission.TIFFFILE_3D
        ImagesSubmission.TIFFFILE_HE
        ImagesSubmission.FROM_EXISTED
        ImagesSubmission.PROTEIN_FROM_EXISTED

    Segmentation:
        # Transcriptomics Technologies
        SegmentationSubmission.COSMX_VER1
        SegmentationSubmission.COSMX_VER2
        SegmentationSubmission.MERSCOPE_VER1
        SegmentationSubmission.MERSCOPE_VER2
        SegmentationSubmission.XENIUM
        SegmentationSubmission.XENIUM_HE

        # Bulk Technologies
        SegmentationSubmission.VISIUM
        SegmentationSubmission.VISIUM_HD
        SegmentationSubmission.SLIDE_SEQ
        SegmentationSubmission.STOMICS_BINS
        SegmentationSubmission.STOMICS_CELL_BINS

        # Processed Data
        SegmentationSubmission.ZARR_SPATIALDATA

        # Specific cases
        SegmentationSubmission.PARQUET
        SegmentationSubmission.GEOJSON
        SegmentationSubmission.FEATHER
        SegmentationSubmission.HALO
        SegmentationSubmission.CELL_MASKS

    Trasncripts:
        # Transcriptomics Technologies
        TrasncriptsSubmission.COSMX_VER1
        TrasncriptsSubmission.COSMX_VER2
        TrasncriptsSubmission.MERSCOPE_VER1
        TrasncriptsSubmission.MERSCOPE_VER2
        TrasncriptsSubmission.XENIUM
        TrasncriptsSubmission.XENIUM_HE

        # Processed Data
        TrasncriptsSubmission.ZARR_SPATIALDATA

        # Specific cases
        TrasncriptsSubmission.DATAFRAME

    Expression:

        # Bulk
        ExpressionSubmission.VISIUM
        ExpressionSubmission.VISIUM_HD
        ExpressionSubmission.SLIDE_SEQ
        ExpressionSubmission.GEOMX
        ExpressionSubmission.STOMICS_BINS
        ExpressionSubmission.STOMICS_CELL_BINS

        # Processed data
        ExpressionSubmission.ZARR_SPATIALDATA

    SubmissionElementKeys:
        SubmissionElementKeys.IMAGES
        SubmissionElementKeys.PROTEIN_IMAGES
        SubmissionElementKeys.SEGMENTATION
        SubmissionElementKeys.TRANSCRIPTS
        SubmissionElementKeys.CELL_CENTERS
        SubmissionElementKeys.EXPRESSION
        SubmissionElementKeys.ALIGNMENT
        SubmissionElementKeys.MPP

        SubmissionElementKeys.IMAGES_ID
        SubmissionElementKeys.SEGMENTATION_ID
        SubmissionElementKeys.SPATIAL_ID
        SubmissionElementKeys.NUCLEI_CHANNELS
        SubmissionElementKeys.MEMBRANE_CHANNELS

    ```

    **Step 2: Define Element Paths and Arguments**

    After defining the element types, specify the file paths for each element and any associated arguments. This step involves mapping the defined `Enum` values to the actual file locations and configuration parameters. This will be explained in a following section.

```python
connector.add_custom_sample(
    study_id=study_id,
    sample_name="human_pancreas_codex",
    data_name="human_pancreas_codex",
    technology=Technologies.PROTEIN_QPTIFF,
    adding_types=[
        ImagesSubmission.PROTEIN_QPTIFF,
        SegmentationSubmission.PARQUET,
        ExpressionSubmission.IMPORT_ANNDATA,
    ],
    paths={
        SubmissionElementKeys.PROTEIN_IMAGES: os.path.join(
            connector.s3["bioturingpublic"],
            "mount/examples/spatialx/human_pancreas_codex/human_pancreas_codex.qptiff",
        ),
        SubmissionElementKeys.SEGMENTATION: os.path.join(
            connector.s3["bioturingpublic"],
            "mount/examples/spatialx/human_pancreas_codex/human_pancreas_segmentation.parquet",
        ),
        SubmissionElementKeys.EXPRESSION: os.path.join(
            connector.s3["bioturingpublic"],
            "mount/examples/spatialx/human_pancreas_codex/human_pancreas_protein.h5ad",
        ),
    },
    args={
        SubmissionElementKeys.MPP: 1,
    },
)
```

###  1.9. <a name='Analysis'></a>Analysis
You can now run analyses and see the results directly in the SpatialX connector! This is our first version, and we're planning to add features like analysis logs and result export soon. Stay tuned for updates!
Also, we'd love to hear your feedback! If you have any function requests, please reach out to us at support@bioturing.com.

```python
data_id = submission_results[ConnectorKeys.SAMPLE_DATA.value][-1][ConnectorKeys.DATA_ID.value]
data_id
```

####  1.9.1. <a name='Embeddings'></a> Embeddings


```python
response = connector.analysis.embeddings.pca(data_id=data_id, title="Connector - PCA")
spatialx_connector.format_print(response)
```
```yaml
{
    study_id: ST-01JCGFMAK3GBMXBEAE2FYE02DV
    sample_id: SP-01JCGFMB7GEV299VR986Z193DW
    data_id: DA-01JCGFMQ5GHYYEYRQKT0W061RF
    analysis_id: AN-01JCGGHV7N620FCZMXWHB03Z1W
    job_id: 3
}
```


```python
response = connector.analysis.embeddings.scvi(data_id=data_id, title="Connector - scVI", n_top_genes=2000)
spatialx_connector.format_print(response)
```
```yaml
{
    study_id: ST-01JCGFMAK3GBMXBEAE2FYE02DV
    sample_id: SP-01JCGFMB7GEV299VR986Z193DW
    data_id: DA-01JCGFMQ5GHYYEYRQKT0W061RF
    analysis_id: AN-01JCGGKWNF53MJBN8363YJHWEE
    job_id: 4
}
``````


```python
embeddings = connector.analysis.list_embedding(data_id)
spatialx_connector.format_print(embeddings)
```
```yaml
    [
        Connector - PCA
        Spatial Cell centers
    ]
```


```python
response = connector.analysis.embeddings.umap(data_id=data_id, embedding_key=embeddings[0], title="Connector - UMAP")
spatialx_connector.format_print(response)
```
```yaml
{
    study_id: ST-01JCGFMAK3GBMXBEAE2FYE02DV
    sample_id: SP-01JCGFMB7GEV299VR986Z193DW
    data_id: DA-01JCGFMQ5GHYYEYRQKT0W061RF
    analysis_id: AN-01JCGGPV0M7TEWAG5F8T3GDYY1
    job_id: 5
}
```


```python
response = connector.analysis.embeddings.tsne(data_id=data_id, embedding_key=embeddings[0], title="Connector - tSNE")
spatialx_connector.format_print(response)
```
```yaml
{
    study_id: ST-01JCGFMAK3GBMXBEAE2FYE02DV
    sample_id: SP-01JCGFMB7GEV299VR986Z193DW
    data_id: DA-01JCGFMQ5GHYYEYRQKT0W061RF
    analysis_id: AN-01JCGGQH9ZJE3A8P4JPZRS2JPG
    job_id: 6
}
```

####  1.9.2. <a name='Clustering'></a> Clustering


```python
response = connector.analysis.clustering.louvain(
    data_id=data_id,
    embedding_key=embeddings[0],
    resolution=0.1,
    title="Connector - Louvain",
)
spatialx_connector.format_print(response)
```
```yaml
{
    study_id: ST-01JCGFMAK3GBMXBEAE2FYE02DV
    sample_id: SP-01JCGFMB7GEV299VR986Z193DW
    data_id: DA-01JCGFMQ5GHYYEYRQKT0W061RF
    analysis_id: AN-01JCGGSSRGEP7KAKC47ZVBEDPK
    job_id: 7
}
```


```python
response = connector.analysis.clustering.kmeans(
    data_id=data_id,
    embedding_key=embeddings[0],
    n_clusters=5,
    title="Connector - k-means",
)
spatialx_connector.format_print(response)
```
```yaml
{
    study_id: ST-01JCGFMAK3GBMXBEAE2FYE02DV
    sample_id: SP-01JCGFMB7GEV299VR986Z193DW
    data_id: DA-01JCGFMQ5GHYYEYRQKT0W061RF
    analysis_id: AN-01JCGGY0VS4JR5VAKY5NXANJM1
    job_id: 9
}
```

####  1.9.3. <a name='CellTypePrediction'></a> Cell Type Prediction


```python
embeddings = connector.analysis.list_embedding(data_id)
spatialx_connector.format_print(embeddings)
```
```yaml
[
    Connector - PCA
    Connector - UMAP
    Connector - scVI
    Connector - tSNE
    Spatial Cell centers
    UMAP - n_neighbors=15
    scVI - 20 latents - 486 top genes
    t-SNE - perplexity=30
]
```


```python
metadata = connector.analysis.list_metadata(data_id)
spatialx_connector.format_print(metadata)
```
```yaml
[
    Connector - Louvain
    Connector - Louvain (1)
    Connector - k-means
    Louvain clustering - resolution=0.1
    Louvain clustering - resolution=0.5
    Louvain clustering - resolution=1
    MetaReference prediction
    MetaReference prediction (1)
    Number of genes
    Number of mRNA transcripts
]
```


```python
response = connector.analysis.prediction.metadata_reference(
    data_id=data_id,
    cluster_key=metadata[0],
    species=Species.HUMAN.value,
    title="Connector - Metadata Reference",
)
spatialx_connector.format_print(response)
```
```yaml
{
    study_id: ST-01JCGFMAK3GBMXBEAE2FYE02DV
    sample_id: SP-01JCGFMB7GEV299VR986Z193DW
    data_id: DA-01JCGFMQ5GHYYEYRQKT0W061RF
    analysis_id: AN-01JCGM66JYNBRM5E890NTXHFDJ
    job_id: 14
}
```

####  1.9.4. <a name='DifferentialExpression'></a> Differential Expression


```python
response = connector.analysis.de.differential_expression_genes(
    data_id_1=data_id,
    data_id_2=data_id,
    group_1_indices=[i for i in range(10000)],
    group_2_indices=[i for i in range(10000, 20000)],
    title="Connector - DE genes",
)
spatialx_connector.format_print(response)
```
```yaml
{
    study_id: ST-01JCGFMAK3GBMXBEAE2FYE02DV
    sample_id: SP-01JCGFMB7GEV299VR986Z193DW
    data_id: DA-01JCGFMQ5GHYYEYRQKT0W061RF
    analysis_id: AN-01JCGJZ1WP9EXMFRYHTVJAQE51
    job_id: 10
}
```

####  1.9.5. <a name='SpatialAnalysis-RegionSegmentation'></a> Spatial Analysis - Region Segmentation


```python
response = connector.analysis.spatial_analysis.region_segmentation(
    data_id=data_id,
    radius=50,
    mpp=0.2125,
    resolution=0.5,
    species=Species.HUMAN.value,
    title="Connector - Region Segmentation",
)
spatialx_connector.format_print(response)
```
```yaml
{
    study_id: ST-01JCGFMAK3GBMXBEAE2FYE02DV
    sample_id: SP-01JCGFMB7GEV299VR986Z193DW
    data_id: DA-01JCGFMQ5GHYYEYRQKT0W061RF
    analysis_id: AN-01JCGK68MJXRWVD450CAHS42JV
    job_id: 11
}
```

###  1.10. <a name='ConvertDatafromLens'></a>Convert Data from Lens
This section guides existing BioTuring Lens users on how to migrate their data to SpatialX.

####  1.10.1. <a name='InstallBioTuringLensConnector'></a>Install BioTuring Lens Connector
Before proceeding, ensure you have installed the BioTuring Lens connector in addition to the SpatialX connector.

```python
!pip install bioturing_connector
```

    Requirement already satisfied: bioturing_connector in /home/nhatnguyen/BioTuring/spatialx/pyapps/lib/python3.12/site-packages (1.13.0)
    Requirement already satisfied: numpy in /home/nhatnguyen/BioTuring/spatialx/pyapps/lib/python3.12/site-packages (from bioturing_connector) (1.26.4)
    Requirement already satisfied: pandas in /home/nhatnguyen/BioTuring/spatialx/pyapps/lib/python3.12/site-packages (from bioturing_connector) (2.2.2)
    Requirement already satisfied: requests in /home/nhatnguyen/BioTuring/spatialx/pyapps/lib/python3.12/site-packages (from bioturing_connector) (2.32.3)
    Requirement already satisfied: requests_toolbelt>=1.0.0 in /home/nhatnguyen/BioTuring/spatialx/pyapps/lib/python3.12/site-packages (from bioturing_connector) (1.0.0)
    Requirement already satisfied: scipy in /home/nhatnguyen/BioTuring/spatialx/pyapps/lib/python3.12/site-packages (from bioturing_connector) (1.12.0)
    Requirement already satisfied: tqdm in /home/nhatnguyen/BioTuring/spatialx/pyapps/lib/python3.12/site-packages (from bioturing_connector) (4.66.4)
    Requirement already satisfied: charset-normalizer<4,>=2 in /home/nhatnguyen/BioTuring/spatialx/pyapps/lib/python3.12/site-packages (from requests->bioturing_connector) (3.3.2)
    Requirement already satisfied: idna<4,>=2.5 in /home/nhatnguyen/BioTuring/spatialx/pyapps/lib/python3.12/site-packages (from requests->bioturing_connector) (3.10)
    Requirement already satisfied: urllib3<3,>=1.21.1 in /home/nhatnguyen/BioTuring/spatialx/pyapps/lib/python3.12/site-packages (from requests->bioturing_connector) (1.26.20)
    Requirement already satisfied: certifi>=2017.4.17 in /home/nhatnguyen/BioTuring/spatialx/pyapps/lib/python3.12/site-packages (from requests->bioturing_connector) (2024.8.30)
    Requirement already satisfied: python-dateutil>=2.8.2 in /home/nhatnguyen/BioTuring/spatialx/pyapps/lib/python3.12/site-packages (from pandas->bioturing_connector) (2.9.0.post0)
    Requirement already satisfied: pytz>=2020.1 in /home/nhatnguyen/BioTuring/spatialx/pyapps/lib/python3.12/site-packages (from pandas->bioturing_connector) (2024.2)
    Requirement already satisfied: tzdata>=2022.7 in /home/nhatnguyen/BioTuring/spatialx/pyapps/lib/python3.12/site-packages (from pandas->bioturing_connector) (2024.2)
    Requirement already satisfied: six>=1.5 in /home/nhatnguyen/BioTuring/spatialx/pyapps/lib/python3.12/site-packages (from python-dateutil>=2.8.2->pandas->bioturing_connector) (1.16.0)


####  1.10.2. <a name='InputDomainandToken'></a>Input Domain and Token
To obtain your domain URL and personal token, navigate to "BioTuring Lens SDK" in the left panel of your BioTuring Lens interface. Then, enter the information in the fields below. For example:

DOMAIN = "https://example.bioturing.com/lens_sc/"

TOKEN = "000000000000000000000000NM"

- Example of BioTuring Lens SC (Single cell)

```python
LENS_SC_HOST: str = ""
LENS_SC_TOKEN: str = ""
lens_sc_studies = connector.list_lens_sc_studies(
    host=LENS_SC_HOST, token=LENS_SC_TOKEN,
    group=DefaultGroup.PERSONAL_WORKSPACE,
    species=Species.HUMAN.value,
)
spatialx_connector.format_print(lens_sc_studies)
```
```yaml
Connecting to host at https://dev.bioturing.com/lens_sc/api/v1/test_connection
Connection successful
[
    {
        id: 96f6e21e9ac74f74bfe656a2a59ba058
        accession_id: XENIUM
        title: breast
        abstract: TBD
        authors: TBD
        reference: TBD
        species: human
        group_id: 662bd88b50da063e1870a4efc01fe185
    }
    {
        id: 49998dd7de8340c19a0acdd177b71fb4
        accession_id: XENIUM
        title: TBD
        abstract: TBD
        authors: TBD
        reference: TBD
        species: human
        group_id: 662bd88b50da063e1870a4efc01fe185
    }
]
```

- Example of BioTuring Lens Bulk
```python
LENS_BULK_HOST: str = ""
LENS_BULK_TOKEN: str = ""
lens_bulk_studies = connector.list_lens_bulk_studies(
    host=LENS_BULK_HOST, token=LENS_BULK_TOKEN,
    group=DefaultGroup.PERSONAL_WORKSPACE,
    species=Species.HUMAN.value,
)
spatialx_connector.format_print(lens_bulk_studies)
```
```yaml
Connecting to host at https://dev.bioturing.com/lens_bulk/api/v1/test_connection
Connection successful
[
    {
        id: f92a884e42bf43749011d71593e727ba
        accession_id: VISIUM
        title: TBD
        abstract: TBD
        authors: TBD
        reference: TBD
        species: human
        group_id: 662bd88b50da063e1870a4efc01fe185
    }
    {
        id: 8b3e1737007c47fc81667f54ea998740
        accession_id: CURIO
        title: TBD
        abstract: TBD
        authors: TBD
        reference: TBD
        species: human
        group_id: 662bd88b50da063e1870a4efc01fe185
    }
]
```

#### 1.10.3. <a name='ConvertStudy'></a>Converting Studies

We offer two options for converting studies:

* **Convert a Specific Study:** To convert an individual study, specify its index within the study list. For example, `lens_sc_studies[0]` converts the first study in your Lens_SC data.
* **Convert All Studies:** To convert all studies from a specific data type (e.g., Lens_Bulk), simply provide the study list name without an index. For example, `lens_bulk_studies` will convert all studies from your Lens_Bulk data.

```python
# Convert a study
connector.convert_data_from_lens(lens_sc_studies[0])
```

```python
# Convert multiple studies
connector.convert_data_from_lens(lens_bulk_studies)
```
