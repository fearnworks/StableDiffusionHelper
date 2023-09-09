Stable Diffusion Helper 

The repo is a general library with logic used during my stable diffussion workflows


## Features

### Deforum Helpers 

```
VideoFrameSequence Class: Create sequences of frames, schedule weights, and exports to JSON.
Path Conversion: Convert Windows paths to UNIX format since sd-webui doesn't handle those well.
Dictionary Manipulation: Modify dictionaries to remove negative objects and return the most common negative line.
```
### Getting Started

Installation
Clone the repository:
```bash
git clone https://github.com/fearnworks/StableDiffusionHelper.git
```

Install dependencies in desired virtual environment and see the example_notebook for usage:
```bash
cd VideoFrameSequence
python -m venv venv
source bin venv/bin/activate
pip install -e . 
```

The library is currently designed to be used with a jupyter notebook instead of a standalone executable. 


### Example Logic 
Run your desired Python script or integrate the classes and functions into your own project.

Using the VideoFrameSequence Class
Create an instance of VideoFrameSequence:
```python

sequence = VideoFrameSequence(global_attributes={"background": 1}, max_frames=150)
```
Schedule attributes and their weights for specific frames:
```python
sequence.schedule_weights(start_frame=1, end_frame=80, attributes="attribute_name", start_weights=0.01, end_weights=0.99)
```

Convert the sequence to JSON and print:
```python
sequence_json = sequence.to_json()
print(sequence_json)
```

Utility Functions
Convert Windows paths to UNIX paths:

```python
unix_path = convert_to_unix_path(r"C:\Users\Username\Documents")
```

Modify dictionaries to remove negative objects:
```python

modified_dict, most_common_neg_line = remove_neg_objects({"key": "value --neg item"})
```

### Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### License
This program is distributed under the terms of the GNU Affero Public License v3.0

