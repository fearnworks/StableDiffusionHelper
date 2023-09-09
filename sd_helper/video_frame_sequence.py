from typing import List, Dict, Union, Optional
import json 
from collections import OrderedDict

class VideoFrameSequence:
    def __init__(self, global_attributes=None, max_frames=None):
        self.frames = {}
        self.scheduled_attrs = set()
        self.global_attrs = OrderedDict(global_attributes) if global_attributes else OrderedDict()
        self.loras = set()
        self.priority_list = []
        self.persistent_attrs = set()
        self.max_frames = max_frames

    def _order_attributes(self, attrs):
        """Order attributes based on insertion and priority."""
        return sorted(attrs, key=lambda x: (
            x not in self.global_attrs,
            x not in self.priority_list,
            list(self.global_attrs.keys()).index(x) if x in self.global_attrs else 0,
            self.priority_list.index(x) if x in self.priority_list else 0,
            x
        ))

    def _initialize_attributes(self, attributes, start_weights, end_weights):
        """Initialize attributes as lists and validate their lengths."""
        if not isinstance(attributes, list):
            attributes = [attributes]
        if not isinstance(start_weights, list):
            start_weights = [start_weights] * len(attributes)
        if not isinstance(end_weights, list):
            end_weights = [end_weights] * len(attributes)

        if len(attributes) != len(start_weights) or len(attributes) != len(end_weights):
            raise ValueError("Length of attributes, start_weights, and end_weights must be the same.")

        return attributes, start_weights, end_weights

    def _handle_lora_attributes(self, attributes):
        """Handle attributes that are loras."""
        for attribute in attributes:
            if attribute.startswith("<lora:"):
                self.loras.add(attribute[6:-1])
            else:
                self.scheduled_attrs.add(attribute)

    def _calculate_weight_for_frame(self, frame, start_frame, end_frame, start_weight, end_weight):
        """Calculate the attribute weight for a given frame, truncated to 4 decimal places."""
        weight = start_weight + (end_weight - start_weight) * (frame - int(start_frame)) / (int(end_frame) - int(start_frame))
        return round(weight, 4)
    
    def _update_frame_attributes(self, frame, attributes, start_weights, end_weights, start_frame, end_frame):
        """Update the attributes of a frame based on the scheduled weights."""
        if self.max_frames is not None and frame > self.max_frames:
            return
        
        str_frame = str(frame)
        if str_frame not in self.frames:
            self.frames[str_frame] = {}

        for i in range(len(attributes)):
            attribute = attributes[i]
            start_weight = start_weights[i]
            end_weight = end_weights[i]
            weight = self._calculate_weight_for_frame(frame, start_frame, end_frame, start_weight, end_weight)
            attr_key = attribute[6:-1] if attribute.startswith("<lora:") else attribute
            self.frames[str_frame][attr_key] = weight


        for global_attr, weight in self.global_attrs.items():
            self.frames[str_frame][global_attr] = weight


        prev_frame = str(frame - 1)
        if prev_frame in self.frames:
            for attr, prev_weight in self.frames[prev_frame].items():
                if attr not in self.scheduled_attrs:
                    self.frames[str_frame][attr] = prev_weight
                    
        for attr in self.persistent_attrs:
            if attr not in self.frames[str(frame)]:
                prev_frame = str(frame - 1)
                if prev_frame in self.frames and attr in self.frames[prev_frame]:
                    self.frames[str(frame)][attr] = self.frames[prev_frame][attr]

        ordered_attributes = self._order_attributes(self.frames[str_frame])
        self.frames[str_frame] = {k: self.frames[str_frame][k] for k in ordered_attributes}

    def schedule_weights(self, start_frame, end_frame, attributes, start_weights, end_weights, include_in_future=True):
        attributes, start_weights, end_weights = self._initialize_attributes(attributes, start_weights, end_weights)
        self._handle_lora_attributes(attributes)

        if include_in_future:
            for attribute in attributes:
                self.persistent_attrs.add(attribute)

        for frame in range(int(start_frame), int(end_frame) + 1):
            self._update_frame_attributes(frame, attributes, start_weights, end_weights, start_frame, end_frame)

    def to_json(self):
        json_object = self.frames

        def convert_frames_to_single_string_with_parentheses(json_object):
            for frame, attrs in json_object.items():
                attributes_list = []
                for key, value in attrs.items():
                    if key in self.loras:
                        attributes_list.append(f"<{key}:{value}>")
                    elif ':' in key:
                        attributes_list.append(f"[{key}:{value}]")
                    else:
                        attributes_list.append(f"({key}:{value})")
                json_object[frame] = ', '.join(attributes_list)
            return json_object

        json_object = convert_frames_to_single_string_with_parentheses(json_object)
        return json.dumps(json_object, indent=4)