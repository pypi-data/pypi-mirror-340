<!-- inject desc here -->
<!-- inject-desc -->

a package to set different types of input parameters for comfyui node easily

## File size

<!-- inject size of bundles here -->
<!-- inject-file-size -->

## Features

<!-- inject feat here -->
<!-- inject-features -->

## Usage

```bash
pip install yors_pano_zero_field
```

<!-- inject demo here -->

```py
from yors_pano_zero_field import ZeroField
class MyComfyUINode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_int": ZeroField.int(default=10, min=1, max=100, force=True),
                "input_float": ZeroField.float(default=0.5, min=0, max=1),
                "input_string": ZeroField.string(default="default text")
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "process"
    CATEGORY = "custom"

    def process(self, input_int, input_float, input_string):
        # 处理输入参数
        print(f"Received integer: {input_int}")
        print(f"Received float: {input_float}")
        print(f"Received string: {input_string}")
        return ()
```
