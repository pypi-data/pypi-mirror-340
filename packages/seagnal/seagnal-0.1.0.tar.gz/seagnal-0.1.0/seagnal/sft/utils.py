def translate_action_to_tool_call(action_dict):
    """
    Translates a dataset action into a Qwen tool call for the agent.
    See `https://github.com/QwenLM/Qwen2.5-VL/blob/main/cookbooks/computer_use.ipynb` for more details.

    The dataset action is expected to be a dictionary with a "name" key and a "parameters" key.
    The mapping is as follows:
      - For actions with name "click":
          * Maps to "left_click" (if button is "left"), "right_click" (if button is "right"),
            or "middle_click" (if button is "middle").
          * The x and y coordinates (from parameters "x" and "y") are passed as the "coordinate".
      - For actions with name "move_mouse":
          * Maps to "mouse_move", with "coordinate": [x, y].
      - For actions with name "scroll":
          * Maps to "scroll", with the converted "pixels" under "pixels".
      - For actions with name "press_key":
          * Maps to "key". The key pressed is provided as a list under "keys".
      - For actions with name "type_text":
          * Maps to "type", with the provided text under "text".

    Parameters:
        action_dict (dict): A dictionary representing the dataset action.

    Returns:
        dict: A dictionary representing the tool call for the agent.
              For example:
              {
                  "name": "computer_use",
                  "arguments": {
                      "action": "<agent_action>",
                      ... other required parameters ...
                  }
              }

    Raises:
        ValueError: If the action name is not recognized.
    """
    action_name = action_dict.get("name")
    params = action_dict.get("parameters", {})

    if action_name == "click":
        # Determine the correct click action based on the button type.
        button = params.get("button", "left")
        if button == "left":
            agent_action = "left_click"
        elif button == "right":
            agent_action = "right_click"
        elif button == "middle":
            agent_action = "middle_click"
        else:
            # Default to left_click if unrecognized
            agent_action = "left_click"
        x = params.get("x")
        y = params.get("y")
        return {
            "name": "computer_use",
            "arguments": {"action": agent_action, "coordinate": [x, y]},
        }

    elif action_name == "move_mouse":
        x = params.get("x")
        y = params.get("y")
        return {
            "name": "computer_use",
            "arguments": {"action": "mouse_move", "coordinate": [x, y]},
        }

    elif action_name == "scroll":
        clicks = params.get("clicks", 0)
        pixels = clicks * 100
        return {
            "name": "computer_use",
            "arguments": {"action": "scroll", "pixels": pixels},
        }

    elif action_name == "double_click":
        x = params.get("x")
        y = params.get("y")
        return {
            "name": "computer_use",
            "arguments": {"action": "double_click", "coordinate": [x, y]},
        }

    elif action_name == "press_key":
        key = params.get("key")
        return {"name": "computer_use", "arguments": {"action": "key", "keys": [key]}}

    elif action_name == "type_text":
        text = params.get("text")
        return {"name": "computer_use", "arguments": {"action": "type", "text": text}}

    else:
        raise ValueError(f"Unknown action name: {action_name}")
